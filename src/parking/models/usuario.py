"""Clase que representa una fila de la base de datos de usuarios y su lógica"""

from typing import List
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from parking.data_utils.validators import es_dni_valido, es_email_valido
from parking.models.bd import Bd, Base
from parking.models.bici import Bici

bd = Bd()


class Usuario(Base):
    __tablename__ = "usuarios"

    dni: Mapped[str] = mapped_column(String, primary_key=True)
    nombre: Mapped[str] = mapped_column(String, nullable=False)
    email: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    bicis: Mapped[list[Bici]] = relationship("Bici", back_populates="usuario")

    def __init__(self, dni: str, nombre: str = "", email: str = "") -> None:
        """
        Devuelve una instancia de Usuario.

        Args:
            dni (str): DNI del usuario, tiene que ser único
            nombre (str, optional): Nombre del usuario. Por defecto vacío.
            email (str, optional): Email del usuario, tiene que ser único. Por defecto vacío.
        Returns:
            Usuario: El usuario
        """
        self.dni = dni
        self.nombre = nombre
        self.email = email

    @classmethod
    def obtener_usuario(cls, dni: str) -> "Usuario":
        """
        Devuelve la instancia del Usuario con ese DNI si existe

        Args:
            dni (str): DNI del usuario
        Returns:
            Usuario: El usuario

        Raises:
            UsuarioError: Si no existe un Usuario con ese DNI en la base de datos
        """
        with bd.crear_sesion() as sesion:
            usuario_orm = sesion.query(cls).filter_by(dni=dni).first()
            if usuario_orm:
                return usuario_orm
            else:
                raise UsuarioError("DNI no encontrado")

    def es_valido(self) -> bool:
        """
        Valida que el usuario esté bien formado sin campos vacíos y con dni e email válidos

        Returns:
            bool: True si valido.
        """
        if not es_dni_valido(self.dni):
            return False
        if not es_email_valido(self.email):
            return False
        return True

    def guardar(self) -> None:
        """Guarda el usuario en la base de datos siempre y cuando sea válido y único"""
        if not self.es_valido():
            raise UsuarioError("ERROR: El usuario no es válido")

        with bd.crear_sesion() as sesion:
            # Comprobar unicidad
            if sesion.query(Usuario).filter_by(dni=self.dni).first():
                raise UsuarioError("ERROR: El DNI introducido ya está registrado")
            if sesion.query(Usuario).filter_by(email=self.email).first():
                raise UsuarioError("ERROR: El email introducido ya está registrado")
            try:
                sesion.add(self)
            except Exception as e:
                raise UsuarioError(
                    f"ERROR: ha habido un error inesperado al escribir en la base de datos: {e}"
                )

    def borrar(self) -> None:
        """Intenta borrar el usuario siempre y cuando ya exista el DNI y no tenga bicis asociadas"""
        if len(self.bicis) != 0:
            raise UsuarioError(
                "ERROR: El usuario tiene bicicletas asociadas, no se puede borrar"
            )

        with bd.crear_sesion() as sesion:
            usuario = sesion.query(Usuario).filter_by(dni=self.dni).first()
            if not usuario:
                raise UsuarioError("ERROR: El DNI no existe en la base de datos")
            try:
                sesion.delete(usuario)
            except Exception as e:
                raise UsuarioError(
                    f"ERROR: ha habido un error inesperado al borrar de la base de datos: {e}"
                )


class UsuarioError(Exception):
    """Error genérico de gestión de usuario"""

    pass
