import random

LIMPIO = "Limpio"
SUCIO = "Sucio"

entorno = {
    "A": SUCIO,
    "B": SUCIO
}

posicion = random.choice(["A", "B"])

movimientos = 20

print("Estado inicial:", entorno)
print("Posición inicial:", posicion)
print("-" * 40)

for i in range(1, movimientos + 1):
    print(f"Movimiento {i}")

    estado_actual = entorno[posicion]

    # Regla del agente
    if estado_actual == SUCIO:
        print(f"Está en {posicion} y está SUCIO → Limpia")
        entorno[posicion] = LIMPIO
    else:
        print(f"Está en {posicion} y está LIMPIO → Se mueve")
        if posicion == "A":
            posicion = "B"
        else:
            posicion = "A"

    print("Entorno:", entorno)
    print("Posición actual:", posicion)
    print("-" * 40)