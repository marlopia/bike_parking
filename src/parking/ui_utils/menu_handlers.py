"""Archivo de funciones de interacciones en el menú de la aplicación"""

from ..rules import guardar_usuario, guardar_bici, registrar


def _preguntar(texto: str) -> bool:
    """
    Método auxiliar de preguntas si o no.
    Itera hasta obtener una respuesta válida.

    Args:
        texto (str): Texto a sacar por pantalla para preguntar

    Returns:
        bool: True si respuesta es S/s, False si es N/n
    """
    res = input(texto).upper().strip()
    while res != "S" and res != "N":
        res = input(texto).upper().strip()
    if res == "S":
        return True
    else:
        return False


def menu_anadir_usuario() -> bool:
    """
    Pide al usuario dni, nombre y email para registrarse.
    Se repite en bucle si el usuario acepta continuar

    Returns:
        bool: True si se completa la operación
    """
    dni = input("Introduce tu DNI con letra: ").strip()
    nombre = input("Introduce tu nombre: ").strip()
    email = input("Introduce tu email: ").strip()

    while not guardar_usuario(dni, nombre, email):
        if not _preguntar("Intentarlo de nuevo? (S/N): "):
            return False
        dni = input("Introduce tu DNI con letra: ").strip()
        nombre = input("Introduce tu nombre: ").strip()
        email = input("Introduce tu email: ").strip()

    return True


def menu_anadir_bici() -> bool:
    """
    Pide al usuario número de serie, su DNI, marca y modelo para registrar su bicicleta.
    Se repite en bucle si el usuario acepta continuar

    Returns:
        bool: True si se completa la operación
    """
    num_serie = input("Introduce el número de serie de tu bicicleta: ").strip()
    dni = input("Introduce tu DNI con letra: ").strip()
    marca = input("Introduce la marca de tu bicicleta: ").strip()
    modelo = input("Introduce el modelo de tu bicicleta: ").strip()

    while not guardar_bici(num_serie, dni, marca, modelo):
        if not _preguntar("Intentarlo de nuevo? (S/N): "):
            return False
        num_serie = input("Introduce el número de serie de tu bicicleta: ").strip()
        dni = input("Introduce tu DNI con letra: ").strip()
        marca = input("Introduce la marca de tu bicicleta: ").strip()
        modelo = input("Introduce el modelo de tu bicicleta: ").strip()

    return True


def registro_entrada() -> bool:
    """
    Pide al usuario su DNI y número de serie de bicicleta para insertar la bicicleta.
    Se repite en bucle si el usuario acepta continuar

    Returns:
        bool: True si se completa la operación
    """
    dni = input("Introduce tu DNI con letra: ").strip()
    num_serie = input("Introduce el número de serie de tu bicicleta: ").strip()

    while not registrar("IN", dni, num_serie):
        if not _preguntar("Intentarlo de nuevo? (S/N): "):
            return False
        dni = input("Introduce tu DNI con letra: ").strip()
        num_serie = input("Introduce el número de serie de tu bicicleta: ").strip()

    return True


def registro_salida() -> bool:
    """
    Pide al usuario su DNI y número de serie de bicicleta para sacar la bicicleta.
    Se repite en bucle si el usuario acepta continuar

    Returns:
        bool: True si se completa la operación
    """
    dni = input("Introduce tu DNI con letra: ").strip()
    num_serie = input("Introduce el número de serie de tu bicicleta: ").strip()

    while not registrar("OUT", dni, num_serie):
        if not _preguntar("Intentarlo de nuevo? (S/N): "):
            return False
        dni = input("Introduce tu DNI con letra: ").strip()
        num_serie = input("Introduce el número de serie de tu bicicleta: ").strip()

    return True
