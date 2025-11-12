
import pytest
import builtins
from src.models import Proyecto, Usuario
from src.cli import CliInterface

def make_inputs(*valores):
    it = iter(valores)
    def fake_input(prompt=""):
        try:
            return next(it)
        except StopIteration:
            return ""
    return fake_input

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


# CASO DE PRUEBA PM12-TC-56    
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
    
    usuario1 = Usuario("Alex", "alexander.suarez20@gmail.com")
    id_usuario = usuario1.usuario_id
    
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
    ), f"La tarea no fue asignada correctamente"


    
 