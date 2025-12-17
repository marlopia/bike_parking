"""Objeto para gestionar la conexión a la base de datos"""

from contextlib import contextmanager
from sqlalchemy import ForeignKey, create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()


# ====== MODELOS ORM ======
class UsuarioORM(Base):
    __tablename__ = "usuarios"
    dni = Column(String, primary_key=True)
    nombre = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)


class BiciORM(Base):
    __tablename__ = "bicis"
    num_serie = Column(String, primary_key=True)
    dni_usuario = Column(String, ForeignKey("usuarios.dni"), nullable=False)
    marca = Column(String, nullable=False)
    modelo = Column(String, nullable=False)


class RegistroORM(Base):
    __tablename__ = "registros"
    timestamp = Column(String, primary_key=True)
    accion = Column(String)
    num_serie = Column(String, ForeignKey("bicis.num_serie"), nullable=False)
    dni_usuario = Column(String, ForeignKey("usuarios.dni"), nullable=False)


# ====== BD MANAGER ======
class Bd:
    def __init__(self, db_file="bd.db"):
        self.engine = create_engine(f"sqlite:///{db_file}", echo=False)
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)

    @contextmanager
    def crear_sesion(self):
        session = self.Session()
        try:
            yield session
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()
