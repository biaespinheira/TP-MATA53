from urllib.parse import unquote
from directed_graph import DirectedGraph


class GraphLoader:

    @staticmethod
    def load(
        articles_path: str,
        links_path: str
    ) -> DirectedGraph:

        graph = DirectedGraph()

        with open(articles_path, "r", encoding="utf-8") as file:
            for line in file:
                article = line.strip()

                if not article or article.startswith("#"):
                    continue

                graph.add_node(unquote(article))

        with open(links_path, "r", encoding="utf-8") as file:
            for line in file:
                line = line.strip()

                if not line or line.startswith("#"):
                    continue

                source, target = line.split("\t")

                graph.add_edge(
                    unquote(source),
                    unquote(target)
                )

        return graph
    
if __name__ == "__main__":
    graph = GraphLoader.load(
        "wikispeedia_paths-and-graph/articles.tsv",
        "wikispeedia_paths-and-graph/links.tsv"
    )

    print(graph)

    article = "Åland"

    print(f"\nVizinhos de '{article}':")
    print(graph.neighbors(article))
