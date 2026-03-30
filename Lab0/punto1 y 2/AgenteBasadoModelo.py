import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

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
        
        match robot:
            case "A":
                if self.modelo[SeisCuartos.INDICE["B"]] == "sucio":
                    return "ir_Derecha"
                return "subir"
            
            case "B":
                if self.modelo[SeisCuartos.INDICE["A"]] == "sucio":
                    return "ir_Izquierda"
                if self.modelo[SeisCuartos.INDICE["C"]] == "sucio":
                    return "ir_Derecha"

            case "C":
                if self.modelo[SeisCuartos.INDICE["B"]] == "sucio":
                    return "ir_Izquierda"
                return "subir"
            
            case "D":
                return "ir_Derecha"
            
            case "E":
                if self.modelo[SeisCuartos.INDICE["D"]] == "sucio":
                    return "ir_Izquierda"
                
                if self.modelo[SeisCuartos.INDICE["F"]] == "sucio":
                    return "ir_Derecha"
                return "bajar"
            
            case "F":
                return "ir_Izquierda"
            
        return "nada"