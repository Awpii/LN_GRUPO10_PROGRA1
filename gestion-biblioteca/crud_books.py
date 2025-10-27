from . import gestion_datos
from . import utils as utilidades

def registrar_libro():
    """Pide datos y crea un nuevo libro en books.json."""
    print("\n--- Registro de Nuevo Libro ---")
    titulo = input("Título: ").strip().title()
    autor = input("Autor: ").strip().title()

    if not titulo or not autor:
        utilidades.imprimir_error("Título y autor son obligatorios.")
        return

    libros = gestion_datos.cargar_libros()
    nuevo_id = utilidades.generar_nuevo_id(libros, 'L')
    
    nuevo_libro = {
        "ID_Libro": nuevo_id,
        "Titulo": titulo,
        "Autor": autor,
        "Estado": "Disponible",
        "Fecha_Ingreso": utilidades.obtener_fecha_actual_str()
    }
    
    libros.append(nuevo_libro)
    if gestion_datos.guardar_libros(libros):
        utilidades.imprimir_exito(f"Libro '{titulo}' registrado con ID: {nuevo_id}")

def eliminar_libro():
    """Elimina un libro por su ID, verificando que no esté en un préstamo activo."""
    print("\n--- Eliminar Libro ---")
    id_libro = input("Ingrese el ID del libro a eliminar (ej. L001): ").strip().upper()

    if not utilidades.validar_id(id_libro, 'libro'):
        utilidades.imprimir_error("Formato de ID inválido.")
        return

    prestamos = gestion_datos.cargar_prestamos()
    # Se busca si el ID del libro está en la lista de libros de algún préstamo activo
    prestamo_activo_encontrado = False
    for p in prestamos:
        # Se comprueba la pertenencia con el operador 'in'
        if p['Estado_Prestamo'] == 'Activo' and id_libro in p['ID_Libros']:
            prestamo_activo_encontrado = True
    
    if prestamo_activo_encontrado:
        utilidades.imprimir_error(f"No se puede eliminar el libro {id_libro}, está en un préstamo activo.")
        return

    libros = gestion_datos.cargar_libros()
    longitud_inicial = len(libros)
    libros_actualizados = list(filter(lambda l: l['ID_Libro'] != id_libro, libros))

    if len(libros_actualizados) == longitud_inicial:
        utilidades.imprimir_error(f"No se encontró un libro con el ID {id_libro}.")
    else:
        if gestion_datos.guardar_libros(libros_actualizados):
            utilidades.imprimir_exito(f"Libro con ID {id_libro} eliminado correctamente.")

def ver_libros():
    """Muestra una lista formateada de todos los libros."""
    print("\n--- Inventario de Libros ---")
    libros = gestion_datos.cargar_libros()
    if not libros:
        utilidades.imprimir_advertencia("No hay libros en el inventario.")
    else:
        print(f"{'ID':<7} | {'Título':<40} | {'Autor':<25} | {'Estado':<12}")
        print("-" * 90)
        for l in libros:
            print(f"{l['ID_Libro']:<7} | {l['Titulo']:<40} | {l['Autor']:<25} | {l['Estado']:<12}")