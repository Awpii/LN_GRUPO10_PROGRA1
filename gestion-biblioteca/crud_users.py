from . import gestion_datos
from . import utils as utilidades

def registrar_usuario():
    #Pide datos y crea usuarios en user.json
    print("\n--- Registro de Nuevo Usuario ---")
    nombre = input("Nombre: ").strip().capitalize()
    apellido = input("Apellido: ").strip().capitalize()
    email = input("E-mail: ").strip().lower()
    
    if nombre and apellido and email:
        usuarios = gestion_datos.cargar_usuarios()
        nuevo_id = utilidades.generar_nuevo_id(usuarios, 'U')
        nuevo_usuario = {
            "ID_Usuario": nuevo_id,
            "Nombre": nombre,
            "Apellido": apellido,
            "Email": email,
            "Telefono": input("Teléfono: ").strip(),
            "Fecha_Registro": utilidades.obtener_fecha_actual_str()
        }
        
    usuarios.append(nuevo_usuario)
    if gestion_datos.guardar_usuarios(usuarios):
        utilidades.imprimir_exito(f"Usuario '{nombre} {apellido}' registrado con ID: {nuevo_id}")
    else:
        utilidades.imprimir_error("Todos los campos son obligatorios.")

def eliminar_usuario():
    #Eliminar un usuario por ID, siempre que NO TENGA PRESTAMOS ACTIVOS
    print("\n--- Eliminar Usuario ---")
    id_usuario = input("Ingrese el ID del usuario a eliminar (ej. U001): ").strip().upper()
    
    if not utilidades.validar_id(id_usuario, 'usuario'):
        prestamos = gestion_datos.cargar_prestamos()
        prestamos_activos = list(filter(lambda p:['ID_Usuario'] == id_usuario and p['Estado_Prestamo'] == 'Activo', prestamos))
        
    if not prestamos_activos:
        usuarios = gestion_datos.cargar_usuarios()
        longitud_inicial = len(usuarios)
        usuarios_actualizados = list(filter(lambda u: u['ID_Usuario'] != id_usuario, usuarios))
        
        if len(usuarios_actualizados) < longitud_inicial:
            if gestion_datos.guardar_usuarios(usuarios_actualizados):
                utilidades.imprimir_exito(f"Usuario con ID {id_usuario} eliminado correctamente.")
            else:
                utilidades.imprimir_error(f"No se encontró un usuario con el ID {id_usuario}.")
        else:
            utilidades.imprimir_error(f"No se puede eliminar el usuario {id_usuario}. El usuario tiene préstamos activos.")
    else:
        utilidades.imprimir_error("Formato de ID inválido.")

def ver_usuarios():
    #Muesra lista de usuarios por apellido
    print("\n--- Lista de Usuarios ---")
    usuarios = gestion_datos.cargar_usuarios()
    if not usuarios:
        utilidades.imprimir_advertencia("No hay usuarios registrados.")
    else:
        usuarios_ordenados = sorted(usuarios, key=lambda usuario: usuario['Apellido'])
        print(f"{'ID':<7} | {'Nombre':<20} | {'Apellido':<20} | {'E-mail':<30} | {'Teléfono':<35}")
        print("-" * 80)
        for u in usuarios_ordenados:
            print(f"{u['ID_Usuario']:<7} | {u['Nombre']:<20} | {u['Apellido']:<20} | {u['Email']:<30} | {u['Telefono']:<35}")