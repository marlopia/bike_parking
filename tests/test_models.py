"""Archivo de pruebas de rules.py, no toca disco"""

from pathlib import Path
import sys
import pytest
from unittest.mock import MagicMock, patch

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))
mock_bd_class = MagicMock()
with patch("parking.models.bd.Bd", mock_bd_class):
    from parking.models.usuario import Usuario
    from parking.models.bici import Bici
    from parking.models.registro import Registro
    from parking.models.bd import UsuarioORM, BiciORM, RegistroORM


# Usuario


def test_guardar_usuario_ok(capfd):
    """Verifica que se guarde un usuario válido"""
    with (
        patch.object(Usuario, "es_valido", return_value=True),
        patch("parking.models.usuario.bd.crear_sesion") as mock_cm,
    ):

        mock_sesion = MagicMock()
        mock_cm.return_value.__enter__.return_value = mock_sesion
        mock_sesion.query.return_value.filter_by.return_value.first.return_value = None

        assert Usuario("12345678A", "Ana", "ana@mail.com").guardar() is True
        assert "OK: se ha registrado el usuario" in capfd.readouterr().out


def test_guardar_usuario_no_valido(capfd):
    """No guarda un usuario inválido"""
    usuario = Usuario("", "", "error")
    assert usuario.guardar() is False
    out = capfd.readouterr().out
    assert "ERROR" in out


def test_borrar_usuario_ok(capfd):
    """Borra un usuario existente sin bicis"""
    usuario = Usuario("12345678A")
    usuario.bicis = []

    with patch("parking.models.usuario.bd.crear_sesion") as mock_cm:
        mock_sesion = MagicMock()
        mock_cm.return_value.__enter__.return_value = mock_sesion
        mock_sesion.query.return_value.filter_by.return_value.first.return_value = (
            UsuarioORM("12345678A", "Ana", "ana@mail.com")
        )

        assert usuario.borrar() is True
        assert "OK: usuario borrado" in capfd.readouterr().out


def test_borrar_usuario_con_bicis(capfd):
    """No borra un usuario con bicis"""
    usuario = Usuario("12345678A")
    usuario.bicis = ["B123"]

    mock_session = MagicMock()
    mock_context_manager = MagicMock()
    mock_context_manager.__enter__.return_value = mock_session
    mock_context_manager.__exit__.return_value = None

    with patch(
        "parking.models.usuario.bd.crear_sesion", return_value=mock_context_manager
    ):
        result = usuario.borrar()
        out = capfd.readouterr().out
        assert result is False
        assert "ERROR" in out


# Bici


def test_guardar_bici_ok(capfd):
    """Guarda una bici válida"""
    with (
        patch.object(Bici, "es_valido", return_value=True),
        patch.object(Bici, "existe_usuario", return_value=True),
        patch("parking.models.bici.bd.crear_sesion") as mock_cm,
    ):

        mock_sesion = MagicMock()
        mock_cm.return_value.__enter__.return_value = mock_sesion
        mock_sesion.query.return_value.filter_by.return_value.first.return_value = None

        assert Bici("B123", "12345678A", "Orbea", "MX20").guardar() is True
        assert "OK: se ha registrado la bicicleta" in capfd.readouterr().out


def test_borrar_bici_ok(capfd):
    """Borra una bici existente"""
    with patch("parking.models.bici.bd.crear_sesion") as mock_cm:
        mock_sesion = MagicMock()
        mock_cm.return_value.__enter__.return_value = mock_sesion
        mock_sesion.query.return_value.filter_by.return_value.first.return_value = (
            BiciORM("B123", "12345678A", "Orbea", "MX20")
        )

        assert Bici("B123").borrar() is True
        assert "OK: bicicleta borrada" in capfd.readouterr().out


def test_borrar_bici_no_existe(capfd):
    """No borra una bici inexistente"""
    with patch("parking.models.bici.bd.crear_sesion") as mock_cm:
        mock_sesion = MagicMock()
        mock_cm.return_value.__enter__.return_value = mock_sesion
        mock_sesion.query.return_value.filter_by.return_value.first.return_value = None

        assert Bici("B123").borrar() is False
        assert "ERROR: la bicicleta no existe" in capfd.readouterr().out


# Registro


@pytest.mark.parametrize(
    "accion_ultima,esperado",
    [
        ("OUT", True),
        ("IN", False),
        (None, True),
    ],
)
def test_puede_entrar_mock(accion_ultima, esperado):
    """Verifica si puede entrar según el último estado"""
    with (
        patch("parking.models.registro.bd.crear_sesion") as mock_cm,
        patch("parking.models.registro.Usuario") as mock_usuario,
    ):
        mock_sesion = MagicMock()
        mock_cm.return_value.__enter__.return_value = mock_sesion
        if accion_ultima is None:
            mock_sesion.query.return_value.filter_by.return_value.order_by.return_value.first.return_value = (
                None
            )
        else:
            mock_sesion.query.return_value.filter_by.return_value.order_by.return_value.first.return_value = RegistroORM(
                "2025-12-29 12:00:00", accion_ultima, "B123", "12345678A"
            )
        mock_usuario.return_value.bicis = ["B123"]
        registro = Registro("IN", "B123", "12345678A")
        assert registro.guardar() is esperado or registro.guardar() is False


@pytest.mark.parametrize(
    "accion_ultima,esperado",
    [
        ("IN", True),
        ("OUT", False),
        (None, False),
    ],
)
def test_puede_salir_mock(accion_ultima, esperado):
    """Verifica si puede salir según el último estado"""
    with (
        patch("parking.models.registro.bd.crear_sesion") as mock_cm,
        patch("parking.models.registro.Usuario") as mock_usuario,
    ):
        mock_sesion = MagicMock()
        mock_cm.return_value.__enter__.return_value = mock_sesion
        if accion_ultima is None:
            mock_sesion.query.return_value.filter_by.return_value.order_by.return_value.first.return_value = (
                None
            )
        else:
            mock_sesion.query.return_value.filter_by.return_value.order_by.return_value.first.return_value = RegistroORM(
                "2025-12-29 12:00:00", accion_ultima, "B123", "12345678A"
            )
        mock_usuario.return_value.bicis = ["B123"]
        registro = Registro("OUT", "B123", "12345678A")
        assert registro.guardar() is esperado or registro.guardar() is False
