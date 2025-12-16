"""Clase que representa una fila del csv de bicis"""

from parking.data_utils.validators import es_campo_vacio, es_dni_unico, es_serie_unica
from parking.data_utils.csv_utils import borrar_filas, escribir_csv_dic
from ..config import BICIS_CSV


class Bici:

    def __init__(
        self, num_serie: str, dni_usuario: str = "", marca: str = "", modelo: str = ""
    ) -> None:
        """
        Devuelve un objeto bici dado su número de serie (dni del usuario, marca y modelo opcional)

        Args:
            num_serie (str): Número de serie de la bicicleta
            dni_usuario (str, optional): DNI del usuario propietario de la bici. Por defecto vacío.
            marca (str, optional): Marca de la bici. Por defecto vacío.
            modelo (str, optional): Modelo de la bici. Por defecto vacío.
        """
        self.num_serie = num_serie
        self.dni_usuario = dni_usuario
        self.marca = marca
        self.modelo = modelo

    def es_valido(self) -> bool:
        """
        Valida que la bici esté bien formada sin campos vacíos

        Returns:
            bool: True si válida
        """
        for key, value in vars(self).values():
            if es_campo_vacio(value):
                print(f"ERROR: el campo {key} no puede estar vacío")
                return False
        return True

    def es_unico(self) -> bool:
        if not es_serie_unica(self.num_serie):
            print("ERROR: el número de serie ya está registrado")
            return False
        else:
            return True

    def existe_usuario(self) -> bool:
        # Mirando si el DNI es unico en el csv sabemos si existe ya
        if not es_dni_unico(self.dni_usuario):
            print("ERROR: el usuario no está registrado")
            return False
        else:
            return True

    def crear_fila(self) -> dict:
        """
        Devuelve los valores de la bici en formato diccionario

        Returns:
            dict: El diccionario
        """
        return {
            "num_serie": self.num_serie,
            "dni_usuario": self.dni_usuario,
            "marca": self.marca,
            "modelo": self.modelo,
        }

    def guardar(self) -> bool:
        """
        Guarda la bici en el csv siempre y cuando sea válida, única y tenga un usuario creado

        Returns:
            bool: True si se ha guardado la bici
        """
        if self.es_valido() and self.es_unico() and self.existe_usuario():
            try:
                escribir_csv_dic(BICIS_CSV, [self.crear_fila()])
                print("OK: se ha registrado la bicicleta")
                return True
            except:
                print("ERROR: ha habido un error inexperado al escribir al CSV")
                return False
        else:
            return False

    def borrar(self) -> bool:
        """
        Intenta borrar la bici siempre y cuando tenga un número de serie válido

        Returns:
            bool: _description_
        """
        if self.es_unico():
            try:
                borrar_filas(BICIS_CSV, "num_serie", self.num_serie)
                print("OK: bicicleta borrada")
                return True
            except:
                print("ERROR: ha habido un error inexperado al borrar del CSV")
                return False
        else:
            return False
