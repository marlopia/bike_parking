"""Objeto para gestionar la conexión a la base de datos"""

from contextlib import contextmanager
from sqlalchemy import ForeignKey, create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()

DB_NAME = "data/bd.db"


# ====== MODELOS ORM ======
class UsuarioORM(Base):
    __tablename__ = "usuarios"
    dni = Column(String, primary_key=True)
    nombre = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)

    def __init__(self, dni: str, nombre: str, email: str):
        self.dni = dni
        self.nombre = nombre
        self.email = email


class BiciORM(Base):
    __tablename__ = "bicis"
    num_serie = Column(String, primary_key=True)
    dni_usuario = Column(String, ForeignKey("usuarios.dni"), nullable=False)
    marca = Column(String, nullable=False)
    modelo = Column(String, nullable=False)

    def __init__(self, num_serie: str, dni_usuario: str, marca: str, modelo: str):
        self.num_serie = num_serie
        self.dni_usuario = dni_usuario
        self.marca = marca
        self.modelo = modelo


class RegistroORM(Base):
    __tablename__ = "registros"
    timestamp = Column(String, primary_key=True)
    accion = Column(String)
    num_serie = Column(String, ForeignKey("bicis.num_serie"), nullable=False)
    dni_usuario = Column(String, ForeignKey("usuarios.dni"), nullable=False)

    def __init__(self, timestamp: str, accion: str, num_serie: str, dni_usuario: str):
        self.timestamp = timestamp
        self.accion = accion
        self.num_serie = num_serie
        self.dni_usuario = dni_usuario


# ====== BD MANAGER ======
class Bd:
    _instance = None

    def __new__(cls, db_file=DB_NAME):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._init(db_file)
        return cls._instance

    def _init(self, db_file=DB_NAME):
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
