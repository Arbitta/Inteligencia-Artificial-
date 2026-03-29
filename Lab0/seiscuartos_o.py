import entornos_o

class SeisCuartos(entornos_o.Entorno):
    INDICE = {
        "A": 1, "B": 2, "C": 3,
        "D": 4, "E": 5, "F": 6       
    }
    
    def __init__(self, x0=["A","sucio","sucio","sucio","sucio","sucio","sucio"]):
        self.x = x0[:]
        self.desempeño =0
    
    def acción_legal(self, acción):
        robot = self.x[0]
        if acción not in ("ir_Derecha", "ir_Izquierda", "subir", "bajar", "limpiar", "nada"):
            return False
        
        if acción == "subir":
            return robot in ("A","C") #ubicacion
        if acción == "bajar":
            return robot == "E"
        if acción == "ir_Izquierda":
            return robot not in ("A", "D")
        if acción == "ir_Derecha":
            return robot not in ("C", "F")
        
        return True
    
    
    def transición(self, acción):
        if not self.acción_legal(acción):
            raise ValueError ("Accion invalida")
        
        robot = self.x[0]
        
        match acción:
            case "limpiar":
                self.limpiar(robot)
            case "ir_Izquierda":
                self.mover_izquierda(robot)
            case "ir_Derecha":
                self.mover_derecha(robot)
            case "subir":
                self.subir(robot)
            case "bajar":
                self.bajar()
            case "nada":
                #consultar
                pass
    
    def percepción(self):
        robot = self.x[0]
        return robot, self.x[self.INDICE[robot]]
    
    def mover_derecha(self, robot):
        self.desempeño -=2
        if robot == "A":
            self.x[0] = "B"
        elif robot == "B":
            self.x[0] = "C"
        elif robot == "D":
            self.x[0] = "E"
        elif robot == "E":
            self.x[0] = "F"
    
    def mover_izquierda(self, robot):
        self.desempeño -=2
        if robot == "B":
            self.x[0] = "A"
        elif robot == "C":
            self.x[0] = "B"
        elif robot == "E":
            self.x[0] = "D"
        elif robot == "F":
            self.x[0] = "E"
    
    def subir (self, robot):
        self.desempeño -=3
        if robot == "A":
            self.x[0] = "D"
        elif robot == "C":
            self.x[0] = "F"
    
    def bajar (self):
        self.desempeño -= 3 
        self.x[0] = "B"
    
    def limpiar(self, robot):
        self.desempeño -= 1
        self.x[self.INDICE[robot]] = "limpio"