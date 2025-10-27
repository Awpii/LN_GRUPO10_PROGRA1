import json

# Definición de rutas a los archivos de datos
RUTA_LIBROS = 'data/books.json'
RUTA_USUARIOS = 'data/users.json'
RUTA_PRESTAMOS = 'data/loans.txt'

# --- Funciones Genéricas para JSON ---
def cargar_json(ruta):
    """Carga datos desde un archivo JSON. Usa try/except para manejar errores."""
    try:
        with open(ruta, 'r', encoding='utf-8') as archivo:
            # json.load() deserializa un archivo JSON a un objeto Python
            return json.load(archivo)
    except FileNotFoundError:
        # Se retorna una matriz (lista) vacía si el archivo no existe
        return []
    except json.JSONDecodeError:
        # Se maneja el caso de un JSON vacío o corrupto
        return []

def guardar_json(ruta, datos):
    """Guarda una lista de diccionarios en un archivo JSON."""
    try:
        with open(ruta, 'w', encoding='utf-8') as archivo:
            # json.dump() serializa un objeto Python a un archivo JSON
            # indent=2 para formato legible, ensure_ascii=False para caracteres como tildes
            json.dump(datos, archivo, indent=2, ensure_ascii=False)
            return True
    except IOError:
        return False

# --- Funciones Específicas para cada tipo de dato ---
def cargar_libros():
    return cargar_json(RUTA_LIBROS)

def guardar_libros(libros):
    return guardar_json(RUTA_LIBROS, libros)

def cargar_usuarios():
    return cargar_json(RUTA_USUARIOS)

def guardar_usuarios(usuarios):
    return guardar_json(RUTA_USUARIOS, usuarios)

def cargar_prestamos():
    """
    Lee el archivo loans.txt y lo convierte en una matriz de diccionarios.
    Cada línea del archivo es un préstamo.
    """
    matriz_prestamos = []
    try:
        with open(RUTA_PRESTAMOS, 'r', encoding='utf-8') as archivo:
            # .readlines() lee todas las líneas y las devuelve como una lista de strings
            lineas = archivo.readlines()
            
            # Se usa un diccionario para mapear los índices a las claves
            claves = ("ID_Prestamo", "ID_Usuario", "ID_Libros", "Fecha_Prestamo", 
                    "Fecha_Devolucion_Prevista", "Fecha_Devolucion_Real", "Estado_Prestamo")

            # Se usa map y lambda para procesar cada línea
            matriz_prestamos = list(map(
                lambda linea: dict(zip(claves, linea.strip().split('|'))),
                lineas
            ))
    except FileNotFoundError:
        pass # Si el archivo no existe, simplemente se retorna una lista vacía
    return matriz_prestamos


def guardar_prestamos(matriz_prestamos):
    """
    Convierte una matriz de diccionarios de préstamos a formato de texto y lo guarda en .txt.
    """
    lineas_a_escribir = []
    # Itera sobre la matriz de diccionarios de préstamos
    for prestamo_dict in matriz_prestamos:
        # .values() obtiene los valores del diccionario en orden
        # Se usa map para asegurar que todos los valores sean strings
        valores = list(map(str, prestamo_dict.values()))
        # .join() une los elementos de la lista en un solo string con el separador '|'
        linea = "|".join(valores)
        lineas_a_escribir.append(linea + "\n")
    
    try:
        # Se abre el archivo en modo escritura ('w') para sobreescribirlo completamente
        with open(RUTA_PRESTAMOS, 'w', encoding='utf-8') as archivo:
            # .writelines() escribe una lista de strings en el archivo
            archivo.writelines(lineas_a_escribir)
    except IOError as e:
        # Se levanta una excepción si hay un error de escritura
        raise Exception(f"No se pudo guardar el archivo de préstamos: {e}")