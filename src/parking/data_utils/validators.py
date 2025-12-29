"""Paquete de validaciones para comprobar entrada de datos y consistencias de datos en los archivos"""

import re
from typing import Optional

from sqlalchemy import desc

from parking.models.bd import Bd, BiciORM, RegistroORM, UsuarioORM
from ..config import PATRON_DNI, PATRON_EMAIL, USUARIOS_CSV, BICIS_CSV, REGISTROS_CSV


bd = Bd()


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
        email (str): Email a evaluar

    Returns:
        bool: True si coincide el patrón, False si no
    """
    return bool(re.match(PATRON_EMAIL, email))


def es_dni_unico(dni: str) -> bool:
    """
    Valida que un DNI no aparezca en la tabla de usuarios

    Args:
        dni (str): DNI a validar

    Returns:
        bool: Si no existe el DNI devuelve True, si existe False
    """
    with bd.crear_sesion() as sesion:
        if sesion.query(UsuarioORM).filter_by(dni=dni).first():
            return False
        else:
            return True


def es_email_unico(email: str) -> bool:
    """
    Valida que un email no aparezca en la tabla de usuarios

    Args:
        email (str): email a validar

    Returns:
        bool: Si no existe el email devuelve True, si existe False
    """
    with bd.crear_sesion() as sesion:
        if sesion.query(UsuarioORM).filter_by(email=email).first():
            return False
        else:
            return True


def es_serie_unica(num_serie: str) -> bool:
    """
    Valida que una serie no aparezca en la tabla de bicis

    Args:
        num_serie (str): número de serie a validar

    Returns:
        bool: Si no existe el DNI devuelve True, si existe False
    """
    with bd.crear_sesion() as sesion:
        if sesion.query(BiciORM).filter_by(num_serie=num_serie).first():
            return False
        else:
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
    return text.lower().replace(" ", "")


def puede_entrar(num_serie: str) -> bool:
    """
    Devuelve si la bici puede ser guardada

    Args:
        num_serie (str): Número de serie de la bici

    Returns:
        bool: True si la bici nunca ha entrado o su último estado es OUT
    """
    with bd.crear_sesion() as sesion:
        registro_reciente: Optional[RegistroORM] = (
            sesion.query(RegistroORM)
            .filter_by(num_serie=num_serie)
            .order_by(desc(RegistroORM.timestamp))
            .first()
        )

        if registro_reciente is None:
            return True  # La bici entra por primera vez
        elif registro_reciente.accion == "OUT":  # type: ignore
            return True  # Ultima accion fue OUT
        else:
            return False


def puede_salir(num_serie: str) -> bool:
    """
    Devuelve si la bici puede ser retirada

    Args:
        num_serie (str): Número de serie de la bici

    Returns:
        bool: True si el último estado de la bici es IN
    """
    with bd.crear_sesion() as sesion:
        registro_reciente: Optional[RegistroORM] = (
            sesion.query(RegistroORM)
            .filter_by(num_serie=num_serie)
            .order_by(desc(RegistroORM.timestamp))
            .first()
        )

        if registro_reciente is None:
            return False  # La bici nunca ha entrado, no puede salir
        elif registro_reciente.accion == "IN":  # type: ignore
            return True  # Ultima accion fue IN
        else:
            return False
