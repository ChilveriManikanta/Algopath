"""
Graph data structure for AlgoPath.

Implemented from scratch using an adjacency list (a dict of dicts), rather
than relying on a library graph type, so the underlying representation used
by the search algorithms is fully transparent.
"""

from collections import defaultdict


class Graph:
    """A weighted graph backed by an adjacency-list representation.

    Nodes can be any hashable value (str, int, ...). Edges are stored as
    ``adjacency[u][v] = weight``. By default the graph is undirected, i.e.
    adding an edge (u, v) also adds (v, u).
    """

    def __init__(self, directed: bool = False):
        self.directed = directed
        self.adjacency: dict[str, dict[str, float]] = defaultdict(dict)

    def add_node(self, node: str) -> None:
        # Touching the defaultdict entry is enough to register the node,
        # even if it ends up with no edges.
        _ = self.adjacency[node]

    def add_edge(self, u: str, v: str, weight: float = 1.0) -> None:
        if weight < 0:
            raise ValueError("AlgoPath's algorithms assume non-negative edge weights.")
        self.adjacency[u][v] = weight
        if not self.directed:
            self.adjacency[v][u] = weight
        else:
            # Ensure v is still registered as a node even with no out-edges.
            self.add_node(v)

    def neighbors(self, node: str):
        return self.adjacency[node].items()

    def nodes(self):
        return list(self.adjacency.keys())

    def edges(self):
        seen = set()
        result = []
        for u, nbrs in self.adjacency.items():
            for v, w in nbrs.items():
                key = (u, v) if self.directed else tuple(sorted((u, v)))
                if key not in seen:
                    seen.add(key)
                    result.append((u, v, w))
        return result

    def node_count(self) -> int:
        return len(self.adjacency)

    def edge_count(self) -> int:
        return len(self.edges())

    @classmethod
    def random_graph(cls, num_nodes: int, edge_probability: float = 0.15,
                      min_weight: int = 1, max_weight: int = 20, seed: int | None = None):
        """Generate a random connected weighted graph for benchmarking."""
        import random
        rng = random.Random(seed)
        g = cls(directed=False)
        node_names = [f"N{i}" for i in range(num_nodes)]
        for n in node_names:
            g.add_node(n)

        # First guarantee connectivity with a random spanning chain.
        shuffled = node_names[:]
        rng.shuffle(shuffled)
        for a, b in zip(shuffled, shuffled[1:]):
            g.add_edge(a, b, rng.randint(min_weight, max_weight))

        # Then sprinkle extra random edges.
        for i, a in enumerate(node_names):
            for b in node_names[i + 1:]:
                if a in g.adjacency and b in g.adjacency[a]:
                    continue
                if rng.random() < edge_probability:
                    g.add_edge(a, b, rng.randint(min_weight, max_weight))
        return g
