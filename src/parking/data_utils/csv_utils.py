"""Utilidad para cargar y escribir información en csv"""

import csv
import os

from ..config import (
    USUARIOS_CSV,
    BICIS_CSV,
    REGISTROS_CSV,
    CABECERA_USUARIOS,
    CABECERA_BICIS,
    CABECERA_REGISTROS,
)


def asegurar_csvs() -> None:
    """
    Comprueba que existan los archivos csv con sus cabeceras en las rutas necesarias,
    si están malformados los borra y genera unos limpios,
    si no existen crea los archivos con sus cabeceras.
    """
    if not os.path.exists(USUARIOS_CSV):
        with open(USUARIOS_CSV, "w") as f:
            f.write(CABECERA_USUARIOS)
    elif _extraer_cabecera(USUARIOS_CSV) != CABECERA_USUARIOS:
        os.remove(USUARIOS_CSV)
        with open(USUARIOS_CSV, "w") as f:
            f.write(CABECERA_USUARIOS)

    if not os.path.exists(BICIS_CSV):
        with open(BICIS_CSV, "w") as f:
            f.write(CABECERA_BICIS)
    elif _extraer_cabecera(BICIS_CSV) != CABECERA_BICIS:
        os.remove(BICIS_CSV)
        with open(BICIS_CSV, "w") as f:
            f.write(CABECERA_BICIS)

    if not os.path.exists(REGISTROS_CSV):
        with open(REGISTROS_CSV, "w") as f:
            f.write(CABECERA_REGISTROS)
    elif _extraer_cabecera(REGISTROS_CSV) != CABECERA_REGISTROS:
        os.remove(REGISTROS_CSV)
        with open(REGISTROS_CSV, "w") as f:
            f.write(CABECERA_REGISTROS)


def _extraer_cabecera(path: str) -> str:
    """
    Método auxiliar para extraer la cabecera en texto plano de un csv

    Args:
        path (str): Ruta al csv

    Returns:
        str: La cabecera del csv sin alterar
    """
    with open(path, "r", encoding="utf-8") as f:
        return f.readline().strip()


def leer_csv_dic(path: str) -> list[dict[str, str]]:
    """
    Lee filas de un archivo csv dado por un path y devuelve una lista de diccionarios,
    un diccionario por fila con sus claves de la cabecera y valor de la columna.

    Args:
        path (str): Path al fichero .csv

    Returns:
        list[dict[str, str]]: Una lista con diccionarios por cada fila
    """
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        filas = list(reader)
        return filas


def escribir_csv_dic(path: str, filas: list[dict[str, str]]) -> None:
    """
    Escribe filas en el csv de la ruta dada,
    si no coinciden las claves se ignora y si las claves van vacías se rellena con ''

    Args:
        path (str): Ruta al csv
        filas (list[dict[str, str]]): Lista de diccionarios (diccionario por fila) con clave valor estilo
            [{cabecera:valor,cabecera:valor},{cabecera:valor,cabecera:valor}]
    """
    if not filas:
        return

    with open(path, mode="a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=filas[0].keys())
        writer.writerows(filas)
