"""Objeto para gestionar la conexión a la base de datos"""

from contextlib import contextmanager
from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()

BASE_DIR = Path(__file__).resolve().parent.parent.parent
DB_NAME = BASE_DIR / "data" / "bd.db"

DB_NAME = "data/bd.db"


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
