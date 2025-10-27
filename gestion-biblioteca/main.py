import colorama
from gestion_biblioteca import crud_libros, crud_usuarios, crud_prestamos

def mostrar_menu():
    """Imprime el menú principal de opciones usando colorama para el estilo."""
    # Se usa una tupla de strings y el método .join() para construir el menú
    menu_items = (
        f"{colorama.Fore.YELLOW}====================================================",
        "           Sistema de Gestión de Biblioteca",
        "====================================================",
        f"{colorama.Fore.CYAN}--- Gestión de Usuarios ---",
        "  1 - Registrar Usuario",
        "  2 - Eliminar Usuario",
        "  3 - Ver todos los Usuarios",
        f"{colorama.Fore.CYAN}--- Gestión de Libros ---",
        "  4 - Registrar Libro",
        "  5 - Eliminar Libro",
        "  6 - Ver todos los Libros",
        f"{colorama.Fore.CYAN}--- Gestión de Préstamos ---",
        "  7 - Registrar Préstamo (con uno o varios libros)",
        "  8 - Registrar Devolución (Modificar Préstamo)",
        "  9 - Ver Préstamos Activos",
        " 10 - Ver Historial de Préstamos",
        f"{colorama.Fore.RED}\n 11 - Salir",
        f"{colorama.Fore.YELLOW}===================================================="
    )
    print("\n".join(menu_items))

def ejecutar_programa():
    """Función principal que ejecuta el bucle del menú y gestiona las opciones."""
    colorama.init(autoreset=True)
    
    # Se usa un diccionario para mapear opciones a funciones, es más eficiente que un if/elif
    # Se usan funciones lambda para llamar a ver_prestamos con diferentes argumentos
    opciones = {
        "1": crud_usuarios.registrar_usuario,
        "2": crud_usuarios.eliminar_usuario,
        "3": crud_usuarios.ver_usuarios,
        "4": crud_libros.registrar_libro,
        "5": crud_libros.eliminar_libro,
        "6": crud_libros.ver_libros,
        "7": crud_prestamos.registrar_prestamo,
        "8": crud_prestamos.modificar_prestamo,
        "9": lambda: crud_prestamos.ver_prestamos(solo_activos=True),
        "10": lambda: crud_prestamos.ver_prestamos(solo_activos=False),
    }

    terminar = False
    # El bucle se controla con la variable booleana 'terminar'
    while not terminar:
        mostrar_menu()
        opcion = input("Seleccione una opción: ").strip()

        if opcion == "11":
            terminar = True
        else:
            # .get() busca la opción en el diccionario. Si no la encuentra, devuelve None.
            funcion_a_ejecutar = opciones.get(opcion)
            if funcion_a_ejecutar:
                try:
                    funcion_a_ejecutar()
                except Exception as e:
                    # Captura de excepción genérica para errores no esperados
                    print(f"{colorama.Fore.RED}Ocurrió un error inesperado: {e}")
            else:
                print(f"{colorama.Fore.RED}Opción no válida. Por favor, intente de nuevo.")
    
    print(f"\n{colorama.Fore.MAGENTA}Gracias por usar el sistema. ¡Hasta pronto!")

# Este es el punto de entrada del programa.
# El código dentro de este if solo se ejecuta cuando el archivo es corrido directamente.
if __name__ == "__main__":
    ejecutar_programa()