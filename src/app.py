"""Archivo principal de la aplicación, controla el ciclo de vida"""

from parking.data_utils.csv_utils import asegurar_csvs
from parking.config import OPCIONES, TITULO
from parking.ui_utils.ui_console import clear_screen, manage_options, pause, render_menu


if __name__ == "__main__":
    asegurar_csvs()

    eleccion = render_menu(TITULO, OPCIONES)

    while 0 < eleccion and eleccion < len(OPCIONES):
        if manage_options(eleccion):
            pause()
        clear_screen()
        eleccion = render_menu(TITULO, OPCIONES)

    print("Hasta pronto!")
