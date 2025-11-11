# TEST DE HU007 - GESTOR DE COLUMNAS

import pytest
import builtins
import types
from src.models import Proyecto, Columna, Tarea, Usuario
from src.cli import CliInterface
from src.storage import StorageManager

@pytest.fixture
def proyecto_vacio():
    """Crea un proyecto vacío de prueba"""
    return Proyecto(nombre="Proyecto Prueba", descripcion="Proyecto de testing")

# CASOS DE PRUEBA HU-001
#CASO DE PRUEBA PM12-TC-6

def test_nombre_columna_es_obligatorio(proyecto_vacio):
    with pytest.raises(TypeError):
        Columna()  # Falta nombre, debe lanzar error de argumentos
    # Alternativamente, validamos comportamiento de Proyecto:
    with pytest.raises(ValueError):
        proyecto_vacio.agregar_columna("")  # Nombre vacío no permitido


# CASO DE PRUEBA PM12-TC-10

def make_inputs(*values):
    """Devuelve una función para simular builtins.input consumiendo los values en orden."""
    it = iter(values)
    def fake_input(prompt=""):
        try:
            return next(it)
        except StopIteration:
            return ""
    return fake_input

def test_crear_usuario_rechaza_email_sin_punto(monkeypatch, capsys):
    # Se crea interfaz para probar desde la interfaz
    cli = CliInterface()
    # Se ingresa un usuario con monkeypatch para ingresar por consola
    monkeypatch.setattr(builtins, "input", make_inputs("alex", "alex@correo", ""))
    # Se prueba una función de guardar falsa para que intente guardar el usuario
    called = {"ok": False, "usuario": None}
    def fake_guardar(usuario):
        called["ok"] = True
        called["usuario"] = usuario
        return True
    cli.storage.guardar_usuario = fake_guardar
    # Se crea el usuario
    cli.crear_usuario()
    out = capsys.readouterr().out
    # En que caso de que "Ok sea falsa la prueba no fue creada, por lo que la prueba casa 
    # En caso de que no la prueba es fallida
    assert called["ok"] is False, "ERROR: guardar_usuario fue llamado aunque el email no tiene '.'"

    

# CASO DE PRUEBA PM12-TC-7

def test_crear_usuario_rechaza_email_sin_arroba(monkeypatch, capsys):
    # Se crea la interfaz
    cli = CliInterface()
    # Se ingresa un usuario con monkeypatch para ingresar por consola
    monkeypatch.setattr(builtins, "input", make_inputs("alex", "alexcorreo.com", ""))

    # Se prueba una función de guardar falsa para que intente guardar el usuario
    called = {"ok": False, "usuario": None}
    def fake_guardar(usuario):
        called["ok"] = True
        called["usuario"] = usuario
        return True
    cli.storage.guardar_usuario = fake_guardar
    # Se crea el usuario
    cli.crear_usuario()
    # Se guarda la respuesta
    out = capsys.readouterr().out

    # En que caso de que "Ok sea falsa la prueba no fue creada, por lo que la prueba casa 
    # En caso de que no la prueba es fallida
    assert called["ok"] is False, "ERROR: guardar_usuario fue llamado aunque el email no tiene '@'"


# CASO DE PRUEBA PM12-TC-20
def test_crear_usuario_rechaza_email_repetido():
    storage = StorageManager()
    usuario1 = Usuario("jhon", "alexander.suarez20@gmail.com")
    respuesta1 = storage.guardar_usuario(usuario1)
    usuario2 = Usuario("alex", "alexander.suarez20@gmail.com")
    respuesta2 = storage.guardar_usuario(usuario2)
    datos = storage.cargar_datos()
    usuarios = datos.get("usuarios", [])
    
    emails = [u["email"] for u in usuarios]
    count = emails.count("alexander.suarez20@gmail.com")

    
    assert count == 1, "BUG: el sistema permite guardar dos usuarios con el mismo email."
    
