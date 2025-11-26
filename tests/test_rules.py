"""Archivo de pruebas de rules.py, no toca disco"""

import pytest
from datetime import datetime
from unittest.mock import patch

from parking.config import TIMESTAMP_FMT
from parking.rules import (
    borrar_bici,
    borrar_usuario,
    guardar_usuario,
    guardar_bici,
    listar_bicis_usuario,
    registrar,
)


# guardar_usuario


def test_guardar_usuario_ok(capfd):
    """Verifica que se guarde el usuario válido y muestre el mensaje de confirmación"""
    with (
        patch("parking.rules.es_dni_unico", return_value=True),
        patch("parking.rules.es_email_unico", return_value=True),
        patch("parking.rules.escribir_csv_dic"),
    ):
        assert guardar_usuario("12345678A", "Ana", "ana@mail.com") is True
        assert "OK: se ha registrado el usuario" in capfd.readouterr().out


def test_guardar_usuario_dni_vacio(capfd):
    """Verifica que no guarde un DNI vacío y muestre el mensaje de error relevante"""
    with patch("parking.rules.escribir_csv_dic"):
        assert guardar_usuario("", "Ana", "ana@mail.com") is False
        assert "ERROR: Campo DNI vacío" in capfd.readouterr().out


def test_guardar_usuario_nombre_vacio(capfd):
    """Verifica que no guarde un nombre vacío y muestre el mensaje de error relevante"""
    with patch("parking.rules.escribir_csv_dic"):
        assert guardar_usuario("12345678Z", "", "ana@mail.com") is False
        assert "ERROR: Campo nombre vacío" in capfd.readouterr().out


def test_guardar_usuario_email_vacio(capfd):
    """Verifica que no guarde un email vacío y muestre el mensaje de error relevante"""
    with patch("parking.rules.escribir_csv_dic"):
        assert guardar_usuario("12345678Z", "Ana", "") is False
        assert "ERROR: Campo email vacío" in capfd.readouterr().out


def test_guardar_usuario_dni_invalido(capfd):
    """Verifica que no guarde un DNI inválido y muestre el mensaje de error relevante"""
    with patch("parking.rules.escribir_csv_dic"):
        assert guardar_usuario("error", "Ana", "ana@mail.com") is False
        assert "ERROR: Formato de DNI no reconocido" in capfd.readouterr().out


def test_guardar_usuario_email_invalido(capfd):
    """Verifica que no guarde un email inválido y muestre el mensaje de error relevante"""
    with patch("parking.rules.escribir_csv_dic"):
        assert guardar_usuario("12345678Z", "Ana", "ana.com") is False
        assert "ERROR: Formato de email no reconocido" in capfd.readouterr().out


def test_guardar_usuario_dni_duplicado(capfd):
    """Verifica que no guarde un DNI duplicado y muestre el mensaje de error relevante"""
    with (
        patch("parking.rules.es_dni_unico", return_value=False),
        patch("parking.rules.es_email_unico", return_value=True),
        patch("parking.rules.escribir_csv_dic"),
    ):
        assert guardar_usuario("12345678A", "Ana", "ana@mail.com") is False
        assert "ERROR: El DNI 12345678A ya está registrado" in capfd.readouterr().out


def test_guardar_usuario_email_duplicado(capfd):
    """Verifica que no guarde un email duplicado y muestre el mensaje de error relevante"""
    with (
        patch("parking.rules.es_dni_unico", return_value=True),
        patch("parking.rules.es_email_unico", return_value=False),
        patch("parking.rules.escribir_csv_dic"),
    ):
        assert guardar_usuario("12345678A", "Ana", "ana@mail.com") is False
        assert (
            "ERROR: El email ana@mail.com ya está registrado" in capfd.readouterr().out
        )


# guardar_bici


def test_guardar_bici_ok(capfd):
    """Verifica que se guarde la bicicleta válida y muestre el mensaje de confirmación"""
    with (
        patch("parking.rules.es_dni_unico", return_value=False),
        patch("parking.rules.es_serie_unica", return_value=True),
        patch("parking.rules.escribir_csv_dic"),
    ):
        assert guardar_bici("B123", "12345678A", "Orbea", "MX20") is True
        assert "OK: se ha registrado la bicicleta" in capfd.readouterr().out


