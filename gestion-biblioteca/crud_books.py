from . import gestion_datos
from . import utils
from colorama import Fore, Style

#trying to commit this garbage

def ver_libros():
    print(Fore.CYAN + "\n --- Listado de Todos los Libros ---")
    books = gestion_datos.cargar_libros()
    if not books:
        print(Fore.YELLOW + "No hay libros disponibles en la biblioteca")
    else:
        print(Fore.WHITE + f"{'ID':<6} {'Título':<30} {'Autor':<20} {'Año':<6} {'Género':<15} {'Disponibilidad':<15}")
        print(Fore.WHITE + "-" * 90)
        
        for book in books:
            print(f"{book.get('ID_Book', ''):<6} | {book.get('Title', ''):<40} | { book.get('Author', ''):<30} | {book.get('Status', ''):<12}")
            
def buscar_libros():
    #Busca por titulo o autor
    search_term = input("Ingrese el titulo o autor del libro a buscar: ").lower()
    books = gestion_datos.cargar_libros()
    
    results = list(filter(
                lambda book: search_term in book['Title'].lower() or search_term in book['Autor'].lower()
                books
    ))
    print(Fore.CYAN + f"\n--- Resultados de la busqueda para '{search_term}' ---")
    if not results:
        print(Fore.YELLOW + "No se encontraron resultados.")
    else:
        for book in results:
            print(f"ID: {book['ID_Book']}, Titulo: {book['Title']}, Autor: {book['Author']}, Estado: {book['Status']}")
            
def agregar_libro():
    #Agrega nuevo libro a json de libros
    print(Fore.CYAN + "\n--- Agregar un nuevo libro ---")
    title = input("Ingrese el titulo del libro: ").strip().title()
    author = input("Ingrese el autor del libro: ").strip().title()
    
    
    if not title or not author:
        print(Fore.RED + "ERROR: El titulo y/o Autor no pueden estar vacios.")
        return
    
    books = gestion_datos.cargar_libros()
    new_id = utils.generar_nuevo_id(books, 'L')
    
    new_book = {
        "ID_Book": new_id,
        "Titulo": title,
        "Autor": author,
        "Estado": "Disponible",
        "Fecha_Ingreso": utils.obtener_fecha_actual()
    }
    
    books.append(new_book)
    if gestion_datos.guardar_libros(books):
        print(Fore.GREEN + f"El libro {'title'} se ha agregado con exito (ID: {new_id}")

def editar_libro():
    id_book = input("Ingrese el ID del libro a editar (ej. L001): ").strip().upper()
    
    if not utils.validar_id(id_book, 'book'):
        print(Fore.RED + "ERROR: El formato del ID es inválido.")
        return
    
    books = gestion_datos.cargar_libros()
    found_book = next((book for book in books if book['ID_Book'] == id_book), None)
    
    if found_book is None:
        print(Fore.RED + f"ERROR: No se encontró un Libro con ID {id_book}.")
        return
    
    field = input("Indique que le gustaría editar (titulo - autor): ").lower().strip()
    if field not in ['title', 'author']:
        print(Fore.RED + "ERROR: El campo indicado es inválido")
        return
    
    new_value = input(f"Ingrese el nuevo valor para {field}: ").strip().title()
    if gestion_datos.guardar_libros(books):
        print(Fore.GREEN + "Libro editado correctamente.")
        
def eliminar_libro():
    id_book = input("Ingrese el ID del libro a eliminar (ej. L001): ").strip().upper()
    
    if not utils.validar_id(id_book, 'book'):
        print(Fore.RED + "ERROR: El formato de ID es Inválido.")
    
    books = gestion_datos.cargar_libros()
    updated_books = list(filter(lambda book: book['ID_Book'] != id_book, books))
    
    if len(updated_books) == len(books):
        print(Fore.RED + f"ERROR: No se encontró ningun libro con el id {id_book}.")
    else:
        if gestion_datos.guardar_libros(updated_books):
            print(Fore.GREEN f"Libro con ID {id_book} eliminado correctamente.")