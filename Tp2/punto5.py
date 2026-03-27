dias_laborales = ["Lunes", "Martes", "Miercoles", "Jueves", "Viernes"]
fin_semana = ["Sabado", "Domingo"]
print(dias_laborales)

dias = dias_laborales + fin_semana
print(dias)
dia = input("Ingrese un dia de la semana: ")

if dia in fin_semana:
    print("Es fin de Semana")
elif dia in dias_laborales:
    print("Es dia laboral")
else:
    print("Dia invalido")