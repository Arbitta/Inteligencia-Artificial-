import entornos_o
from seiscuartos_o import SeisCuartos
from AgenteAleatorio import AgenteAleatorio
from AgenteBasadoModelo import AgenteBasadoModelo

def comparar_agentes():
    
    print("\nAgente Aleatorio (100 pasos)\n")
    entorno1 = SeisCuartos()
    agente1 = AgenteAleatorio()
    
    _, _, desempeño1 = entornos_o.simulador(entorno1, agente1, pasos=100)
    
    print("Desempeño final agente aleatorio:", desempeño1[-1])
    
    
    print("\n Agente con Modelo (100 pasos)\n")
    entorno2 = SeisCuartos()
    agente2 = AgenteBasadoModelo()
    
    _, _, desempeño2 = entornos_o.simulador(entorno2, agente2, pasos=100)
    
    print("Desempeño final de Agente Basado en Modelo:", desempeño2[-1])

if __name__ == "__main__":
    comparar_agentes()