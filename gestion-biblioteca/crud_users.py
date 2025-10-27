from . import gestion_datos
from . import utils as utilidades

def registrar_usuario():
    """Pide datos y crea un nuevo usuario en users.json."""
    print("\n--- Registro de Nuevo Usuario ---")
    nombre = input("Nombre: ").strip().capitalize()
    apellido = input("Apellido: ").strip().capitalize()
    email = input("Email: ").strip().lower()
    
    # Se valida que los campos no estén vacíos
    if not nombre or not apellido or not email:
        utilidades.imprimir_error("Todos los campos son obligatorios.")
        return

    usuarios = gestion_datos.cargar_usuarios()
    
    # Se genera un ID único para el nuevo usuario
    nuevo_id = utilidades.generar_nuevo_id(usuarios, 'U')
    
    # Se crea el diccionario del nuevo usuario
    nuevo_usuario = {
        "ID_Usuario": nuevo_id,
        "Nombre": nombre,
        "Apellido": apellido,
        "Email": email,
        "Telefono": input("Teléfono (opcional): ").strip(),
        "Fecha_Registro": utilidades.obtener_fecha_actual_str()
    }
    
    # Se añade el nuevo usuario a la matriz (lista) de usuarios
    usuarios.append(nuevo_usuario)
    if gestion_datos.guardar_usuarios(usuarios):
        utilidades.imprimir_exito(f"Usuario '{nombre} {apellido}' registrado con ID: {nuevo_id}")

def eliminar_usuario():
    """Elimina un usuario por su ID, verificando que no tenga préstamos activos."""
    print("\n--- Eliminar Usuario ---")
    id_usuario = input("Ingrese el ID del usuario a eliminar (ej. U001): ").strip().upper()

    if not utilidades.validar_id(id_usuario, 'usuario'):
        utilidades.imprimir_error("Formato de ID inválido.")
        return

    prestamos = gestion_datos.cargar_prestamos()
    # Se busca si el usuario tiene préstamos activos
    prestamos_activos = list(filter(
        lambda p: p['ID_Usuario'] == id_usuario and p['Estado_Prestamo'] == 'Activo',
        prestamos
    ))

    if prestamos_activos:
        utilidades.imprimir_error(f"No se puede eliminar el usuario {id_usuario} porque tiene préstamos activos.")
        return

    usuarios = gestion_datos.cargar_usuarios()
    # len() se usa para verificar si el usuario fue encontrado antes y después de filtrar
    longitud_inicial = len(usuarios)
    
    # filter() crea una nueva lista excluyendo al usuario a eliminar
    usuarios_actualizados = list(filter(lambda u: u['ID_Usuario'] != id_usuario, usuarios))

    if len(usuarios_actualizados) == longitud_inicial:
        utilidades.imprimir_error(f"No se encontró un usuario con el ID {id_usuario}.")
    else:
        if gestion_datos.guardar_usuarios(usuarios_actualizados):
            utilidades.imprimir_exito(f"Usuario con ID {id_usuario} eliminado correctamente.")

def ver_usuarios():
    """Muestra una lista formateada de todos los usuarios."""
    print("\n--- Listado de Usuarios ---")
    usuarios = gestion_datos.cargar_usuarios()
    if not usuarios:
        utilidades.imprimir_advertencia("No hay usuarios registrados.")
    else:
        # Se usan métodos de string como .ljust() para alinear el texto en columnas
        print(f"{'ID':<7} | {'Nombre':<20} | {'Apellido':<20} | {'Email':<30}")
        print("-" * 80)
        for u in usuarios:
            print(f"{u['ID_Usuario']:<7} | {u['Nombre']:<20} | {u['Apellido']:<20} | {u['Email']:<30}")