import unittest
from pathlib import Path
from src.models import Proyecto, Columna, Tarea
from src.storage import StorageManager
import sys
import os



class TestBusquedaParcial(unittest.TestCase):

    def setUp(self):
        # Ruta para datos de prueba
        self.ruta_datos = Path("ruta/datos_test.json")
        self.storage = StorageManager(self.ruta_datos)
        
        # Crea proyecto de ejemplo con columnas y tareas variadas
        proyecto = Proyecto(proyecto_id="proyecto1", nombre="Proyecto Test", descripcion="")
        columna1 = Columna(nombre="Pendiente", orden=0)
        columna1.agregar_tarea(Tarea(titulo="Pago pendiente", descripcion="", prioridad="Media"))
        columna1.agregar_tarea(Tarea(titulo="Revisar módulo de facturación", descripcion="", prioridad="Media"))
        columna1.agregar_tarea(Tarea(titulo="Pago automático", descripcion="", prioridad="Media"))
        
        proyecto.columnas.append(columna1)
        
        # Guarda datos iniciales para la prueba
        datos_guardar = {
            "proyectos": [proyecto.to_dict()],
            "usuarios": []
        }
        self.storage.guardar_datos(datos_guardar)
    
    def test_busqueda_parcial_titulo_tareas(self):
        palabra_busqueda = "Pago"
        datos = self.storage.cargar_datos()
        proyectos_data = datos.get("proyectos", [])
        proyectos = [Proyecto.from_dict(p) for p in proyectos_data]
        
        proyecto = next((p for p in proyectos if p.proyecto_id == "proyecto1"), None)
        self.assertIsNotNone(proyecto, "Proyecto no encontrado")
        
        resultados = []
        for columna in proyecto.columnas:
            for tarea in columna.tareas:
                if palabra_busqueda.lower() in tarea.titulo.lower():
                    resultados.append(tarea.titulo)
        
        titulos_esperados = [
            "Pago pendiente",
            "Pago automático"
        ]
        self.assertCountEqual(resultados, titulos_esperados)

        #Prueba numero 2

        #Prueba numero 3

class TestVisualizarColumnaPorTarea(unittest.TestCase):

    def setUp(self):
        self.ruta_datos = Path("ruta/datos_visualizacion.json")
        self.storage = StorageManager(self.ruta_datos)
        
        proyecto = Proyecto(proyecto_id="p1", nombre="Proyecto Vis", descripcion="")
        
        col_pendiente = Columna(nombre="Pendiente", orden=0)
        col_enprogreso = Columna(nombre="En Progreso", orden=1)

        tarea1 = Tarea(tarea_id="t1", titulo="Tarea 1")
        tarea2 = Tarea(tarea_id="t2", titulo="Tarea 2")
        
        col_pendiente.agregar_tarea(tarea1)
        col_enprogreso.agregar_tarea(tarea2)
        
        proyecto.columnas.append(col_pendiente)
        proyecto.columnas.append(col_enprogreso)
        
        datos_guardar = {
            "proyectos": [proyecto.to_dict()],
            "usuarios": []
        }
        self.storage.guardar_datos(datos_guardar)

    def test_visualizar_columna_por_tarea(self):  # ✅ AHORA SÍ DENTRO DE LA CLASE
        datos = self.storage.cargar_datos()
        proyectos_data = datos.get("proyectos", [])

        # ✅ Corrección del método del modelo
        proyectos = [Proyecto.from_dict(p) for p in proyectos_data]
        
        proyecto = next((p for p in proyectos if p.proyecto_id == "p1"), None)
        self.assertIsNotNone(proyecto, "Proyecto no encontrado")
        
        tarea_a_columna = {}
        for columna in proyecto.columnas:
            for tarea in columna.tareas:
                tarea_a_columna[tarea.tarea_id] = columna.nombre
        
        self.assertEqual(tarea_a_columna.get("t1"), "Pendiente")
        self.assertEqual(tarea_a_columna.get("t2"), "En Progreso")

    #Prueba numero 4

