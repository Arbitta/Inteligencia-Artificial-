import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import entornos_o
from dosCuartoCiego import DosCuartosCiego
from AgenteRacional import AgenteRacional
from AgenteAleatorio import AgenteAleatorio

def comparar_agentes():
    
    print("\nAgente Aleatorio (10 pasos)\n")
    entorno1 = DosCuartosCiego()
    agente1 = AgenteAleatorio()
    
    _, _, desempeño1 = entornos_o.simulador(entorno1, agente1, pasos=10)
    
    print("Desempeño final agente aleatorio:", desempeño1[-1])
    
    
    print("\n Agente con Modelo (10 pasos)\n")
    entorno2 = DosCuartosCiego()
    agente2 = AgenteRacional()
    
    _, _, desempeño2 = entornos_o.simulador(entorno2, agente2, pasos=10)
    
    print("Desempeño final de Agente Racional:", desempeño2[-1])

if __name__ == "__main__":
    comparar_agentes()