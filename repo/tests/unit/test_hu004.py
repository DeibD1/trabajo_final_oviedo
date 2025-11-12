import unittest
import pytest
from src.models import Proyecto
from src.cli import CliInterface
import builtins
import types
from src.models import Proyecto, Columna, Tarea, Usuario
from src.storage import StorageManager
from pathlib import Path



class TestEditarTituloTarea(unittest.TestCase):

    def setUp(self):
        self.ruta_datos = Path("test_datos.json")
        self.manager = StorageManager(self.ruta_datos)

        # Crear usuario propietario del proyecto
        usuario = Usuario(nombre="Juan", email="juan@example.com")

        # Crear proyecto
        self.proyecto = Proyecto(
            proyecto_id="p1",
            nombre="Proyecto de Prueba",
            descripcion="",
            propietario_id=usuario.usuario_id
        )

        # Crear columna y tarea
        columna = Columna(nombre="Pendiente", orden=0)
        tarea = Tarea(tarea_id="t1", titulo="Título Original")
        columna.agregar_tarea(tarea)

        self.proyecto.columnas.append(columna)

        # Guardar proyecto inicial
        self.manager.guardar_proyecto(self.proyecto)

    def tearDown(self):
        if self.ruta_datos.exists():
            self.ruta_datos.unlink()

    def test_editar_titulo_tarea(self):
        proyecto = self.manager.cargar_proyecto("p1")
        tarea = proyecto.columnas[0].tareas[0]

        # Editar título
        tarea.titulo = "Título Editado"
        self.manager.guardar_proyecto(proyecto)

        # Verificar
        proyecto_actualizado = self.manager.cargar_proyecto("p1")
        tarea_actualizada = proyecto_actualizado.columnas[0].tareas[0]

        self.assertEqual(tarea_actualizada.titulo, "Título Editado")
        


        # Segunda Prueba
class TestEditarDescripcionTarea(unittest.TestCase):

    def setUp(self):
        self.ruta_datos = Path("test_descripcion.json")
        self.manager = StorageManager(self.ruta_datos)

        # Crear usuario válido
        self.usuario = Usuario(
            nombre="Usuario Test",
            email="usuario@test.com",
            usuario_id="user1"
        )
        self.manager.guardar_usuario(self.usuario)

        # Crear proyecto válido con parámetros correctos
        self.proyecto = Proyecto(
            nombre="Proyecto Prueba",
            descripcion="Descripción original",
            propietario_id=self.usuario.usuario_id,
            proyecto_id="p123"
        )
        self.manager.guardar_proyecto(self.proyecto)


    def test_editar_descripcion_tarea(self):
        usuario_autenticado = self.manager.cargar_usuario("user1")
        self.assertIsNotNone(usuario_autenticado)

        proyecto = self.manager.cargar_proyecto("p123")
        self.assertIsNotNone(proyecto)

        descripcion_anterior = proyecto.descripcion
        proyecto.descripcion = "Descripción editada para prueba"

        resultado = self.manager.guardar_proyecto(proyecto)
        self.assertTrue(resultado)

        proyecto_actualizado = self.manager.cargar_proyecto("p123")
        self.assertNotEqual(descripcion_anterior, proyecto_actualizado.descripcion)
        self.assertEqual(proyecto_actualizado.descripcion, "Descripción editada para prueba")


    def tearDown(self):
        if self.ruta_datos.exists():
            self.ruta_datos.unlink()


        #Caso de Prueba #3
