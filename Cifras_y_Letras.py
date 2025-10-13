import operator
import random


# Definimos operaciones permitidas
def safe_div(a, b):
    return a // b if b != 0 and a % b == 0 else None


ops = {
    '+': operator.add,
    '-': operator.sub,
    '*': operator.mul,
    '/': safe_div
}


def quitar_duplicados(soluciones):
    vistas = set()
    unicas = []
    for sol in soluciones:
        firma = tuple(sorted(
            sol))  # pasos en orden alfabético. Se convierte en tupla para ser hashable y poder ser ordenado, y firma toma el valor de la tupla
        if firma not in vistas:
            vistas.add(firma)  # marcamos esta firma como vista
            unicas.append(
                sol)  # guardamos la versión original. Si guardáramos la firma, perderíamos el orden lógico porque ha sido ordenada previamente
    return unicas


def buscar_solucion(numeros, objetivo, pasos=None):
    if pasos is None:
        pasos = []

    # condición de éxito

    if numeros[0] == objetivo:
        return [pasos]
        # return pasos

        # return None

    # probar todos los pares
    sol = []  # En caso de querer almacenar todas las soluciones
    for i in range(len(numeros)):
        for j in range(i + 1, len(numeros)):
            a, b = numeros[i], numeros[j]

            for simbolo, func in ops.items():
                if (a > b):# descartamos negativos/None
                    r = func(a, b)
                else:
                    a, b = b, a
                    r = func(a, b)
                if r is None or r < 0:
                    continue

                nueva_lista = [r] + [numeros[k] for k in range(len(numeros)) if k not in (i, j)]
                nueva_pasos = pasos + [f"{a} {simbolo} {b} = {r}"]

                sol.extend(buscar_solucion(nueva_lista, objetivo, nueva_pasos))

    return sol
    # return None


x = int(input("primer numero: "))
y = int(input("segundo numero: "))
z = int(input("tercer numero: "))
w = int(input("cuarto numero: "))
v = int(input("quinto numero: "))
u = int(input("sexto numero: "))
nums = [x, y, z, w, v, u]
objetivo = int(input("numero objetivo: "))

solucion = buscar_solucion(nums, objetivo)

if solucion:
    # calcular longitud mínima
    min_len = min(len(s) for s in solucion)
    # filtrar todas las soluciones más cortas
    mejores = [s for s in solucion if len(s) == min_len]

    mejores_unicas = quitar_duplicados(mejores)
    print(f"Se encontraron {len(mejores_unicas)} soluciones únicas más cortas:")

    for i, sol in enumerate(mejores_unicas, 1):
        print(f"\nSolución {i}:")
        for paso in sol:
            print(paso)
        print("----------------")
else:
    print("No se encontró solución")


