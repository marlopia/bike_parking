# TODO: portar tests
"""Archivo de pruebas de rules.py, no toca disco"""

import pytest
from datetime import datetime
from unittest.mock import MagicMock, patch

from parking.config import TIMESTAMP_FMT

from parking.models.usuario import Usuario
from parking.models.bici import Bici
from parking.models.registro import Registro

# Usuario


## Guardar
def test_guardar_usuario_ok(capfd):
    """Verifica que se guarde el usuario válido y muestre el mensaje de confirmación"""
    with (
        patch.object(Usuario, "es_valido", return_value=True),
        patch.object(Usuario, "es_unico", return_value=True),
        patch("parking.models.usuario.escribir_csv_dic"),
    ):
        assert Usuario("12345678A", "Ana", "ana@mail.com").guardar() is True
        assert "OK: se ha registrado el usuario" in capfd.readouterr().out


def test_guardar_usuario_dni_vacio(capfd):
    """Verifica que no guarde un DNI vacío y muestre el mensaje de error relevante"""
    with patch("parking.models.usuario.escribir_csv_dic"):
        assert Usuario("", "Ana", "ana@mail.com").guardar() is False
        assert "ERROR: el DNI introducido no es válido" in capfd.readouterr().out


def test_guardar_usuario_nombre_vacio(capfd):
    """Verifica que no guarde un nombre vacío y muestre el mensaje de error relevante"""
    with patch("parking.models.usuario.escribir_csv_dic"):
        assert Usuario("12345678A", "", "ana@mail.com").guardar() is False
        assert "ERROR: el nombre no puede estar vacío" in capfd.readouterr().out


def test_guardar_usuario_email_vacio(capfd):
    """Verifica que no guarde un email vacío y muestre el mensaje de error relevante"""
    with patch("parking.models.usuario.escribir_csv_dic"):
        assert Usuario("12345678A", "Ana", "").guardar() is False
        assert "ERROR: el email introducido no es válido" in capfd.readouterr().out


def test_guardar_usuario_dni_invalido(capfd):
    """Verifica que no guarde un DNI inválido y muestre el mensaje de error relevante"""
    with patch("parking.models.usuario.escribir_csv_dic"):
        assert Usuario("error", "Ana", "ana@mail.com").guardar() is False
        assert "ERROR: el DNI introducido no es válido" in capfd.readouterr().out


def test_guardar_usuario_email_invalido(capfd):
    """Verifica que no guarde un email inválido y muestre el mensaje de error relevante"""
    with patch("parking.models.usuario.escribir_csv_dic"):
        assert Usuario("12345678A", "Ana", "error").guardar() is False
        assert "ERROR: el email introducido no es válido" in capfd.readouterr().out


def test_guardar_usuario_dni_duplicado(capfd):
    """Verifica que no guarde un DNI duplicado y muestre el mensaje de error relevante"""
    with (
        patch.object(Usuario, "es_valido", return_value=True),
        patch("parking.models.usuario.es_dni_unico", return_value=False),
        patch("parking.models.usuario.escribir_csv_dic"),
    ):
        assert Usuario("12345678A", "Ana", "ana@mail.com").guardar() is False
        assert "ERROR: el DNI introducido ya está registrado" in capfd.readouterr().out


def test_guardar_usuario_email_duplicado(capfd):
    """Verifica que no guarde un email duplicado y muestre el mensaje de error relevante"""
    with (
        patch.object(Usuario, "es_valido", return_value=True),
        patch("parking.models.usuario.es_email_unico", return_value=False),
        patch("parking.models.usuario.escribir_csv_dic"),
    ):
        assert Usuario("12345678A", "Ana", "ana@mail.com").guardar() is False
        assert (
            "ERROR: el email introducido ya está registrado" in capfd.readouterr().out
        )


## usuario.bicis


