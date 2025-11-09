# TEST DE HU007 - GESTOR DE COLUMNAS

import pytest
from src.models import Proyecto, Columna, Tarea, Usuario


def proyecto_vacio():
    """Crea un proyecto vacío de prueba"""
    return Proyecto(nombre="Proyecto Prueba", descripcion="Proyecto de testing")

#CASO DE PRUEBA PM12-TC-6

def test_nombre_columna_es_obligatorio(proyecto_vacio):
    with pytest.raises(TypeError):
        Columna()  # Falta nombre, debe lanzar error de argumentos
    # Alternativamente, validamos comportamiento de Proyecto:
    with pytest.raises(ValueError):
        proyecto_vacio.agregar_columna("")  # Nombre vacío no permitido

