import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import entornos_o
from random import choice

class AgenteAleatorio(entornos_o.Agente):
    
    def __init__(self):
        self.acciones = ["ir_B", "ir_A", "limpiar","nada"]
    
    def programa(self, percepcion):
        return choice(self.acciones)