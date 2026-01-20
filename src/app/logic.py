"""Archivo de funciones de lógica"""

import re
from parking.config import PATRON_DNI, LETRAS_DNI
from parking.models.bd import Bd
from parking.models.usuario import Usuario

bd = Bd()


def es_dni_valido(dni: str) -> bool:
    """
    Valida que un DNI tenga 8 digitos y una letra mayúscula o minúscula.

    Args:
        dni (str): Número de DNI a evaluar

    Returns:
        bool: True si coincide el patrón, False si no
    """
    dni = dni.strip().upper()
    if not re.match(PATRON_DNI, dni):
        return False

    numero = int(dni[:8])
    letra = dni[8]
    return LETRAS_DNI[numero % 23] == letra


def es_usuario_registrado(dni: str) -> bool:
    """
    Comprueba que exista el DNI del usuario dado en la base de datos

    Args:
        usuario (str): DNI del usuario

    Returns:
        bool: true si el usuario está registrado
    """
    with bd.crear_sesion() as sesion:
        if sesion.query(Usuario).filter_by(dni=dni).first():
            return True
        else:
            return False


def buscar_usuario_por_dni(dni: str) -> Usuario:
    return Usuario.obtener_o_crear(dni)
