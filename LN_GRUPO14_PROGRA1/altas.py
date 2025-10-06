import re
from matriz import Gastos, Categorias

def generar_id(): #genera un id automatico
    return len(Gastos) + 1

def alta_gasto():
    print("== Alta de Gasto ==")
    id_mov = generar_id()

    fecha = input("Ingrese la fecha (DD/MM/AAAA): ") #valida la fecha usando regex
    while not re.match("^[0-9]{2}/[0-9]{2}/[0-9]{4}$", fecha):
        print("Formato invalido. Debe ser DD/MM/AAAA")
        fecha = input("Ingrese la fecha (DD/MM/AAAA): ")

    monto = input("Ingrese el monto: ")
    while not re.match("^[0-9]+$", monto):
        print("Monto invalido, solo numeros")
        monto = input("Ingrese el monto: ")

    tipo_mov = input("Ingrese el tipo de movimiento (Gasto/Ingreso/Transferencia): ")

    if Categorias: #Agrego funcion lambda porque hay que agregar al menos una al TP..
        categorias_dict = dict(map(lambda x: (x[0]+1, x[1]), enumerate(Categorias))) #Devuelve par de indice & valor, map lo aplica a todos los elementos y dict convierte las tuplas a diccionarios

        print("\nSeleccione una categoria:")
        for k, v in categorias_dict.items():
            print(f"{k} - {v}")

        cat_opcion = input("Ingrese número de categoria: ")
        if re.match("^[0-9]+$", cat_opcion) and int(cat_opcion) in categorias_dict:
            categoria = categorias_dict[int(cat_opcion)]
        else:
            categoria = "Sin categoria"
    else:
        categoria = "Sin categoria"

    descripcion = input("Ingrese una descripcion: ")
    cuenta_origen = input("Ingrese la cuenta origen: ")
    cuenta_destino = input("Ingrese la cuenta destino: ")

    nuevo_gasto = (id_mov, fecha, int(monto), tipo_mov, categoria, descripcion, cuenta_origen, cuenta_destino)
    Gastos.append(nuevo_gasto)

    print("Gasto agregado correctamente")