from collections import deque

def bfs(graph, start_node):
    if not graph.has_node(start_node):
        return []

    visited = set([start_node])
    queue = deque([start_node]) 
    
    caminho_explorado = []

    while queue:
        current = queue.popleft()
        caminho_explorado.append(current)

        for neighbor in graph.neighbors(current):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)

    return caminho_explorado