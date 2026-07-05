"""
Benchmark BFS, DFS, and Dijkstra across increasing graph sizes to give an
empirical view of how runtime and operation count scale, alongside their
theoretical Big-O complexity.
"""

import time

from .graph import Graph
from .algorithms import ALGORITHMS


def run_benchmark(sizes=(10, 25, 50, 100, 200, 400), seed: int = 7):
    rows = []
    for n in sizes:
        graph = Graph.random_graph(n, edge_probability=max(0.08, 6 / n), seed=seed)
        nodes = graph.nodes()
        start, goal = nodes[0], nodes[-1]

        row = {"nodes": n, "edges": graph.edge_count()}
        for name, fn in ALGORITHMS.items():
            t0 = time.perf_counter()
            result = fn(graph, start, goal)
            elapsed_ms = (time.perf_counter() - t0) * 1000
            row[name] = {
                "time_ms": round(elapsed_ms, 4),
                "operations": result.operations,
                "found": result.found,
                "cost": result.cost,
            }
        rows.append(row)
    return rows


def print_benchmark_table(rows):
    header = f"{'Nodes':>6} {'Edges':>6} | " + " | ".join(
        f"{name.upper():^24}" for name in ALGORITHMS
    )
    print(header)
    print("-" * len(header))
    for row in rows:
        parts = [f"{row['nodes']:>6} {row['edges']:>6} |"]
        for name in ALGORITHMS:
            d = row[name]
            parts.append(f" {d['time_ms']:>7.3f} ms / {d['operations']:>5} ops |")
        print("".join(parts))


if __name__ == "__main__":
    rows = run_benchmark()
    print_benchmark_table(rows)
