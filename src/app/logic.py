"""Archivo de funciones de lógica"""

import re
from email_validator import validate_email, EmailNotValidError
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
        bool: True si válido
    """
    dni = dni.strip().upper()
    if not re.fullmatch(PATRON_DNI, dni):
        print("REGEX ERROR")
        return False

    numero = int(dni[:8])
    letra = dni[8]
    return LETRAS_DNI[numero % 23] == letra


def es_email_valido(email: str) -> bool:
    """
    Valida que un email tenga un usuario, una arroba y un FQDN válido.
    Usa el paquete email-validator para externalizar la validación.

    Args:
        email (str): Email a evaluar

    Returns:
        bool: True si válido
    """
    try:
        validate_email(email)
        return True
    except EmailNotValidError:
        return False


def es_usuario_registrado(dni: str) -> bool:
    """
    Comprueba que exista el DNI dado en la base de datos

    Args:
        dni (str): El DNI

    Returns:
        bool: true si el DNI está registrado
    """
    with bd.crear_sesion() as sesion:
        if sesion.query(Usuario).filter_by(dni=dni).first():
            return True
        else:
            return False


def es_email_registrado(email: str) -> bool:
    """
    Comprueba que exista el email dado en la base de datos

    Args:
        email (str): El email

    Returns:
        bool: true si el email está registrado
    """
    with bd.crear_sesion() as sesion:
        if sesion.query(Usuario).filter_by(email=email).first():
            return True
        else:
            return False


def obtener_usuario(dni: str) -> Usuario:
    """
    Devuelve un objeto Usuario dado un DNI.

    Args:
        dni (str): El DNI

    Returns:
        Usuario: El usuario

    Raises:
        UsuarioError: Si el usuario no existe
    """
    return Usuario.obtener_usuario(dni)


def registrar_usuario(nombre: str, dni: str, email: str) -> None:
    """
    Dado datos de un usuario, lo registra en la base de datos

    Args:
        nombre (str): Nombre del usuario
        dni (str): DNI del usuario
        email (str): Email del usuario

    Raises:
        UsuarioError: Si el usuario no es válido o no se ha podido guardar
    """
    usuario = Usuario(dni, nombre, email)
    usuario.guardar()
