"""Clase que representa una fila del csv de usuarios"""

from parking.data_utils.validators import (
    es_dni_valido,
    es_dni_unico,
    es_email_valido,
    es_email_unico,
    es_campo_vacio,
)
from parking.data_utils.csv_utils import borrar_filas, escribir_csv_dic, leer_csv_dic
from ..config import BICIS_CSV, USUARIOS_CSV


class Usuario:

    def __init__(self, dni: str, nombre: str = "", email: str = "") -> None:
        """
        Genera un usuario dado su DNI (nombre e email opcional) y le asocia sus bicicletas si tiene

        Args:
            dni (str): DNI del usuario, tiene que ser único
            nombre (str, optional): Nombre del usuario. Por defecto vacío.
            email (str, optional): Email del usuario, tiene que ser único. Por defecto vacío.
        """
        self.dni = dni
        self.nombre = nombre
        self.email = email
        self.bicis = []
        for fila in leer_csv_dic(BICIS_CSV):
            if fila["dni_usuario"] == dni:
                self.bicis.append(fila["num_serie"])

    def es_valido(self) -> bool:
        """
        Valida que el usuario esté bien formado sin campos vacíos y con dni e email válidos

        Returns:
            bool: True si valido.
        """
        if not es_dni_valido(self.dni):
            print("ERROR: el DNI introducido no es válido")
            return False
        elif not es_email_unico(self.email):
            print("ERROR: el email introducido no es válido")
            return False
        elif es_campo_vacio(self.nombre):
            print("ERROR: el nombre no puede estar vacío")
            return False
        else:
            return True

    def es_unico(self) -> bool:
        """
        Valida que el usuario no se repita

        Returns:
            bool: True si es unico
        """
        if not es_dni_unico(self.dni):
            print("ERROR: el DNI introducido ya está registrado")
            return False
        elif not es_email_unico(self.email):
            print("ERROR: el email introducido ya está registrado")
            return False
        else:
            return True

    def crear_fila(self) -> dict:
        """
        Devuelve los valores del usuario en formato diccionario

        Returns:
            dict: El diccionario
        """
        return {"dni": self.dni, "nombre": self.nombre, "email": self.email}

    def guardar(self) -> bool:
        """
        Guarda el usuario en el csv siempre y cuando sea válido y único

        Returns:
            bool: True si se ha guardado el usuario
        """
        if self.es_valido() and self.es_unico():
            try:
                escribir_csv_dic(USUARIOS_CSV, [self.crear_fila()])
                print("OK: se ha registrado el usuario")
                return True
            except:
                print("ERROR: ha habido un error inexperado al escribir al CSV")
                return False
        else:
            return False

    def borrar(self) -> bool:
        """
        Intenta borrar el usuario siempre y cuando ya exista el DNI y no tenga bicis asociadas

        Returns:
            bool: _description_
        """
        if es_dni_unico(self.dni):
            print("ERROR: el DNI no existe o está mal escrito")
            return False
        if len(self.bicis) > 0:
            print(
                "ERROR: el usuario tiene bicicletas registradas, no se puede eliminar"
            )
            return False
        else:
            try:
                borrar_filas(USUARIOS_CSV, "dni", self.dni)
                print("OK: usuario borrado")
                return True
            except:
                print("ERROR: ha habido un error inexperado al borrar del CSV")
                return False
