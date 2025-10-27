import re
from datetime import datetime, timedelta
from colorama import Fore, Style

# --- Expresiones Regulares Pre-compiladas para eficiencia ---
# re.compile() crea un objeto Regex para reutilizar el patrón
# ^: inicio de la cadena, \d{3}: exactamente 3 dígitos, $: fin de la cadena
REGEX_ID_LIBRO = re.compile(r'^L\d{3}$')
REGEX_ID_USUARIO = re.compile(r'^U\d{3}$')
REGEX_ID_PRESTAMO = re.compile(r'^P\d{3}$')

def validar_id(id_str, tipo):
    """Valida un ID usando la expresión regular correspondiente."""
    # assert se usa para comprobar una condición que debe ser siempre verdadera
    assert tipo in ('libro', 'usuario', 'prestamo'), "Tipo de ID no válido"
    
    if tipo == 'libro':
        # .match() intenta hacer coincidir el patrón desde el inicio del string
        return REGEX_ID_LIBRO.match(id_str)
    if tipo == 'usuario':
        return REGEX_ID_USUARIO.match(id_str)
    if tipo == 'prestamo':
        return REGEX_ID_PRESTAMO.match(id_str)

def generar_nuevo_id(lista_de_dicts, prefijo):
    """Genera un nuevo ID autoincremental (ej. L007 -> L008)."""
    if not lista_de_dicts:
        # zfill(3) rellena con ceros a la izquierda hasta tener 3 dígitos
        return f"{prefijo}{'1'.zfill(3)}"
    
    # Se define la clave del diccionario a buscar usando f-strings
    clave_id = f'ID_{"Libro" if prefijo == "L" else "Usuario" if prefijo == "U" else "Prestamo"}'
    
    # Se usa map y lambda para extraer los números de los IDs
    numeros = list(map(lambda item: int(item[clave_id].lstrip(prefijo)), lista_de_dicts))
    
    # max() encuentra el número más alto, se le suma 1
    nuevo_numero = max(numeros) + 1
    return f"{prefijo}{str(nuevo_numero).zfill(3)}"

def obtener_fecha_actual_str():
    """Retorna la fecha actual como string en formato dd/mm/YYYY."""
    # datetime.now() obtiene la fecha y hora actual
    # .strftime() formatea el objeto datetime a un string
    return datetime.now().strftime('%d/%m/%Y')

def calcular_fecha_devolucion_str(dias=15):
    """Calcula la fecha de devolución sumando días a la fecha actual."""
    # timedelta representa una duración de tiempo
    fecha_devolucion = datetime.now() + timedelta(days=dias)
    return fecha_devolucion.strftime('%d/%m/%Y')

# --- Funciones de Interfaz de Usuario con Colorama ---
def imprimir_error(mensaje):
    print(f"{Fore.RED}[ERROR] {mensaje}{Style.RESET_ALL}")

def imprimir_exito(mensaje):
    print(f"{Fore.GREEN}[ÉXITO] {mensaje}{Style.RESET_ALL}")

def imprimir_advertencia(mensaje):
    print(f"{Fore.YELLOW}[AVISO] {mensaje}{Style.RESET_ALL}")