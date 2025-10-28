from . import gestion_datos
from . import utils as utilidades

def registrar_prestamo():
    #Registrar prestamo nuevo con usuario de uno o varios libros
    print("\n--- Registrar nuevo préstamo ---")
    id_usuario = input("Ingrese el ID del usuario (ej. U001): ").strip().upper()
    
    if utilidades.validar_id(id_usuario, 'usuario'):
        ids_libro_str = input("Ingrese los IDs de los libros a prestar (separados por comas, ej. L001,L002): ").strip().upper()
        ids_libros_list = ids_libro_str.replace(' ', '').split(',')
        
        libros = gestion_datos.cargar_libros()
        usuarios = gestion_datos.cargar_usuarios()
        
        if any(u['ID_Usuario'] == id_usuario for u in usuarios):
            libros_a_prestar = []
            error_encontrado = False
            
            for id_l in ids_libros_list:
                if not error_encontrado:
                    libro_encontrado = next(filter(lambda l: l['ID_Libro'] == id_l, libros), None)
                    if libro_encontrado is None:
                        utilidades.imprimir_error(f"El libro con ID {id_l} no existe.")
                        error_encontrado = True
                    elif libro_encontrado['Estado'] != 'Disponible':
                        utilidades.imprimir_error(f"El libro con ID {id_l} no está disponible para préstamo.")
                        error_encontrado = True
                    else:
                        libros_a_prestar.append(libro_encontrado)
            
            if not error_encontrado:
                #Crear prestamo
                prestamos = gestion_datos.cargar_prestamos()
                nuevo_id_prestamo = utilidades.generar_nuevo_id(prestamos, 'P')
                nuevo_prestamo = {
                    "ID_Prestamo": nuevo_id_prestamo,
                    "ID_Libros": ",".join(ids_libros_list),
                    "Fecha_Prestamo": utilidades.obtener_fecha_actual_str(),
                    "Fecha_Devolucion_Prevista": utilidades.calcular_fecha_devolucion_str(),
                    "Fecha_Devolucion_Real": "null", "Estado_Prestamo": "Activo"
                }
                prestamos.append(nuevo_prestamo)
                for libro_obj in libros_a_prestar:
                    libro_obj['Estado'] = 'Prestado'
                try:
                    gestion_datos.guardar_prestamos(prestamos)
                    gestion_datos.guardar_libros(libros)
                    utilidades.imprimir_exito(f"Prestamo {nuevo_id_prestamo} registrado con éxito.")
                except Exception as e:
                    utilidades.imprimir_error(str(e))
            else:
                utilidades.imprimir_error(f"El usuario con ID {id_usuario} no existe.")
        else:
            utilidades.imprimir_error("ID de usuario inválido.")
            
def modificar_prestamo():
    #Modifica prestamos para registrar devoluciones
    print("\n--- Modificar prestamo ---")
    id_prestamo = input("Ingrees el ID del prestamo a modificar (ej. P001): ").strip().upper()
    if utilidades.validar_id(id_prestamo, 'prestamo'):
        prestamos = gestion_datos.cargar_prestamos()
        libros = gestion_datos.cargar_libros()
        prestamo_a_modificar = next(filter(lambda p: p['ID_Prestamo'] == id_prestamo, prestamos), None)
        
        if prestamo_a_modificar:
            if prestamo_a_modificar['Estado_Prestamo'] != 'Devuelto':
                #Actualizar prestamo, liros
                prestamo_a_modificar['Estado_Prestamo'] = 'Devuelto'
                prestamo_a_modificar['Fecha_Devolucion_Real'] = utilidades.obtener_fecha_actual_str()
                ids_libros_devueltos = prestamo_a_modificar['ID_Libros'].split(',')
                for id_l in ids_libros_devueltos:
                    libro_obj = next(filter(lambda l: l['ID_Libro'] == id_l, libros), None)
                    if libro_obj:
                        libro_obj['Estado'] = 'Disponible'
                try:
                    gestion_datos.guardar_prestamos(prestamos)
                    gestion_datos.guardar_libros(libros)
                    utilidades.imprimir_exito(f"Devolución para el prestamo {id_prestamo} registrada con éxito, el libro se marcara como disponible.")
                except Exception as e:
                    utilidades.imprimir_error(str(e))
            else:
                utilidades.imprimir_advertencia("Este préstamo ya ha sido devuelto.")
        else:
            utilidades.imprimir_error(f"No se encontró un préstamo con el ID {id_prestamo}.")
    else:
        utilidades.imprimir_error(f"El ID de prestamo {id_prestamo} es inválido.")

def ver_prestamos(solo_activos = False):
    #Mostrar prestamos en su totalidad
    titulo = "Prestamos Activos" if solo_activos else "Historial de Prestamos"
    print(f"\n--- {titulo} ---")
    prestamos = gestion_datos.cargar_prestamos()
    lista_a_mostrar = prestamos
    if solo_activos:
        prestamos = list(filter(lambda p: p['Estado_Prestamo'] == 'Activo', prestamos))
    if not lista_a_mostrar:
        utilidades.imprimir_advertencia("No hay préstamos para mostrar.")
    else:
        print(f"{'ID Prestamos':<12} | {'IDs Usuario':<12} | {'ID_Libro': <20} | {'Fecha Prestamo':<20} | {'Fecha Devolucion Prevista':<25} | {'Fecha Devolucion Real':<20}")
        print("-" * 80)
        for p in lista_a_mostrar:
            print(f"{p['ID_Prestamo']:<5} | {P['ID_Usuario']:<5} | {p['ID_Libros']:<20} | {p['Estado_Prestamo']:<10} | {p['Fecha Prestamo']:<12} | {p['Fecha_Devolucion_Prevista']:12}")
            
def ver_prestamos_activos():
    ver_prestamos(solo_activos = True)

def ver_historial_prestamos():
    ver_prestamos(solo_activos = False)