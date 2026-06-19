def tarjan_scc(graph):
    index_counter = [0]
    indices = {}
    lowlinks = {}
    on_stack = set()
    stack = []
    sccs = []

    def strongconnect(node):
        indices[node] = index_counter[0]
        lowlinks[node] = index_counter[0]
        index_counter[0] += 1
        stack.append(node)
        on_stack.add(node)

        for neighbor in graph.neighbors(node):
            if neighbor not in indices:

                strongconnect(neighbor)
                lowlinks[node] = min(lowlinks[node], lowlinks[neighbor])
            elif neighbor in on_stack:
                lowlinks[node] = min(lowlinks[node], indices[neighbor])

        if lowlinks[node] == indices[node]:
            scc = []
            while True:
                w = stack.pop()
                on_stack.remove(w)
                scc.append(w)
                if w == node:
                    break
            sccs.append(scc)

    for node in graph.nodes():
        if node not in indices:
            strongconnect(node)

    return sccs