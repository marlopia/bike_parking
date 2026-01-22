"""Clase que representa una fila de la base de datos de bicis"""

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from parking.data_utils.validators import es_dni_unico
from parking.models.bd import Bd, Base

bd = Bd()


class Bici(Base):

    __tablename__ = "bicis"

    num_serie: Mapped[str] = mapped_column(String, primary_key=True)
    dni_usuario: Mapped[str] = mapped_column(ForeignKey("usuarios.dni"), nullable=False)
    usuario: Mapped["Usuario"] = relationship("Usuario", back_populates="bicis")  # type: ignore
    marca: Mapped[str] = mapped_column(String, nullable=False)
    modelo: Mapped[str] = mapped_column(String, nullable=False)
    registro: Mapped[list["Registro"]] = relationship("Registro", back_populates="bicis")  # type: ignore

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

    @classmethod
    def obtener_bici(cls, num_serie: str) -> "Bici":
        """
        Devuelve la instancia de la Bici con ese número de serie si existe

        Args:
            num_serie (str): Número de serie de la bici
        Returns:
            Bici: La bici
        Raises:
            BiciError: Si no existe una bici con ese número de serie en la base de datos
        """
        with bd.crear_sesion() as sesion:
            bici_orm = sesion.query(cls).filter_by(num_serie=num_serie).first()
            if bici_orm:
                return bici_orm
            else:
                raise BiciError("Número de serie no encontrado")

    def es_valido(self) -> bool:
        """
        Valida que la bici esté bien formada sin campos vacíos

        Returns:
            bool: True si válida
        """
        for key, value in vars(self).items():
            if value == "":
                return False
        return True

    def existe_usuario(self) -> bool:
        """
        Valida si existe el usuario para asociarle la bici

        Returns:
            bool: True si existe
        """
        if not es_dni_unico(self.dni_usuario):
            return False
        else:
            return True

    def guardar(self) -> None:
        """Guarda la bici en el csv siempre y cuando sea válida, única y tenga un usuario creado"""
        with bd.crear_sesion() as sesion:
            if sesion.query(Bici).filter_by(num_serie=self.num_serie).first():
                raise BiciError("ERROR: el número de serie ya está registrado")
            elif self.es_valido():
                try:
                    sesion.add(self)
                except:
                    raise BiciError(
                        "ERROR: ha habido un error inexperado al escribir en la base de datos"
                    )

    def borrar(self) -> None:
        """Intenta borrar la bici siempre y cuando tenga un número de serie válido"""
        with bd.crear_sesion() as sesion:
            bici = sesion.query(Bici).filter_by(num_serie=self.num_serie).first()
            if bici:
                try:
                    sesion.delete(self)
                except:
                    raise BiciError(
                        "ERROR: ha habido un error inexperado al borrar de la base de datos"
                    )
            else:
                raise BiciError("ERROR: la bicicleta no existe")


class BiciError(Exception):
    """Error genérico de gestión de bici"""

    pass
