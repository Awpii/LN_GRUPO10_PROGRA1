# busqueda.py
from matriz import Gastos, Categorias

# ---------------------------------------
# Utilitarios de fechas y salida (sin 're')
# ---------------------------------------
def _es_fecha_valida_ddmmaaaa(txt):
    partes = txt.strip().split("/")
    if len(partes) != 3:
        return False
    d, m, a = partes
    return (len(d) == 2 and d.isdigit()
            and len(m) == 2 and m.isdigit()
            and len(a) == 4 and a.isdigit())

def _leer_fecha(mensaje):
    f = input(mensaje).strip()
    while not _es_fecha_valida_ddmmaaaa(f):
        print("Formato inválido. Use DD/MM/AAAA.")
        f = input(mensaje).strip()
    return f

def _fecha_a_tuple(fecha_ddmmaaaa):
    d, m, a = fecha_ddmmaaaa.split("/")
    return (int(a), int(m), int(d))  # (AAAA, MM, DD) para comparar

def _mostrar_resultados(lista):
    if not lista:
        print("\nNo se encontraron resultados.")
        return 0
    print("\nResultados:")
    print("-"*80)
    print("ID  | Fecha       | Monto   | Tipo      | Categoria         | Descripción")
    print("-"*80)
    for g in lista:
        gid, fecha, monto, tipo, cat, desc = g[0], g[1], g[2], g[3], g[4], g[5]
        print(f"{gid:>3} | {fecha:<10}  | {monto:>7} | {tipo:<8} | {cat:<16} | {desc}")
    print("-"*80)
    print(f"Total encontrados: {len(lista)}")
    return len(lista)

# ---------------------------------------
# Búsquedas
# ---------------------------------------
def buscar_por_rango_fechas():
    if not Gastos:
        print("No hay gastos cargados.")
        return
    print("\n=== Búsqueda por rango de fechas ===")
    f_desde = _leer_fecha("Fecha DESDE (DD/MM/AAAA): ")
    f_hasta = _leer_fecha("Fecha HASTA (DD/MM/AAAA): ")
    t_desde, t_hasta = _fecha_a_tuple(f_desde), _fecha_a_tuple(f_hasta)
    if t_desde > t_hasta:
        print("Advertencia: DESDE > HASTA. Se intercambian valores.")
        t_desde, t_hasta = t_hasta, t_desde
    resultado = []
    for g in Gastos:
        if t_desde <= _fecha_a_tuple(g[1]) <= t_hasta:
            resultado.append(g)
    _mostrar_resultados(resultado)

def _armar_dic_categorias():
    dic = {}
    for fila in Categorias:
        if len(fila) >= 2:
            try:
                dic[int(fila[0])] = str(fila[1])
            except:
                continue
    return dic

def buscar_por_categoria():
    if not Gastos:
        print("No hay gastos cargados.")
        return
    print("\n=== Búsqueda por categoría ===")
    dic = _armar_dic_categorias()
    if not dic:
        print("No hay categorías cargadas. ¿Buscar 'Sin categoria'?")
        resp = input("s/n: ").strip().lower()
        if resp == "s":
            filtrados = [g for g in Gastos if g[4] == "Sin categoria"]
            _mostrar_resultados(filtrados)
        else:
            print("Operación cancelada.")
        return

    print("\nSeleccione una categoría:")
    for cid in sorted(dic.keys()):
        print(f"{cid} - {dic[cid]}")
    print("0 - Sin categoria")

    while True:
        op_txt = input("Ingrese número de categoría: ").strip()
        try:
            op = int(op_txt)
            break
        except:
            print("Opción inválida. Debe ser un número.")

    if op == 0:
        nombre_cat = "Sin categoria"
    elif op in dic:
        nombre_cat = dic[op]
    else:
        print("Categoría inexistente.")
        return

    filtrados = [g for g in Gastos if g[4] == nombre_cat]
    _mostrar_resultados(filtrados)

def buscar_por_monto():
    if not Gastos:
        print("No hay gastos cargados.")
        return
    print("\n=== Búsqueda por monto ===")
    txt_min = input("Monto mínimo (entero, vacío = sin mínimo): ").strip()
    txt_max = input("Monto máximo (entero, vacío = sin máximo): ").strip()

    mmin = None
    mmax = None
    if txt_min != "":
        try:
            mmin = int(txt_min)
        except:
            print("Mínimo inválido.")
            return
    if txt_max != "":
        try:
            mmax = int(txt_max)
        except:
            print("Máximo inválido.")
            return

    resultado = []
    for g in Gastos:
        monto = g[2]
        if (mmin is None or monto >= mmin) and (mmax is None or monto <= mmax):
            resultado.append(g)
    _mostrar_resultados(resultado)

def buscar_por_texto_en_descripcion():
    if not Gastos:
        print("No hay gastos cargados.")
        return
    print("\n=== Búsqueda por texto en descripción ===")
    patron = input("Ingrese texto a buscar: ").strip().lower()
    if patron == "":
        print("Texto vacío. Operación cancelada.")
        return
    resultado = []
    for g in Gastos:
        if patron in str(g[5]).lower():
            resultado.append(g)
    _mostrar_resultados(resultado)

# ---------------------------------------
# Menú local de búsqueda
# ---------------------------------------
def menu_busquedas():
    while True:
        print("""
=== BUSQUEDAS ===
1 - Por rango de fechas
2 - Por categoría
3 - Por monto
4 - Por texto en descripción
0 - Volver
""")
        # leer opción con try/except
        while True:
            txt = input("Seleccione opción: ").strip()
            try:
                op = int(txt); break
            except:
                print("Entrada inválida. Debe ser un número entero.")

        if op == 1:
            buscar_por_rango_fechas()
        elif op == 2:
            buscar_por_categoria()
        elif op == 3:
            buscar_por_monto()
        elif op == 4:
            buscar_por_texto_en_descripcion()
        elif op == 0:
            break
        else:
            print("Opción inválida.")
