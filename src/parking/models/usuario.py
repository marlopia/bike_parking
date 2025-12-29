"""Clase que representa una fila de la base de datos de usuarios"""

from parking.data_utils.validators import (
    es_dni_valido,
    es_email_valido,
)
from parking.models.bd import Bd, BiciORM, UsuarioORM

bd = Bd()


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
        with bd.crear_sesion() as sesion:
            for bici in sesion.query(BiciORM).filter_by(dni_usuario=dni).all():
                self.bicis.append(bici)

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

    def guardar(self) -> bool:
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

    def borrar(self) -> bool:
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
            elif len(self.bicis) is not 0:
                print("ERROR: el usuario tiene bicis asignadas, no se puede borrar")
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