#CASO DE PRUEBA PM12-TC-21

def test_crear_usuario_rechaza_id_repetido():
    storage = StorageManager()
    usuario1 = Usuario("jonathan", "alexander.suarez20@gmail.com")
    r1 = storage.guardar_usuario(usuario1)
    usuario2 = Usuario("jose", "alexander.suarezg@gmail.com")
    usuario2.usuario_id = usuario1.usuario_id    
    r2 = storage.guardar_usuario(usuario2)

    datos = storage.cargar_datos()
    usuarios = datos.get("usuarios", [])

    # lista de IDs actuales en el archivo
    ids = [u["usuario_id"] for u in usuarios]

    # contar cuántas veces aparece ese ID
    count = ids.count(usuario1.usuario_id)

    # la prueba falla si se permitió duplicado
    assert count == 1, "BUG: el sistema permitió guardar dos usuarios con el mismo ID"
    
# CASO DE PRUEBA PM12-TC-14
def test_eliminar_usuario_existente():
    storage = StorageManager()
    usuario1 = Usuario("jorge", "jorgemendoza@gmail.com")
    r1 = storage.guardar_usuario(usuario1)
    usuario_id=usuario1.usuario_id
    storage.eliminar_usuario(usuario_id)
    datos = storage.cargar_datos()
    usuarios = datos.get("usuarios", [])

    # lista de IDs actuales en el archivo
    ids = [u["usuario_id"] for u in usuarios]

    # contar cuántas veces aparece ese ID
    count = ids.count(usuario1.usuario_id)

    # la prueba falla si se permitió duplicado
    assert count == 0, "BUG: el sistema no elimina correctamente los usuarios"
    
# CASO DE PRUEBA HU-002

#CASO DE PRUEBA PM12-TC-24
def test_crear_proyecto_titulo_vacio(monkeypatch, capsys):
    cli = CliInterface()
    monkeypatch.setattr(builtins, "input", make_inputs("", "", ""))

    called = {"ok": False, "proyecto": None}
    def fake_guardar(proyecto):
        called["ok"] = True
        called["proyecto"] = proyecto
        return True
    cli.storage.guardar_proyecto = fake_guardar

    cli.crear_proyecto()

    out = capsys.readouterr().out

    # No debe haberse guardado
    assert called["ok"] is False, "ERROR: guardar_proyecto fue llamado aunque el nombre estuviera vacio"

# CASO DE PRUEBA PM12-TC-47

def test_listar_proyectos_con_conteo_tares(monkeypatch, capsys):
    cli = CliInterface()
    storage = cli.storage

   
    p1 = Proyecto("data_management", "Ninguna", "")
    p2 = Proyecto("coffe_shop", "Ninguna", "")
    p3 = Proyecto("clothing_store", "Ninguna", "")


    def fake_contar_tareas_p1(): return 0
    def fake_contar_tareas_p2(): return 2
    def fake_contar_tareas_p3(): return 1

    p1.contar_tareas = fake_contar_tareas_p1
    p2.contar_tareas = fake_contar_tareas_p2
    p3.contar_tareas = fake_contar_tareas_p3

    monkeypatch.setattr(storage, "cargar_todos_proyectos", lambda: [p1, p2, p3])

    monkeypatch.setattr(builtins, "input", make_inputs(""))
    
    cli.listar_proyectos()

    out = capsys.readouterr().out
    
    assert "1. data_management" in out
    assert "0 tareas" in out
    assert "2. coffe_shop" in out
    assert "2 tareas" in out
    assert "3. clothing_store" in out
    assert "1 tareas" in out

# CASO DE PRUEBA PM12-TC-32

