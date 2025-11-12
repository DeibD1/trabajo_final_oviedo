import unittest
from pathlib import Path
from src.models import Proyecto, Columna, Tarea
from src.storage import StorageManager
import sys
import os
import uuid


class TestVisualizacionColumnasTablero(unittest.TestCase):

    def setUp(self):
        self.ruta = Path("datos_test_columnas.json")
        self.storage = StorageManager(self.ruta)

        # Crear proyecto con columnas configuradas
        proyecto = Proyecto(proyecto_id="p1", nombre="Proyecto Columnas", descripcion="")

        nombres_columnas = ["Pendiente", "En Progreso", "Revisión", "Completada"]
        for i, nombre in enumerate(nombres_columnas):
            proyecto.columnas.append(Columna(nombre=nombre, orden=i))

        datos = {"proyectos": [proyecto.to_dict()], "usuarios": []}
        self.storage.guardar_datos(datos)

    def tearDown(self):
        import os
        if self.ruta.exists():
            os.remove(self.ruta)

    def test_visualizar_todas_columnas(self):
        datos = self.storage.cargar_datos()
        proyectos_data = datos.get("proyectos", [])
        proyectos = [Proyecto.from_dict(p) for p in proyectos_data]

        proyecto = next((p for p in proyectos if p.proyecto_id == "p1"), None)
        self.assertIsNotNone(proyecto)

        nombres_esperados = ["Pendiente", "En Progreso", "Revisión", "Completada"]
        nombres_columnas = [columna.nombre for columna in proyecto.columnas]

        self.assertCountEqual(nombres_columnas, nombres_esperados)

        #Prueba numero 2

class TestVisualizacionTareasEnColumnas(unittest.TestCase):

    def setUp(self):
        self.ruta = Path("datos_test_tareas_por_columna.json")
        self.storage = StorageManager(self.ruta)
        
        proyecto = Proyecto(proyecto_id="p1", nombre="Proyecto Tareas Columnas", descripcion="")
        
        col_pendiente = Columna(nombre="Pendiente", orden=0)
        col_enprogreso = Columna(nombre="En Progreso", orden=1)
        
        tareas_pendientes = [
            Tarea(tarea_id="t1", titulo="Tarea 1"),
            Tarea(tarea_id="t2", titulo="Tarea 2"),
        ]
        tareas_enprogreso = [
            Tarea(tarea_id="t3", titulo="Tarea 3"),
            Tarea(tarea_id="t4", titulo="Tarea 4"),
        ]
        
        for tarea in tareas_pendientes:
            col_pendiente.agregar_tarea(tarea)
        for tarea in tareas_enprogreso:
            col_enprogreso.agregar_tarea(tarea)
        
        proyecto.columnas.extend([col_pendiente, col_enprogreso])
        
        datos_guardar = {
            "proyectos": [proyecto.to_dict()],
            "usuarios": []
        }
        self.storage.guardar_datos(datos_guardar)
    
    def tearDown(self):
        import os
        if self.ruta.exists():
            os.remove(self.ruta)
    
    def test_visualizar_tareas_columnas(self):
        datos = self.storage.cargar_datos()
        proyectos_data = datos.get("proyectos", [])
        proyectos = [Proyecto.from_dict(p) for p in proyectos_data]
        
        proyecto = next((p for p in proyectos if p.proyecto_id == "p1"), None)
        self.assertIsNotNone(proyecto)
        
        # Diccionario con nombre columna -> lista de IDs de tareas
        tareas_en_columnas = {
            columna.nombre: [tarea.tarea_id for tarea in columna.tareas]
            for columna in proyecto.columnas
        }
        
        self.assertCountEqual(tareas_en_columnas.get("Pendiente", []), ["t1", "t2"])
        self.assertCountEqual(tareas_en_columnas.get("En Progreso", []), ["t3", "t4"])

        #Prueba numero 3

