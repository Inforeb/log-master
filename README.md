# 🛡️ LogMaster Pro

**LogMaster Pro** es una solución avanzada de análisis y visualización de logs de eventos de Windows (`.evtx`). Está diseñada para permitir a los analistas de seguridad e ingenieros de sistemas identificar ráfagas de errores (**bursts**) y patrones anómalos en cuestión de segundos.

---

## 🚀 Características Principales

* **🚀 Ultra-fast EVTX Parsing:** Motor de análisis escrito en Rust para procesar miles de eventos en milisegundos.
* **🐍 Python-Powered UI:** Interfaz intuitiva y moderna construida con CustomTkinter, con escalado de fuente dinámico para análisis prolongados.
* **⚡ Modo Ráfaga (Burst Detection):** Detecta picos de eventos en intervalos de tiempo ajustables (1-300 seg) para identificar ataques de fuerza bruta o fallos en cascada.
* **📅 Filtro Temporal Granular:** Acota búsquedas a rangos de tiempo específicos con precisión de segundos.
* **🔍 Motor de Búsqueda Global:** Filtrado instantáneo por Event ID (EID), Fuente (Source) o palabras clave dentro del mensaje.
* **📊 Dashboard de KPIs:** Resumen en tiempo real del estado de salud del sistema (Total, Errors, Warnings).
* **🔒 Privacidad por Diseño:** Procesamiento 100% local. Los datos nunca salen de tu máquina.

## Multi-Version Native Engine
LogMaster incluye binarios nativos (compilados en Rust) compatibles con múltiples versiones de Python (3.9, 3.10, 3.11, 3.12, 3.13 y 3.14) para Windows x64. El sistema detecta automáticamente la versión de Python en ejecución y carga el parser optimizado correspondiente.

## 🛠️ Instalación y Uso

### 1. Requisitos previos
Asegúrate de tener Python 3.9 o superior instalado.

### 2. Clonar y Configurar

#### Clonar el repositorio
git clone [https://github.com/Inforeb/log-master.git](https://github.com/Inforeb/log-master.git)

cd log-master

#### Instalar dependencias
pip install -r requirements.txt

### 3. Ejecución
python main.py

## 📂 Estructura del Repositorio

El proyecto se organiza de la siguiente manera para separar la lógica de procesamiento de la interfaz de usuario y los componentes de bajo nivel:

* **`main.py`**: Punto de entrada principal de la aplicación.
* **`log_master/gui.py`**: Motor de la interfaz gráfica (CustomTkinter) y gestión de eventos de usuario.
* **`log_master/core/engine.py`**: Lógica de procesamiento de datos, filtrado y analítica con Pandas.
* **`log_master/core/parsers/`**: Carpeta que contiene los motores de extracción.
    * **`rust_parser.pyd`**: Binario compilado en Rust para el parsing de alta velocidad de archivos EVTX.
* **`requirements.txt`**: Dependencias necesarias para el entorno de Python.


## 🤝 Contacto y Feedback

Este proyecto está en constante evolución. Si tienes sugerencias, has encontrado algún error o quieres proponer nuevas funcionalidades para el motor de análisis:

📩 **Agradecemos tus comentarios por mensaje directo (MD).** ¡Tu feedback es fundamental para seguir optimizando el rendimiento de LogMaster Pro!