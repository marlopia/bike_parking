"""Archivo de funciones de interacciones en el menú de la aplicación"""

from parking.models.usuario import Usuario
from parking.models.bici import Bici
from parking.models.registro import Registro


def preguntar_bool(texto: str) -> bool:
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


def preguntar_dato(texto: str) -> str:
    """
    Método auxiliar de preguntas sobre un dato.
    Recorta espacios delante y detrás del dato con .strip()

    Args:
        texto (str): Texto a sacar por pantalla para preguntar

    Returns:
        str: Cadena de texto introducida por el usuario
    """
    return input(texto).strip()


def menu_anadir_usuario() -> bool:
    """
    Pide al usuario dni, nombre y email para registrarse.
    Se repite en bucle si el usuario acepta continuar

    Returns:
        bool: True si se completa la operación
    """
    dni = preguntar_dato("Introduce tu DNI con letra: ")
    nombre = preguntar_dato("Introduce tu nombre: ")
    email = preguntar_dato("Introduce tu email: ")

    usuario = Usuario(dni, nombre, email)

    while not usuario.guardar():
        if not preguntar_bool("Intentarlo de nuevo? (S/N): "):
            return False
        dni = preguntar_dato("Introduce tu DNI con letra: ")
        nombre = preguntar_dato("Introduce tu nombre: ")
        email = preguntar_dato("Introduce tu email: ")

        usuario = Usuario(dni, nombre, email)

    return True


def menu_borrar_usuario() -> bool:
    """
    Pide al usuario dni para borrar.
    Se repite en bucle si el usuario acepta continuar

    Returns:
        bool: True si se completa la operación
    """
    dni = preguntar_dato("Introduce tu DNI con letra: ")
    usuario = Usuario(dni)

    while not usuario.borrar():
        if not preguntar_bool("Intentarlo de nuevo? (S/N): "):
            return False
        dni = preguntar_dato("Introduce tu DNI con letra: ")
        usuario = Usuario(dni)

    return True


def menu_anadir_bici() -> bool:
    """
    Pide al usuario número de serie, su DNI, marca y modelo para registrar su bicicleta.
    Se repite en bucle si el usuario acepta continuar

    Returns:
        bool: True si se completa la operación
    """
    num_serie = preguntar_dato("Introduce el número de serie de tu bicicleta: ")
    dni = preguntar_dato("Introduce tu DNI con letra: ")
    marca = preguntar_dato("Introduce la marca de tu bicicleta: ")
    modelo = preguntar_dato("Introduce el modelo de tu bicicleta: ")

    bici = Bici(num_serie, dni, marca, modelo)

    while not bici.guardar():
        if not preguntar_bool("Intentarlo de nuevo? (S/N): "):
            return False
        num_serie = preguntar_dato("Introduce el número de serie de tu bicicleta: ")
        dni = preguntar_dato("Introduce tu DNI con letra: ")
        marca = preguntar_dato("Introduce la marca de tu bicicleta: ")
        modelo = preguntar_dato("Introduce el modelo de tu bicicleta: ")
        bici = Bici(num_serie, dni, marca, modelo)

    return True


def menu_borrar_bici() -> bool:
    """
    Pide al usuario número de serie para borrar una bicicleta.
    Se repite en bucle si el usuario acepta continuar

    Returns:
        bool: True si se completa la operación
    """
    num_serie = preguntar_dato("Introduce el número de serie de tu bicicleta: ")
    bici = Bici(num_serie)

    while not bici.borrar():
        if not preguntar_bool("Intentarlo de nuevo? (S/N): "):
            return False
        num_serie = preguntar_dato("Introduce el número de serie de tu bicicleta: ")
        bici = Bici(num_serie)

    return True


def registro_entrada() -> bool:
    """
    Pide al usuario su DNI y número de serie de bicicleta para insertar la bicicleta.
    Se repite en bucle si el usuario acepta continuar

    Returns:
        bool: True si se completa la operación
    """
    dni = preguntar_dato("Introduce tu DNI con letra: ")
    num_serie = preguntar_dato("Introduce el número de serie de tu bicicleta: ")
    registro = Registro("IN", num_serie, dni)

    while not registro.guardar():
        if not preguntar_bool("Intentarlo de nuevo? (S/N): "):
            return False
        dni = preguntar_dato("Introduce tu DNI con letra: ")
        num_serie = preguntar_dato("Introduce el número de serie de tu bicicleta: ")
        registro = Registro("IN", num_serie, dni)

    return True


def registro_salida() -> bool:
    """
    Pide al usuario su DNI y número de serie de bicicleta para sacar la bicicleta.
    Se repite en bucle si el usuario acepta continuar

    Returns:
        bool: True si se completa la operación
    """
    dni = preguntar_dato("Introduce tu DNI con letra: ")
    num_serie = preguntar_dato("Introduce el número de serie de tu bicicleta: ")
    registro = Registro("OUT", num_serie, dni)

    while not registro.guardar():
        if not preguntar_bool("Intentarlo de nuevo? (S/N): "):
            return False
        dni = preguntar_dato("Introduce tu DNI con letra: ")
        num_serie = preguntar_dato("Introduce el número de serie de tu bicicleta: ")
        registro = Registro("OUT", num_serie, dni)

    return True
