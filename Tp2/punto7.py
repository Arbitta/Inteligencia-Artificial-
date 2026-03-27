grafo = {
    "Arad": ["Zerind", "Sibiu", "Timisoara"],
    "Zerind": ["Arad", "Oradea"],
    "Oradea": ["Zerind", "Sibiu"],
    "Sibiu": ["Arad", "Oradea", "Fagaras", "Rimnicu"],
    "Timisoara": ["Arad", "Lugoj"],
    "Lugoj": ["Timisoara", "Mehadia"],
    "Mehadia": ["Lugoj", "Drobeta"],
    "Drobeta": ["Mehadia", "Craiova"],
    "Craiova": ["Drobeta", "Rimnicu", "Pitesti"],
    "Rimnicu": ["Sibiu", "Craiova", "Pitesti"],
    "Fagaras": ["Sibiu", "Bucarest"],
    "Pitesti": ["Rimnicu", "Craiova", "Bucarest"],
    "Bucarest": ["Fagaras", "Pitesti", "Giurgiu", "Urziceni"],
    "Giurgiu": ["Bucarest"],
    "Urziceni": ["Bucarest", "Hirsova", "Vaslui"],
    "Hirsova": ["Urziceni", "Eforie"],
    "Eforie": ["Hirsova"],
    "Vaslui": ["Urziceni", "Iasi"],
    "Iasi": ["Vaslui", "Neamt"],
    "Neamt": ["Iasi"]
}

def dfs(grafo, actual, destino, visitados=None):
    if visitados is None:
        visitados = set()
    
    if actual == destino:
        return True
    
    visitados.add(actual)
    
    for vecino in grafo[actual]:
        if vecino not in visitados:
            if dfs(grafo, vecino, destino, visitados):
                return True
    
    return False



print(dfs(grafo, "Bucarest", "Oradea"))   # True
print(dfs(grafo, "Bucarest", "Mehadia"))  # True