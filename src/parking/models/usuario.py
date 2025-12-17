"""Clase que representa una fila del csv de usuarios"""

from sqlalchemy.orm import Session
from parking.data_utils.validators import (
    es_dni_valido,
    es_dni_unico,
    es_email_valido,
    es_email_unico,
    es_campo_vacio,
)
from parking.data_utils.csv_utils import borrar_filas, escribir_csv_dic, leer_csv_dic
from parking.models.bd import Bd, UsuarioORM
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
        elif not es_email_valido(self.email):
            print("ERROR: el email introducido no es válido")
            return False
        else:
            return True

    def crear_fila(self) -> UsuarioORM:
        """
        Devuelve los valores del usuario como objeto del ORM

        Returns:
            UsuarioORM: El objeto de ORM
        """
        return UsuarioORM(self.dni, self.nombre, self.email)

    def guardar(self, bd: Bd) -> bool:
        """
        Guarda el usuario en el csv siempre y cuando sea válido y único

        Returns:
            bool: True si se ha guardado el usuario
        """
        with bd.crear_sesion() as sesion:
            if self.es_valido():
                if sesion.query(UsuarioORM).filter_by(dni=self.dni).first():
                    print("ERROR: el DNI introducido ya está registrado")
                    return False
                elif sesion.query(UsuarioORM).filter_by(email=self.email).first():
                    print("ERROR: el email introducido ya está registrado")
                    return False
                else:
                    try:
                        sesion.add(self.crear_fila())
                        print("OK: se ha registrado el usuario")
                        return True
                    except:
                        print(
                            "ERROR: ha habido un error inexperado al escribir en la base de datos"
                        )
                        return False
            else:
                return False

    def borrar(self, bd: Bd) -> bool:
        """
        Intenta borrar el usuario siempre y cuando ya exista el DNI y no tenga bicis asociadas

        Returns:
            bool: _description_
        """
        with bd.crear_sesion() as sesion:
            usuario = sesion.query(UsuarioORM).filter_by(dni=self.dni).first()
            if not usuario:
                print("ERROR: el DNI no existe o está mal escrito")
                return False
            else:
                try:
                    sesion.delete(usuario)
                    print("OK: usuario borrado")
                    return True
                except:
                    print(
                        "ERROR: ha habido un error inexperado al borrar de la base de datos"
                    )
                    return False
