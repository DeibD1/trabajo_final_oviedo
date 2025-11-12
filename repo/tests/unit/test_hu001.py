import pytest
import builtins
from src.models import Usuario
from src.cli import CliInterface
from src.storage import StorageManager

# CASOS DE PRUEBA HU-001

#Esta función permite crear las entradas para probrar la interfaz grafica
def make_inputs(*valores):
    it = iter(valores)
    def fake_input(prompt=""):
        try:
            return next(it)
        except StopIteration:
            return ""
    return fake_input

# CASO DE PRUEBA PM12-TC-10

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
    # Se crea una instancia de storage
    storage = StorageManager()
    # Se crea un usuario con nombre y email
    usuario1 = Usuario("jhon", "alexander.suarez20@gmail.com")
    #Se guarda el usuario
    storage.guardar_usuario(usuario1)
    usuario2 = Usuario("alex", "alexander.suarez20@gmail.com")
    storage.guardar_usuario(usuario2)
    #Se cargan los datos del storage
    datos = storage.cargar_datos()
    # Se obtiene la lista de los usuarios
    usuarios = datos.get("usuarios", [])
    # Se obtiene una lista de los emails
    emails = [u["email"] for u in usuarios]
    # Se cuenta la cantidad de emails con el correo alexander.suarez20@gmail.com 
    count = emails.count("alexander.suarez20@gmail.com")
    # Si No existe un solo email con ese valor  existe un error
    assert count == 1, "BUG: el sistema permite guardar dos usuarios con el mismo email."
    
#CASO DE PRUEBA PM12-TC-21

def test_crear_usuario_rechaza_id_repetido():
    # Se crea una instancia de storage
    storage = StorageManager()
    # Se crea un usuario con nombre y email
    usuario1 = Usuario("jonathan", "alexander.suarez20@gmail.com")
    #Se guarda el usuario
    storage.guardar_usuario(usuario1)
    usuario2 = Usuario("jose", "alexander.suarezg@gmail.com")
    usuario2.usuario_id = usuario1.usuario_id    
    storage.guardar_usuario(usuario2)
    # Se cargan los datos
    datos = storage.cargar_datos()
    #Se guarda en una lista los usuarios
    usuarios = datos.get("usuarios", [])
    # Se guarda en una lista los id de los usuarios
    ids = [u["usuario_id"] for u in usuarios]
    #Se cuentan los id del usuario 1
    count = ids.count(usuario1.usuario_id)
    #Si solo se cuenta 1 solo hay un usuario con ese id por lo tanto no se repitio
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
    ids = [u["usuario_id"] for u in usuarios]
    count = ids.count(usuario1.usuario_id)
    assert count == 0, "BUG: el sistema no elimina correctamente los usuarios"
    