@pytest.mark.parametrize(
    "dni, fake_data, expected",
    [
        (
            "12345678A",
            [
                {"dni_usuario": "12345678A", "num_serie": "B123"},
                {"dni_usuario": "12345678A", "num_serie": "B456"},
                {"dni_usuario": "98765432Z", "num_serie": "B789"},
            ],
            ["B123", "B456"],
        ),
        (
            "98765432Z",
            [
                {"dni_usuario": "12345678A", "num_serie": "B123"},
                {"dni_usuario": "12345678A", "num_serie": "B456"},
                {"dni_usuario": "98765432Z", "num_serie": "B789"},
            ],
            ["B789"],
        ),
        (
            "00000000X",
            [
                {"dni_usuario": "12345678A", "num_serie": "B123"},
                {"dni_usuario": "12345678A", "num_serie": "B456"},
            ],
            [],
        ),
    ],
)
def test_listar_bicis_usuario_param(monkeypatch, dni, fake_data, expected):
    """Comprueba que se devuelvan los números de series de las biciclestas del usuario introducido"""
    monkeypatch.setattr("parking.models.usuario.leer_csv_dic", lambda path: fake_data)
    usuario = Usuario(dni)
    assert usuario.bicis == expected


## Borrar
def test_borrar_usuario_ok(capfd):
    """Comprueba que se borra un usuario y se muestra un mensaje de confirmación"""
    usuario = Usuario("12345678A")
    usuario.bicis = []

    with (
        patch("parking.models.usuario.es_dni_unico", return_value=False),
        patch("parking.models.usuario.borrar_filas"),
    ):
        assert usuario.borrar() is True
        assert "OK: usuario borrado" in capfd.readouterr().out


def test_borrar_usuario_error_csv(capfd):
    """Comprueba que se gestiona un error inesperado con un mensaje"""
    usuario = Usuario("12345678A")
    usuario.bicis = []

    with (
        patch("parking.models.usuario.es_dni_unico", return_value=False),
        patch("parking.models.usuario.borrar_filas", side_effect=Exception("fail")),
    ):
        assert usuario.borrar() is False
        assert (
            "ERROR: ha habido un error inexperado al borrar del CSV"
            in capfd.readouterr().out
        )


def test_borrar_usuario_no_existe(capfd):
    """Comprueba que se muestra un mensaje de error cuando no existe el usuario"""
    usuario = Usuario("12345678A")
    usuario.bicis = []

    with (
        patch("parking.models.usuario.es_dni_unico", return_value=True),
        patch("parking.models.usuario.borrar_filas"),
    ):
        assert usuario.borrar() is False
        assert "ERROR: el DNI no existe o está mal escrito" in capfd.readouterr().out


def test_borrar_usuario_con_bicis(capfd):
    """Comprueba que se muestra un mensaje de error al borrar un usuario con bicis"""
    usuario = Usuario("12345678A")
    usuario.bicis = ["BK123"]

    with (
        patch("parking.models.usuario.es_dni_unico", return_value=False),
        patch("parking.models.usuario.borrar_filas"),
    ):
        assert usuario.borrar() is False
        assert (
            "ERROR: el usuario tiene bicicletas registradas, no se puede eliminar"
            in capfd.readouterr().out
        )


# Bici

## Guardar


def test_guardar_bici_ok(capfd):
    """Verifica que se guarde la bicicleta válida y muestre el mensaje de confirmación"""
    with (
        patch.object(Bici, "es_valido", return_value=True),
        patch.object(Bici, "es_unico", return_value=True),
        patch.object(Bici, "existe_usuario", return_value=True),
        patch("parking.models.bici.escribir_csv_dic"),
    ):
        assert Bici("B123", "12345678A", "Orbea", "MX20").guardar() is True
        assert "OK: se ha registrado la bicicleta" in capfd.readouterr().out


def test_guardar_bici_serie_vacia(capfd):
    """Verifica que no se guarde el número de serie vacío y muestre el mensaje de error relevante"""
    with patch("parking.models.bici.escribir_csv_dic"):
        assert Bici("", "12345678A", "Orbea", "MX20").guardar() is False
        assert (
            "ERROR: el campo num_serie no puede estar vacío" in capfd.readouterr().out
        )


