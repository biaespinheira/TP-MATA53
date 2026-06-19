def bellman_ford(graph, start_node):
    if not graph.has_node(start_node):
        return {}, {}

    distances = {node: float('infinity') for node in graph.nodes()}
    distances[start_node] = 0
    predecessores = {node: None for node in graph.nodes()}

    nodes = list(graph.nodes())
    
    for _ in range(len(nodes) - 1):
        for node in nodes:
            if distances[node] == float('infinity'):
                continue
                
            for neighbor in graph.neighbors(node):
                weight = 1 
                if distances[node] + weight < distances[neighbor]:
                    distances[neighbor] = distances[node] + weight
                    predecessores[neighbor] = node


    return distances, predecessores
