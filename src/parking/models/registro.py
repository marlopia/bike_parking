"""Clase que representa una fila de la base de datos de bicis"""

from datetime import datetime
from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app import db
from parking.models.usuario import Usuario
from parking.data_utils.validators import (
    puede_entrar,
    puede_salir,
    es_dni_unico,
    es_serie_unica,
)
from ..config import TIMESTAMP_FMT


class Registro(db.Model):

    __tablename__ = "registros"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    timestamp: Mapped[str] = mapped_column(String, nullable=False)
    accion: Mapped[str] = mapped_column(String, nullable=False)

    num_serie: Mapped[str] = mapped_column(
        String, ForeignKey("bicis.num_serie"), nullable=False
    )
    dni_usuario: Mapped[str] = mapped_column(
        String, ForeignKey("usuarios.dni"), nullable=False
    )

    bici: Mapped["Bici"] = relationship("Bici")  # type: ignore
    usuario: Mapped["Usuario"] = relationship("Usuario")

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

    @classmethod
    def obtener_registro(cls, id: int) -> "Registro":
        """
        Devuelve la instancia del Registro según un ID interno

        Args:
            id (int): ID interno del registro
        Returns:
            Registro: El registro
        Raises:
            RegistroError: Si no existe un registro con ese ID en la base de datos
        """
        registro_orm = cls.query.filter_by(id=id).first()
        if registro_orm:
            return registro_orm
        else:
            raise RegistroError("ID no encontrado")

    def es_valido(self) -> bool:
        """
        Valida que el registro esté bien formado sin campos vacíos y con un usuario y bici existentes

        Returns:
            bool: True si valido.
        """
        for key, value in vars(self).items():
            if value == "":
                return False
        if es_dni_unico(self.dni_usuario):
            return False
        elif es_serie_unica(self.num_serie):
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
                return False
            else:
                return True
        elif self.accion == "OUT":
            if not puede_salir(self.num_serie):
                return False
            else:
                return True
        else:
            return False

    def guardar(self) -> None:
        """Guarda el registro en la base de datos siempre y cuando sea válido y tenga un usuario y bici creados"""

        if self.es_valido() and self.es_permitido():
            usuario = Usuario.obtener_usuario(self.dni_usuario)
            if not any(bici.num_serie == self.num_serie for bici in usuario.bicis):
                raise RegistroError("ERROR: esta bicicleta NO pertenece al usuario")
            else:
                try:
                    db.session.add(self)
                    db.session.commit()
                except:
                    db.session.rollback()
                    raise RegistroError(
                        "ERROR: ha habido un error inexperado al escribir en la base de datos"
                    )


class RegistroError(Exception):
    """Error genérico de gestión de registro"""

    pass
