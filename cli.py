"""
AlgoPath CLI — compute and visualize shortest paths with BFS, DFS, and Dijkstra.

Usage examples:
    python -m algopath.cli --start Hyderabad --goal Chennai
    python -m algopath.cli --start Hyderabad --goal Chennai --algo dijkstra
    python -m algopath.cli --benchmark
    python -m algopath.cli --random 40 --start N0 --goal N39
"""

import argparse
import os

from .algorithms import ALGORITHMS
from .benchmark import run_benchmark, print_benchmark_table
from .graph import Graph
from .sample_data import build_sample_graph
from .visualizer import draw_graph


def print_result_table(results):
    print(f"\n{'Algorithm':<10} {'Found':<7} {'Cost':<8} {'Nodes Expanded':<16} {'Complexity':<16} Path")
    print("-" * 90)
    for r in results:
        path_str = " -> ".join(r.path) if r.found else "(no path)"
        print(f"{r.algorithm:<10} {str(r.found):<7} {r.cost:<8} {r.operations:<16} {r.complexity:<16} {path_str}")


def main():
    parser = argparse.ArgumentParser(description="AlgoPath: graph-based route optimizer")
    parser.add_argument("--start", type=str, help="Start node")
    parser.add_argument("--goal", type=str, help="Goal node")
    parser.add_argument("--algo", choices=list(ALGORITHMS.keys()) + ["all"], default="all",
                         help="Which algorithm to run (default: all, for comparison)")
    parser.add_argument("--random", type=int, metavar="N",
                         help="Use a random graph with N nodes instead of the sample city graph")
    parser.add_argument("--benchmark", action="store_true",
                         help="Run the runtime/operations benchmark across graph sizes and exit")
    parser.add_argument("--out-dir", type=str, default="output",
                         help="Directory to save visualization PNGs into")
    args = parser.parse_args()

    if args.benchmark:
        print("Running benchmark across graph sizes (10 -> 400 nodes)...\n")
        rows = run_benchmark()
        print_benchmark_table(rows)
        return

    if args.random:
        graph = Graph.random_graph(args.random, seed=1)
    else:
        graph = build_sample_graph()

    nodes = graph.nodes()
    start = args.start or nodes[0]
    goal = args.goal or nodes[-1]

    if start not in graph.adjacency:
        raise SystemExit(f"Start node '{start}' not found. Available nodes: {nodes}")
    if goal not in graph.adjacency:
        raise SystemExit(f"Goal node '{goal}' not found. Available nodes: {nodes}")

    print(f"Graph: {graph.node_count()} nodes, {graph.edge_count()} edges")
    print(f"Finding path from '{start}' to '{goal}'...")

    algos_to_run = ALGORITHMS.items() if args.algo == "all" else [(args.algo, ALGORITHMS[args.algo])]
    results = [fn(graph, start, goal) for _name, fn in algos_to_run]
    print_result_table(results)

    os.makedirs(args.out_dir, exist_ok=True)
    for r in results:
        out_path = os.path.join(args.out_dir, f"{r.algorithm.lower()}_path.png")
        draw_graph(graph, r, start, goal, out_path)
        print(f"Saved visualization -> {out_path}")


if __name__ == "__main__":
    main()