class TestVisualizacionParcialIDTarea(unittest.TestCase):

    def setUp(self):
        self.ruta = Path("datos_test_id_parcial.json")
        self.storage = StorageManager(self.ruta)

        proyecto = Proyecto(proyecto_id="p1", nombre="Proyecto Visualización ID", descripcion="")

        columna = Columna(nombre="Pendiente", orden=0)

        # Crear tareas con UUID válido (si no se pasa se generan automáticamente)
        tarea1 = Tarea(tarea_id=str(uuid.uuid4()), titulo="Tarea 1")
        tarea2 = Tarea(tarea_id=str(uuid.uuid4()), titulo="Tarea 2")

        columna.agregar_tarea(tarea1)
        columna.agregar_tarea(tarea2)

        proyecto.columnas.append(columna)

        datos = {"proyectos": [proyecto.to_dict()], "usuarios": []}
        self.storage.guardar_datos(datos)

    def tearDown(self):
        import os
        if self.ruta.exists():
            os.remove(self.ruta)

    def test_visualizar_parcial_id_tarea(self):
        datos = self.storage.cargar_datos()
        proyectos_data = datos.get("proyectos", [])
        proyectos = [Proyecto.from_dict(p) for p in proyectos_data]
        proyecto = next((p for p in proyectos if p.proyecto_id == "p1"), None)
        self.assertIsNotNone(proyecto)

        for columna in proyecto.columnas:
            for tarea in columna.tareas:
                self.assertEqual(len(tarea.tarea_id), 36, "UUID inválido para tarea")
                id_parcial = tarea.tarea_id[:8]
                self.assertEqual(len(id_parcial), 8, "ID parcial debe tener 8 caracteres")
                print(f"Tarea {tarea.titulo} ID parcial: {id_parcial}")

        #Prueba numero 4

class TestValidacionLayoutTablero(unittest.TestCase):

    def setUp(self):
        self.ruta = Path("datos_test_layout.json")
        self.storage = StorageManager(self.ruta)
        
        proyecto = Proyecto(proyecto_id="p1", nombre="Proyecto Layout", descripcion="")
        
        col_pendiente = Columna(nombre="Pendiente", orden=0)
        col_enprogreso = Columna(nombre="En Progreso", orden=1)
        
        tarea1 = Tarea(tarea_id="t1", titulo="Tarea 1")
        tarea2 = Tarea(tarea_id="t2", titulo="Tarea 2")
        
        col_pendiente.agregar_tarea(tarea1)
        col_enprogreso.agregar_tarea(tarea2)
        
        proyecto.columnas.extend([col_pendiente, col_enprogreso])
        
        datos = {"proyectos": [proyecto.to_dict()], "usuarios": []}
        self.storage.guardar_datos(datos)

    def tearDown(self):
        import os
        if self.ruta.exists():
            os.remove(self.ruta)

    def test_validar_layout_tablero(self):
        datos = self.storage.cargar_datos()
        proyectos_data = datos.get("proyectos", [])
        proyectos = [Proyecto.from_dict(p) for p in proyectos_data]
        proyecto = next((p for p in proyectos if p.proyecto_id == "p1"), None)
        self.assertIsNotNone(proyecto)

        # Verificar columnas están ordenadas por orden lógico ascendente
        ordenes = [col.orden for col in proyecto.columnas]
        self.assertEqual(ordenes, sorted(ordenes), "Columnas no están ordenadas por orden ascendente")
        
        # Verificar columnas no vacías
        for col in proyecto.columnas:
            self.assertTrue(len(col.tareas) > 0, f"Columna {col.nombre} está vacía")
        
        # Verificar tareas únicas y con título legible
        ids_tareas = set()
        for col in proyecto.columnas:
            for tarea in col.tareas:
                self.assertNotIn(tarea.tarea_id, ids_tareas, f"Tarea {tarea.tarea_id} duplicada")
                ids_tareas.add(tarea.tarea_id)
                self.assertTrue(tarea.titulo.strip(), f"Tarea {tarea.tarea_id} tiene título vacío")



if __name__ == "__main__":
    unittest.main()