def test_guardar_bici_serie_vacia(capfd):
    """Verifica que no se guarde el número de serie vacío y muestre el mensaje de error relevante"""
    with patch("parking.rules.escribir_csv_dic"):
        assert guardar_bici("", "12345678A", "Orbea", "MX20") is False
        assert "ERROR: Campo número de serie vacío" in capfd.readouterr().out


def test_guardar_bici_dni_vacio(capfd):
    """Verifica que no se guarde el DNI vacío y muestre el mensaje de error relevante"""
    with patch("parking.rules.escribir_csv_dic"):
        assert guardar_bici("B123", "", "Orbea", "MX20") is False
        assert "ERROR: Campo DNI vacío" in capfd.readouterr().out


def test_guardar_bici_marca_vacio(capfd):
    """Verifica que no se guarde la marca vacía y muestre el mensaje de error relevante"""
    with patch("parking.rules.escribir_csv_dic"):
        assert guardar_bici("B123", "12345678A", "", "MX20") is False
        assert "ERROR: Campo marca vacío" in capfd.readouterr().out


def test_guardar_bici_modelo_vacio(capfd):
    """Verifica que no se guarde el modelo vacío y muestre el mensaje de error relevante"""
    with patch("parking.rules.escribir_csv_dic"):
        assert guardar_bici("B123", "12345678A", "Orbea", "") is False
        assert "ERROR: Campo modelo vacío" in capfd.readouterr().out


def test_guardar_bici_dni_no_registrado(capfd):
    """Verifica que no se guarde el DNI no registrado y muestre el mensaje de error relevante"""
    with (
        patch("parking.rules.es_dni_unico", return_value=True),
        patch("parking.rules.es_serie_unica", return_value=True),
        patch("parking.rules.escribir_csv_dic"),
    ):
        assert guardar_bici("B123", "12345678A", "Orbea", "MX20") is False
        assert "ERROR: DNI no regristado en el sistema" in capfd.readouterr().out


def test_guardar_bici_serie_duplicado(capfd):
    """Verifica que no se guarde el número de serie duplicado y muestre el mensaje de error relevante"""
    with (
        patch("parking.rules.es_dni_unico", return_value=False),
        patch("parking.rules.es_serie_unica", return_value=False),
        patch("parking.rules.escribir_csv_dic"),
    ):
        assert guardar_bici("B123", "12345678A", "Orbea", "MX20") is False
        assert (
            "ERROR: la bicicleta con el número de serie B123 ya está en el sistema"
            in capfd.readouterr().out
        )


# registrar


def test_registrar_in_ok(capfd):
    """Verifica que se guarda la entrada de la bicicleta correctamente y que muestre un mensaje de confirmación"""
    with (
        patch("parking.rules.puede_entrar", return_value=True),
        patch("parking.rules.escribir_csv_dic"),
    ):
        assert registrar("IN", "12345678A", "B123") is True
        assert (
            f"OK: registrado entrada bicicleta a las {datetime.now().strftime(TIMESTAMP_FMT)}"
            in capfd.readouterr().out
        )


def test_registrar_in_error(capfd):
    """Verifica que no se guarda la entrada de la bicicleta incorrecta y que muestre un mensaje de error relevante"""
    with (
        patch("parking.rules.puede_entrar", return_value=False),
        patch("parking.rules.escribir_csv_dic"),
    ):
        assert registrar("IN", "12345678A", "B123") is False
        assert "ERROR: la bicicleta no puede entrar" in capfd.readouterr().out


def test_registrar_out_ok(capfd):
    """Verifica que se guarda la salida de la bicicleta correctamente y que muestre un mensaje de confirmación"""
    with (
        patch("parking.rules.puede_salir", return_value=True),
        patch("parking.rules.escribir_csv_dic"),
    ):
        assert registrar("OUT", "12345678A", "B123") is True
        assert (
            f"OK: registrado salida bicicleta a las {datetime.now().strftime(TIMESTAMP_FMT)}"
            in capfd.readouterr().out
        )


