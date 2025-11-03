import colorama
import crud_books
import crud_users
import crud_loans
import stats as estadisticas

def mostrar_menu():     #Mostrar el menu principal, colorama para que quede flama. Tupla de strings y joins para el print, queda joya
    menu_items = (
        f"{colorama.Fore.YELLOW}====================================================",
        "           Sistema de gestion de bibliotecas 3000X",
        "====================================================",
        f"{colorama.Fore.CYAN}--- Gestión de usuarios ---",
        "  1 - Registrar usuario",
        "  2 - Eliminar usuario",
        "  3 - Ver todos los usuarios",
        f"{colorama.Fore.CYAN}--- Gestión de libros ---",
        "  4 - Registrar libro",
        "  5 - Eliminar libro",
        "  6 - Ver todos los libros",
        f"{colorama.Fore.CYAN}--- Gestión de prestamos ---",
        "  7 - Registrar prestamo",
        "  8 - Registrar devolucion (modificar prestamo)",
        "  9 - Ver prestamos activos",
        " 10 - Ver historial de prestamos",
        f"{colorama.Fore.CYAN}--- Estadisticas ---",
        " 11 - Ver Estadisticas",
        f"{colorama.Fore.RED}\n 12 - Salir",
        f"{colorama.Fore.YELLOW}===================================================="
    )
    print("\n".join(menu_items))

def ejecutar_programa(): #Ejecuta el loop del menu para mostrar las opciones durante la navegacion
    colorama.init(autoreset = True)
    opciones = {     #Diccionario para mappear funciones a opciones del menu y lambbdas para funciones con argumentos especificos, me dio fiaca usar IF/ELSE
        "1": crud_users.registrar_usuario,
        "2": crud_users.eliminar_usuario,
        "3": crud_users.ver_usuarios,
        "4": crud_books.registrar_libro,
        "5": crud_books.eliminar_libro,
        "6": crud_books.ver_libros,
        "7": crud_loans.registrar_prestamo,
        "8": crud_loans.modificar_prestamo,
        "9": lambda: crud_loans.ver_prestamos(solo_activos = True),
        "10": lambda: crud_loans.ver_prestamos(solo_activos = False),
        "11": estadisticas.mostrar_estadisticas,
    }

    terminar = False #Para controlar la salida del loop
    while not terminar:
        mostrar_menu()
        opcion = input("Elija una opcion: ").strip()

        if opcion == "12":
            terminar = True
        else:
            funcion_a_ejecutar = opciones.get(opcion) #.get para buscar opciones, None si no existe la opcion
            if funcion_a_ejecutar:
                try:
                    funcion_a_ejecutar()
                except Exception as e: #No podía pensar en que excepciones podian salir asi que puse una generica
                    print(f"{colorama.Fore.RED}Hubo un error inesperado: {e}")
            else:
                print(f"{colorama.Fore.RED}Opción invalida, proba de nuevo")
    print(f"\n{colorama.Fore.MAGENTA}Chau loco")

if __name__ == "__main__":
    ejecutar_programa()