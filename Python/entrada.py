nombre = input("Ingrese tu nombre: ")
edad = input("Ingrese su edad: ")

print("Hola, "+ nombre)
print("tiene: " + edad)

archivo = open("datos.txt", "r")
contenido = archivo.read()
print(contenido)
archivo.close()

archivo = open("datos.txt", "w")
archivo.write("Hola, mundo!")
archivo.close()