import re
from datetime import datetime, timedelta

#REGEX para validacion
REGEX_ID_LIBRO = re.compile(r'^L\d{3}$')
REGEX_ID_USUARIO = re.compile(r'^U\d{3}$')
REGEX_ID_PRESTAMO = re.compile(r'^P\d{3}$')

def validar_id(id_str, type):
    #Valida id segun tipo (libro, user, prestamo)
    regex_map = {
        "Book": REGEX_ID_LIBRO,
        "User": REGEX_ID_USUARIO,
        "Loan": REGEX_ID_PRESTAMO
    }
    regex = regex_map.get(type)
    assert regex is not None, "Tipo de ID inválido."
    return regex.match(id_str)

def generar_nuevo_id(list_of_dicts, prefix):
    #Genera ID incremental, prefijo DEBE ser L, U o P.
    if not list_of_dicts:
        return f"{prefix}001"
    
    #lambda extrae numero de id, convierte a int y encuentra max
    max_id_num = max(map(lambda item: int(item[f'ID_{prefix.capitalize()}'].lstrip(prefix)), list_of_dicts))
    new_id_num = max_id_num + 1
    return f"{prefix}{str(new_id_num).zfill(3)}" #zfill añade 0s a la izq

def obtener_fecha_actual():
    #devuelve fecha actual como DD/MM/YYYY
    return datetime.now().strftime('%d/%m/%Y')

def calc_fecha_devol(days = 15):
    #Calcula fecha de devolucion sumando dias a fecha actual
    return_date = datetime.now() + timedelta(days=days)
    return return_date.strftime('%d/%m/%Y')