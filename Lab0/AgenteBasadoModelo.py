import entornos_o
from seiscuartos_o import SeisCuartos

class AgenteBasadoModelo (entornos_o.Agente):
    def __init__(self):
        self.modelo = ["A", "sucio", "sucio", "sucio", "sucio","sucio", "sucio"]
    
    def programa(self, percepcion):
        robot, situacion = percepcion

        self.modelo[0] = robot
        self.modelo[SeisCuartos.INDICE[robot]] = situacion

        if all(x == "limpio" for x in self.modelo[1:]):
            return "nada"

        if situacion == "sucio":
            return "limpiar"
        
        if robot == "A" and self.modelo[SeisCuartos.INDICE["D"]] == "sucio":
            return "subir"
        if robot == "C" and self.modelo[SeisCuartos.INDICE["F"]] == "sucio":
            return "subir"

        if robot == "E" and self.modelo[SeisCuartos.INDICE["B"]] == "sucio":
            return "bajar"

        if robot not in ("C", "F"):
            return "ir_Derecha"

        return "nada"