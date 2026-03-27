print ("hola, mundo")
var = 4; 

if var > 0:
    print ("la variable es positiva")
else:
    print ("la variable es negativa")

#comentario 

var2 = 2 + (var * 3)

print (var2)

#string 
nombre = "juan"
mensaje = 'hola mundo'

#boolranos
falso = False
verdaero = True

frutas = ["manzana", "banana", "naranja"]

for fruta in frutas:
    if fruta == "naranja":
        print(fruta)

contador = 0
while contador < 5:
    print (contador)
    contador += 1

#listas
verduras = ["arveja", "papa", "cebolla"]
print(verduras[1])

#agregar un elemento final a la lista 
verduras.append("zanahoria")

#agrega un elemento en uan psoscion especifica
verduras.insert(2,"lechuga")

#elimina la primera aparecion de un elemento en la lista
verduras.remove("papa")

#elimina y devuelve el elemento en una posicion especifica

verdura_eliminada = verduras.pop(1)

#ordena los elemento en orden ascedente
verduras.sort()

#inverte ele orde de los elementos
verduras.reverse()

#las tuplas no se pueden modificar unas vez creada
punto = (3, 2, 1)
print(punto[2])

#diccionario 
persona = {"nombre": "juan", "edad": 23, "ciudad": "Comodoro"}
print(persona["nombre"])