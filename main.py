import sys
import os

# Añade la carpeta actual al path de búsqueda de Python
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from log_master.gui import LogMasterGUI
except ImportError:
    # Por si acaso lo lanzas desde dentro de la subcarpeta
    from gui import LogMasterGUI

def main():
    app = LogMasterGUI()
    app.mainloop()

if __name__ == "__main__":
    main()