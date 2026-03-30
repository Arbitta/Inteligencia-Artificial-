import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import entornos_o
from dosCuartoCiego import DosCuartosCiego

class AgenteRacional(entornos_o.Agente):
    
    def __init__(self):
        self.modelo = {"pos": "A",
                    "A": "sucio",
                    "B": "sucio"}  # ← diccionario
        self.pos = None
    
    def programa(self, percepcion):
        pos = percepcion
        self.pos = pos
        
        if self.modelo[pos] == "sucio":
            self.modelo[pos] = "limpio"
            return "limpiar"
        
        if self.modelo["A"] == "limpio" and self.modelo["B"] == "limpio":
            return "nada"
        
        if pos == "A":
            return "ir_B"
        else:
            return "ir_A"