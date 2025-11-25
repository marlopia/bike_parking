import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))
from parking.data_utils.validators import (
    es_campo_vacio,
    es_dni_unico,
    es_dni_valido,
    es_email_unico,
    es_email_valido,
    es_serie_unica,
    normalizar_texto,
    puede_entrar,
    puede_salir,
)
from parking.data_utils.csv_utils import leer_csv_dic


# es_dni_valido
@pytest.mark.parametrize(
    "test_input", ["27363397K", "64084713C", "07415485D", "10549082V", "43798002E"]
)
def test_dni_valido_correcto(test_input):
    """Comprueba que el DNI tenga formato 12345678A (8 dígitos seguidos de una letra)"""
    assert es_dni_valido(test_input) == True


@pytest.mark.parametrize(
    "test_input", ["27363397k", "64084713c", "07415485d", "10549082v", "43798002e"]
)
def test_dni_valido_letra_minuscula(test_input):
    """Comprueba que el validador de DNI acepte también letras minúsculas"""
    assert es_dni_valido(test_input) == True


@pytest.mark.parametrize("test_input", ["7K", "613C", "5485D", "105082V", "4378002E"])
def test_dni_valido_invalido_formato(test_input):
    """Comprueba que el validador de DNI rechace formatos incorrectos"""
    assert es_dni_valido(test_input) == False


@pytest.mark.parametrize(
    "test_input", ["27363397", "64084713", "07415485", "10549082", "43798002"]
)
def test_dni_valido_sin_letra(test_input):
    """Comprueba que el validador de DNI rechace DNIs sin letra"""
    assert es_dni_valido(test_input) == False


# es_email_valido
@pytest.mark.parametrize(
    "test_input",
    [
        "ana@example.com",
        "test@gmail.es",
        "okay@yahoo.fr",
        "valid@outlook.it",
        "correct@proton.tv",
    ],
)
def test_es_email_valido_correcto(test_input):
    """Comprueba que el validador de emails devuelva True para emails válidos"""
    assert es_email_valido(test_input) == True


@pytest.mark.parametrize(
    "test_input",
    [
        "anaexample.com",
        "testgmail.es",
        "okayyahoo.fr",
        "validoutlook.it",
        "correctproton.tv",
    ],
)
def test_email_valido_sin_arroba(test_input):
    """Comprueba que el validador de emails devuelva False para emails que no tengan un @ (arroba)"""
    assert es_email_valido(test_input) == False


@pytest.mark.parametrize("test_input", ["ana@", "test@", "okay@", "valid@", "correct@"])
def test_email_valido_sin_dominio(test_input):
    """Comprueba que el validador de emails devuelva False para emails que no tengan un dominio"""
    assert es_email_valido(test_input) == False


@pytest.mark.parametrize("test_input", [""])
def test_email_valido_vacio(test_input):
    """Comprueba que el validador de emails devuelva False si el string es vacío"""
    assert es_email_valido(test_input) == False


# fixture para es_foo_unico


@pytest.fixture
def mock_leer_csv(monkeypatch):
    """Fixture que permite devolver cualquier lista de diccionarios como CSV simulado"""

    def _mock(data):
        monkeypatch.setattr(
            "parking.data_utils.validators.leer_csv_dic", lambda path: data
        )

    return _mock


# es_dni_unico
@pytest.mark.parametrize("test_dni", ["12345678A", "87654321B", "12121212Z"])
def test_es_dni_unico_nuevo(test_dni, mock_leer_csv):
    """Comprueba que se devuelva True en el validador si el DNI no coincide con ninguno del csv"""
    mock_leer_csv(
        [{"dni": "99999999Z", "nombre": "Ana López", "email": "ana@example.com"}]
    )
    assert es_dni_unico(test_dni) is True


@pytest.mark.parametrize("test_dni", ["99999999Z"])
def test_es_dni_unico_duplicado(test_dni, mock_leer_csv):
    """Comprueba que se devuelva False en el validador si el DNI coincide con alguno del csv"""
    mock_leer_csv(
        [{"dni": "99999999Z", "nombre": "Ana López", "email": "ana@example.com"}]
    )
    assert es_dni_unico(test_dni) is False


# es_email_unico
@pytest.mark.parametrize(
    "test_email", ["test@gmail.es", "okay@yahoo.fr", "correct@proton.tv"]
)
def test_es_email_unico_nuevo(test_email, mock_leer_csv):
    """Comprueba que se devuelva True en el validador si el email no coincide con ninguno del csv"""
    mock_leer_csv(
        [{"dni": "99999999Z", "nombre": "Ana López", "email": "ana@example.com"}]
    )
    assert es_email_unico(test_email) is True


@pytest.mark.parametrize(
    "test_email", ["ANA@example.com", "ana@example.com", "ana@EXAMPLE.com"]
)
def test_es_email_unico_duplicado(test_email, mock_leer_csv):
    """
    Comprueba que se devuelva False en el validador si el
    email coincide con alguno del csv,
    sin importar mayusculas o minusculas
    """
    mock_leer_csv(
        [{"dni": "99999999Z", "nombre": "Ana López", "email": "ANA@example.com"}]
    )
    assert es_email_unico(test_email) is False


