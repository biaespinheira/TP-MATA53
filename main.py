import time
import random
from graph_loader import GraphLoader
from directed_graph import DirectedGraph
from part2.euclerian_check import check_eulerian_status
from part2.bfs import bfs as bfs
from part2.dfs import dfs as dfs
from part2.dijkstra import dijkstra
from part2.bellman_ford import bellman_ford
from part2.tarjan import tarjan_scc
from part2.kruskal_mst import kruskal_mst
from part2.floyd_warshall import floyd_warshall
from part3.robustness_analysis import run_robustness_analysis
from part3.small_world_metrics import calculate_small_world_metrics
from part3.power_law import plot_power_law_verification
from utils import calcular_estatisticas
import sys

sys.setrecursionlimit(10000)


if __name__ == "__main__":
    print("="*60)
    print(" CARREGANDO DADOS")
    print("="*60)
    
    graph_completo = GraphLoader.load(
        "wikispeedia_paths-and-graph/articles.tsv",
        "wikispeedia_paths-and-graph/links.tsv"
    )

    # =================================================================
    # PARTE I - ANÁLISE ESTRUTURAL
    # =================================================================
    print("\n" + "="*60)
    print(" PARTE I - ANÁLISE ESTRUTURAL DO GRAFO")
    print("="*60)
    
    # 1 e 2. Vértices e Arestas
    print(f"1. Número de vértices: {graph_completo.number_of_nodes()}")
    print(f"2. Número de arestas: {graph_completo.number_of_edges()}")

    # 3. Graus (Min, Max, Médio)
    out_stats = graph_completo.degree_statistics("out")
    in_stats = graph_completo.degree_statistics("in")
    print("\n3. Grau mínimo, máximo e médio:")
    print(f"   - Saída   -> Min: {out_stats['min']} | Max: {out_stats['max']} | Médio: {out_stats['avg']:.2f}")
    print(f"   - Entrada -> Min: {in_stats['min']} | Max: {in_stats['max']} | Médio: {in_stats['avg']:.2f}")

    # 4. Distribuição de Graus
    print("\n4. Distribuição de graus:")
    dist_in = graph_completo.degree_distribution("in")
    dist_out = graph_completo.degree_distribution("out")
    print(f"   - Frequências de Entrada calculadas ({len(dist_in)} graus distintos).")
    print(f"   - Frequências de Saída calculadas ({len(dist_out)} graus distintos).")
    print("   -> Abrindo Histograma Linear (Grau Total) para visualização...")
    # Chama o método da classe que você acabou de adicionar para plotar as barras
    graph_completo.plot_degree_histogram(degree_type="total")

    # 5. Densidade
    print(f"\n5. Densidade: {graph_completo.density():.6f}")

    # 6. Número de Componentes Conexas
    scc = graph_completo.strongly_connected_components()
    print(f"\n6. Número de componentes conexas (SCCs): {len(scc)}")

    # 7. Tamanho de cada Componente
    scc_sizes = sorted([len(c) for c in scc], reverse=True)
    media_demais = sum(scc_sizes[1:]) / (len(scc) - 1) if len(scc) > 1 else 0
    print("7. Tamanho de cada componente:")
    print(f"   - Maior Componente Conexa: {scc_sizes[0]} vértices")
    print(f"   - Demais {len(scc)-1} componentes possuem média de {media_demais:.2f} vértices cada.")

    print("\n" + "-"*60)
    print(" [!] EXTRAINDO MAIOR COMPONENTE PARA MÉTRICAS DE DISTÂNCIA [!]")
    print("-"*60)
    grafo_gigante = graph_completo.extract_largest_component(connection_type="strong")

    # 8 e 9. Diâmetro e Raio
    print("\n8 e 9. Calculando Diâmetro e Raio (na Componente Gigante)...")
    diameter, radius = grafo_gigante.diameter_and_radius(grafo_gigante.nodes())
    print(f"   - Diâmetro: {diameter}")
    print(f"   - Raio: {radius}")

    # 10. Comprimento médio dos caminhos
    print("\n10. Comprimento médio dos caminhos (Amostragem Rápida - 50 nós)...")
    L = grafo_gigante.average_shortest_path_length_sample(grafo_gigante.nodes(), sample_size=50)
    print(f"   - Comprimento médio: {L:.4f} saltos")

    # 11. Coeficiente de Clusterização
    print("\n11. Coeficiente de clusterização médio:")
    C = grafo_gigante.average_clustering_coefficient()
    print(f"   - Coeficiente: {C:.6f}")

    # 12. Número de Triângulos
    print("\n12. Número de triângulos:")
    triangles = grafo_gigante.number_of_triangles()
    print(f"   - Total de triângulos: {triangles}")

    # 13. Visualização do Grafo
    print("\n13. Visualização do grafo:")
    print("   -> Abrindo janela com amostra reduzida (50 nós)...")
    grafo_gigante.plot_graph(max_nodes=50)
    

    # =================================================================
    # PARTE II - ALGORITMOS DA DISCIPLINA (ANÁLISE ESTATÍSTICA)
    # =================================================================
    print("\n" + "="*60)
    print(" PARTE II - DESEMPENHO DOS ALGORITMOS")
    print("="*60)

    NUM_EXECUCOES = 30
    print(f"Iniciando bateria de testes com {NUM_EXECUCOES} execuções para cada algoritmo...\n")

    nos_validos = list(grafo_gigante.nodes())
    

    tempos_bfs = []
    tempos_dfs = []
    tempos_euler = []
    tempos_dijkstra = []
    tempos_bellman = []
    tempos_tarjan = []
    tempos_kruskal = []


    for i in range(NUM_EXECUCOES):
        start_node = random.choice(nos_validos)

        inicio_bfs = time.time()
        _ = bfs(grafo_gigante, start_node)
        tempos_bfs.append(time.time() - inicio_bfs)

        inicio_dfs = time.time()
        _ = dfs(grafo_gigante, start_node)
        tempos_dfs.append(time.time() - inicio_dfs)

        inicio_euler = time.time()
        _ = check_eulerian_status(grafo_gigante) 
        tempos_euler.append(time.time() - inicio_euler)

        inicio_dijkstra = time.time()
        _ = dijkstra(grafo_gigante, start_node)
        tempos_dijkstra.append(time.time() - inicio_dijkstra)


        inicio_tarjan = time.time()
        _ = tarjan_scc(grafo_gigante)
        tempos_tarjan.append(time.time() - inicio_tarjan)


        inicio_kruskal = time.time()
        _ = kruskal_mst(grafo_gigante)
        tempos_kruskal.append(time.time() - inicio_kruskal)


    print("\n--- RESULTADOS ESTÁTICOS DA MAIOR COMPONENTE ---")
    calcular_estatisticas(tempos_bfs, "Busca em Largura (BFS)")
    calcular_estatisticas(tempos_dfs, "Busca em Profundidade (DFS)")
    calcular_estatisticas(tempos_euler, "Verificação de Eulerianidade")
    calcular_estatisticas(tempos_dijkstra, "Dijkstra (Peso 1)")
    calcular_estatisticas(tempos_tarjan, "Algoritmo de Tarjan (SCCs)")
    calcular_estatisticas(tempos_kruskal, "Algoritmo de Kruskal (MST)")


    print("\n" + "="*60)
    print(" AVALIAÇÃO ESPECIAL: BELLMAN-FORD E FLOYD-WARSHALL")
    print("="*60)
    print("Devido à alta complexidade O(V*E) e O(V^3), estes algoritmos")
    print("foram testados em subgrafos menores para evitar travamentos.\n")
    
    amostra_bf = nos_validos[:500]
    subgrafo_bf = DirectedGraph()
    for no in amostra_bf:
        subgrafo_bf.add_node(no)
        for vizinho in grafo_gigante.neighbors(no):
            if vizinho in amostra_bf:
                subgrafo_bf.add_edge(no, vizinho)

    print(f"-> Testando Bellman-Ford em subgrafo de {subgrafo_bf.number_of_nodes()} nós...")
    tempos_bellman = []
    EXECS_BF = 30 
    
    for _ in range(EXECS_BF):
        start_node_bf = random.choice(amostra_bf)
        inicio_bellman = time.time()
        _ = bellman_ford(subgrafo_bf, start_node_bf)
        tempos_bellman.append(time.time() - inicio_bellman)

    calcular_estatisticas(tempos_bellman, f"Bellman-Ford (Amostra 500 nós)")


    amostra_fw = nos_validos[:150]
    subgrafo_fw = DirectedGraph()
    for no in amostra_fw:
        subgrafo_fw.add_node(no)
        for vizinho in grafo_gigante.neighbors(no):
            if vizinho in amostra_fw:
                subgrafo_fw.add_edge(no, vizinho)

    print(f"\n-> Testando Floyd-Warshall em subgrafo de {subgrafo_fw.number_of_nodes()} nós...")
    tempos_fw = []
    EXECS_FW = 10 
    
    for _ in range(EXECS_FW):
        inicio_fw = time.time()
        _ = floyd_warshall(subgrafo_fw)
        tempos_fw.append(time.time() - inicio_fw)

    calcular_estatisticas(tempos_fw, f"Floyd-Warshall (Amostra 150 nós)")

    print("\n" + "="*60)
    print(" FIM DA EXECUÇÃO")
    print("="*60)


    # =================================================================
    # PARTE III 
    # =================================================================
    print("\n" + "="*60)
    print(" PARTE III - AVALIAÇÃO DE SMALL-WORLD")
    print("="*60)
    
    nos_da_componente = list(grafo_gigante.nodes())
    resultados_sw = calculate_small_world_metrics(grafo_gigante, nos_da_componente)

    print("\n" + "="*60)
    print(" PARTE III - VERIFICAÇÃO DA LEI DE POTÊNCIA")
    print("="*60)
    
    plot_power_law_verification(grafo_gigante, degree_type="total")

    print("\n" + "="*60)
    print(" PARTE III - ANÁLISE DE ROBUSTEZ")
    print("="*60)
    
    run_robustness_analysis(grafo_gigante, num_simulations=30, remove_pct=0.05)