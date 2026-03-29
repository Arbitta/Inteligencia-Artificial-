import entornos_o
from seiscuartos_o import SeisCuartos
from random import choice

class AgenteAleatorio(entornos_o.Agente):
    def __init__(self):
        self.acciones = [
            "ir_Derecha",
            "ir_Izquierda",
            "subir",
            "bajar",
            "limpiar",
            "nada"
        ]
    
    def programa(self, percepcion):
        robot, _ = percepcion

        acciones = ["limpiar", "nada"]  # siempre posibles

        # movimientos horizontales
        if robot not in ("A", "D"):
            acciones.append("ir_Izquierda")
        if robot not in ("C", "F"):
            acciones.append("ir_Derecha")

        # subir
        if robot in ("A", "C"):
            acciones.append("subir")

        # bajar
        if robot == "E":
            acciones.append("bajar")

        return choice(acciones)