"""Archivo de constantes globales para el resto de módulos"""

DATA_DIR = "data"
TESTS_DIR = "tests"

USUARIOS_CSV = f"{DATA_DIR}/usuarios.csv"
CABECERA_USUARIOS = "dni,nombre,email"
BICIS_CSV = f"{DATA_DIR}/bicis.csv"
CABECERA_BICIS = "num_serie,dni_usuario,marca,modelo"
REGISTROS_CSV = f"{DATA_DIR}/registros.csv"
CABECERA_REGISTROS = "timestamp,accion,num_serie,dni_usuario"

TIMESTAMP_FMT = "%Y-%m-%d %H:%M:%S"
