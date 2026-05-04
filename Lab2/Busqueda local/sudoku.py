import random
import math
import copy

SUDOKU_4X4 = [
    [1, 0, 0, 0],
    [0, 0, 0, 4],
    [0, 0, 3, 0],
    [2, 0, 0, 0]
]

# Un 9x9 generado ya que el ejercicio no especifica uno en particular
SUDOKU_9x9 = [
    [5, 3, 0, 0, 7, 0, 0, 0, 0],
    [6, 0, 0, 1, 9, 5, 0, 0, 0],
    [0, 9, 8, 0, 0, 0, 0, 6, 0],
    [8, 0, 0, 0, 6, 0, 0, 0, 3],
    [4, 0, 0, 8, 0, 3, 0, 0, 1],
    [7, 0, 0, 0, 2, 0, 0, 0, 6],
    [0, 6, 0, 0, 0, 0, 2, 8, 0],
    [0, 0, 0, 4, 1, 9, 0, 0, 5],
    [0, 0, 0, 0, 8, 0, 0, 7, 9],
]

#no mira las filas porque mantiene correca al generar estados 
def h(tablero): #heuristica
    N = len(tablero)
    SUB = int(N ** 0.5)
    conflictos = 0

    # columnas
    for col in range(N):
        valores = [tablero[fila][col] for fila in range(N)]
        conflictos += len(valores) - len(set(valores))

    # bloques
    for i in range(0, N, SUB):
        for j in range(0, N, SUB):
            bloque = []
            for x in range(SUB):
                for y in range(SUB):
                    bloque.append(tablero[i + x][j + y])
            conflictos += len(bloque) - len(set(bloque))

    return conflictos

def obtener_fijas(base):
    return [[cell != 0 for cell in fila] for fila in base]


def crear_tablero_inicial(base): #rellana los espacios vacíos con números aleatorios
    N = len(base)
    tablero = copy.deepcopy(base)
    for fila in range(N):
        faltantes = [x for x in range(1, N + 1) if x not in tablero[fila]]
        random.shuffle(faltantes)
        for col in range(N):
            if tablero[fila][col] == 0:
                tablero[fila][col] = faltantes.pop()
    return tablero


def generar_vecinos(tablero, fijas): #genera vecinos intercambiando dos celdas libres en la misma fila
    N = len(tablero)
    vecinos = []
    for fila in range(N):
        indices = [i for i in range(N) if not fijas[fila][i]]
        for i in range(len(indices)):
            for j in range(i + 1, len(indices)):
                nuevo = copy.deepcopy(tablero)
                a, b = indices[i], indices[j]
                nuevo[fila][a], nuevo[fila][b] = nuevo[fila][b], nuevo[fila][a]
                vecinos.append(nuevo)
    return vecinos


#genera un vecino aleatorio intercambiando dos celdas libres en la misma fila (más eficiente que generar todos los vecinos)
def generar_vecino_random(tablero, fijas): 
    N = len(tablero)
    filas_validas = [
        f for f in range(N)
        if sum(1 for c in range(N) if not fijas[f][c]) >= 2
    ]
    fila = random.choice(filas_validas)
    indices = [i for i in range(N) if not fijas[fila][i]]
    a, b = random.sample(indices, 2)
    vecino = copy.deepcopy(tablero)
    vecino[fila][a], vecino[fila][b] = vecino[fila][b], vecino[fila][a]
    return vecino


def hill_climbing(base, fijas, max_reinicios=50):
    mejor_global = None
    mejor_h_global = float('inf')

    for reinicio in range(max_reinicios):
        actual = crear_tablero_inicial(base)
        while True:
            vecinos = generar_vecinos(actual, fijas)
            mejor_vecino = min(vecinos, key=h)
            if h(mejor_vecino) >= h(actual):
                # si no hay vecino mejor, termina esta corrida
                break
            actual = mejor_vecino

        h_actual = h(actual)#actualiza el mejor encontrado en esta corrida
        if h_actual < mejor_h_global:
            mejor_h_global = h_actual
            mejor_global = actual

        if mejor_h_global == 0:
            print(f"  Hill Climbing: solución encontrada en reinicio {reinicio + 1}")
            break
    else:
        print(f"  Hill Climbing: mejor h={mejor_h_global} tras {max_reinicios} reinicios")

    return mejor_global


def simulated_annealing(base, fijas, T=5.0, T_min=0.1, enfriamiento=0.99, max_iter=100000):
    actual = crear_tablero_inicial(base)
    mejor = copy.deepcopy(actual)
    mejor_h = h(actual)

    for _ in range(max_iter):
        if T < T_min:
            break

        vecino = generar_vecino_random(actual, fijas)
        delta = h(vecino) - h(actual)

        if delta < 0 or random.random() < math.exp(-delta / T):
            actual = vecino

        h_actual = h(actual) #actualiza el mejor encontrado
        if h_actual < mejor_h:
            mejor_h = h_actual
            mejor = copy.deepcopy(actual)

        if mejor_h == 0:
            break

        T *= enfriamiento

    if mejor_h > 0:
        print(f"  Simulated Annealing: terminó con h={mejor_h} (no encontró solución perfecta)")
    else:
        print(f"  Simulated Annealing: solución encontrada")

    return mejor


def imprimir(tablero):
    for fila in tablero:
        print(fila)
    print(f"Conflictos: {h(tablero)}\n")


if __name__ == "__main__":
    
    #para que imprima ambos tableros 
    for nombre, base in [("4x4", SUDOKU_4X4), ("9x9", SUDOKU_9x9)]:
        print(f"  SUDOKU {nombre}")
        fijas = obtener_fijas(base)

        print("\nTablero inicial (pistas)")
        imprimir(base)

        print("--- HILL CLIMBING ---")
        resultado_hc = hill_climbing(base, fijas, max_reinicios=50)
        imprimir(resultado_hc)

        print("--- SIMULATED ANNEALING ---")
        resultado_sa = simulated_annealing(base, fijas, T=5.0, T_min=0.1, enfriamiento=0.99, max_iter=100000)
        imprimir(resultado_sa)