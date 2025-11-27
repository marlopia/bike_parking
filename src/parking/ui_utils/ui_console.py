"""Archivo que gestiona los menús y visuales de la aplicación"""

import os
import platform
from typing import Optional
from parking.config import OPCIONES
from parking.ui_utils.menu_handlers import (
    menu_anadir_bici,
    menu_anadir_usuario,
    menu_borrar_bici,
    menu_borrar_usuario,
    preguntar_bool,
    registro_entrada,
    registro_salida,
)


def render_menu(titulo: str, opciones: Optional[list[str]] = None) -> int:
    """
    Imprime la cabecera de la aplicación con el titulo centrado y una lista de opciones.
    Luego solicita al usuario un valor numérico que corresponda a las opciones y lo devuelve.
    Por defecto imprime una cabecera de 50 caracteres de ancho, pero si el titulo es más
    largo la extenderá.

    Args:
        titulo (str): Titulo para la cabecera
        opciones Optional[list[str]]: Lista de nombres de opciones,
            si no se usa esta función solo muestra el título y devolverá 0

    Returns:
        int: Posición de la lista con íncide 1 de la opción seleccionada, si se cancela devuelve 0
    """

    chars = 50
    if len(titulo) > 50:
        chars = len(titulo) + 6  # Padding de 2 chars a cada lado
    print("#" * chars)
    print("#" + " " * (chars - 2) + "#")
    print("#" + titulo.center((chars - 2), " ") + "#")
    print("#" + " " * (chars - 2) + "#")
    print("#" * chars)

    eleccion = "0"

    if opciones:
        for num, opcion in enumerate(opciones, start=1):
            print(str(num) + ": " + opcion)

        eleccion = input("Elige una opción de las de arriba: ")

        while not (eleccion.isnumeric() and 0 < int(eleccion) <= len(opciones)):
            if not preguntar_bool(
                "Respuesta no reconocida. Intentarlo de nuevo? (S/N): "
            ):
                return 0
            eleccion = input("Elige una opción de las de arriba: ")

    return int(eleccion)


def clear_screen() -> None:
    """Comprueba el sistema operativo del usuario y limpia la consola"""
    cmd = ""
    if platform.system() == "Windows":
        cmd = "cls"
    else:
        cmd = "clear"
    os.system(cmd)


def manage_options(eleccion: int) -> bool:
    """
    Maneja la opción elegida por render_menu()

    Args:
        eleccion (int): Número de la elección

    Returns:
        bool: True si se realiza la operación, False si no o
    """
    if eleccion < 0 or eleccion > len(OPCIONES):
        print("ERROR: Opción no válida")
        return False

    clear_screen()

    render_menu(OPCIONES[eleccion - 1])
    if eleccion == 1:
        return menu_anadir_usuario()
    elif eleccion == 2:
        return menu_borrar_usuario()
    elif eleccion == 3:
        return menu_anadir_bici()
    elif eleccion == 4:
        return menu_borrar_bici()
    elif eleccion == 5:
        return registro_entrada()
    elif eleccion == 6:
        return registro_salida()
    else:  # eleccion == 7
        return exit_app()


def exit_app():
    # TODO manejar en app.py
    raise NotImplementedError