class TestCambiarPrioridadTarea(unittest.TestCase):

    def setUp(self):
        self.ruta_datos = Path("test_prioridad.json")
        self.manager = StorageManager(self.ruta_datos)

        # Crear usuario válido (email obligatorio)
        self.usuario = Usuario(
            nombre="Usuario Prueba",
            email="usuario@test.com",
            usuario_id="user1"
        )
        self.manager.guardar_usuario(self.usuario)

        # Crear proyecto válido
        self.proyecto = Proyecto(
            nombre="Proyecto Prioridad",
            descripcion="",
            propietario_id=self.usuario.usuario_id,
            proyecto_id="p001"
        )

        # Crear columna y tarea con prioridad inicial 'Media'
        columna = Columna(nombre="Pendiente", orden=0)
        tarea = Tarea(
            tarea_id="t1",
            titulo="Tarea con Prioridad",
            prioridad="Media"
        )
        columna.agregar_tarea(tarea)

        self.proyecto.columnas.append(columna)

        # Guardar proyecto inicial
        self.manager.guardar_proyecto(self.proyecto)

    def test_cambiar_prioridad(self):
        # Confirmar usuario autenticado
        usuario = self.manager.cargar_usuario("user1")
        self.assertIsNotNone(usuario)

        # Cargar proyecto y verificar prioridad inicial
        proyecto = self.manager.cargar_proyecto("p001")
        tarea = proyecto.columnas[0].tareas[0]

        self.assertEqual(tarea.prioridad, "Media")

        # Cambiar prioridad
        tarea.prioridad = "Alta"
        resultado = self.manager.guardar_proyecto(proyecto)

        # Verificar cambio persistido
        proyecto_modificado = self.manager.cargar_proyecto("p001")
        tarea_modificada = proyecto_modificado.columnas[0].tareas[0]

        self.assertEqual(tarea_modificada.prioridad, "Alta")
        self.assertTrue(resultado)

    def tearDown(self):
        if self.ruta_datos.exists():
            self.ruta_datos.unlink()

        #Caso de Prueba #4


    # Caso de Prueba #5

def test_reasignar_responsable_tarea(tmp_path):
    # Archivo temporal para pruebas
    ruta = tmp_path / "datos.json"
    storage = StorageManager(ruta)

    # ----- Crear usuarios -----
    usuario_original = Usuario(nombre="User A", email="a@test.com", usuario_id="user_a")
    usuario_nuevo = Usuario(nombre="User B", email="b@test.com", usuario_id="user_b")

    storage.guardar_usuario(usuario_original)
    storage.guardar_usuario(usuario_nuevo)

    # ----- Crear proyecto con columna y tarea -----
    proyecto = Proyecto(
        nombre="Proyecto Test",
        descripcion="",
        propietario_id=usuario_original.usuario_id,
        proyecto_id="proyecto1"
    )

    columna = Columna(nombre="Pendiente", orden=0)
    tarea = Tarea(
        titulo="Tarea X",
        tarea_id="T-005",
        asignado_id=usuario_original.usuario_id
    )
    columna.agregar_tarea(tarea)

    proyecto.columnas.append(columna)
    storage.guardar_proyecto(proyecto)

    # -------------------------------
    # Ejecutar prueba: cambiar responsable
    # -------------------------------
    proyecto = storage.cargar_proyecto("proyecto1")
    tarea = proyecto.columnas[0].tareas[0]

    # Verificar asignación original
    assert tarea.asignado_id == "user_a"

    # Reasignar
    tarea.asignado_id = "user_b"

    # Guardar cambios
    storage.guardar_proyecto(proyecto)

    # Recargar
    proyecto2 = storage.cargar_proyecto("proyecto1")
    tarea2 = proyecto2.columnas[0].tareas[0]

    # Validar
    assert tarea2.asignado_id == "user_b"

    # Caso de Prueba #6

