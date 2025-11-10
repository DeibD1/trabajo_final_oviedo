#HISTORIA DE USUARIO HU009-EXPORTAR DATOS
from src.utils import ExportadorDatos
from src.models import Proyecto, Columna, Tarea
import pytest

#CREACION DE PROYECTO DE PRUEBA
@pytest.fixture
def test_proyecto():
    proyecto = Proyecto("Proyecto Prueba")
    columna1 = proyecto.agregar_columna("Pendiente")
    columna2 = proyecto.agregar_columna("Completadas")

    # Crear tareas
    tarea1 = Tarea(titulo= "Tarea 1", prioridad="Alta", asignado_a="Juan")
    tarea2 = Tarea(titulo= "Tarea 2", prioridad="Media")  # sin asignar
    tarea3 = Tarea(titulo= "Tarea 3", prioridad="Urgente", asignado_a="Hammer")
    tarea3.estado = "Completada"

    columna1.agregar_tarea(tarea1)
    columna1.agregar_tarea(tarea2)
    columna2.agregar_tarea(tarea3)

    return proyecto

#CASO DE PRUEBA PM12-TC-40/EXPORTAR TAREAS A FORMATO CSV
def test_exportar_tareas_a_csv(test_proyecto):
    csv_data = ExportadorDatos.exportar_a_csv(test_proyecto)

    #SE COMPRUEBA QUE SE GENERA TEXTO
    assert isinstance(csv_data, str)

    # VERIFICACIÓN DE CABECERAS
    assert "titulo" in csv_data.lower() or "tã\xadtulo" in csv_data.lower()
    assert "prioridad" in csv_data.lower()

#CASO DE PRUEBA PM12-TC-37/CONFIRMACIÓN DE EXPORTACIÓN
@pytest.mark.skip(reason="El sistema aún no muestra mensaje de confirmación")
def test_mensaje_confirmacion_exportacion():
    pass

#CASO DE PRUEBA PM12-TC-42/VERIFICACION DE EXPORTACION DE FORMATO JSON
def test_datos_exportados_completos(test_proyecto):
    datos_json = ExportadorDatos.exportar_a_json_simple(test_proyecto)

    # Revisar que contenga claves importantes
    assert "nombre" in datos_json
    assert "columnas" in datos_json
    assert "proyecto_id" in datos_json

