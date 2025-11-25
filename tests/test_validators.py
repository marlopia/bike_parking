import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))
from parking.data_utils.validators import es_dni_valido


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
