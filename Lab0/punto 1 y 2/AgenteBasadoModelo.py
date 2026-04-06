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
                elif self.modelo[SeisCuartos.INDICE["C"]] == "sucio":
                    return "ir_Derecha"
                else:
                    return "subir"             
            case "B":
                if self.modelo[SeisCuartos.INDICE["A"]] == "sucio":
                    return "ir_Izquierda"
                elif self.modelo[SeisCuartos.INDICE["C"]] == "sucio":
                    return "ir_Derecha"
                else:
                    lado_izq = sum(1 for c in ("D", "E") if self.modelo[SeisCuartos.INDICE[c]] == "sucio")
                    lado_der = sum(1 for c in ("E", "F") if self.modelo[SeisCuartos.INDICE[c]] == "sucio")
                    if lado_izq >= lado_der:
                        return "ir_Izquierda"  
                    else:
                        return "ir_Derecha"   #para ver si lo laterales estaban sucios 

            case "C":
                if self.modelo[SeisCuartos.INDICE["B"]] == "sucio":
                    return "ir_Izquierda"
                elif self.modelo[SeisCuartos.INDICE["A"]] == "sucio":
                    return "ir_Izquierda"
                else:
                    return "subir"
            
            case "D":
                if self.modelo[SeisCuartos.INDICE["E"]] == "sucio":
                    return "ir_Derecha"
                elif self.modelo[SeisCuartos.INDICE["F"]] == "sucio":
                    return "ir_Derecha"
                else:
                    return "ir_Derecha"
            
            case "E":
                if self.modelo[SeisCuartos.INDICE["D"]] == "sucio":
                    return "ir_Izquierda"
                if self.modelo[SeisCuartos.INDICE["F"]] == "sucio":
                    return "ir_Derecha"
                return "bajar"
            
            case "F":
                if self.modelo[SeisCuartos.INDICE["E"]] == "sucio":
                    return "ir_Izquierda"
                elif self.modelo[SeisCuartos.INDICE["D"]] == "sucio":
                    return "ir_Izquierda"
                else:
                    return "ir_Izquierda"
            
        return "nada"