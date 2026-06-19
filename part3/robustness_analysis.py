import random
import matplotlib.pyplot as plt

from directed_graph import DirectedGraph

def extract_subgraph_excluding(graph, nodes_to_exclude):
    """Cria um novo grafo excluindo uma lista específica de vértices."""
    from collections import defaultdict 
    
    subgraph = DirectedGraph() 
    exclude_set = set(nodes_to_exclude)
    
    for node in graph.nodes():
        if node not in exclude_set:
            subgraph.add_node(node)
            
    for node in subgraph.nodes():
        for neighbor in graph.neighbors(node):
            if neighbor not in exclude_set:
                subgraph.add_edge(node, neighbor)
                
    return subgraph

def run_robustness_analysis(graph, num_simulations=30, remove_pct=0.05):
    """
    Executa os testes de falha aleatória e ataque direcionado,
    e plota os boxplots das 4 métricas exigidas.
    """
    n_total = graph.number_of_nodes()
    r = int(n_total * remove_pct) 
    
    print(f"\nIniciando Análise de Robustez (Removendo {r} vértices de {n_total})")
    
    results_random = {'A': [], 'B': [], 'C': [], 'D': []}
    
    print(f"-> Executando {num_simulations} simulações de falha aleatória...")
    nos_originais = list(graph.nodes())
    
    for i in range(num_simulations):
        nodes_to_remove = random.sample(nos_originais, r)
        sub_g = extract_subgraph_excluding(graph, nodes_to_remove)
        
        wccs = sub_g.weakly_connected_components()
        results_random['B'].append(len(wccs))
        
        if wccs:
            largest_wcc = max(wccs, key=len)
            results_random['A'].append(len(largest_wcc))
            
            dist_media = sub_g.average_shortest_path_length_sample(largest_wcc, sample_size=50)
            results_random['C'].append(dist_media)
        else:
            results_random['A'].append(0)
            results_random['C'].append(0)
            
        isolados = sum(1 for node in sub_g.nodes() if sub_g.total_degree(node) == 0)
        frac_isolados = isolados / sub_g.number_of_nodes() if sub_g.number_of_nodes() > 0 else 0
        results_random['D'].append(frac_isolados)

    print("-> Executando ataque direcionado (Removendo 5% Top Hubs)...")
    
    degrees = {node: graph.total_degree(node) for node in nos_originais}
    
    sorted_nodes = sorted(degrees.items(), key=lambda item: item[1], reverse=True)
    top_hubs_to_remove = [node for node, deg in sorted_nodes[:r]]
    
    sub_g_targeted = extract_subgraph_excluding(graph, top_hubs_to_remove)
    
    wccs_t = sub_g_targeted.weakly_connected_components()
    metric_b_t = len(wccs_t)
    
    if wccs_t:
        largest_wcc_t = max(wccs_t, key=len)
        metric_a_t = len(largest_wcc_t)
        metric_c_t = sub_g_targeted.average_shortest_path_length(largest_wcc_t)
    else:
        metric_a_t = 0
        metric_c_t = 0
        
    isolados_t = sum(1 for node in sub_g_targeted.nodes() if sub_g_targeted.total_degree(node) == 0)
    metric_d_t = isolados_t / sub_g_targeted.number_of_nodes() if sub_g_targeted.number_of_nodes() > 0 else 0


    print("-> Gerando Boxplots...")
    fig, axs = plt.subplots(2, 2, figsize=(12, 10))
    fig.suptitle('Análise de Robustez: Remoção de 5% dos Vértices', fontsize=16, fontweight='bold')

    def plot_metric(ax, random_data, targeted_val, title, ylabel):
        bp = ax.boxplot([random_data], positions=[1], widths=0.4, patch_artist=True)
        for box in bp['boxes']:
            box.set(facecolor='lightblue')
            
        ax.scatter([2], [targeted_val], color='red', s=100, zorder=3, label='Ataque Direcionado')
        
        ax.set_xticks([1, 2])
        ax.set_xticklabels(['Aleatória\n(30 Simulações)', 'Direcionada\n(Top 5% Hubs)'])
        ax.set_title(title)
        ax.set_ylabel(ylabel)
        ax.grid(axis='y', linestyle='--', alpha=0.7)

    plot_metric(axs[0, 0], results_random['A'], metric_a_t, 
                'Métrica A: Tamanho da Maior Componente ($S$)', 'Número de Vértices')

    plot_metric(axs[0, 1], results_random['B'], metric_b_t, 
                'Métrica B: Número de Componentes ($c$)', 'Quantidade de Componentes')

    plot_metric(axs[1, 0], results_random['C'], metric_c_t, 
                'Métrica C: Comprimento Médio dos Caminhos', 'Distância (Saltos)')

    plot_metric(axs[1, 1], results_random['D'], metric_d_t, 
                'Métrica D: Fração de Nós Isolados', 'Fração do Total (%)')

    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    plt.show()