def test_guardar_bici_dni_vacio(capfd):
    """Verifica que no se guarde el DNI vacío y muestre el mensaje de error relevante"""
    with patch("parking.models.bici.escribir_csv_dic"):
        assert Bici("B123", "", "Orbea", "MX20").guardar() is False
        assert (
            "ERROR: el campo dni_usuario no puede estar vacío" in capfd.readouterr().out
        )


def test_guardar_bici_marca_vacio(capfd):
    """Verifica que no se guarde la marca vacía y muestre el mensaje de error relevante"""
    with patch("parking.models.bici.escribir_csv_dic"):
        assert Bici("B123", "12345678A", "", "MX20").guardar() is False
        assert "ERROR: el campo marca no puede estar vacío" in capfd.readouterr().out


def test_guardar_bici_modelo_vacio(capfd):
    """Verifica que no se guarde el modelo vacío y muestre el mensaje de error relevante"""
    with patch("parking.models.bici.escribir_csv_dic"):
        assert Bici("B123", "12345678A", "Orbea", "").guardar() is False
        assert "ERROR: el campo modelo no puede estar vacío" in capfd.readouterr().out


def test_guardar_bici_dni_no_registrado(capfd):
    """Verifica que no se guarde el DNI no registrado y muestre el mensaje de error relevante"""
    with (
        patch.object(Bici, "es_valido", return_value=True),
        patch.object(Bici, "es_unico", return_value=True),
        patch("parking.models.bici.es_dni_unico", return_value=False),
        patch("parking.models.bici.escribir_csv_dic"),
    ):
        assert Bici("B123", "12345678A", "Orbea", "MX20").guardar() is False
        assert "ERROR: el usuario no está registrado" in capfd.readouterr().out


def test_guardar_bici_serie_duplicado(capfd):
    """Verifica que no se guarde el número de serie duplicado y muestre el mensaje de error relevante"""
    with (
        patch.object(Bici, "es_valido", return_value=True),
        patch("parking.models.bici.es_serie_unica", return_value=False),
        patch.object(Bici, "existe_usuario", return_value=True),
        patch("parking.models.bici.escribir_csv_dic"),
    ):
        assert Bici("B123", "12345678A", "Orbea", "MX20").guardar() is False
        assert "ERROR: el número de serie ya está registrado" in capfd.readouterr().out


## Borrar
def test_borrar_bici_no_existe(capfd):
    """Comprueba que se lanza el mensaje de error cuando no existe la bici a borrar"""
    with (
        patch("parking.models.bici.es_serie_unica", return_value=True),
        patch("parking.models.bici.borrar_filas"),
    ):
        assert Bici("B123").borrar() is False
        assert "ERROR: la bicicleta no existe" in capfd.readouterr().out


def test_borrar_bici_ok(capfd):
    """Comprueba que se borra la bici con exito y se lanza el mensaje de confirmación"""
    with (
        patch("parking.models.bici.es_serie_unica", return_value=False),
        patch("parking.models.bici.borrar_filas"),
    ):
        assert Bici("B123").borrar() is True
        assert "OK: bicicleta borrada" in capfd.readouterr().out


def test_borrar_bici_error_csv(capfd):
    """Comprueba que se gestiona un error inexperado con un mensaje"""
    with (
        patch("parking.models.bici.es_serie_unica", return_value=False),
        patch("parking.models.bici.borrar_filas", side_effect=Exception("fail")),
    ):
        assert Bici("B123").borrar() is False
        assert (
            "ERROR: ha habido un error inexperado al borrar del CSV"
            in capfd.readouterr().out
        )


# Registro

## Guardar


def test_registrar_in_ok(capfd):
    """Verifica que se guarda la entrada de la bicicleta correctamente y que muestre un mensaje de confirmación"""
    usuario_mock = MagicMock()
    usuario_mock.bicis = ["B123"]

    with (
        patch.object(Registro, "es_valido", return_value=True),
        patch("parking.models.registro.puede_entrar", return_value=True),
        patch("parking.models.registro.escribir_csv_dic"),
        patch("parking.models.registro.Usuario", return_value=usuario_mock),
    ):
        assert Registro("IN", "B123", "12345678A").guardar() is True
        assert "OK: se ha registrado el registro" in capfd.readouterr().out