def test_mover_tarea_entre_columnas(tmp_path):
    ruta = tmp_path / "datos.json"
    storage = StorageManager(ruta)

    # Crear usuario
    usuario = Usuario(nombre="User A", email="a@test.com", usuario_id="user_a")
    storage.guardar_usuario(usuario)

    # Crear proyecto con dos columnas
    proyecto = Proyecto(
        nombre="Proyecto Test",
        descripcion="",
        propietario_id=usuario.usuario_id,
        proyecto_id="proyecto1"
    )

    columna1 = Columna(nombre="Pendiente", orden=0)
    columna2 = Columna(nombre="En Progreso", orden=1)

    # Crear tarea en la primera columna
    tarea = Tarea(
        titulo="Mover Tarea",
        tarea_id="T-006"
    )
    columna1.agregar_tarea(tarea)
    proyecto.columnas.extend([columna1, columna2])

    storage.guardar_proyecto(proyecto)

    # ------------------------------
    # MOVER LA TAREA DE COLUMNA
    # ------------------------------
    proyecto = storage.cargar_proyecto("proyecto1")

    columna_origen = proyecto.columnas[0]
    columna_destino = proyecto.columnas[1]

    tarea = columna_origen.tareas[0]

    # Quitar de la columna origen
    columna_origen.tareas.remove(tarea)

    # Agregar a la columna destino
    columna_destino.tareas.append(tarea)

    # Guardar cambios
    storage.guardar_proyecto(proyecto)

    # ------------------------------
    # VERIFICAR DESPUÉS DE RECARGAR
    # ------------------------------
    proyecto2 = storage.cargar_proyecto("proyecto1")

    col1 = proyecto2.columnas[0]
    col2 = proyecto2.columnas[1]

    # No debe estar en la columna Pendiente
    assert len(col1.tareas) == 0

    # Debe estar en En Progreso
    assert col2.tareas[0].tarea_id == "T-006"

    # Caso de Prueba #7

def test_agregar_etiquetas_a_tarea(tmp_path):
    ruta = tmp_path / "datos.json"
    storage = StorageManager(ruta)

    # Crear usuario
    usuario = Usuario(nombre="User A", email="a@test.com", usuario_id="user_a")
    storage.guardar_usuario(usuario)

    # Crear proyecto con columna y tarea (sin pasar etiquetas en constructor)
    proyecto = Proyecto(
        nombre="Proyecto Test",
        descripcion="",
        propietario_id=usuario.usuario_id,
        proyecto_id="proyecto1"
    )

    columna = Columna(nombre="Pendiente", orden=0)

    tarea = Tarea(
        titulo="Tarea Etiquetas",
        tarea_id="T-007"
    )

    # Asegurar que la lista existe
    tarea.etiquetas = []

    columna.agregar_tarea(tarea)
    proyecto.columnas.append(columna)
    storage.guardar_proyecto(proyecto)

    # ------------------------------
    # Agregar nuevas etiquetas
    # ------------------------------
    nuevas_etiquetas = ["importante", "pendiente"]

    proyecto = storage.cargar_proyecto("proyecto1")
    tarea = proyecto.columnas[0].tareas[0]

    # Agregar etiquetas
    for etiqueta in nuevas_etiquetas:
        if etiqueta not in tarea.etiquetas:
            tarea.etiquetas.append(etiqueta)

    storage.guardar_proyecto(proyecto)

    # ------------------------------
    # Verificar
    # ------------------------------
    proyecto2 = storage.cargar_proyecto("proyecto1")
    tarea2 = proyecto2.columnas[0].tareas[0]

    for etiqueta in nuevas_etiquetas:
        assert etiqueta in tarea2.etiquetas

        # Caso de Prueba #8

def test_quitar_etiquetas_de_tarea(tmp_path):
    ruta = tmp_path / "datos.json"
    storage = StorageManager(ruta)

    # Crear usuario
    usuario = Usuario(nombre="User A", email="a@test.com", usuario_id="user_a")
    storage.guardar_usuario(usuario)

    # Crear proyecto con una tarea que tiene etiquetas
    proyecto = Proyecto(
        nombre="Proyecto Test",
        descripcion="",
        propietario_id=usuario.usuario_id,
        proyecto_id="proyecto1"
    )

    columna = Columna(nombre="Pendiente", orden=0)

    tarea = Tarea(
        titulo="Tarea para eliminar etiquetas",
        tarea_id="T-008"
    )

    # Definir etiquetas iniciales
    tarea.etiquetas = ["backend", "api"]

    columna.agregar_tarea(tarea)
    proyecto.columnas.append(columna)

    storage.guardar_proyecto(proyecto)

    # ------------------------------
    # Eliminar etiquetas
    # ------------------------------
    etiquetas_a_eliminar = ["backend"]

    proyecto = storage.cargar_proyecto("proyecto1")
    tarea = proyecto.columnas[0].tareas[0]

    for etiqueta in etiquetas_a_eliminar:
        if etiqueta in tarea.etiquetas:
            tarea.etiquetas.remove(etiqueta)

    storage.guardar_proyecto(proyecto)

    # ------------------------------
    # Verificar persistencia
    # ------------------------------
    proyecto2 = storage.cargar_proyecto("proyecto1")
    tarea2 = proyecto2.columnas[0].tareas[0]

    for etiqueta in etiquetas_a_eliminar:
        assert etiqueta not in tarea2.etiquetas

        # Caso de Prueba #9

