import sys
import os

# ==========================================================
# BLOQUE DE DIAGNÓSTICO DE SEGURIDAD
# ==========================================================
print("--- [SISTEMA] Iniciando Verificación de Entorno ---")
try:
    from log_master.core.parsers import rust_parser
    print("✅ [OK] Motor Rust cargado correctamente.")
except ImportError as e:
    print(f"❌ [ERROR CRÍTICO] No se puede cargar el motor de análisis.")
    print(f"   Detalle Técnico: {e}")
    if "DLL load failed" in str(e):
        print("\n💡 CAUSA PROBABLE: Faltan las librerías 'Microsoft Visual C++ Redistributable'.")
        print("   Por favor, instala: https://aka.ms/vs/17/release/vc_redist.x64.exe\n")
    sys.exit(1)

# IMPORTACIÓN CORREGIDA: Usamos LogMasterGUI
try:
    from log_master.gui import LogMasterGUI
except ImportError as e:
    print(f"❌ [ERROR DE ESTRUCTURA] No se pudo importar la interfaz: {e}")
    sys.exit(1)

def main():
    try:
        # Instanciamos la clase correcta
        app = LogMasterGUI()
        app.mainloop()
    except Exception as e:
        print(f"❌ Error al iniciar la interfaz: {e}")

if __name__ == "__main__":
    main()
