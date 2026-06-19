def floyd_warshall(graph, limit_nodes=300):
    nodes = list(graph.nodes())
    
    if len(nodes) > limit_nodes:
        print(f"AVISO: Grafo com {len(nodes)} nós. Floyd-Warshall O(V^3) demorará muito.")
        print(f"Limitando a análise aos primeiros {limit_nodes} nós para evitar travamento.")
        nodes = nodes[:limit_nodes]

    distances = {u: {v: float('infinity') for v in nodes} for u in nodes}

    for node in nodes:
        distances[node][node] = 0

    for u in nodes:
        for v in graph.neighbors(u):
            if v in distances[u]: 
                distances[u][v] = 1

    for k in nodes:
        for i in nodes:
            for j in nodes:
                if distances[i][k] + distances[k][j] < distances[i][j]:
                    distances[i][j] = distances[i][k] + distances[k][j]

    return distances