# es_serie_unica
@pytest.mark.parametrize("test_serie", ["BK002", "BK003", "BK004"])
def test_es_serie_unica_nuevo(test_serie, mock_leer_csv):
    """Comprueba que se devuelva True en el validador si la serie no coincide con ninguna del csv"""
    mock_leer_csv(
        [
            {
                "num_serie": "BK001",
                "dni_usuario": "99999999Z",
                "marca": "Orbea",
                "modelo": "Carpe",
            }
        ]
    )
    assert es_serie_unica(test_serie) is True


@pytest.mark.parametrize("test_serie", ["BK001"])
def test_es_serie_unica_duplicado(test_serie, mock_leer_csv):
    """Comprueba que se devuelva False en el validador si la serie coincide con alguno del csv"""
    mock_leer_csv(
        [
            {
                "num_serie": "BK001",
                "dni_usuario": "99999999Z",
                "marca": "Orbea",
                "modelo": "Carpe",
            }
        ]
    )
    assert es_serie_unica(test_serie) is False


# es_campo_vacio
@pytest.mark.parametrize(
    "test_text, expected",
    [
        ("", True),
        ("foo", False),
        ("123", False),
    ],
)
def test_es_campo_vacio(test_text, expected):
    """Comprueba que se devuelva True cuando el texto es vacío y False cuando no"""
    assert es_campo_vacio(test_text) == expected


# es_campo_vacio
@pytest.mark.parametrize(
    "test_text, expected",
    [
        ("a b c d", "abcd"),
        ("ABCd", "abcd"),
        ("A B c D", "abcd"),
    ],
)
def test_normalizar_texto(test_text, expected):
    """Comprueba que se devuelva True cuando el texto es vacío y False cuando no"""
    assert normalizar_texto(test_text) == expected


# puede_entrar
@pytest.mark.parametrize(
    "test_serie,mock_data",
    [
        (
            "BK001",
            [
                {
                    "timestamp": "2025-03-01 08:15:22",
                    "accion": "IN",
                    "num_serie": "BK001",
                    "dni_usuario": "12345678A",
                },
                {
                    "timestamp": "2025-03-01 08:17:22",
                    "accion": "OUT",
                    "num_serie": "BK001",
                    "dni_usuario": "12345678A",
                },
            ],
        ),
        ("BK001", []),
    ],
)
def test_puede_entrar_correcto(test_serie, mock_data, mock_leer_csv):
    """
    Comprueba que el validador vea que el ultimo estado de la bici
    es OUT o que no ha sido introducida
    """
    mock_leer_csv(mock_data)
    assert puede_entrar(test_serie) is True


@pytest.mark.parametrize(
    "test_serie,mock_data",
    [
        (
            "BK001",
            [
                {
                    "timestamp": "2025-03-01 08:15:22",
                    "accion": "OUT",
                    "num_serie": "BK001",
                    "dni_usuario": "12345678A",
                },
                {
                    "timestamp": "2025-03-01 08:17:22",
                    "accion": "IN",
                    "num_serie": "BK001",
                    "dni_usuario": "12345678A",
                },
            ],
        )
    ],
)
def test_puede_entrar_incorrecto(test_serie, mock_data, mock_leer_csv):
    """
    Comprueba que el validador vea que el ultimo estado de la bici
    es OUT o que no ha sido introducida,
    como es IN devuelve False
    """
    mock_leer_csv(mock_data)
    assert puede_entrar(test_serie) is False


# puede_salir
@pytest.mark.parametrize(
    "test_serie,mock_data",
    [
        (
            "BK001",
            [
                {
                    "timestamp": "2025-03-01 08:15:22",
                    "accion": "OUT",
                    "num_serie": "BK001",
                    "dni_usuario": "12345678A",
                },
                {
                    "timestamp": "2025-03-01 08:17:22",
                    "accion": "IN",
                    "num_serie": "BK001",
                    "dni_usuario": "12345678A",
                },
            ],
        )
    ],
)
def test_puede_salir_correcto(test_serie, mock_data, mock_leer_csv):
    """Comprueba que el validador vea que el ultimo estado de la bici es IN"""
    mock_leer_csv(mock_data)
    assert puede_salir(test_serie) is True


@pytest.mark.parametrize(
    "test_serie,mock_data",
    [
        (
            "BK001",
            [
                {
                    "timestamp": "2025-03-01 08:15:22",
                    "accion": "IN",
                    "num_serie": "BK001",
                    "dni_usuario": "12345678A",
                },
                {
                    "timestamp": "2025-03-01 08:17:22",
                    "accion": "OUT",
                    "num_serie": "BK001",
                    "dni_usuario": "12345678A",
                },
            ],
        ),
        ("BK001", []),
    ],
)
def test_puede_salir_incorrecto(test_serie, mock_data, mock_leer_csv):
    """
    Comprueba que el validador vea que el ultimo estado de la bici es IN,
    si ya esta fuera o nunca ha sido introducida devuelve False
    """
    mock_leer_csv(mock_data)
    assert puede_salir(test_serie) is False
