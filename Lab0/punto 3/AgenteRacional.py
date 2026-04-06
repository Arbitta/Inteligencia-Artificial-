import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import entornos_o
from dosCuartoCiego import DosCuartosCiego

class AgenteRacional(entornos_o.Agente):
    
    def __init__(self):
        self.modelo = {"A": "sucio", "B": "sucio"}  # ← diccionario
    
    def programa(self, percepcion):
        pos = percepcion
        
        if self.modelo[pos] == "sucio":
            self.modelo[pos] = "limpio"
            return "limpiar"
        
        if self.modelo["A"] == "limpio" and self.modelo["B"] == "limpio":
            return "nada"
        
        return "ir_B" if pos == "A" else "ir_A"