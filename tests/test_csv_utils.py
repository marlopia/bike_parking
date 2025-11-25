import pytest

from parking.config import CABECERA_USUARIOS, CABECERA_BICIS, CABECERA_REGISTROS
from parking.data_utils.csv_utils import asegurar_csvs, escribir_csv_dic, leer_csv_dic


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
