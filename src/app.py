"""Archivo principal de la aplicación, controla el ciclo de vida"""

# los comentarios de pragma son para que pytest-cov no cuente el modulo
from parking.config import OPCIONES, TITULO  # pragma: no cover
from parking.ui_utils.ui_console import (
    clear_screen,
    manage_options,
    pause,
    render_menu,
)  # pragma: no cover


if __name__ == "__main__":  # pragma: no cover

    eleccion = render_menu(TITULO, OPCIONES)

    while 0 < eleccion and eleccion < len(OPCIONES):
        if manage_options(eleccion):
            pause()
        clear_screen()
        eleccion = render_menu(TITULO, OPCIONES)

    print("Hasta pronto!")
