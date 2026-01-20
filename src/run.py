"""Entrypoint de la aplicación, archivo a ejecutar como main"""

from app import create_app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