def test_eliminar_tarea_con_confirmacion(tmp_path):
    ruta = tmp_path / "datos.json"
    storage = StorageManager(ruta)

    # Crear usuario
    usuario = Usuario(nombre="User A", email="a@test.com", usuario_id="user_a")
    storage.guardar_usuario(usuario)

    # Crear proyecto con una columna y una tarea
    proyecto = Proyecto(
        nombre="Proyecto Test",
        descripcion="",
        propietario_id=usuario.usuario_id,
        proyecto_id="proyecto1"
    )

    columna = Columna(nombre="Pendiente", orden=0)
    tarea = Tarea(
        titulo="Tarea a eliminar",
        tarea_id="T-010"
    )
    columna.agregar_tarea(tarea)
    proyecto.columnas.append(columna)
    storage.guardar_proyecto(proyecto)

    # -----------------------------
    # Ejecutar eliminación
    # -----------------------------
    confirmacion = True     # Simulación de confirmación

    proyecto = storage.cargar_proyecto("proyecto1")
    columna = proyecto.columnas[0]
    tarea = columna.tareas[0]

    assert tarea.tarea_id == "T-010"

    if confirmacion:
        columna.tareas.remove(tarea)

    storage.guardar_proyecto(proyecto)

    # -----------------------------
    # Verificar persistencia
    # -----------------------------
    proyecto2 = storage.cargar_proyecto("proyecto1")

    tarea_existe = any(
        t.tarea_id == "T-010"
        for col in proyecto2.columnas
        for t in col.tareas
    )

    assert not tarea_existe, "La tarea no fue eliminada"

        #Caso de prueba 10

def test_reasignar_responsable_tarea(tmp_path):
    ruta = tmp_path / "datos.json"
    storage = StorageManager(ruta)

    # Crear usuarios
    usuario_original = Usuario(
        nombre="User A",
        email="a@test.com",
        usuario_id="user_a"
    )

    usuario_nuevo = Usuario(
        nombre="User B",
        email="b@test.com",
        usuario_id="user_b"
    )

    storage.guardar_usuario(usuario_original)
    storage.guardar_usuario(usuario_nuevo)

    # Crear proyecto y tarea
    proyecto = Proyecto(
        nombre="Proyecto Test",
        descripcion="",
        propietario_id=usuario_original.usuario_id,
        proyecto_id="proyecto1"
    )

    columna = Columna(nombre="Pendiente", orden=0)
    tarea = Tarea(
        titulo="Tarea X",
        tarea_id="T-005",
        asignado_a="user_a"   # ✅ CORRECTO
    )

    columna.agregar_tarea(tarea)
    proyecto.columnas.append(columna)
    storage.guardar_proyecto(proyecto)

    # ---------------------
    # Reasignar responsable
    # ---------------------
    proyecto = storage.cargar_proyecto("proyecto1")
    tarea = proyecto.columnas[0].tareas[0]

    # Verificar responsable inicial
    assert tarea.asignado_a == "user_a"

    # Cambiar responsable
    tarea.asignado_a = "user_b"
    storage.guardar_proyecto(proyecto)

    # ---------------------
    # Verificar persistencia
    # ---------------------
    proyecto2 = storage.cargar_proyecto("proyecto1")
    tarea2 = proyecto2.columnas[0].tareas[0]

    assert tarea2.asignado_a == "user_b"


if __name__ == "__main__":
    unittest.main()
