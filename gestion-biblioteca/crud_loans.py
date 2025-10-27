from . import gestion_datos
from . import utils as utilidades

def registrar_prestamo():
    """Registra un nuevo préstamo para un usuario y uno o varios libros."""
    print("\n--- Registrar Nuevo Préstamo ---")
    id_usuario = input("ID del Usuario (ej. U001): ").strip().upper()
    
    if not utilidades.validar_id(id_usuario, 'usuario'):
        utilidades.imprimir_error("ID de usuario inválido.")
        return

    # Se piden los IDs de los libros, separados por comas
    ids_libros_str = input("IDs de los libros a prestar, separados por coma (ej. L001,L003): ")
    # .replace(' ', '') quita espacios, .upper() convierte a mayúsculas, .split(',') crea una lista
    ids_libros_list = ids_libros_str.replace(' ', '').upper().split(',')

    libros = gestion_datos.cargar_libros()
    usuarios = gestion_datos.cargar_usuarios()
    
    # --- Validaciones ---
    # 1. Validar que el usuario exista
    if not any(u['ID_Usuario'] == id_usuario for u in usuarios):
        utilidades.imprimir_error(f"El usuario con ID {id_usuario} no existe.")
        return

    # 2. Validar que todos los libros existan y estén disponibles
    libros_a_prestar = []
    error_encontrado = False
    for id_l in ids_libros_list:
        if not error_encontrado:
            libro_encontrado = next(filter(lambda l: l['ID_Libro'] == id_l, libros), None)
            if libro_encontrado is None:
                utilidades.imprimir_error(f"El libro con ID {id_l} no existe.")
                error_encontrado = True
            elif libro_encontrado['Estado'] != 'Disponible':
                utilidades.imprimir_error(f"El libro '{libro_encontrado['Titulo']}' no está disponible.")
                error_encontrado = True
            else:
                libros_a_prestar.append(libro_encontrado)
    
    if error_encontrado:
        return # Termina la función si hubo algún error

    # --- Creación del Préstamo ---
    prestamos = gestion_datos.cargar_prestamos()
    nuevo_id_prestamo = utilidades.generar_nuevo_id(prestamos, 'P')
    
    nuevo_prestamo = {
        "ID_Prestamo": nuevo_id_prestamo,
        "ID_Usuario": id_usuario,
        "ID_Libros": ",".join(ids_libros_list), # Se unen los IDs en un string
        "Fecha_Prestamo": utilidades.obtener_fecha_actual_str(),
        "Fecha_Devolucion_Prevista": utilidades.calcular_fecha_devolucion_str(),
        "Fecha_Devolucion_Real": "null", # Se usa 'null' como string para consistencia
        "Estado_Prestamo": "Activo"
    }

    prestamos.append(nuevo_prestamo)
    
    # --- Actualización de estado de libros ---
    for libro_obj in libros_a_prestar:
        libro_obj['Estado'] = 'Prestado'

    # --- Guardado de datos ---
    try:
        gestion_datos.guardar_prestamos(prestamos)
        gestion_datos.guardar_libros(libros)
        utilidades.imprimir_exito(f"Préstamo {nuevo_id_prestamo} registrado correctamente.")
    except Exception as e:
        utilidades.imprimir_error(str(e))


def modificar_prestamo():
    """Modifica un préstamo para registrar una devolución."""
    print("\n--- Registrar Devolución (Modificar Préstamo) ---")
    id_prestamo = input("ID del Préstamo a modificar (ej. P001): ").strip().upper()

    if not utilidades.validar_id(id_prestamo, 'prestamo'):
        utilidades.imprimir_error("ID de préstamo inválido.")
        return

    prestamos = gestion_datos.cargar_prestamos()
    libros = gestion_datos.cargar_libros()
    
    prestamo_a_modificar = next(filter(lambda p: p['ID_Prestamo'] == id_prestamo, prestamos), None)

    if prestamo_a_modificar is None:
        utilidades.imprimir_error(f"No se encontró el préstamo con ID {id_prestamo}.")
        return
    
    if prestamo_a_modificar['Estado_Prestamo'] == 'Devuelto':
        utilidades.imprimir_advertencia("Este préstamo ya fue devuelto.")
        return

    # --- Actualizar Préstamo ---
    prestamo_a_modificar['Estado_Prestamo'] = 'Devuelto'
    prestamo_a_modificar['Fecha_Devolucion_Real'] = utilidades.obtener_fecha_actual_str()

    # --- Actualizar Libros ---
    ids_libros_devueltos = prestamo_a_modificar['ID_Libros'].split(',')
    for id_l in ids_libros_devueltos:
        libro_obj = next(filter(lambda l: l['ID_Libro'] == id_l, libros), None)
        if libro_obj:
            libro_obj['Estado'] = 'Disponible'
    
    # --- Guardar Cambios ---
    try:
        gestion_datos.guardar_prestamos(prestamos)
        gestion_datos.guardar_libros(libros)
        utilidades.imprimir_exito(f"Devolución para el préstamo {id_prestamo} registrada.")
    except Exception as e:
        utilidades.imprimir_error(str(e))

def ver_prestamos(solo_activos=False):
    """Muestra una lista de todos los préstamos o solo los activos."""
    titulo = "Préstamos Activos" if solo_activos else "Historial de Todos los Préstamos"
    print(f"\n--- {titulo} ---")
    
    prestamos = gestion_datos.cargar_prestamos()
    
    lista_a_mostrar = prestamos
    if solo_activos:
        lista_a_mostrar = list(filter(lambda p: p['Estado_Prestamo'] == 'Activo', prestamos))
    
    if not lista_a_mostrar:
        utilidades.imprimir_advertencia("No hay préstamos para mostrar.")
    else:
        print(f"{'ID Prést.':<11} | {'ID Usuario':<12} | {'IDs Libros':<20} | {'Estado':<10} | {'F. Préstamo':<12} | {'F. Devolución':<12}")
        print("-" * 85)
        for p in lista_a_mostrar:
            print(f"{p['ID_Prestamo']:<11} | {p['ID_Usuario']:<12} | {p['ID_Libros']:<20} | {p['Estado_Prestamo']:<10} | {p['Fecha_Prestamo']:<12} | {p['Fecha_Devolucion_Prevista']:<12}")