import colorama
from . import crud_books, crud_users, crud_loans

def mostrar_menu():
    #Mostrar el menu principal, colorama para que quede flama. Tupla de strings y joins para el print, queda joya
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

def ejecutar_programa(): #Ejecuta el loop del menu para mostrar las opciones durante la navegacion
    colorama.init(autoreset=True)
    
    #Diccionario para mappear funciones a opciones del menu y lambbdas para funciones con argumentos especificos, me dio fiaca usar IF/ELSE
    opciones = {
        "1": crud_users.registrar_usuario,
        "2": crud_users.eliminar_usuario,
        "3": crud_users.ver_usuarios,
        "4": crud_books.registrar_libro,
        "5": crud_books.eliminar_libro,
        "6": crud_books.ver_libros,
        "7": crud_loans.registrar_prestamo,
        "8": crud_loans.modificar_prestamo,
        "9": lambda: crud_loans.ver_prestamos(solo_activos=True),
        "10": lambda: crud_loans.ver_prestamos(solo_activos=False),
    }

    terminar = False #Para controlar la salida del loop
    while not terminar:
        mostrar_menu()
        opcion = input("Seleccione una opción: ").strip()

        if opcion == "11":
            terminar = True
        else:
            funcion_a_ejecutar = opciones.get(opcion) #.get para buscar opciones, None si no existe la opcion
            if funcion_a_ejecutar:
                try:
                    funcion_a_ejecutar()
                except Exception as e: #No podía pensar en que excepciones podian salir asi que puse una generica
                    print(f"{colorama.Fore.RED}Ocurrió un error inesperado: {e}")
            else:
                print(f"{colorama.Fore.RED}Opción no válida. Por favor, intente de nuevo.")
    print(f"\n{colorama.Fore.MAGENTA}Gracias por usar el sistema. ¡Hasta pronto!")

if __name__ == "__main__":
    ejecutar_programa()