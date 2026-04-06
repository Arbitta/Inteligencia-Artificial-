import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..')) 

import entornos_o
import random
from random import choice

class DosCuartosEstocastico(entornos_o.Entorno):
    def __init__(self, x0=["A", "sucio", "sucio"]):
        self.x = x0[:]
        self.desempeño = 0
    
    def acción_legal(self, acción):
        return acción in ("ir_A", "ir_B", "limpiar", "nada")

    def transición(self, acción):
        if not self.acción_legal(acción):
            raise ValueError("La acción no es legal para este estado")

        robot, a, b = self.x
        if acción is not "nada" or a is "sucio" or b is "sucio":
            self.desempeño -= 1

        if acción is "limpiar":
            
            idx = " AB".find(self.x[0])
            if random.random() < 0.8:
                self.x[idx] = "limpio"

        elif acción is "ir_A":
            if random.random() < 0.9:
                self.x[0] = "A"
                
        elif acción is "ir_B":
            if random.random() < 0.9:
                self.x[0] = "B"

    def percepción(self):
        return self.x[0], self.x[" AB".find(self.x[0])]

class AgenteAleatorio(entornos_o.Agente):
    def __init__(self, acciones):
        self.acciones = acciones

    def programa(self, percepcion):
        return choice(self.acciones)


class AgenteReactivoDoscuartos(entornos_o.Agente):
    """
    Un agente reactivo simple

    """
    def programa(self, percepción):
        robot, situación = percepción
        return ('limpiar' if situación == 'sucio' else
                'ir_A' if robot == 'B' else 'ir_B')


class AgenteReactivoModeloDosCuartos(entornos_o.Agente):
    def __init__(self):
        self.modelo = ["A", "sucio", "sucio"]
    
    def programa(self, percepcion):
        robot, situacion = percepcion
        self.modelo[0] = robot
        self.modelo[' AB'.find(robot)] = situacion
        
        a, b = self.modelo[1], self.modelo[2]
        if a == "limpio" and b == "limpio":
            return "nada"
        
        if situacion == "sucio":
            return "limpiar"
        
        return "ir_A" if robot == "B" else "ir_B"


def test():
    """
    Prueba del entorno y los agentes

    """
    print("Prueba del entorno con un agente aleatorio")
    acciones=['ir_A', 'ir_B', 'limpiar', 'nada']
    entornos_o.simulador(DosCuartosEstocastico(),AgenteAleatorio(acciones),10)

    print("Prueba del entorno con un agente reactivo con modelo")
    entornos_o.simulador(DosCuartosEstocastico(), AgenteReactivoModeloDosCuartos(), 10)


if __name__ == "__main__":
    test()