def test_validar_creacion_proyecto_se_asigne_usuario_actual_como_propietario(monkeypatch, capsys): 
    cli = CliInterface()
    storage = cli.storage
    usuario_actual = Usuario("jonathan", "jonathan234@gmail.com")
    cli.usuario_actual = usuario_actual 
    
    monkeypatch.setattr("builtins.input", make_inputs("mi_proyecto", "descripcion", ""))
    captured = {"proyecto": None}
    
    def fake_guardar_proyecto(proyecto):
        captured["proyecto"] = proyecto
        return True  
    
    monkeypatch.setattr(storage, "guardar_proyecto", fake_guardar_proyecto)
    cli.crear_proyecto()
    proj = captured["proyecto"]
    
    assert proj.propietario_id == usuario_actual.usuario_id, "No se guardo el usuario actual"
   
# CASO DE PRUEBA PM12-TC-48


# CASO DE PRUEBA PM12-TC-14
def test_eliminar_proyecto_existente():
    storage = StorageManager()
    proyecto1 = Proyecto("Hormiga dc","","")
    r1 = storage.guardar_proyecto(proyecto1)
    proyecto_id=proyecto1.proyecto_id
    storage.eliminar_proyecto(proyecto_id)
    datos = storage.cargar_datos()
    proyectos = datos.get("proyectos", [])

    # lista de IDs actuales en el archivo
    ids = [u["proyecto_id"] for u in proyectos]

    # contar cuántas veces aparece ese ID
    count = ids.count(proyecto1.proyecto_id)

    # la prueba falla si se permitió duplicado
    assert count == 0, "BUG: el sistema no elimina correctamente los proyectos"

# CASO DE PRUEBA PM12-TC-42
def test_validar_crear_proyecto_se_crean_automaticamente_columnas(monkeypatch):
    cli = CliInterface()
    cli.usuario_actual = Usuario("Jonathan", "jonathan234@gmail.com")
    monkeypatch.setattr("builtins.input", make_inputs("Glass corporation", "", ""))
    captured = {"proyecto": None}
    def fake_guardar_proyecto(proyecto):
        captured["proyecto"] = proyecto
        return True
    monkeypatch.setattr(cli.storage, "guardar_proyecto", fake_guardar_proyecto)
    cli.crear_proyecto()
    proyecto_creado = captured["proyecto"]
    assert proyecto_creado is not None, "No se creó el proyecto"
    nombres_columnas = [c.nombre for c in proyecto_creado.columnas]
    esperadas = ["Pendiente", "En Progreso", "Completada"]
    for columna in esperadas:
        assert columna in nombres_columnas, f"Falta la columna esperada: {columna}"
        
#HU 003: Crear Tarea

# PM12-TC-50

def test_crear_tarea_titulo_vacio(monkeypatch, capsys):
    cli = CliInterface()
    
    proyecto = Proyecto("Proyecto prueba", "", "")
    proyecto.agregar_columna("Pendiente")
    proyecto.agregar_columna("En Progreso")
    proyecto.agregar_columna("Completada")
    cli.proyecto_actual = proyecto  

    monkeypatch.setattr(builtins, "input", lambda prompt="": "")

    called = {"ok": False}
    def fake_guardar(proyecto):
        called["ok"] = True
        return True

    cli.storage.guardar_proyecto = fake_guardar
    cli.agregar_tarea()

    out = capsys.readouterr().out
    assert "El titulo no puede estar vacio" in out.lower()

    assert called["ok"] is False, "ERROR: La tarea fue guardada aunque el titulo estaba vacio"


