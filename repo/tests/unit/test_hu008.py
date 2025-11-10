#TEST HU008-VER ESTADISTICAS

import pytest
from src.models import Proyecto, Columna, Tarea, Usuario
from src.utils import ProyectoAnalytics
from datetime import datetime, timedelta

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

# CASO DE PRUEBA PM12-TC-22/VISUALIZACION DEL TOTAL DE TAREAS
def test_visualizar_total_tareas_proyecto(test_proyecto):
    total_tareas = test_proyecto.contar_tareas()
    assert total_tareas == 3

# CASO DE PRUEBA PM12-TC-29/CONTEO DE TAREAS ASIGNADAS VS SIN ASIGNAR
def test_tareas_asignadas_vs_sin_asignar(test_proyecto):
    conteo_tareas = ProyectoAnalytics.obtener_tareas_por_usuario(test_proyecto)
    assert conteo_tareas["Sin Asignar"] == 1
    assert conteo_tareas["Juan"] == 1
    assert conteo_tareas["Hammer"] == 1

# CASO DE PRUEBA PM12-TC-26/VISUALIZACIÓN DE TAREAS POR ESTADO
def test_porcentaje_tareas_estado(test_proyecto):
    # Obtener el conteo de tareas por estado
    estados_tareas = ProyectoAnalytics.obtener_tareas_por_estado(test_proyecto)
    total_estados = sum(estados_tareas.values())

    #CALCULO DE PORCENTAJES
    porcentajes = {}
    for estado, cantidad in estados_tareas.items():
        porcentaje = (cantidad / total_estados) * 100
        porcentajes[estado] = porcentaje

    #VERIFICACIÓN DE ESTADOS
    assert "Pendiente" in porcentajes
    assert "En Progreso" in porcentajes
    assert "Completada" in porcentajes

    #VALIDACIÓN DE RANGOS
    for valor in porcentajes.values():
        assert valor >= 0
        assert valor <= 100

# CASO DE PRUEBA PM12-TC-30/PORCENTAJE GENERAL DEL PROYECTO
def test_progreso_general_proyecto(test_proyecto):
    assert ProyectoAnalytics.obtener_progreso_proyecto(test_proyecto)

# CASO DE PRUEBA PM12-TC-31/IDENTIFICAR TAREAS RETRASADAS
def test_identificar_tareas_retrasadas(test_proyecto):
    # SE CREA UNA TAREA VENCIDA
    tareaV = Tarea("Tarea Vencida")
    tareaV.fecha_vencimiento = (datetime.now() - timedelta(days=5)).isoformat()
    
    #SE AGREGA AL PROYECTO
    test_proyecto.columnas[0].agregar_tarea(tareaV)
    tareas_retrasadas = ProyectoAnalytics.obtener_tareas_retrasadas(test_proyecto)

    #SE COMPRUEBA LA LISTA DE TAREAS VENCIDAS
    assert tareas_retrasadas[0].titulo == "Tarea Vencida"