def test_registrar_out_error(capfd):
    """Verifica que no se guarda la salida de la bicicleta incorrecta y que muestre un mensaje de error relevante"""
    with (
        patch("parking.rules.puede_salir", return_value=False),
        patch("parking.rules.escribir_csv_dic"),
    ):
        assert registrar("OUT", "12345678A", "B123") is False
        assert "ERROR: la bicicleta no puede salir" in capfd.readouterr().out


def test_registrar_invalido():
    """Verifica que salte el error NotImplementedError al intentar usar una accion no programada"""
    with (
        patch("parking.rules.escribir_csv_dic"),
        pytest.raises(NotImplementedError),
    ):
        registrar("ALGO", "12345678A", "B123")


# listar_bicis_usuario


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
    monkeypatch.setattr("parking.rules.leer_csv_dic", lambda path: fake_data)
    assert listar_bicis_usuario(dni) == expected


# borrar_bici


def test_borrar_bici_no_existe(capfd):
    """Comprueba que se lanza el mensaje de error cuando no existe la bici a borrar"""
    with (
        patch("parking.rules.es_serie_unica", return_value=True),
        patch("parking.rules.borrar_filas"),
    ):
        assert borrar_bici("B123") is False
        assert (
            "ERROR: no existe la bicicleta con ese número de serie"
            in capfd.readouterr().out
        )


def test_borrar_bici_ok(capfd):
    """Comprueba que se borra la bici con exito y se lanza el mensaje de confirmación"""
    with (
        patch("parking.rules.es_serie_unica", return_value=False),
        patch("parking.rules.borrar_filas"),
    ):
        assert borrar_bici("B123") is True
        assert "OK: bicicleta borrada" in capfd.readouterr().out


def test_borrar_bici_error_csv(capfd):
    """Comprueba que se gestiona un error inexperado con un mensaje"""
    with (
        patch("parking.rules.es_serie_unica", return_value=False),
        patch("parking.rules.borrar_filas", side_effect=Exception("fail")),
    ):
        assert borrar_bici("B123") is False
        assert (
            "ERROR: ha habido un error inexperado al borrar del CSV"
            in capfd.readouterr().out
        )


def test_borrar_usuario_no_existe(capfd):
    """Comprueba que se muestra un mensaje de error cuando no existe el usuario"""
    with (
        patch("parking.rules.es_dni_unico", return_value=True),
        patch("parking.rules.listar_bicis_usuario"),
        patch("parking.rules.borrar_filas"),
    ):
        assert borrar_usuario("12345678A") is False
        assert "ERROR: no existe ese DNI en el registro" in capfd.readouterr().out


def test_borrar_usuario_con_bicis(capfd):
    """Comprueba que se muestra un mensaje de error al borrar un usuario con bicis"""
    with (
        patch("parking.rules.es_dni_unico", return_value=False),
        patch("parking.rules.listar_bicis_usuario", return_value=["B123"]),
        patch("parking.rules.borrar_filas"),
    ):
        assert borrar_usuario("12345678A") is False
        assert (
            "ERROR: el usuario tiene bicicletas registradas, no se puede borrar"
            in capfd.readouterr().out
        )


def test_borrar_usuario_ok(capfd):
    """Comprueba que se borra un usuario y se muestra un mensaje de confirmación"""
    with (
        patch("parking.rules.es_dni_unico", return_value=False),
        patch("parking.rules.listar_bicis_usuario", return_value=[]),
        patch("parking.rules.borrar_filas"),
    ):
        assert borrar_usuario("12345678A") is True
        assert "OK: usuario borrado" in capfd.readouterr().out


def test_borrar_usuario_error_csv(capfd):
    """Comprueba que se gestiona un error inesperado con un mensaje"""
    with (
        patch("parking.rules.es_dni_unico", return_value=False),
        patch("parking.rules.listar_bicis_usuario", return_value=[]),
        patch("parking.rules.borrar_filas", side_effect=Exception("fail")),
    ):
        assert borrar_usuario("12345678A") is False
        assert (
            "ERROR: ha habido un error inexperado al borrar del CSV"
            in capfd.readouterr().out
        )
