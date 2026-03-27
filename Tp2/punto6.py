materias = ["IA", "Programacion", "Base De Datos", "Redes", "Matematica", "Fisica", "Quimica"]
aprobadas = []
desaprobadas = []
for preg in materias:
    respuesta = int(input(f"Ingrese la nota de {preg}: "))
    if respuesta <= 6:
        desaprobadas.append(preg)
    else:
        aprobadas.append(preg)

materias.clear()

print("---------------------------------")
print("MATERIAS QUE DEBE VOVLER A RENDIR")
print(desaprobadas)
print("---------------------------------")
print("MATERIAS APROBADAS")
print(aprobadas)


