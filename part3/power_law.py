import matplotlib.pyplot as plt

def plot_power_law_verification(graph, degree_type="total"):
    """
    Calcula a probabilidade P(k) e plota o gráfico em escala Log-Log 
    para verificar a existência de uma Lei de Potência.
    """
    print(f"\nGerando gráfico Log-Log para graus do tipo: '{degree_type}'...")
    

    dist = graph.degree_distribution(degree_type)
    
    total_nodes = graph.number_of_nodes()
    
    x_k = []      
    y_pk = []      
    

    for k, count in dist.items():
        if k > 0:  
            x_k.append(k)
            y_pk.append(count / total_nodes)
            
    plt.figure(figsize=(10, 6))
    
    plt.scatter(x_k, y_pk, color='royalblue', alpha=0.6, edgecolors='black', linewidth=0.5)
    
    plt.xscale('log')
    plt.yscale('log')
    
    plt.title(f"Verificação de Lei de Potência (Grau {degree_type.capitalize()})\nEscala Log-Log", fontsize=14, fontweight='bold')
    plt.xlabel("Grau do Vértice $k$ (Log)", fontsize=12)
    plt.ylabel("Probabilidade $P(k)$ (Log)", fontsize=12)
    
    plt.grid(True, which="both", ls="--", alpha=0.3)
    
    plt.tight_layout()
    plt.show()
