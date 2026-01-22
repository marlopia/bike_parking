"""Inicializador del paquete app de Flask, devuelve la app"""

from pathlib import Path
from flask import Flask
from dotenv import load_dotenv
import os
from flask_sqlalchemy import SQLAlchemy

load_dotenv()

db = SQLAlchemy()


def create_app():
    """Crea la app de Flask y carga tanto la clave de sesión como la base de datos"""
    app = Flask(__name__)

    from .routes import main
    from parking.models.usuario import Usuario
    from parking.models.bici import Bici
    from parking.models.registro import Registro

    app.secret_key = os.getenv("SECRET_KEY")

    BASE_DIR = Path(__file__).resolve().parent.parent.parent
    DB_NAME = BASE_DIR / "data" / "bd.db"
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DB_NAME}"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)

    app.register_blueprint(main)

    with app.app_context():
        db.create_all()

    return app