def test_registrar_in_bici_incorrecta(capfd):
    """Verifica que no se guarda la entrada de la bicicleta que no es del usuario y que muestre un mensaje de error relevante"""
    usuario_mock = MagicMock()
    usuario_mock.bicis = ["B123"]

    with (
        patch.object(Registro, "es_valido", return_value=True),
        patch("parking.models.registro.puede_entrar", return_value=True),
        patch("parking.models.registro.escribir_csv_dic"),
        patch("parking.models.registro.Usuario", return_value=usuario_mock),
    ):
        assert Registro("IN", "error", "12345678A").guardar() is False
        assert "ERROR: esta bicicleta NO pertenece al usuario" in capfd.readouterr().out


def test_registrar_in_error(capfd):
    """Verifica que no se guarda la entrada de la bicicleta incorrecta y que muestre un mensaje de error relevante"""
    usuario_mock = MagicMock()
    usuario_mock.bicis = ["B123"]

    with (
        patch.object(Registro, "es_valido", return_value=True),
        patch("parking.models.registro.puede_entrar", return_value=False),
        patch("parking.models.registro.escribir_csv_dic"),
        patch("parking.models.registro.Usuario", return_value=usuario_mock),
    ):
        assert Registro("IN", "B123", "12345678A").guardar() is False
        assert "ERROR: Esta bicicleta no puede entrar" in capfd.readouterr().out


def test_registrar_out_ok(capfd):
    """Verifica que se guarda la salida de la bicicleta correctamente y que muestre un mensaje de confirmación"""
    usuario_mock = MagicMock()
    usuario_mock.bicis = ["B123"]

    with (
        patch.object(Registro, "es_valido", return_value=True),
        patch("parking.models.registro.puede_salir", return_value=True),
        patch("parking.models.registro.escribir_csv_dic"),
        patch("parking.models.registro.Usuario", return_value=usuario_mock),
    ):
        assert Registro("OUT", "B123", "12345678A").guardar() is True
        assert "OK: se ha registrado el registro" in capfd.readouterr().out


def test_registrar_out_error(capfd):
    """Verifica que no se guarda la salida de la bicicleta incorrecta y que muestre un mensaje de error relevante"""
    usuario_mock = MagicMock()
    usuario_mock.bicis = ["B123"]

    with (
        patch.object(Registro, "es_valido", return_value=True),
        patch("parking.models.registro.puede_salir", return_value=False),
        patch("parking.models.registro.escribir_csv_dic"),
        patch("parking.models.registro.Usuario", return_value=usuario_mock),
    ):
        assert Registro("OUT", "B123", "12345678A").guardar() is False
        assert "ERROR: Esta bicicleta no puede salir" in capfd.readouterr().out


def test_registrar_out_bici_incorrecta(capfd):
    """Verifica que no se guarda la salida de la bicicleta que no es del usuario y que muestre un mensaje de error relevante"""
    usuario_mock = MagicMock()
    usuario_mock.bicis = ["B123"]

    with (
        patch.object(Registro, "es_valido", return_value=True),
        patch("parking.models.registro.puede_salir", return_value=True),
        patch("parking.models.registro.escribir_csv_dic"),
        patch("parking.models.registro.Usuario", return_value=usuario_mock),
    ):
        assert Registro("OUT", "error", "12345678A").guardar() is False
        assert "ERROR: esta bicicleta NO pertenece al usuario" in capfd.readouterr().out


def test_registrar_invalido(capfd):
    """Verifica que no se guarda el registro si la acción no es válida y que muestre un mensaje de error relevante"""
    usuario_mock = MagicMock()
    usuario_mock.bicis = ["B123"]

    with (
        patch.object(Registro, "es_valido", return_value=True),
        patch("parking.models.registro.puede_salir", return_value=True),
        patch("parking.models.registro.escribir_csv_dic"),
        patch("parking.models.registro.Usuario", return_value=usuario_mock),
    ):
        assert Registro("error", "B123", "12345678A").guardar() is False
        assert (
            "ERROR: Las acciones aceptadas son solo IN y OUT" in capfd.readouterr().out
        )
