def has_eulerian_circuit(graph):
    """
    Verifica se um grafo direcionado possui um Circuito Euleriano.
    Recebe uma instância de DirectedGraph.
    """
    for node in graph.nodes():
        if graph.in_degree(node) != graph.out_degree(node):
            return False

    sccs = graph.strongly_connected_components()
    sccs_with_edges = 0
    
    for component in sccs:
        if any(graph.total_degree(node) > 0 for node in component):
            sccs_with_edges += 1

    return sccs_with_edges <= 1

def has_eulerian_path(graph):
    """
    Verifica se um grafo direcionado possui um Caminho Euleriano.
    Recebe uma instância de DirectedGraph.
    """
    start_nodes = 0
    end_nodes = 0

    for node in graph.nodes():
        out_d = graph.out_degree(node)
        in_d = graph.in_degree(node)

        if out_d - in_d == 1:
            start_nodes += 1
        elif in_d - out_d == 1:
            end_nodes += 1
        elif in_d != out_d:
            return False

    valid_degrees = (start_nodes == 0 and end_nodes == 0) or (start_nodes == 1 and end_nodes == 1)
    if not valid_degrees:
        return False

    wccs = graph.weakly_connected_components()
    wccs_with_edges = 0
    
    for component in wccs:
        if any(graph.total_degree(node) > 0 for node in component):
            wccs_with_edges += 1

    return wccs_with_edges <= 1

def check_eulerian_status(graph):
    """
    Retorna uma string descritiva sobre o status euleriano do grafo.
    Recebe uma instância de DirectedGraph.
    """
    if has_eulerian_circuit(graph):
        return "O grafo possui um Circuito Euleriano (e, portanto, também um Caminho Euleriano)."
    elif has_eulerian_path(graph):
        return "O grafo possui apenas um Caminho Euleriano."
    else:
        return "O grafo não é Euleriano (não possui caminho nem circuito)."