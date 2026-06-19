from collections import deque
import statistics
import math

def calcular_estatisticas(tempos, nome_algoritmo):
    """Função auxiliar para imprimir Média, Desvio Padrão e IC seguindo a regra estatística."""
    n = len(tempos)
    
    if n == 0:
        return
        
    media = statistics.mean(tempos)
    desvio = statistics.stdev(tempos) if n > 1 else 0.0
    
    if n >= 30:
        valor_critico = 1.96
        distribuicao_usada = "Normal (Z)"
    else:
        valor_critico = 2.262 if n == 10 else 2.262 
        distribuicao_usada = "t-Student"

    margem_erro = valor_critico * (desvio / math.sqrt(n))
    limite_inf = media - margem_erro
    limite_sup = media + margem_erro

    print(f"{nome_algoritmo} ({n} execuções) -> Usou {distribuicao_usada}:")
    print(f"  -> Média: {media:.6f} segundos")
    print(f"  -> Desvio Padrão: {desvio:.6f} segundos")
    print(f"  -> Intervalo de Confiança (95%): [{limite_inf:.6f}s, {limite_sup:.6f}s]\n")


def bfs_distances(start, adjacency):

    distances = {start: 0}

    queue = deque([start])

    while queue:

        node = queue.popleft()

        for neighbor in adjacency[node]:

            if neighbor not in distances:

                distances[neighbor] = distances[node] + 1

                queue.append(neighbor)

    return distances

def dfs_finish_order(start, adjacency_list, visited, finish_order):
    stack = [(start, False)]

    while stack:
        node, processed = stack.pop()

        if processed:
            finish_order.append(node)
            continue

        if node in visited:
            continue

        visited.add(node)

        stack.append((node, True))

        for neighbor in adjacency_list.get(node, set()):
            if neighbor not in visited:
                stack.append((neighbor, False))

def dfs_transpose_size(start, transpose, visited):

    stack = [start]
    size = 0

    while stack:

        node = stack.pop()

        if node in visited:
            continue

        visited.add(node)
        size += 1

        for neighbor in transpose[node]:
            if neighbor not in visited:
                stack.append(neighbor)

    return size

def dfs_transpose_component(start, transpose, visited):

    stack = [start]
    component = set()

    while stack:

        node = stack.pop()

        if node in visited:
            continue

        visited.add(node)
        component.add(node)

        for neighbor in transpose[node]:
            if neighbor not in visited:
                stack.append(neighbor)

    return component