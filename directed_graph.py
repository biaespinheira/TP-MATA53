from asyncio import graph
import math
import random
from collections import Counter, defaultdict
from utils import bfs_distances, dfs_finish_order, dfs_transpose_component, dfs_transpose_size
from statistics import mean
import networkx as nx
import matplotlib.pyplot as plt
import random

class DirectedGraph:
    def __init__(self):
        self._nodes = set()
        self._adjacency_list = defaultdict(set)
        self._num_edges = 0

    def add_node(self, node: str):
        self._nodes.add(node)

    def add_edge(self, source: str, target: str):
        self.add_node(source)
        self.add_node(target)

        if target not in self._adjacency_list[source]:
            self._adjacency_list[source].add(target)
            self._num_edges += 1

    def nodes(self):
        return self._nodes

    def neighbors(self, node: str):
        return self._adjacency_list.get(node, set())

    def number_of_nodes(self):
        return len(self._nodes)

    def number_of_edges(self):
        return self._num_edges

    def has_node(self, node: str):
        return node in self._nodes
    
    def out_degree(self, node):
        return len(self._adjacency_list.get(node, set()))

    def in_degree(self, node):
        degree = 0

        for neighbors in self._adjacency_list.values():
            if node in neighbors:
                degree += 1

        return degree

    def total_degree(self, node):
        return self.in_degree(node) + self.out_degree(node)
    
    def degree_statistics(self, degree_type="out"):
        if not self._nodes:
            return {
                "min": 0,
                "max": 0,
                "avg": 0
            }

        if degree_type == "out":
            degrees = [self.out_degree(node) for node in self._nodes]

        elif degree_type == "in":
            degrees = [self.in_degree(node) for node in self._nodes]

        elif degree_type == "total":
            degrees = [self.total_degree(node) for node in self._nodes]

        else:
            raise ValueError(
                "degree_type deve ser 'in', 'out' ou 'total'"
            )

        return {
            "min": min(degrees),
            "max": max(degrees),
            "avg": mean(degrees)
        }

    def degree_distribution(self, degree_type="out"):
    
        if degree_type == "out":
            degrees = [
                self.out_degree(node)
                for node in self._nodes
            ]

        elif degree_type == "in":
            degrees = [
                self.in_degree(node)
                for node in self._nodes
            ]

        elif degree_type == "total":
            degrees = [
                self.total_degree(node)
                for node in self._nodes
            ]

        else:
            raise ValueError(
                "degree_type deve ser 'in', 'out' ou 'total'"
            )

        return dict(Counter(degrees))

    def weakly_connected_components(self):

        visited = set()
        components = []

        graph = self.undirected_graph()

        for node in self._nodes:

            if node in visited:
                continue

            component = set()
            stack = [node]

            while stack:

                current = stack.pop()

                if current in visited:
                    continue

                visited.add(current)
                component.add(current)

                for neighbor in graph[current]:
                    if neighbor not in visited:
                        stack.append(neighbor)

            components.append(component)

        return components
    
    def strongly_connected_components(self):

        visited = set()
        finish_order = []

        for node in self._nodes:
            if node not in visited:
                dfs_finish_order(
                    node,
                    self._adjacency_list,
                    visited,
                    finish_order
                )

        transpose = {
            node: set()
            for node in self._nodes
        }

        for source in self._adjacency_list:
            for target in self._adjacency_list[source]:
                transpose[target].add(source)

        visited.clear()

        components = []

        while finish_order:

            node = finish_order.pop()

            if node not in visited:

                component = dfs_transpose_component(
                    node,
                    transpose,
                    visited
                )

                components.append(component)

        return components
    
    def density(self):
        n = self.number_of_nodes()

        if n <= 1:
            return 0.0

        max_edges = n * (n - 1)

        return self._num_edges / max_edges

    def undirected_graph(self):

        graph = {node: set() for node in self._nodes}

        for source in self._adjacency_list:
            for target in self._adjacency_list[source]:

                graph[source].add(target)
                graph[target].add(source)

        return graph

    def average_shortest_path_length(self, component):

        graph = self.undirected_graph()

        total_distance = 0
        total_pairs = 0

        for node in component:

            distances = bfs_distances(node, graph)

            for target in component:

                if target == node:
                    continue

                total_distance += distances[target]
                total_pairs += 1

        return total_distance / total_pairs

    def average_shortest_path_length_sample(self, component, sample_size=50):
        """
        Alternativa rápida: Estima o comprimento médio dos caminhos calculando 
        a distância a partir de uma amostra aleatória de vértices de origem.
        """

        graph = self.undirected_graph()
        
        component_list = list(component)
        
        actual_sample_size = min(sample_size, len(component_list))
        
        sampled_nodes = random.sample(component_list, actual_sample_size)

        total_distance = 0
        total_pairs = 0

        for node in sampled_nodes:
            distances = bfs_distances(node, graph)

            for target in component_list:
                if target == node:
                    continue
                    
                if target in distances:
                    total_distance += distances[target]
                    total_pairs += 1

        if total_pairs == 0:
            return 0.0

        return total_distance / total_pairs
    
    def diameter_and_radius(self, component):

        graph = self.undirected_graph()

        eccentricities = []

        for node in component:

            distances = bfs_distances(node, graph)

            eccentricity = max(
                distances[target]
                for target in component
            )

            eccentricities.append(eccentricity)

        diameter = max(eccentricities)
        radius = min(eccentricities)

        return diameter, radius
    
    def average_clustering_coefficient(self):

        graph = self.undirected_graph()
        total_clustering = 0.0
        n = self.number_of_nodes()

        if n == 0:
            return 0.0

        for node in self._nodes:
            neighbors = list(graph.get(node, set()))
            degree = len(neighbors)

            if degree < 2:
                continue

            edges_between_neighbors = 0
            for i in range(degree):
                for j in range(i + 1, degree):
                    if neighbors[j] in graph.get(neighbors[i], set()):
                        edges_between_neighbors += 1

            possible_edges = degree * (degree - 1)
            clustering_v = (2.0 * edges_between_neighbors) / possible_edges
            total_clustering += clustering_v

        return total_clustering / n

    def number_of_triangles(self):
        graph = self.undirected_graph()
        triangles = 0

        for node in self._nodes:
            neighbors = list(graph.get(node, set()))
            degree = len(neighbors)

            for i in range(degree):
                for j in range(i + 1, degree):
                    if neighbors[j] in graph.get(neighbors[i], set()):
                        triangles += 1

        return triangles // 3
    
    def plot_graph(self, max_nodes=50):

        nx_graph = nx.DiGraph()


        undirected = self.undirected_graph()
        
        start_node = random.choice(list(self._nodes))
        
        sample_nodes = {start_node}
        queue = [start_node]

        while queue and len(sample_nodes) < max_nodes:
            current = queue.pop(0)
            neighbors = undirected.get(current, set())
            
            for neighbor in neighbors:
                if neighbor not in sample_nodes:
                    sample_nodes.add(neighbor)
                    queue.append(neighbor)
                    if len(sample_nodes) >= max_nodes:
                        break

        for source in sample_nodes:
            for target in self._adjacency_list.get(source, set()):
                if target in sample_nodes:
                    nx_graph.add_edge(source, target)

        if nx_graph.number_of_nodes() == 0:
            nx_graph.add_nodes_from(sample_nodes)


        plt.figure(figsize=(12, 8))
        
        pos = nx.spring_layout(nx_graph, seed=42, k=0.5) 

        nx.draw(
            nx_graph, 
            pos, 
            with_labels=True, 
            node_color='lightcoral', 
            node_size=700, 
            edge_color='gray', 
            linewidths=1.0, 
            font_size=9,
            font_weight='bold',
            arrows=True,
            arrowsize=15
        )
        
        plt.title(f"Amostra Conectada (A partir do nó '{start_node}') - {len(sample_nodes)} vértices")
        plt.show()
    
    def extract_largest_component(self, connection_type="strong"):
        """
        Extrai a maior componente conexa do grafo e retorna um novo
        objeto DirectedGraph contendo apenas os nós e arestas dessa componente.
        """
        if connection_type == "weak":
            components = self.weakly_connected_components()
        elif connection_type == "strong":
            components = self.strongly_connected_components()
        else:
            raise ValueError("connection_type deve ser 'weak' ou 'strong'")

        if not components:
            return DirectedGraph()

        largest_component_nodes = max(components, key=len)

        subgraph = DirectedGraph()

        for node in largest_component_nodes:
            subgraph.add_node(node)
            
            for neighbor in self._adjacency_list.get(node, set()):
                if neighbor in largest_component_nodes:
                    subgraph.add_edge(node, neighbor)

        return subgraph
    
    def plot_degree_histogram(self, degree_type="total"):
        """
        Plota a distribuição de graus no formato tradicional (Histograma/Barras)
        usando a escala linear comum.
        """
        print(f"\nGerando Histograma Linear para graus do tipo: '{degree_type}'...")
        
        dist = self.degree_distribution(degree_type)
        
        x_k = list(dist.keys())
        y_count = list(dist.values())
        
        plt.figure(figsize=(10, 6))
        
        plt.bar(x_k, y_count, color='skyblue', edgecolor='black', width=1.0)
        
        plt.title(f"Histograma da Distribuição de Graus ({degree_type.capitalize()})\nEscala Linear Tradicional", fontsize=14, fontweight='bold')
        plt.xlabel("Grau do Vértice $k$", fontsize=12)
        plt.ylabel("Frequência (Número de Vértices)", fontsize=12)
        

        plt.grid(axis='y', linestyle='--', alpha=0.7)
        
        plt.tight_layout()
        plt.show()

    def __str__(self):
        return (
            f"DirectedGraph("
            f"nodes={self.number_of_nodes()}, "
            f"edges={self.number_of_edges()})"
        )