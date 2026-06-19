def kruskal_mst(graph):
    parent = {node: node for node in graph.nodes()}
    rank = {node: 0 for node in graph.nodes()}

    def find(item):
        if parent[item] == item:
            return item
        else:
            parent[item] = find(parent[item])
            return parent[item]

    def union(set1, set2):
        root1 = find(set1)
        root2 = find(set2)

        if root1 != root2:
            if rank[root1] > rank[root2]:
                parent[root2] = root1
            elif rank[root1] < rank[root2]:
                parent[root1] = root2
            else:
                parent[root2] = root1
                rank[root1] += 1

    mst_edges = []
    
    all_edges = set()
    for u in graph.nodes():
        for v in graph.neighbors(u):
            all_edges.add(frozenset([u, v]))

    
    for edge in all_edges:
        nodes = list(edge)
        if len(nodes) == 1: 
            continue
            
        u, v = nodes[0], nodes[1]

        if find(u) != find(v):
            union(u, v)
            mst_edges.append((u, v))

    return mst_edges