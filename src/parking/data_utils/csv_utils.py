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
    archivos = [
        (USUARIOS_CSV, CABECERA_USUARIOS),
        (BICIS_CSV, CABECERA_BICIS),
        (REGISTROS_CSV, CABECERA_REGISTROS),
    ]

    for path, cabecera in archivos:
        crear = False
        if not os.path.exists(path):
            crear = True
        else:
            with open(path, "r", encoding="utf-8") as f:
                primera_linea = f.readline()
            if primera_linea != cabecera + "\n":
                os.remove(path)
                crear = True

        if crear:
            with open(path, "w", encoding="utf-8") as f:
                f.write(cabecera + "\n")


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


def borrar_filas(csv_path: str, columna: str, valor: str) -> None:
    """
    Reescribe el fichero csv por completo omitiendo las filas que tengan una columna con valor coincidente

    Args:
        csv_path (str): Ruta al archivo csv
        columna (str): Nombre de la columna a buscar
        valor (str): Valor de la columna objetivo de las filas a borrar
    """
    filas_keep = []

    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row[columna] != valor:
                filas_keep.append(row)

    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        fieldnames = reader.fieldnames or []
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(filas_keep)
