def saludo():
    print("hola mundo")

saludo()

def saludo2 (nombre):
    print(f"Hola, {nombre}")

saludo2("juan")

def suma (a,b):
    return a + b

print(suma(2,3))

def suma_variables(*numeros):
    total = 0
    for numero in numeros:
        total+=numero
    return total
    
print(suma_variables(1,23,4,2))

try:
    resultado = 10 / 0
    print(resultado)
except ZeroDivisionError:
    print("error: division por cero")