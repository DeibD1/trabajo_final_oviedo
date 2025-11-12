import pytest
import builtins
from src.models import Proyecto, Usuario
from src.cli import CliInterface
from src.storage import StorageManager

def make_inputs(*valores):
    it = iter(valores)
    def fake_input(prompt=""):
        try:
            return next(it)
        except StopIteration:
            return ""
    return fake_input

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
    #Se crea una instancia del storage
    storage = StorageManager()
    #Se crea un proyecto
    proyecto1 = Proyecto("Hormiga","","")
    # Se guarda el proyecto 1
    storage.guardar_proyecto(proyecto1)
    #Se guarda el proyecto id
    proyecto_id=proyecto1.proyecto_id
    # Se elimina el proyecto
    storage.eliminar_proyecto(proyecto_id)
    datos = storage.cargar_datos()
    proyectos = datos.get("proyectos", [])

    ids = [u["proyecto_id"] for u in proyectos]
    count = ids.count(proyecto1.proyecto_id)

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
        