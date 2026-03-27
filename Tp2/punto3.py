import random

lista = []
indice = 0

for i in range(20):
    num = random.randint(0,10)
    lista.append(num)

for i in lista:
    indice += 1
    print(f"elemento {indice}: {i}")

conjunto = set(lista)
i= 0
for num in conjunto:
    i+=1
    print(f"elemento {i}: {num}")
