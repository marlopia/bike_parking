"""Paquete de validaciones para comprobar entrada de datos y consistencias de datos en los archivos"""

import re


dni_pattern = r"^\d{8}[A-Za-z]$"
email_pattern = r"^[\w\.\-]+@[\w\.\-]+\.\w+$"


def es_dni_valido(dni: str) -> bool:
    """
    Valida que un DNI tenga 8 digitos y una letra mayúscula o minúscula.

    Args:
        dni (str): Número de DNI a evaluar

    Returns:
        bool: True si coincide el patrón, False si no
    """
    return bool(re.match(dni_pattern, dni))


def es_email_valido(email: str) -> bool:
    """
    Valida que un email conste de texto seguido de arroba y un dominio.

    Args:
        email (str): _description_

    Returns:
        bool: _description_
    """
    return bool(re.match(email_pattern, email))
