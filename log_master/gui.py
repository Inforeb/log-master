import customtkinter as ctk
from tkinter import filedialog, ttk
import tkinter as tk
import threading
from datetime import datetime
from log_master.core.engine import LogEngine

class LogMasterGUI(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.engine = LogEngine()
        self.current_view_df = None 
        self.font_size_table = 10
        self.font_size_details = 12
        
        self.title("LogMaster Pro")
        self.geometry("1500x900")
        ctk.set_appearance_mode("Dark")
        
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self._style_tables()
        self._build_sidebar()
        
        self.main_container = ctk.CTkFrame(self, fg_color="transparent")
        self.main_container.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        self.main_container.grid_columnconfigure(0, weight=1)
        self.main_container.grid_rowconfigure(1, weight=1)

        self._build_kpi_panel()
        
        self.paned_window = ttk.PanedWindow(self.main_container, orient=tk.VERTICAL)
        self.paned_window.grid(row=1, column=0, sticky="nsew")

        self.upper_pane = ctk.CTkFrame(self.paned_window, fg_color="transparent")
        self.paned_window.add(self.upper_pane, weight=1)
        self.upper_pane.grid_columnconfigure(0, weight=1)
        self.upper_pane.grid_columnconfigure(1, weight=4)
        self.upper_pane.grid_rowconfigure(0, weight=1)

        self._build_stats_panel(self.upper_pane)
        self._build_main_table(self.upper_pane)

        self.lower_pane = ctk.CTkFrame(self.paned_window, border_width=1, border_color="#333333")
        self.paned_window.add(self.lower_pane, weight=0)
        self._build_details_panel(self.lower_pane)

    def _style_tables(self):
        self.style = ttk.Style()
        self.style.theme_use("default")
        self.style.configure("Treeview", background="#2b2b2b", foreground="white", fieldbackground="#2b2b2b", borderwidth=0, font=("Arial", self.font_size_table))
        self.style.configure("Treeview.Heading", background="#333333", foreground="white", font=("Arial", 10, "bold"))
        self.style.map("Treeview", background=[('selected', '#1f538d')])

    def _build_sidebar(self):
        self.sidebar = ctk.CTkFrame(self, width=220, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        ctk.CTkLabel(self.sidebar, text="LOGMASTER", font=("Arial", 20, "bold")).pack(pady=20)
        
        ctk.CTkButton(self.sidebar, text="📊 Dashboard", command=self._show_all).pack(pady=5, padx=10, fill="x")
        ctk.CTkButton(self.sidebar, text="📥 Import Logs", fg_color="#2e7d32", command=self._start_import_thread).pack(pady=5, padx=10, fill="x")
        
        ctk.CTkLabel(self.sidebar, text="Rango Temporal", font=("Arial", 12, "bold")).pack(pady=(15, 2))
        self.time_start = ctk.CTkEntry(self.sidebar, placeholder_text="YYYY-MM-DD HH:MM:SS")
        self.time_start.insert(0, "2024-01-01 00:00:00")
        self.time_start.pack(pady=2, padx=10)
        self.time_end = ctk.CTkEntry(self.sidebar, placeholder_text="YYYY-MM-DD HH:MM:SS")
        self.time_end.insert(0, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        self.time_end.pack(pady=2, padx=10)
        ctk.CTkButton(self.sidebar, text="📅 Filtrar Tiempo", fg_color="#455a64", command=self._apply_time_filter).pack(pady=5, padx=10, fill="x")

        ctk.CTkLabel(self.sidebar, text="Palabra Clave", font=("Arial", 12, "bold")).pack(pady=(15, 2))
        self.search_entry = ctk.CTkEntry(self.sidebar, placeholder_text="ID, Origen, Texto...")
        self.search_entry.pack(pady=5, padx=10)
        self.search_entry.bind("<Return>", lambda e: self._apply_search())
        ctk.CTkButton(self.sidebar, text="🔍 Buscar", fg_color="#1f538d", command=self._apply_search).pack(pady=5, padx=10, fill="x")

        ctk.CTkLabel(self.sidebar, text="Ráfaga (Seg)", font=("Arial", 12, "bold")).pack(pady=(15, 2))
        self.burst_entry = ctk.CTkEntry(self.sidebar, width=60, justify="center")
        self.burst_entry.insert(0, "60")
        self.burst_entry.pack(pady=2)
        self.burst_slider = ctk.CTkSlider(self.sidebar, from_=1, to=300, command=self._on_slider_move)
        self.burst_slider.set(60)
        self.burst_slider.pack(pady=5, padx=10)
        ctk.CTkButton(self.sidebar, text="⚡ Modo Ráfaga", fg_color="#fbc02d", text_color="black", command=self._show_bursts).pack(pady=10, padx=10, fill="x")
        
        ctk.CTkButton(self.sidebar, text="🗑️ Clear Data", fg_color="#c62828", command=self._clear_all).pack(side="bottom", pady=20, padx=10, fill="x")

    def _apply_time_filter(self):
        base_df = self.current_view_df if self.current_view_df is not None else self.engine.current_data
        filtered = self.engine.filter_by_time(base_df, self.time_start.get(), self.time_end.get())
        self.current_view_df = filtered
        self._refresh_ui_with_df(filtered)

    def _apply_search(self):
        query = self.search_entry.get()
        base_df = self.current_view_df if self.current_view_df is not None else self.engine.current_data
        filtered = self.engine.search_data(base_df, query)
        self._refresh_ui_with_df(filtered)

    def _on_slider_move(self, value):
        self.burst_entry.delete(0, tk.END)
        self.burst_entry.insert(0, str(int(value)))

    def _build_kpi_panel(self):
        self.kpi_frame = ctk.CTkFrame(self.main_container, fg_color="transparent")
        self.kpi_frame.grid(row=0, column=0, pady=(0, 10), sticky="nsew")
        self.btn_total = self._create_kpi(self.kpi_frame, "TOTAL", "#1a237e", self._show_all)
        self.btn_errors = self._create_kpi(self.kpi_frame, "ERRORS", "#b71c1c", lambda: self._filter_by_level("ERROR"))
        self.btn_warnings = self._create_kpi(self.kpi_frame, "WARNINGS", "#ef6c00", lambda: self._filter_by_level("WARNING"))

    def _create_kpi(self, parent, text, color, cmd):
        btn = ctk.CTkButton(parent, text=f"{text}\n0", fg_color=color, height=60, font=("Arial", 13, "bold"), command=cmd)
        btn.pack(side="left", padx=5, expand=True, fill="both")
        return btn

    def _build_stats_panel(self, parent):
        self.stats_frame = ctk.CTkFrame(parent, border_width=1, border_color="#333333")
        self.stats_frame.grid(row=0, column=0, padx=(0, 5), sticky="nsew")
        self.stats_title = ctk.CTkLabel(self.stats_frame, text="TOP EVENT IDs", font=("Arial", 11, "bold"))
        self.stats_title.pack(pady=5)
        self.id_tree = ttk.Treeview(self.stats_frame, columns=("ID", "Qty"), show='headings')
        self.id_tree.heading("ID", text="ID")
        self.id_tree.heading("Qty", text="QTY")
        self.id_tree.column("ID", width=60, anchor="center")
        self.id_tree.column("Qty", width=60, anchor="center")
        self.id_tree.pack(fill="both", expand=True, padx=5, pady=5)
        self.id_tree.bind("<<TreeviewSelect>>", self._on_id_filter)

    def _build_main_table(self, parent):
        self.table_frame = ctk.CTkFrame(parent, border_width=1, border_color="#333333")
        self.table_frame.grid(row=0, column=1, sticky="nsew")
        h = ctk.CTkFrame(self.table_frame, fg_color="transparent")
        h.pack(fill="x", pady=2)
        ctk.CTkLabel(h, text="EVENT LOG LIST", font=("Arial", 11, "bold")).pack(side="left", padx=10, expand=True)
        ctk.CTkButton(h, text="-", width=25, height=20, command=lambda: self._change_font("table", -1)).pack(side="right", padx=2)
        ctk.CTkButton(h, text="+", width=25, height=20, command=lambda: self._change_font("table", 1)).pack(side="right", padx=5)
        
        cols = ("TS", "Lvl", "Src", "ID", "Summary")
        self.tree = ttk.Treeview(self.table_frame, columns=cols, show='headings')
        for c, name in zip(cols, ["TIMESTAMP", "LVL", "SOURCE", "EID", "SUMMARY"]): 
            self.tree.heading(c, text=name)
        
        # --- AJUSTE DE ANCHOS OPTIMIZADOS v2 ---
        self.tree.column("TS", width=140, stretch=False, anchor="center")
        self.tree.column("Lvl", width=70, stretch=False, anchor="center")
        self.tree.column("Src", width=180, stretch=False) # Aumentado para ~12 caracteres
        self.tree.column("ID", width=50, stretch=False, anchor="center")
        self.tree.column("Summary", width=400, stretch=True) 
        
        self.tree.pack(fill="both", expand=True, padx=5, pady=5)
        self.tree.bind("<<TreeviewSelect>>", self._on_log_select)

    def _build_details_panel(self, parent):
        h = ctk.CTkFrame(parent, fg_color="transparent")
        h.pack(fill="x", pady=2)
        ctk.CTkLabel(h, text="LOG DETAILS", font=("Arial", 11, "bold")).pack(side="left", padx=10, expand=True)
        ctk.CTkButton(h, text="-", width=25, height=20, command=lambda: self._change_font("details", -1)).pack(side="right", padx=2)
        ctk.CTkButton(h, text="+", width=25, height=20, command=lambda: self._change_font("details", 1)).pack(side="right", padx=5)
        self.details_box = ctk.CTkTextbox(parent, font=("Consolas", self.font_size_details), wrap="none")
        self.details_box.pack(fill="both", expand=True, padx=5, pady=(0, 5))

    def _change_font(self, target, delta):
        if target == "table":
            self.font_size_table = max(6, self.font_size_table + delta)
            self.style.configure("Treeview", font=("Arial", self.font_size_table))
        else:
            self.font_size_details = max(6, self.font_size_details + delta)
            self.details_box.configure(font=("Consolas", self.font_size_details))

    def _refresh_ui_with_df(self, df):
        for i in self.tree.get_children(): self.tree.delete(i)
        for i in self.id_tree.get_children(): self.id_tree.delete(i)
        for _, r in df.head(2000).iterrows():
            self.tree.insert("", "end", values=(r['TS'], r['Lvl'], r['Src'], r['ID'], r['Summary']))
        for stat in self.engine.get_stats_from_df(df):
            self.id_tree.insert("", "end", values=(stat["ID"], stat["Count"]))

    def _show_bursts(self):
        val = self.burst_entry.get()
        sec = int(val) if val.isdigit() else 60
        stats, title, burst_df = self.engine.get_burst_stats(self.current_view_df, sec)
        self.stats_title.configure(text=title)
        self.current_view_df = burst_df
        self._refresh_ui_with_df(burst_df)

    def _on_id_filter(self, event):
        item = self.id_tree.selection()
        if not item: return
        sid = str(self.id_tree.item(item[0])['values'][0])
        base = self.current_view_df if self.current_view_df is not None else self.engine.current_data
        filtered_by_id = base[base["ID"] == sid]
        
        for i in self.tree.get_children(): self.tree.delete(i)
        for _, r in filtered_by_id.head(2000).iterrows():
            self.tree.insert("", "end", values=(r['TS'], r['Lvl'], r['Src'], r['ID'], r['Summary']))

    def _update_ui(self, filtered_df=None):
        self.current_view_df = filtered_df
        s = self.engine.get_summary()
        self.btn_total.configure(text=f"TOTAL\n{s['total']}")
        self.btn_errors.configure(text=f"ERRORS\n{s['errors']}")
        self.btn_warnings.configure(text=f"WARNINGS\n{s['warnings']}")
        df = filtered_df if filtered_df is not None else self.engine.current_data
        self._refresh_ui_with_df(df)

    def _filter_by_level(self, level): 
        self._update_ui(self.engine.get_filtered_data(level))

    def _show_all(self): 
        self.stats_title.configure(text="TOP EVENT IDs")
        self._update_ui(None)

    def _on_log_select(self, event):
        item = self.tree.selection()
        if not item: return
        vals = self.tree.item(item[0])['values']
        df = self.current_view_df if self.current_view_df is not None else self.engine.current_data
        match = df[(df['TS'] == vals[0]) & (df['ID'] == str(vals[3]))]
        
        if not match.empty:
            self.details_box.configure(state="normal")
            self.details_box.delete("0.0", "end")
            self.details_box.insert("0.0", match.iloc[0]["Msg"])
            self.details_box.configure(state="disabled")

    def _clear_all(self):
        self.engine.current_data = self.engine.current_data.iloc[0:0]
        self.current_view_df = None
        self._update_ui()

    def _start_import_thread(self):
        files = filedialog.askopenfilenames(filetypes=[("Logs", "*.evtx")])
        if files: 
            threading.Thread(target=self._run_import, args=(files,), daemon=True).start()

    def _run_import(self, files):
        self.engine.load_logs(files)
        self.after(0, self._update_ui)
