# AlgoPath: Graph-Based Route Optimizer

A route-optimization engine implemented in **Python and Java** that computes
shortest paths across weighted graphs using three classic algorithms — BFS,
DFS, and Dijkstra — built from scratch (custom adjacency-list graph, and a
hand-rolled binary-heap priority queue in the Python version) rather than
relying on a graph library.

The project exists to demonstrate solid Data Structures & Algorithms
fundamentals: correct graph traversal, shortest-path computation, Big-O
complexity, and empirical benchmarking of how each algorithm scales.

## Why three algorithms?

| Algorithm | Guarantees shortest path? | Complexity        | Notes                                   |
|-----------|---------------------------|--------------------|------------------------------------------|
| BFS       | Only for unweighted graphs | O(V + E)           | Shortest by *edge count*, ignores weights |
| DFS       | No                          | O(V + E)           | Finds *a* path, often not optimal         |
| Dijkstra  | Yes (non-negative weights) | O((V + E) log V)   | Uses a min-priority-queue internally      |

Running all three on the same start/goal pair is the point: it visibly shows
*why* Dijkstra is the right tool for weighted shortest-path problems, while
BFS/DFS solve a different (or looser) version of the problem.

## Project structure

```
algopath/
├── python/
│   ├── algopath/
│   │   ├── graph.py           # Adjacency-list graph (from scratch)
│   │   ├── priority_queue.py  # Binary-heap min-priority-queue (from scratch)
│   │   ├── algorithms.py      # BFS, DFS, Dijkstra
│   │   ├── visualizer.py      # matplotlib/networkx path visualization (PNG)
│   │   ├── benchmark.py       # Runtime & operation-count benchmarking
│   │   ├── sample_data.py     # Sample "city road network" demo graph
│   │   └── cli.py             # Command-line interface
│   └── output/                # Generated path visualizations (created at runtime)
├── java/
│   ├── Graph.java             # Same adjacency-list graph, in Java
│   ├── Algorithms.java        # BFS, DFS, Dijkstra (Java PriorityQueue)
│   └── Main.java              # CLI entry point
└── README.md
```

## Running the Python version

Requires Python 3.10+, `matplotlib`, and `networkx`:

```bash
pip install matplotlib networkx
cd python

# Run all three algorithms on the sample city graph
python -m algopath.cli --start Hyderabad --goal Chennai

# Run just one algorithm
python -m algopath.cli --start Hyderabad --goal Chennai --algo dijkstra

# Try a random graph instead of the sample data
python -m algopath.cli --random 40 --start N0 --goal N39

# Compare runtime & operation count across graph sizes (10 -> 400 nodes)
python -m algopath.cli --benchmark
```

Each run saves a PNG per algorithm into `python/output/`, with the computed
path highlighted in orange, the start node in green, and the goal in red.

## Running the Java version

Requires JDK 17+:

```bash
cd java
javac -encoding UTF-8 *.java

java Main Hyderabad Chennai      # custom start/goal
java Main                        # defaults to Hyderabad -> Chennai
java Main --benchmark            # runtime/operations across graph sizes
```

## Sample output

```
Graph: 10 nodes, 14 edges
Finding path from 'Hyderabad' to 'Chennai'...

Algorithm  Found   Cost   Nodes Expanded   Complexity         Path
BFS        True    1425   10               O(V + E)           Hyderabad -> Vijayawada -> Visakhapatnam -> Chennai
DFS        True    1425   6                O(V + E)           Hyderabad -> Vijayawada -> Visakhapatnam -> Chennai
Dijkstra   True    695    10               O((V + E) log V)   Hyderabad -> Vijayawada -> Guntur -> Nellore -> Chennai
```

Note how BFS/DFS both return a valid path costing 1425, while Dijkstra finds
the actual cheapest route at 695 — the exact distinction the algorithm exists
to make.

## Possible next steps

- A\* search using a straight-line-distance heuristic
- Bellman-Ford to support negative edge weights
- A simple web UI (Flask) instead of/alongside the CLI
- Persisting benchmark results to CSV for tracking improvements over time
