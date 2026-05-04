### En una mesa se encuentran dos jarras, una con capacidad para tres litros 
##(llamada tres) y otra con capacidad para 4 litros (llamada cuatro). Inicialmente, 
##tres y cuatro están vacías. Cualquiera de ellas puede llenarse con el agua de 
##una canilla G. Asimismo, el contenido de las jarras se puede vaciar en una pila 
##P. También es posible verter el agua de una jarra en la otra. No se dispone de 
##dispositivos de medición adicionales. Se trata de encontrar una secuencia de 
##operadores que deje exactamente dos litros de agua en cuatro. 
## a. Modele el problema como un problema de búsqueda 
## b. Encuentre una solución al problema utilizando búsqueda en amplitud 

class EstadoJarras():
    def __init__(self, Jtres):