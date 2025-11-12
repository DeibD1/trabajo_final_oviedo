# 🧪 Guía de Ejecución de Pruebas - Project Manager

Este documento describe la estructura, el entorno y los pasos necesarios para ejecutar correctamente las **pruebas automatizadas** del sistema **Project Manager**, desarrollado en Python.  
El objetivo principal es validar las funcionalidades clave definidas en las HU, garantizando que los criterios de aceptación se cumplan de forma automatizada.

---

## 📁 Estructura del Proyecto

La estructura del repositorio sigue la siguiente organización:

epo/
├─ src/ # Código fuente principal
│ ├─ models.py # Clases base (Usuario, Tarea, Columna, Proyecto)
│ ├─ storage.py # Módulo de persistencia de datos
│ ├─ utils.py # Módulos de análisis y exportación
│ └─ cli.py # Interfaz de línea de comandos
│
├─ tests/
│ ├─ unit/
│ │ ├─ init.py
│ │ ├─ test_hu007.py # Pruebas: Gestión de columnas
│ │ ├─ test_hu008.py # Pruebas: Estadísticas del proyecto
│ │ └─ test_hu009.py # Pruebas: Exportación de datos
│
└─ README.md # Documentación general

### 📦 Instalación de dependencias

Ejecuta en la raíz del proyecto:
.\venv\Scripts\activate

Despues:

en el bash:
pip install pytest pytest-cov

### ▶️ Ejecución de pruebas

Desde la raíz del proyecto, ejecuta:

pytest -v

### 2️⃣ Ejecutar pruebas de una historia de usuario específica

pytest repo/tests/unit/[test_name].py -v

También puedes ejecutar un caso específico usando -k para buscar por nombre:

pytest -k "progreso_general" -v

### 4️⃣ Pruebas pendientes o no implementadas

pytest -rs

```

```
