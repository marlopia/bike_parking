"""Clase que representa una fila del csv de bicis"""

from datetime import datetime

from parking.models.usuario import Usuario
from parking.data_utils.validators import (
    es_campo_vacio,
    puede_entrar,
    puede_salir,
    es_dni_unico,
    es_serie_unica,
)
from parking.data_utils.csv_utils import escribir_csv_dic
from ..config import REGISTROS_CSV, TIMESTAMP_FMT


class Registro:

    def __init__(self, accion: str, num_serie: str, dni_usuario: str) -> None:
        """
        Genera un objeto registro dado sus datos

        Args:
            accion (str): IN para meter la bici, OUT para sacarla
            num_serie (str): Número de serie de la bicicleta
            dni_usuario (str): DNI del propietario de la bicicleta
        """
        self.timestamp = datetime.now().strftime(TIMESTAMP_FMT)
        self.accion = accion
        self.num_serie = num_serie
        self.dni_usuario = dni_usuario

    def es_valido(self) -> bool:
        """
        Valida que el registro esté bien formado sin campos vacíos y con un usuario y bici existentes

        Returns:
            bool: True si valido.
        """
        for key, value in vars(self).values():
            if es_campo_vacio(value):
                print(f"ERROR: el campo {key} no puede estar vacío")
                return False
        if es_dni_unico(self.dni_usuario):
            print("ERROR: el usuario no está registrado")
            return False
        elif es_serie_unica(self.num_serie):
            print("ERROR: la bicicleta no está registrada")
            return False
        else:
            return True

    def es_permitido(self) -> bool:
        """
        Evalua si la bici indicada puede realizar la acción dada.
        Cualquier acción que no sea IN o OUT devuelve False.

        Returns:
            bool: True si puede
        """
        if self.accion == "IN":
            if not puede_entrar(self.num_serie):
                print("ERROR: Esta bicicleta no puede entrar")
                return False
            else:
                return True
        elif self.accion == "OUT":
            if not puede_salir(self.num_serie):
                print("ERROR: Esta bicicleta no puede salir")
                return False
            else:
                return True
        else:
            return False

    def crear_fila(self) -> dict:
        """
        Devuelve los valores de la bici en formato diccionario

        Returns:
            dict: El diccionario
        """
        return {
            "timestamp": self.timestamp,
            "accion": self.accion,
            "num_serie": self.num_serie,
            "dni_usuario": self.dni_usuario,
        }

    def guardar(self) -> bool:
        """
        Guarda el registro en el csv siempre y cuando sea válido y tenga un usuario y bici creados

        Returns:
            bool: True si se ha guardado el registro
        """

        if self.es_valido() and self.es_permitido():
            if not self.num_serie in Usuario(self.dni_usuario).bicis:
                print("ERROR: esta bicicleta NO pertenece al usuario")
                return False
            else:
                try:
                    escribir_csv_dic(REGISTROS_CSV, [self.crear_fila()])
                    print("OK: se ha registrado el registro")
                    return True
                except:
                    print("ERROR: ha habido un error inexperado al escribir al CSV")
                    return False
        else:
            return False
