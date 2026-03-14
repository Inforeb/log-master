# 🛡️ LogMaster Pro

**LogMaster Pro** es una solución avanzada de análisis y visualización de logs de eventos de Windows (`.evtx`). Está diseñada para permitir a los analistas de seguridad e ingenieros de sistemas identificar ráfagas de errores (**bursts**) y patrones anómalos en cuestión de segundos.

---

## 🚀 Características Principales

* **⚡ Modo Ráfaga (Burst Detection):** Detecta picos de eventos en intervalos de tiempo ajustables (1-300 seg) para identificar ataques de fuerza bruta o fallos en cascada.
* **📅 Filtro Temporal Granular:** Acota búsquedas a rangos de tiempo específicos con precisión de segundos.
* **🔍 Motor de Búsqueda Global:** Filtrado instantáneo por Event ID (EID), Fuente (Source) o palabras clave dentro del mensaje.
* **📊 Dashboard de KPIs:** Resumen en tiempo real del estado de salud del sistema (Total, Errors, Warnings).
* **🖥️ Interfaz Profesional:** UI moderna basada en `CustomTkinter` con escalado de fuente dinámico para análisis prolongados.
* **🔒 Privacidad por Diseño:** Procesamiento 100% local. Los datos nunca salen de tu máquina.

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
main.py: Punto de entrada principal.

log_master/gui.py: Motor de la interfaz gráfica y gestión de eventos.

log_master/core/engine.py: Lógica de procesamiento de datos con Pandas.

requirements.txt: Dependencias necesarias para el entorno.
