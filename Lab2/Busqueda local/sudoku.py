import random
import math
import copy

SUDOKU_4X4 = [
    [1,0,0,0],
    [0,0,0,4],
    [0,0,3,0],
    [2,0,0,0]
]

#Un 9x9 random ya que el ejercicio no especifica un en particular
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

def h(tablero):
    N = len(tablero)
    SUB = int(N**0.5)
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
                    bloque.append(tablero[i+x][j+y])
            conflictos += len(bloque) - len(set(bloque))
    
    return conflictos

def obtener_fijas(base):
    return [[cell != 0 for cell in fila] for fila in base]

def crear_tablero_inicial(base):
    N = len(base)
    tablero = copy.deepcopy(base)

    for fila in range(N):
        faltantes = [x for x in range(1, N+1) if x not in tablero[fila]]
        random.shuffle(faltantes)

        for col in range(N):
            if tablero[fila][col] == 0:
                tablero[fila][col] = faltantes.pop()

    return tablero

def generar_vecinos(tablero, fijas):
    N = len(tablero)
    vecinos = []

    for fila in range(N):
        indices = [i for i in range(N) if not fijas[fila][i]]

        for i in range(len(indices)):
            for j in range(i+1, len(indices)):
                nuevo = copy.deepcopy(tablero)
                a, b = indices[i], indices[j]
                nuevo[fila][a], nuevo[fila][b] = nuevo[fila][b], nuevo[fila][a]
                vecinos.append(nuevo)

    return vecinos

def hill_climbing(tablero, fijas):
    actual = tablero

    while True:
        vecinos = generar_vecinos(actual, fijas)
        mejor = min(vecinos, key=h)

        if h(mejor) >= h(actual):
            return actual

        actual = mejor

def simulated_annealing(tablero, fijas):
    actual = tablero
    T = 100

    while T > 0.1:
        vecinos = generar_vecinos(actual, fijas)
        vecino = random.choice(vecinos)

        delta = h(vecino) - h(actual)

        if delta < 0:
            actual = vecino
        else:
            prob = math.exp(-delta / T)
            if random.random() < prob:
                actual = vecino

        if h(actual) == 0:
            return actual

        T *= 0.99

    return actual


def imprimir(tablero):
    for fila in tablero:
        print(fila)
    print("Conflictos:", h(tablero))
    print()
    

if __name__ == "__main__":

    #Elegí cuál usar:
    #base = SUDOKU_4X4
    base = SUDOKU_9x9

    fijas = obtener_fijas(base)
    tablero = crear_tablero_inicial(base)

    print("=== TABLERO INICIAL ===")
    #imprimir(SUDOKU_4X4)
    imprimir(SUDOKU_9x9)

    print("=== HILL CLIMBING ===")
    resultado_hc = hill_climbing(tablero, fijas)
    imprimir(resultado_hc)

    print("=== SIMULATED ANNEALING ===")
    resultado_sa = simulated_annealing(tablero, fijas)
    imprimir(resultado_sa)