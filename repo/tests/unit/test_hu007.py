# TEST DE HU007 - GESTOR DE COLUMNAS

#IMPORTACIONES
import pytest
from src.models import Proyecto, Columna, Tarea, Usuario

#CREACION DE PROYECTO VACIO
@pytest.fixture
def test_proyecto():
    return Proyecto(nombre="Tester", descripcion="Esto es una prueba :D")

#CASO DE PRUEBA PM12-TC-6/NOMBRE DE COLUMNA OBLIGATORIA

def test_nombre_obligatorio_columna(test_proyecto):
    # Validamos agregando un caracter vacio al nombre de la columna
    with pytest.raises(ValueError): #Se captura el error 
        test_proyecto.agregar_columna("")  

#CASO DE PRUEBA PM12-TC-9/TEST DE COMPROBACIÓN DE COLUMNAS DUPLICADAS
def test_validar_creacion_columnas_duplicadas(test_proyecto):
    test_proyecto.agregar_columna("Pendiente") #Columna 1
    with pytest.raises(ValueError):
        test_proyecto.agregar_columna("Pendiente") #Duplicado columna 1

#CASO DE PRUEBA PM12-TC-2/TEST RENOMBRAR COLUMNA YA EXISTENTE EN PROYECTO
def test_renombrar_columna_existente(test_proyecto):
    columna = test_proyecto.agregar_columna("TesterQA") #Se crea una columna de prueba
    columna.nombre = "Hecho" #Se reasigna el nombre de dicha columna
    assert columna.nombre == "Hecho" #Verifica

#CASO DE PRUEBA PM12-TC-4/TEST ELIMINACION DE COLUMNA (¿PIDE CONFIRMACION?)
def test_eliminar_columna_validacion(test_proyecto):
    columna = test_proyecto.agregar_columna("Hecho") #Columna test
    resultado = test_proyecto.eliminar_columna(columna.columna_id) #Resultado eliminacion
    assert resultado is True #¿Si se elimino?
    assert len(test_proyecto.columnas) == 0

#CASO DE PRUEBA PM12-TC-5/ELIMINACION DE COLUMNA Y TAREAS ASOCIADAS
def test_eliminacion_columna_tareas_asociadas(test_proyecto):
    columna_t = test_proyecto.agregar_columna("Columnita")
    tarea_col = Tarea(titulo= "Tareita", descripcion= "test de tareita", 
                      prioridad= "Media")
    tarea_col2 = Tarea(titulo= "Tareita2", descripcion= "test de tareita2", 
                      prioridad= "Media")
    columna_t.agregar_tarea(tarea_col)
    columna_t.agregar_tarea(tarea_col2)
    #Validamos las tareas
    assert columna_t.contar_tareas() >= 1
    #Eliminar columna
    test_proyecto.eliminar_columna(columna_t.columna_id)
    #Validacion de las tareas en el proyecto despues de eliminar
    assert test_proyecto.contar_tareas() == 0
    