class TestBusquedaVaciaRetornaTodasTareas(unittest.TestCase):

    def setUp(self):
        self.ruta_datos = Path("ruta/datos_busqueda_vacia.json")
        self.storage = StorageManager(self.ruta_datos)
        
        proyecto = Proyecto(proyecto_id="p1", nombre="Proyecto Búsqueda Vacía", descripcion="")
        
        col_pendiente = Columna(nombre="Pendiente", orden=0)
        col_enprogreso = Columna(nombre="En Progreso", orden=1)
        
        tareas_pendientes = [
            Tarea(tarea_id="t1", titulo="Tarea A"),
            Tarea(tarea_id="t2", titulo="Tarea B"),
        ]
        tareas_enprogreso = [
            Tarea(tarea_id="t3", titulo="Tarea C"),
            Tarea(tarea_id="t4", titulo="Tarea D"),
        ]
        
        for tarea in tareas_pendientes:
            col_pendiente.agregar_tarea(tarea)
        for tarea in tareas_enprogreso:
            col_enprogreso.agregar_tarea(tarea)
        
        proyecto.columnas.append(col_pendiente)
        proyecto.columnas.append(col_enprogreso)
        
        datos_guardar = {
            "proyectos": [proyecto.to_dict()],
            "usuarios": []
        }
        self.storage.guardar_datos(datos_guardar)
    
    def test_busqueda_vacia_retorna_todas_tareas(self):
        datos = self.storage.cargar_datos()
        proyectos_data = datos.get("proyectos", [])
        proyectos = [Proyecto.from_dict(p) for p in proyectos_data]
        
        proyecto = next((p for p in proyectos if p.proyecto_id == "p1"), None)
        self.assertIsNotNone(proyecto)
        
        campo_busqueda = ""  # búsqueda vacía
        
        tareas_encontradas = []
        for columna in proyecto.columnas:
            for tarea in columna.tareas:
                if campo_busqueda == "" or campo_busqueda.lower() in tarea.titulo.lower():
                    tareas_encontradas.append(tarea.tarea_id)
        
        # Se espera que encuentre todas las tareas (4 en total)
        self.assertCountEqual(
            tareas_encontradas,
            ["t1", "t2", "t3", "t4"],
            "La búsqueda vacía no retorna todas las tareas"
        )

        #Prueba numero 5
class TestBusquedaVacia(unittest.TestCase):

    def setUp(self):
        self.ruta = Path("datos_test_busqueda_vacia.json")
        self.storage = StorageManager(self.ruta)

        # Crear proyecto con múltiples tareas en diferentes columnas
        proyecto = Proyecto(proyecto_id="p1", nombre="Proyecto Test Vacio", descripcion="")
        columna1 = Columna(nombre="Pendiente", orden=0)
        columna2 = Columna(nombre="En Progreso", orden=1)
        
        tareas_col1 = [
            Tarea(tarea_id="t1", titulo="Tarea 1"),
            Tarea(tarea_id="t2", titulo="Tarea 2"),
        ]
        tareas_col2 = [
            Tarea(tarea_id="t3", titulo="Tarea 3")
        ]
        
        for tarea in tareas_col1:
            columna1.agregar_tarea(tarea)
        for tarea in tareas_col2:
            columna2.agregar_tarea(tarea)
        
        proyecto.columnas.extend([columna1, columna2])

        datos = {"proyectos": [proyecto.to_dict()], "usuarios": []}
        self.storage.guardar_datos(datos)

    def tearDown(self):
        import os
        if self.ruta.exists():
            os.remove(self.ruta)

    def test_busqueda_vacia_no_filtra(self):
        datos = self.storage.cargar_datos()
        proyectos_data = datos.get("proyectos", [])
        proyectos = [Proyecto.from_dict(p) for p in proyectos_data]

        proyecto = next((p for p in proyectos if p.proyecto_id == "p1"), None)
        self.assertIsNotNone(proyecto)

        busqueda = ""  # Campo vacío para búsqueda

        tareas_encontradas = []
        for columna in proyecto.columnas:
            for tarea in columna.tareas:
                if busqueda == "" or busqueda.lower() in tarea.titulo.lower():
                    tareas_encontradas.append(tarea.tarea_id)

        self.assertCountEqual(tareas_encontradas, ["t1", "t2", "t3"])




if __name__ == "__main__":
    unittest.main()
