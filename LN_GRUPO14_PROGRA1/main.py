from login import login

# Gastos
from altas import alta_gasto
from bajas import baja_gasto
from busqueda import menu_busquedas
from consulta import menu_consultas
from modificacion import menu_modificaciones

# Matrices y precarga (en matriz)
from matriz import Gastos, Categorias, Presupuestos

# ---------------------------
# Helpers locales (sin validaciones.py)
# ---------------------------
def leer_opcion(mensaje, minimo, maximo):
    """
    Lee un entero en [minimo, maximo] usando solo try/except y bucle while.
    """
    while True:
        txt = input(mensaje).strip()
        try:
            op = int(txt)
            if op < minimo or op > maximo:
                print(f"Opción inválida. Ingrese un número entre {minimo} y {maximo}.")
            else:
                return op
        except:
            print("Entrada inválida. Debe ser un número entero.")

# ---------------------------
# Submenús
# ---------------------------
def menu_gastos():
    while True:
        print("""
=== GASTOS ===
1 - Alta de gasto
2 - Baja de gasto
3 - Búsquedas
4 - Consultas
5 - Modificaciones
0 - Volver
""")
        op = leer_opcion("Seleccione opción: ", 0, 5)
        if op == 1:
            alta_gasto()
        elif op == 2:
            baja_gasto()
        elif op == 3:
            menu_busquedas()
        elif op == 4:
            menu_consultas()
        elif op == 5:
            menu_modificaciones()
        elif op == 0:
            break

def menu_categorias():
    while True:
        print("""
=== CATEGORÍAS ===
1 - Listar categorías
0 - Volver
""")
        op = leer_opcion("Seleccione opción: ", 0, 1)

        if op == 1:
            if not Categorias:
                print("No hay categorías cargadas.")
            else:
                print("\nID | Nombre")
                print("-"*24)
                for fila in Categorias:
                    if len(fila) >= 2:
                        # intenta mostrar id como entero si se puede
                        try:
                            cid = int(fila[0])
                        except:
                            cid = fila[0]
                        nom = str(fila[1])
                        print(f"{str(cid):>2} | {nom}")
                print("-"*24)
        elif op == 0:
            break

def menu_presupuestos():
    print("\n=== PRESUPUESTOS ===")
    print("Módulo no implementado aún en esta versión.\n")

def menu_ahorros():
    print("\n=== AHORROS ===")
    print("Módulo no implementado aún en esta versión.\n")

# ---------------------------
# Carga rápida desde matriz
# ---------------------------
def carga_rapida_matrices():
    # Limpia listas (por si ya tenían datos)
    Gastos.clear()
    Presupuestos.clear()

    # Gastos: (id, fecha, monto, tipo, categoria, descripcion, cuenta_origen, cuenta_destino)
    Gastos.extend([
        (1, "01/09/2025", 2500, "Fijo", "Hogar", "Pago internet", "Cuenta Sueldo", "-"),
        (2, "03/09/2025", 12000, "Variable", "Ocio", "Cena con amigos", "Cuenta Sueldo", "Restaurante"),
        (3, "05/09/2025", 5000, "Fijo", "Transporte", "Recarga Sube", "Cuenta Sueldo", "-"),
        (4, "07/09/2025", 9000, "Variable", "Salud", "Suplementos GYM", "Cuenta Sueldo", "Farmacia"),
    ])

    # Presupuestos: (id, categoria, monto_asignado)
    Presupuestos.extend([
        (1, "Hogar", 15000),
        (2, "Ocio", 20000),
        (3, "Transporte", 10000),
        (4, "Salud", 12000),
    ])

    print(">>> Matrices cargadas con datos de ejemplo <<<")

# ---------------------------
# Programa principal
# ---------------------------
def main():
    print("=== Sistema de Gestión de Gastos (UADE - Programación 1) ===")
    autenticado = login()
    if not autenticado:
        print("No se pudo iniciar sesión. Fin del programa.")
        return

    while True:
        print("""
=== MENÚ PRINCIPAL ===
1 - Gastos
2 - Categorías
3 - Presupuestos
4 - Ahorros
5 - Carga rápida matrices (desde 'matriz')
0 - Salir
""")
        opcion = leer_opcion("Seleccionar opción: ", 0, 5)

        if opcion == 1:
            menu_gastos()
        elif opcion == 2:
            menu_categorias()
        elif opcion == 3:
            menu_presupuestos()
        elif opcion == 4:
            menu_ahorros()
        elif opcion == 5:
            carga_rapida_matrices()
        elif opcion == 0:
            print("Saliendo. ¡Hasta la próxima!")
            break

if __name__ == "__main__":
    main()
