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
    assert es_dni_valido(test_input) == True


@pytest.mark.parametrize(
    "test_input", ["27363397k", "64084713c", "07415485d", "10549082v", "43798002e"]
)
def test_dni_valido_letra_minuscula(test_input):
    assert es_dni_valido(test_input) == True


@pytest.mark.parametrize("test_input", ["7K", "613C", "5485D", "105082V", "4378002E"])
def test_dni_valido_invalido_formato(test_input):
    assert es_dni_valido(test_input) == False


@pytest.mark.parametrize(
    "test_input", ["27363397", "64084713", "07415485", "10549082", "43798002"]
)
def test_dni_valido_sin_letra(test_input):
    assert es_dni_valido(test_input) == False
