def dfs(graph, start_node):
    if not graph.has_node(start_node):
        return []

    visited = set()
    stack = [start_node] 
    
    caminho_explorado = []

    while stack:
        current = stack.pop()

        if current not in visited:
            visited.add(current)
            caminho_explorado.append(current)


            for neighbor in reversed(list(graph.neighbors(current))):
                if neighbor not in visited:
                    stack.append(neighbor)

    return caminho_explorado