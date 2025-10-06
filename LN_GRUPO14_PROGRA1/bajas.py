import re
from matriz import Gastos

def baja_gasto():
    print("== Baja de Gasto ==")
    if not Gastos:
        print("No hay gastos registrados")
        return

    print("Gastos actuales:")
    for gasto in Gastos:
        print(gasto)

    eliminar_id = input("Ingrese el ID del gasto a eliminar: ")
    if re.match("^[0-9]+$", eliminar_id):
        eliminar_id = int(eliminar_id)
        for g in Gastos:
            if g[0] == eliminar_id:  # g[0] es el id_mov que elimina 
                Gastos.remove(g)
                print(f"Gasto con ID {eliminar_id} eliminado correctamente")
                return
        print("ID no encontrado")
    else:
        print("Entrada invalida")
