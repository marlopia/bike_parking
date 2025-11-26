import io
from textwrap import dedent
import pytest

from parking.config import CABECERA_USUARIOS, CABECERA_BICIS, CABECERA_REGISTROS
from parking.data_utils.csv_utils import (
    asegurar_csvs,
    borrar_filas,
    escribir_csv_dic,
    leer_csv_dic,
)


def test_asegurar_csvs_no_existen(tmp_path, monkeypatch):
    """Comprueba que se generen los archivos csv cuando no existen"""
    # Crear rutas temporales
    usuarios_csv = tmp_path / "usuarios.csv"
    bicis_csv = tmp_path / "bicis.csv"
    registros_csv = tmp_path / "registros.csv"

    # Parchear las constantes para que apunten a tmp_path
    monkeypatch.setattr("parking.data_utils.csv_utils.USUARIOS_CSV", str(usuarios_csv))
    monkeypatch.setattr("parking.data_utils.csv_utils.BICIS_CSV", str(bicis_csv))
    monkeypatch.setattr(
        "parking.data_utils.csv_utils.REGISTROS_CSV", str(registros_csv)
    )
    # Llamar a la función
    asegurar_csvs()

    # Comprobar que se crearon con las cabeceras correctas
    with open(usuarios_csv, encoding="utf-8") as f:
        assert f.readline().strip() == CABECERA_USUARIOS
    with open(bicis_csv, encoding="utf-8") as f:
        assert f.readline().strip() == CABECERA_BICIS
    with open(registros_csv, encoding="utf-8") as f:
        assert f.readline().strip() == CABECERA_REGISTROS


def test_asegurar_csvs_corruptos(tmp_path, monkeypatch):
    """Comprueba que se sobrescriban los CSV si tienen cabeceras corruptas"""
    usuarios_csv = tmp_path / "usuarios.csv"
    bicis_csv = tmp_path / "bicis.csv"
    registros_csv = tmp_path / "registros.csv"

    # Crear archivos con cabeceras incorrectas
    usuarios_csv.write_text("dni,usuario,email,extra\n", encoding="utf-8")
    bicis_csv.write_text("num_serie,marca,modelo\n", encoding="utf-8")
    registros_csv.write_text("timestamp,accion,num_serie\n", encoding="utf-8")

    # Parchear las constantes para que apunten a tmp_path
    monkeypatch.setattr("parking.data_utils.csv_utils.USUARIOS_CSV", str(usuarios_csv))
    monkeypatch.setattr("parking.data_utils.csv_utils.BICIS_CSV", str(bicis_csv))
    monkeypatch.setattr(
        "parking.data_utils.csv_utils.REGISTROS_CSV", str(registros_csv)
    )

    # Llamar a la función
    asegurar_csvs()

    # Comprobar que se sobrescribieron con las cabeceras correctas
    with open(usuarios_csv, encoding="utf-8") as f:
        assert f.readline().strip() == CABECERA_USUARIOS
    with open(bicis_csv, encoding="utf-8") as f:
        assert f.readline().strip() == CABECERA_BICIS
    with open(registros_csv, encoding="utf-8") as f:
        assert f.readline().strip() == CABECERA_REGISTROS


import csv
import pytest
from parking.data_utils.csv_utils import escribir_csv_dic, leer_csv_dic


@pytest.mark.parametrize(
    "filas,expected",
    [
        # Lista vacía
        ([], []),
        # Diccionarios con claves correctas
        (
            [{"dni": "12345678A", "usuario": "Ana López", "email": "ana@example.com"}],
            [{"dni": "12345678A", "usuario": "Ana López", "email": "ana@example.com"}],
        ),
        # Diccionarios con claves incompletas o extra
        (
            [{"dni": "87654321B", "usuario": "Luis", "extra": "valor"}],
            [{"dni": "87654321B", "usuario": "Luis", "extra": "valor"}],
        ),
    ],
)
def test_escribir_csv_dic(tmp_path, filas, expected):
    """Comprueba que se lean correctamente lineas de diferentes archivos csv"""
    test_csv = tmp_path / "test.csv"

    if filas:
        # Escribir cabecera para que leer_csv_dic funcione
        with open(test_csv, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=filas[0].keys())
            writer.writeheader()

    # Escribir las filas
    escribir_csv_dic(str(test_csv), filas)

    # Leer y comprobar
    if filas:
        result = leer_csv_dic(str(test_csv))
        assert result == expected
    else:
        # Archivo no debería existir ni tener contenido
        assert not test_csv.exists() or test_csv.read_text(encoding="utf-8") == ""


def test_leer_csv_dic(monkeypatch):
    """Comprueba que la utilidad lea filas correctamente"""
    fake_csv = dedent(
        """\
        dni,nombre,email
        12345678A,Ana,ana@mail.com
        98765432Z,Paco,paco@mail.com
    """
    )

    def fake_open(*args, **kwargs):
        return io.StringIO(fake_csv)

    monkeypatch.setattr("builtins.open", fake_open)

    res = leer_csv_dic("fake.csv")

    assert res == [
        {"dni": "12345678A", "nombre": "Ana", "email": "ana@mail.com"},
        {"dni": "98765432Z", "nombre": "Paco", "email": "paco@mail.com"},
    ]


def test_borrar_filas(monkeypatch):
    """Comprueba que la utilidad borre filas correctamente"""
    fake_csv = dedent(
        """\
        dni,nombre,email
        12345678A,Ana,ana@mail.com
        98765432Z,Paco,paco@mail.com
        45678901X,Maria,maria@mail.com
    """
    )
    fake_file = io.StringIO(fake_csv)
    written_content = io.StringIO()

    class FakeFile:
        def __init__(self, io_obj):
            self.io_obj = io_obj

        def __enter__(self):
            self.io_obj.seek(0)
            return self.io_obj

        def __exit__(self, exc_type, exc_val, exc_tb):
            pass

    def fake_open(path, mode="r", newline=None, encoding=None):
        if "r" in mode:
            return FakeFile(fake_file)
        else:
            written_content.seek(0)
            written_content.truncate(0)
            return FakeFile(written_content)

    monkeypatch.setattr("builtins.open", fake_open)

    borrar_filas("fake.csv", "dni", "98765432Z")

    written_content.seek(0)
    reader = csv.DictReader(written_content)
    rows = list(reader)

    assert rows == [
        {"dni": "12345678A", "nombre": "Ana", "email": "ana@mail.com"},
        {"dni": "45678901X", "nombre": "Maria", "email": "maria@mail.com"},
    ]