# CASO DE PRUEBA PM12-TC-52
def test_crear_tarea_sin_especificar_prioridad(monkeypatch):
    cli = CliInterface()
    
    proyecto = Proyecto("Proyecto prueba", "", "")
    proyecto.agregar_columna("Pendiente")
    proyecto.agregar_columna("En Progreso")
    proyecto.agregar_columna("Completada")
    cli.proyecto_actual = proyecto  
    
    inputs_agregar_tarea = ["Login","","","1","",""]         
    monkeypatch.setattr("builtins.input", lambda _: inputs_agregar_tarea.pop(0))

    called = {"ok": False}
    def fake_guardar(proyecto):
        called["ok"] = True
        return True
    cli.storage.guardar_proyecto = fake_guardar
    
    cli.agregar_tarea()
    
    assert called["ok"] is True, "No se pudo guardar el proyecto"

    tareas_encontradas = []
    for columna in proyecto.columnas:
        for tarea in columna.tareas:
            if "login" in tarea.titulo.lower():
                tareas_encontradas.append(tarea)

    assert len(tareas_encontradas) == 1, "No se encontró la tarea agregada"
    tarea = tareas_encontradas[0]
    assert tarea.prioridad == "Media", "La tarea no asigna por defecto la prioridad Media"

#CASO DE PRUEBA PM12-TC-51

def test_crear_tarea_eligiendo_prioridad(monkeypatch):
    cli = CliInterface()
    
    proyecto = Proyecto("Proyecto prueba", "", "")
    proyecto.agregar_columna("Pendiente")
    proyecto.agregar_columna("En Progreso")
    proyecto.agregar_columna("Completada")
    cli.proyecto_actual = proyecto  
    
    inputs_agregar_tarea = ["login1","","2","1","","",
                            "login2","","1","1","","",
                            "login3","","3","1","","",
                            "login4","","4","1","",""]         
    monkeypatch.setattr("builtins.input", lambda _: inputs_agregar_tarea.pop(0))

    called = {"ok": False}
    def fake_guardar(proyecto):
        called["ok"] = True
        return True
    cli.storage.guardar_proyecto = fake_guardar
    
    for _ in range(4):
        cli.agregar_tarea()
    
    assert called["ok"] is True, "No se pudo guardar el proyecto"

    tareas_encontradas = []
    for columna in proyecto.columnas:
        for tarea in columna.tareas:
            if "login" in tarea.titulo.lower():
                tareas_encontradas.append(tarea)

    assert len(tareas_encontradas) == 4, "No se encontró la tarea agregada"
    tarea1 = tareas_encontradas[0]
    tarea2 = tareas_encontradas[1]
    tarea3 = tareas_encontradas[2]
    tarea4 = tareas_encontradas[3]
    assert tarea1.prioridad == "Media" , "No se guardo la tarea 1"
    assert tarea2.prioridad == "Baja" , "No se guardo la tarea 2"
    assert tarea3.prioridad == "Alta" ,  "No se guardo la tarea 3"
    assert tarea4.prioridad == "Urgente", "No se guardo la tarea 4" 
    
# CASO DE PRUEBA PM12-TC-53


def test_crear_tarea_rechaza_id_repetido(monkeypatch):
    cli = CliInterface()
    
    proyecto = Proyecto("Proyecto prueba", "", "")
    proyecto.agregar_columna("Pendiente")
    proyecto.agregar_columna("En Progreso")
    proyecto.agregar_columna("Completada")
    cli.proyecto_actual = proyecto  
    
    inputs_agregar_tarea = ["login1","","2","1","","",
                            "login2","","1","1","","",
                            "login3","","3","1","","",
                            "login4","","4","1","",""]         
    monkeypatch.setattr("builtins.input", lambda _: inputs_agregar_tarea.pop(0))

    called = {"ok": False}
    def fake_guardar(proyecto):
        called["ok"] = True
        return True
    cli.storage.guardar_proyecto = fake_guardar
    
    for _ in range(4):
        cli.agregar_tarea()
    
    assert called["ok"] is True, "No se pudo guardar el proyecto"

    tareas_encontradas = []
    for columna in proyecto.columnas:
        for tarea in columna.tareas:
            if "login" in tarea.titulo.lower():
                tareas_encontradas.append(tarea)

    assert len(tareas_encontradas) == 4, "No se encontró la tarea agregada"

    ids = [t.tarea_id for t in tareas_encontradas]

    # contar cuántas veces aparece ese ID
    count1 = ids.count(tareas_encontradas[0].tarea_id)
    count2 = ids.count(tareas_encontradas[1].tarea_id)
    count3 = ids.count(tareas_encontradas[2].tarea_id)

    assert count1 == 1 and count2 == 1 and count3 == 1, "ERROR: El sistema guarda tareas con ID Repetido "

