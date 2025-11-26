"""Archivo de la lógica de negocio del programa"""

from datetime import datetime
from .data_utils.csv_utils import borrar_filas, escribir_csv_dic, leer_csv_dic
from .data_utils.validators import (
    es_campo_vacio,
    es_dni_unico,
    es_dni_valido,
    es_email_unico,
    es_email_valido,
    es_serie_unica,
    puede_entrar,
    puede_salir,
)
from .config import BICIS_CSV, REGISTROS_CSV, TIMESTAMP_FMT, USUARIOS_CSV


def guardar_usuario(dni: str, nombre: str, email: str) -> bool:
    """
    Guarda una fila representativa de un usuario en el csv de usuarios.
    Escribe por pantalla un mensaje relativo a la ejecución
    correcta o incorrecta del guardado.

    Args:
        dni (str): Valor no vacío de DNI con formato de 8 digitos y letra sin espacios o guiones.
            No puede coincidir con un valor registrado previamente
        nombre (str): Valor no vacío de nombre de usuario
        email (str): Valor no vacío de email con formato texto@dominio.tld.
            No puede coincidir con un valor registrado previamente

    Returns:
        bool: True si se completa la operación sin fallos
    """

    if es_campo_vacio(dni):
        print("ERROR: Campo DNI vacío")
        return False
    if es_campo_vacio(nombre):
        print("ERROR: Campo nombre vacío")
        return False
    if es_campo_vacio(email):
        print("ERROR: Campo email vacío")
        return False

    if not es_dni_valido(dni):
        print("ERROR: Formato de DNI no reconocido")
        return False

    if not es_email_valido(email):
        print("ERROR: Formato de email no reconocido.")
        return False

    if not es_dni_unico(dni):
        print(f"ERROR: El DNI {dni} ya está registrado")
        return False

    if not es_email_unico(email):
        print(f"ERROR: El email {email} ya está registrado")
        return False

    fila = [{"dni": dni, "nombre": nombre, "email": email}]
    try:
        escribir_csv_dic(USUARIOS_CSV, fila)
        print("OK: se ha registrado el usuario")
        return True
    except:
        print("ERROR: ha habido un error inexperado al escribir al CSV")
        return False


def guardar_bici(num_serie: str, dni: str, marca: str, modelo: str) -> bool:
    """
    Guarda una fila representativa de una bicicleta en el csv de bicicletas.
    Escribe por pantalla un mensaje relativo a la ejecución
    correcta o incorrecta del guardado.

    Args:
        num_serie (str): Valor no vacío del número de serie de la bicicleta.
            No puede coincidir con un valor registrado previamente
        dni (str): Valor no vacío del DNI del usuario.
            Debe de haber sido registrado previamente en el fichero de usuarios
        marca (str): Valor no vacío de la marca de la bicicleta
        modelo (str): Valor no vacío del modelo de la bicicleta

    Returns:
        bool: True si se completa la operación sin fallos
    """

    if es_campo_vacio(num_serie):
        print("ERROR: Campo número de serie vacío")
        return False
    if es_campo_vacio(dni):
        print("ERROR: Campo DNI vacío")
        return False
    if es_campo_vacio(marca):
        print("ERROR: Campo marca vacío")
        return False
    if es_campo_vacio(modelo):
        print("ERROR: Campo modelo vacío")
        return False

    if es_dni_unico(dni):
        print("ERROR: DNI no regristado en el sistema")
        return False

    if not es_serie_unica(num_serie):
        print(
            f"ERROR: la bicicleta con el número de serie {num_serie} ya está en el sistema"
        )
        return False

    try:
        fila = [
            {
                "num_serie": num_serie,
                "dni_usuario": dni,
                "marca": marca,
                "modelo": modelo,
            }
        ]
        escribir_csv_dic(BICIS_CSV, fila)
        print("OK: se ha registrado la bicicleta")
        return True
    except:
        print("ERROR: ha habido un error inexperado al escribir al CSV")
        return False


def registrar(accion: str, dni: str, num_serie: str) -> bool:
    """
    Comprueba si la bicicleta puede entrar o salir y registra su movimiento.
    Escribe por pantalla un mensaje relativo a la ejecución
    correcta o incorrecta del guardado.

    Args:
        accion (str): IN para guardar la bicicleta, OUT para retirarla. No admite otros valores
        dni (str): DNI del usuario a registrar, esta función no lo verifica
        num_serie (str): Número de serie de la bicicleta a registrar, esta función no lo verifica

    Raises:
        NotImplementedError: Si no se acepta la orden del parámetro accion

    Returns:
        bool: True si se completa la operación sin fallos
    """

    accion = accion.upper()
    if accion == "IN":
        if not puede_entrar(num_serie):
            print("ERROR: la bicicleta no puede entrar")
            return False
        now = datetime.now().strftime(TIMESTAMP_FMT)
        fila = [
            {
                "timestamp": now,
                "accion": "IN",
                "num_serie": num_serie,
                "dni_usuario": dni,
            }
        ]
        escribir_csv_dic(REGISTROS_CSV, fila)
        print(f"OK: registrado entrada bicicleta a las {now}")
        return True
    elif accion == "OUT":
        if not puede_salir(num_serie):
            print("ERROR: la bicicleta no puede salir")
            return False
        now = datetime.now().strftime(TIMESTAMP_FMT)
        fila = [
            {
                "timestamp": now,
                "accion": "OUT",
                "num_serie": num_serie,
                "dni_usuario": dni,
            }
        ]
        escribir_csv_dic(REGISTROS_CSV, fila)
        print(f"OK: registrado salida bicicleta a las {now}")
        return True
    else:
        raise NotImplementedError("Accion debe ser IN o OUT")


def listar_bicis_usuario(dni: str) -> list[str]:
    """
    Dado un DNI, devuelve todas las bicicletas del usuario

    Args:
        dni (str): DNI del usuario, no se verifica nada

    Returns:
        list[str]: Listado de números de serie de bicicletas
    """
    bicis = []
    for fila in leer_csv_dic(BICIS_CSV):
        if fila["dni_usuario"] == dni:
            bicis.append(fila["num_serie"])

    return bicis


def borrar_bici(num_serie: str) -> bool:
    """
    Borra la bicicleta dado su número de serie

    Args:
        num_serie (str): Número de serie de la bicicleta

    Returns:
        bool: True si completa la operación
    """
    if es_serie_unica(num_serie):
        print("ERROR: no existe la bicicleta con ese número de serie")
        return False
    else:
        try:
            borrar_filas(BICIS_CSV, "num_serie", num_serie)
            print("OK: bicicleta borrada")
            return True
        except:
            print("ERROR: ha habido un error inexperado al borrar del CSV")
            return False


def borrar_usuario(dni: str) -> bool:
    """
    Borra un usuario dado su DNI, siempre y cuando no tenga bicicletas registradas

    Args:
        dni (str): DNI del usuario

    Returns:
        bool: True si completa la operación
    """
    if es_dni_unico(dni):
        print("ERROR: no existe ese DNI en el registro")
        return False
    elif len(listar_bicis_usuario(dni)) > 0:
        print("ERROR: el usuario tiene bicicletas registradas, no se puede borrar")
        return False
    else:
        try:
            borrar_filas(USUARIOS_CSV, "dni", dni)
            print("OK: usuario borrado")
            return True
        except:
            print("ERROR: ha habido un error inexperado al borrar del CSV")
            return False
