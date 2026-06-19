import math

def calculate_small_world_metrics(graph, component_nodes=None):
    """
    Calcula as métricas de Small-World recebendo o objeto grafo externamente.
    Se component_nodes não for fornecido, avalia o grafo inteiro.
    """
    if component_nodes is None:
        component_nodes = list(graph.nodes())

    N = len(component_nodes)
    
    edges_in_component = 0
    for node in component_nodes:
        for neighbor in graph.neighbors(node):
            if neighbor in component_nodes:
                edges_in_component += 1
                
    if N > 0:
        K = edges_in_component / N
    else:
        return None

    if K <= 1:
        print("Aviso: Grau médio muito baixo para análise de Small-World confiável.")
        return None

    print("Calculando L(G) - Comprimento Médio dos caminhos...")
    L_G = graph.average_shortest_path_length(component_nodes)
    
    print("Calculando C(G) - Coeficiente de Clusterização Médio...")
    C_G = graph.average_clustering_coefficient()

    C_random = K / N
    L_random = math.log(N) / math.log(K)

    L_ratio = L_G / L_random
    C_ratio = C_G / C_random
    sigma = C_ratio / L_ratio

    print("\n--- RELATÓRIO SMALL-WORLD ---")
    print(f"Nós (N): {N} | Grau Médio (K): {K:.2f}")
    print(f"L(G) do Grafo: {L_G:.4f}  |  L(rand) Aleatório: {L_random:.4f}")
    print(f"C(G) do Grafo: {C_G:.4f}  |  C(rand) Aleatório: {C_random:.4f}")
    print(f"\nProporção L: {L_ratio:.4f} (Ideal que seja aprox. 1)")
    print(f"Proporção C: {C_ratio:.2f} (Ideal que seja >> 1)")
    print(f"Coeficiente Small-World (Sigma): {sigma:.2f}")
    
    if sigma > 1 and L_ratio < 1.5:
        print("CONCLUSÃO: O grafo APRESENTA fortes propriedades de Small-World.")
    else:
        print("CONCLUSÃO: O grafo NÃO se comporta como um Small-World típico.")

    return {
        "L_G": L_G, "C_G": C_G, 
        "L_rand": L_random, "C_rand": C_random, 
        "sigma": sigma
    }