# CASO DE USO PM12-TC-53


def test_validar_seleccion_columna_en_crear_tarea(monkeypatch):
    cli = CliInterface()
    
    proyecto = Proyecto("Proyecto prueba", "", "")
    proyecto.agregar_columna("Pendiente")
    proyecto.agregar_columna("En Progreso")
    proyecto.agregar_columna("Completada")
    cli.proyecto_actual = proyecto  
    
    inputs_agregar_tarea = ["login1","","2","","",""]        
    monkeypatch.setattr("builtins.input", lambda _: inputs_agregar_tarea.pop(0))

    called = {"ok": False}
    def fake_guardar(proyecto):
        called["ok"] = True
        return True
    cli.storage.guardar_proyecto = fake_guardar
 
    cli.agregar_tarea()
    
    assert called["ok"] is False, "ERROR: El proyecto fue guardado sin haber seleccionado una columna"


    
def test_validar_asignación_usuario_creación_tarea(monkeypatch):
    cli = CliInterface()
    
    usuario1=Usuario("Alex", "alexander.suarez20@gmail.com")
    proyecto = Proyecto("Proyecto prueba", "", "")
    proyecto.agregar_columna("Pendiente")
    proyecto.agregar_columna("En Progreso")
    proyecto.agregar_columna("Completada")
    cli.proyecto_actual = proyecto  
    
    id_usuario=usuario1.usuario_id
    
    
    inputs_agregar_tarea = ["login1","","2","","",id_usuario]        
    monkeypatch.setattr("builtins.input", lambda _: inputs_agregar_tarea.pop(0))

    called = {"ok": False}
    def fake_guardar(proyecto):
        called["ok"] = True
        return True
    cli.storage.guardar_proyecto = fake_guardar
 
    cli.agregar_tarea()
    
    
    
    assert called["ok"] is False, "ERROR: El proyecto fue guardado sin haber seleccionado una columna"

def test_validar_asignacion_usuario_creacion_tarea(monkeypatch):
    cli = CliInterface()

    # crear usuario que queremos asignar
    usuario1 = Usuario("Alex", "alexander.suarez20@gmail.com")
    id_usuario = usuario1.usuario_id

    # preparar proyecto con columnas y asignarlo al CLI
    proyecto = Proyecto("Proyecto prueba", "", "")
    proyecto.agregar_columna("Pendiente")
    proyecto.agregar_columna("En Progreso")
    proyecto.agregar_columna("Completada")
    cli.proyecto_actual = proyecto
    inputs = ["login1", "", "2", "1", id_usuario, ""]

    def fake_input(prompt=""):
        return inputs.pop(0) if inputs else ""
    monkeypatch.setattr("builtins.input", fake_input)

   
    called = {"ok": False}
    def fake_guardar(proyecto_arg):
        called["ok"] = True
        return True
    cli.storage.guardar_proyecto = fake_guardar
    cli.agregar_tarea()
    tareas_encontradas = []
    for columna in proyecto.columnas:
        for tarea in columna.tareas:
            if tarea.titulo.lower() == "login1":
                tareas_encontradas.append((columna, tarea))

    columna, tarea_creada = tareas_encontradas[0]

    assert (
        tarea_creada.asignado_a == id_usuario
        or tarea_creada.asignado_a == usuario1.nombre
    ), f"La tarea no fue asignada correctamente. asignado_a={tarea_creada.asignado_a!r}, esperado {id_usuario!r} o {usuario1.nombre!r}"


    
 