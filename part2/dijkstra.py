import heapq

def dijkstra(graph, start_node):
    if not graph.has_node(start_node):
        return {}, {}

    distances = {node: float('infinity') for node in graph.nodes()}
    distances[start_node] = 0
    predecessores = {node: None for node in graph.nodes()}

    priority_queue = [(0, start_node)]

    while priority_queue:
        current_distance, current = heapq.heappop(priority_queue)

        if current_distance > distances[current]:
            continue

        for neighbor in graph.neighbors(current):
            weight = 1 
            distance = current_distance + weight

            if distance < distances[neighbor]:
                distances[neighbor] = distance
                predecessores[neighbor] = current
                heapq.heappush(priority_queue, (distance, neighbor))

    return distances, predecessores