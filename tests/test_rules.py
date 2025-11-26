import pytest
from datetime import datetime
from unittest.mock import patch

from parking.config import TIMESTAMP_FMT
from parking.rules import guardar_usuario, guardar_bici, registrar


# guardar_usuario


def test_guardar_usuario_ok(capfd):
    with (
        patch("parking.rules.es_dni_unico", return_value=True),
        patch("parking.rules.es_email_unico", return_value=True),
        patch("parking.rules.escribir_csv_dic"),
    ):
        assert guardar_usuario("12345678A", "Ana", "ana@mail.com") is True
        assert "OK: se ha registrado el usuario" in capfd.readouterr().out


def test_guardar_usuario_dni_vacio(capfd):
    with patch("parking.rules.escribir_csv_dic"):
        assert guardar_usuario("", "Ana", "ana@mail.com") is False
        assert "ERROR: Campo DNI vacío" in capfd.readouterr().out


def test_guardar_usuario_nombre_vacio(capfd):
    with patch("parking.rules.escribir_csv_dic"):
        assert guardar_usuario("12345678Z", "", "ana@mail.com") is False
        assert "ERROR: Campo nombre vacío" in capfd.readouterr().out


def test_guardar_usuario_email_vacio(capfd):
    with patch("parking.rules.escribir_csv_dic"):
        assert guardar_usuario("12345678Z", "Ana", "") is False
        assert "ERROR: Campo email vacío" in capfd.readouterr().out


def test_guardar_usuario_dni_invalido(capfd):
    with patch("parking.rules.escribir_csv_dic"):
        assert guardar_usuario("error", "Ana", "ana@mail.com") is False
        assert "ERROR: Formato de DNI no reconocido" in capfd.readouterr().out


def test_guardar_usuario_email_invalido(capfd):
    with patch("parking.rules.escribir_csv_dic"):
        assert guardar_usuario("12345678Z", "Ana", "ana.com") is False
        assert "ERROR: Formato de email no reconocido" in capfd.readouterr().out


def test_guardar_usuario_dni_duplicado(capfd):
    with (
        patch("parking.rules.es_dni_unico", return_value=False),
        patch("parking.rules.es_email_unico", return_value=True),
        patch("parking.rules.escribir_csv_dic"),
    ):
        assert guardar_usuario("12345678A", "Ana", "ana@mail.com") is False
        assert "ERROR: El DNI 12345678A ya está registrado" in capfd.readouterr().out


def test_guardar_usuario_email_duplicado(capfd):
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
    with (
        patch("parking.rules.es_dni_unico", return_value=False),
        patch("parking.rules.es_serie_unica", return_value=True),
        patch("parking.rules.escribir_csv_dic"),
    ):
        assert guardar_bici("B123", "12345678A", "Orbea", "MX20") is True
        assert "OK: se ha registrado la bicicleta" in capfd.readouterr().out


def test_guardar_bici_serie_vacia(capfd):
    with patch("parking.rules.escribir_csv_dic"):
        assert guardar_bici("", "12345678A", "Orbea", "MX20") is False
        assert "ERROR: Campo número de serie vacío" in capfd.readouterr().out


def test_guardar_bici_dni_vacio(capfd):
    with patch("parking.rules.escribir_csv_dic"):
        assert guardar_bici("B123", "", "Orbea", "MX20") is False
        assert "ERROR: Campo DNI vacío" in capfd.readouterr().out


def test_guardar_bici_marca_vacio(capfd):
    with patch("parking.rules.escribir_csv_dic"):
        assert guardar_bici("B123", "12345678A", "", "MX20") is False
        assert "ERROR: Campo marca vacío" in capfd.readouterr().out


def test_guardar_bici_modelo_vacio(capfd):
    with patch("parking.rules.escribir_csv_dic"):
        assert guardar_bici("B123", "12345678A", "Orbea", "") is False
        assert "ERROR: Campo modelo vacío" in capfd.readouterr().out


def test_guardar_bici_dni_no_unico(capfd):
    with (
        patch("parking.rules.es_dni_unico", return_value=True),
        patch("parking.rules.es_serie_unica", return_value=True),
        patch("parking.rules.escribir_csv_dic"),
    ):
        assert guardar_bici("B123", "12345678A", "Orbea", "MX20") is False
        assert "ERROR: DNI no regristado en el sistema" in capfd.readouterr().out


def test_guardar_bici_serie_no_unica(capfd):
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
    with (
        patch("parking.rules.puede_entrar", return_value=False),
        patch("parking.rules.escribir_csv_dic"),
    ):
        assert registrar("IN", "12345678A", "B123") is False
        assert "ERROR: la bicicleta no puede entrar" in capfd.readouterr().out


def test_registrar_out_ok(capfd):
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
    with (
        patch("parking.rules.puede_salir", return_value=False),
        patch("parking.rules.escribir_csv_dic"),
    ):
        assert registrar("OUT", "12345678A", "B123") is False
        assert "ERROR: la bicicleta no puede salir" in capfd.readouterr().out


def test_registrar_invalido():
    with (
        patch("parking.rules.escribir_csv_dic"),
        pytest.raises(NotImplementedError),
    ):
        registrar("ALGO", "12345678A", "B123")
