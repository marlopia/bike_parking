"""Clase que representa una fila de la base de datos de usuarios y su lógica"""

from typing import List
from sqlalchemy.orm import Mapped, mapped_column
from parking.data_utils.validators import es_dni_valido, es_email_valido
from parking.models.bd import Bd, BiciORM, Base

bd = Bd()


class Usuario(Base):
    __tablename__ = "usuarios"

    dni: Mapped[str] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(unique=True, nullable=False)
    bicis: List = []

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
        self.bicis = []
        # Cargar bicis desde la BD
        with bd.crear_sesion() as sesion:
            bicis_orm = sesion.query(BiciORM).filter_by(dni_usuario=dni).all()
            self.bicis = [bici.toJSON() for bici in bicis_orm]

    @classmethod
    def obtener_o_crear(cls, dni: str, nombre: str = "", email: str = "") -> "Usuario":
        """
        Devuelve la instancia del Usuario con ese DNI si existe,
        sino crea una nueva.

        Args:
            dni (str): DNI del usuario, tiene que ser único
            nombre (str, optional): Nombre del usuario. Por defecto vacío.
            email (str, optional): Email del usuario, tiene que ser único. Por defecto vacío.
        Returns:
            Usuario: El usuario
        """
        with bd.crear_sesion() as sesion:
            usuario_orm = sesion.query(cls).filter_by(dni=dni).first()
            if usuario_orm:
                usuario = cls(
                    dni=usuario_orm.dni,
                    nombre=usuario_orm.nombre,
                    email=usuario_orm.email,
                )
                return usuario
            else:
                usuario = cls(dni=dni, nombre=nombre, email=email)
                return usuario

    def es_valido(self) -> bool:
        """
        Valida que el usuario esté bien formado sin campos vacíos y con dni e email válidos

        Returns:
            bool: True si valido.
        """
        if not es_dni_valido(self.dni):
            print("ERROR: el DNI introducido no es válido")
            return False
        if not es_email_valido(self.email):
            print("ERROR: el email introducido no es válido")
            return False
        return True

    def guardar(self) -> bool:
        """
        Guarda el usuario en la base de datos siempre y cuando sea válido y único

        Returns:
            bool: True si se ha guardado el usuario
        """
        if not self.es_valido():
            return False

        with bd.crear_sesion() as sesion:
            # Comprobar unicidad
            if sesion.query(Usuario).filter_by(dni=self.dni).first():
                print("ERROR: el DNI introducido ya está registrado")
                return False
            if sesion.query(Usuario).filter_by(email=self.email).first():
                print("ERROR: el email introducido ya está registrado")
                return False
            try:
                sesion.add(self)
                print("OK: se ha registrado el usuario")
                return True
            except Exception as e:
                print(
                    f"ERROR: ha habido un error inesperado al escribir en la base de datos: {e}"
                )
                return False

    def borrar(self) -> bool:
        """
        Intenta borrar el usuario siempre y cuando ya exista el DNI y no tenga bicis asociadas

        Returns:
            bool: True si se ha borrado el usuario
        """
        if len(self.bicis) != 0:
            print("ERROR: el usuario tiene bicis asignadas, no se puede borrar")
            return False

        with bd.crear_sesion() as sesion:
            usuario = sesion.query(Usuario).filter_by(dni=self.dni).first()
            if not usuario:
                print("ERROR: el DNI no existe o está mal escrito")
                return False
            try:
                sesion.delete(usuario)
                print("OK: usuario borrado")
                return True
            except Exception as e:
                print(
                    f"ERROR: ha habido un error inesperado al borrar de la base de datos: {e}"
                )
                return False
