"""
Static visualizer for AlgoPath.

Draws the graph using networkx for layout and matplotlib for rendering,
highlighting whichever path was returned by a search algorithm.
"""

import matplotlib
matplotlib.use("Agg")  # headless-safe backend
import matplotlib.pyplot as plt
import networkx as nx

from .graph import Graph
from .algorithms import SearchResult


def draw_graph(graph: Graph, result: SearchResult, start: str, goal: str, out_path: str) -> None:
    G = nx.Graph() if not graph.directed else nx.DiGraph()
    for node in graph.nodes():
        G.add_node(node)
    for u, v, w in graph.edges():
        G.add_edge(u, v, weight=w)

    pos = nx.spring_layout(G, seed=42, k=1.6 / max(len(G.nodes()) ** 0.5, 1))

    path_edges = set()
    path_nodes = set(result.path)
    for a, b in zip(result.path, result.path[1:]):
        path_edges.add((a, b))
        path_edges.add((b, a))

    node_colors = []
    for n in G.nodes():
        if n == start:
            node_colors.append("#2ECC71")   # green start
        elif n == goal:
            node_colors.append("#E74C3C")   # red goal
        elif n in path_nodes:
            node_colors.append("#F5B041")   # orange on-path
        else:
            node_colors.append("#AAB7B8")   # grey other

    edge_colors = []
    edge_widths = []
    for u, v in G.edges():
        if (u, v) in path_edges or (v, u) in path_edges:
            edge_colors.append("#F5B041")
            edge_widths.append(3.0)
        else:
            edge_colors.append("#CCD1D1")
            edge_widths.append(1.0)

    plt.figure(figsize=(9, 7))
    nx.draw_networkx_edges(G, pos, edge_color=edge_colors, width=edge_widths)
    nx.draw_networkx_nodes(G, pos, node_color=node_colors, node_size=550, edgecolors="#2C3E50")
    nx.draw_networkx_labels(G, pos, font_size=9, font_color="#1B2631")
    edge_labels = nx.get_edge_attributes(G, "weight")
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=7)

    title = f"{result.algorithm} — path cost: {result.cost}" if result.found else f"{result.algorithm} — no path found"
    plt.title(title, fontsize=13, fontweight="bold")
    plt.axis("off")
    plt.tight_layout()
    plt.savefig(out_path, dpi=150)
    plt.close()
