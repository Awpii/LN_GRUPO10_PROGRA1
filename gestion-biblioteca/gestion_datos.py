import json

#file paths
RUTA_LIBROS = 'data/books.json'
RUTA_USUARIOS = 'data/users.json'
RUTA_PRESTAMOS = 'data/loans.txt'

def cargar_datos_json(path):
    #carga datos desde json
    try:
        with open(path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Error: El archivo {path} no se pudo encontrar. Se devolvera una lista vacia.")
        return []
    except json.JSONDecodeError:
        print(f"Error: El archivo {path} está vacio o mal formado.")
        return []

def guardar_datos_json(path, data):
    #Guarda los datos en el json:
    try:
        with open(path, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
            return True
    except IOError as e:
        print(f"Error al guardar datos en el archivo {path}: {e}")
        return False
    
def cargar_libros():
    return cargar_datos_json(RUTA_LIBROS)

def guardar_libros(books):
    return guardar_datos_json(RUTA_LIBROS, books)

def cargar_usuarios():
    return cargar_datos_json(RUTA_USUARIOS)

def cargar_prestamos():
    #Lee el archivo txt de prestamos y lo convierte en una matriz de diccionarios
    loans = []
    try:
        with open(RUTA_PRESTAMOS, 'r', encoding='utf-8') as file:
            for line in lines:
                parts = line.rstrip('\n').split('|')
                if len(parts) == 7:
                    loan_dict = {
                        "ID_Loan": parts[0],
                        "ID_User": parts[1],
                        "ID_Book": parts[2],
                        "Loan_Date": parts[3],
                        "Fore_return_date": parts[4],
                        "Real_return_date": parts[5],
                        "Status": parts[6]
                    }
                    loans.append(loan_dict)
    except FileNotFoundError:
        print(f"Warn: El archivo {RUTA_PRESTAMOS} no fue localizado.")
    return loans

def guardar_prestamos(loan_matrix):
    #Convierte matriz de dicc.  prestamos en texto y guarda en txt
    lines_2_wrt = []
    for loan in loan_matrix:
        real_date = loan.get("Real_return_date") or "null")
        line = "|".join([
            loan["ID_Loan"],
            loan["ID_User"],
            loan["ID_Book"],
            loan["Loan_Date"],
            loan["Fore_return_date"],
            real_date,
            loan["Status"]
        ])
        lines_2_wrt.append(line + "\n")
        
    try:
        with open(RUTA_PRESTAMOS, 'w', encoding='utf-8') as file:
            file.writelines(lines_2_wrt)
    except IOError as e:
        print(f"Error: No se pudo guardar el archivo {RUTA_PRESTAMOS}: {e}")