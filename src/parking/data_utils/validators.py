"""Paquete de validaciones para comprobar entrada de datos y consistencias de datos en los archivos"""

import re

from .csv_utils import leer_csv_dic
from ..config import PATRON_DNI, PATRON_EMAIL, USUARIOS_CSV, BICIS_CSV


def es_dni_valido(dni: str) -> bool:
    """
    Valida que un DNI tenga 8 digitos y una letra mayúscula o minúscula.

    Args:
        dni (str): Número de DNI a evaluar

    Returns:
        bool: True si coincide el patrón, False si no
    """
    return bool(re.match(PATRON_DNI, dni))


def es_email_valido(email: str) -> bool:
    """
    Valida que un email conste de texto seguido de arroba y un dominio.

    Args:
        email (str): _description_

    Returns:
        bool: _description_
    """
    return bool(re.match(PATRON_EMAIL, email))


def es_dni_unico(dni: str) -> bool:
    """
    Valida que un DNI no aparezca en el csv de usuarios

    Args:
        dni (str): DNI a validar

    Returns:
        bool: Si no existe el DNI devuelve True, si existe False
    """
    filas = leer_csv_dic(USUARIOS_CSV)
    for fila in filas:
        if fila["dni"] == dni:
            return False

    return True


def es_email_unico(email: str) -> bool:
    """
    Valida que un email no aparezca en el csv de usuarios

    Args:
        email (str): email a validar

    Returns:
        bool: Si no existe el email devuelve True, si existe False
    """
    filas = leer_csv_dic(USUARIOS_CSV)
    for fila in filas:
        if normalizar_texto(fila["email"]) == normalizar_texto(email):
            return False

    return True


def es_serie_unica(num_serie: str) -> bool:
    """
    Valida que una serie no aparezca en el csv de bicis

    Args:
        num_serie (str): número de serie a validar

    Returns:
        bool: Si no existe el DNI devuelve True, si existe False
    """
    filas = leer_csv_dic(BICIS_CSV)
    for fila in filas:
        if fila["num_serie"] == num_serie:
            return False

    return True


def es_campo_vacio(text: str) -> bool:
    """
    Valida que el texto introducido no esté vacío.

    Args:
        text (str): Texto introducido

    Returns:
        bool: True si el texto es vacío, False si no
    """
    return text == ""


def normalizar_texto(text: str) -> str:
    """
    Devuelve la cadena de texto sin espacios ni mayúsculas

    Args:
        text (str): Texto a normalizar

    Returns:
        str: Texto sin espacios ni mayúsculas
    """
    return text.lower().strip()
