import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import entornos_o

class DosCuartosCiego(entornos_o.Entorno):
    
    def __init__(self, x0 = ["A", "sucio", "sucio"]):
        self.x =  x0 [:]
        self.desempeño = 0
    
    def acción_legal(self, acción):
        return acción in ("ir_A", "ir_B", "limpiar", "nada")
    
    def transición(self, acción):
        if not self.acción_legal(acción):
            raise ValueError("Las accion no es legal para este estado")
            
        robot= self.x

        match acción:
            case "limpiar":
                self.desempeño -= 1
                if robot == "A":
                    self.x[1] = "limpio"
                else:
                    self.x[2] = "limpio"

            case "ir_A":
                self.desempeño -= 1
                self.x[0] = "A"

            case "ir_B":
                self.desempeño -= 1
                self.x[0] = "B"

            case "nada":
                self.desempeño -= 1
    
    def percepción(self):
        return self.x[0]