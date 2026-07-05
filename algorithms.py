"""
Core graph-search algorithms for AlgoPath: BFS, DFS, and Dijkstra.

Each function returns a `SearchResult` containing the path found, its total
cost, and an `operations` counter (number of nodes popped/visited) so the
CLI can report a rough empirical comparison of algorithm cost alongside
their theoretical Big-O complexity.
"""

from collections import deque
from dataclasses import dataclass, field

from .graph import Graph
from .priority_queue import PriorityQueue


@dataclass
class SearchResult:
    algorithm: str
    path: list[str]
    cost: float
    operations: int  # number of nodes expanded/visited
    complexity: str
    found: bool = field(init=False)

    def __post_init__(self):
        self.found = len(self.path) > 0


def _reconstruct_path(came_from: dict, start: str, goal: str) -> list[str]:
    if goal not in came_from and goal != start:
        return []
    path = [goal]
    while path[-1] != start:
        prev = came_from.get(path[-1])
        if prev is None:
            return []
        path.append(prev)
    path.reverse()
    return path


def bfs(graph: Graph, start: str, goal: str) -> SearchResult:
    """Breadth-First Search: shortest path by number of edges (unweighted)."""
    visited = {start}
    came_from: dict[str, str] = {}
    queue = deque([start])
    operations = 0

    while queue:
        node = queue.popleft()
        operations += 1
        if node == goal:
            break
        for neighbor, _weight in graph.neighbors(node):
            if neighbor not in visited:
                visited.add(neighbor)
                came_from[neighbor] = node
                queue.append(neighbor)

    path = _reconstruct_path(came_from, start, goal)
    cost = sum(graph.adjacency[a][b] for a, b in zip(path, path[1:])) if path else 0
    return SearchResult("BFS", path, cost, operations, "O(V + E)")


def dfs(graph: Graph, start: str, goal: str) -> SearchResult:
    """Depth-First Search: finds *a* path (not guaranteed shortest)."""
    visited = set()
    came_from: dict[str, str] = {}
    stack = [start]
    operations = 0

    while stack:
        node = stack.pop()
        if node in visited:
            continue
        visited.add(node)
        operations += 1
        if node == goal:
            break
        for neighbor, _weight in graph.neighbors(node):
            if neighbor not in visited:
                came_from.setdefault(neighbor, node)
                stack.append(neighbor)

    path = _reconstruct_path(came_from, start, goal)
    cost = sum(graph.adjacency[a][b] for a, b in zip(path, path[1:])) if path else 0
    return SearchResult("DFS", path, cost, operations, "O(V + E)")


def dijkstra(graph: Graph, start: str, goal: str) -> SearchResult:
    """Dijkstra's algorithm: guaranteed shortest weighted path (non-negative weights)."""
    distances = {node: float("inf") for node in graph.nodes()}
    distances[start] = 0
    came_from: dict[str, str] = {}
    visited = set()
    operations = 0

    pq = PriorityQueue()
    pq.push(0, start)

    while not pq.is_empty():
        dist, node = pq.pop_min()
        if node in visited:
            continue
        visited.add(node)
        operations += 1

        if node == goal:
            break

        for neighbor, weight in graph.neighbors(node):
            new_dist = dist + weight
            if new_dist < distances.get(neighbor, float("inf")):
                distances[neighbor] = new_dist
                came_from[neighbor] = node
                pq.push(new_dist, neighbor)

    path = _reconstruct_path(came_from, start, goal)
    cost = distances.get(goal, float("inf"))
    if cost == float("inf"):
        cost = 0
    return SearchResult("Dijkstra", path, cost, operations, "O((V + E) log V)")


ALGORITHMS = {
    "bfs": bfs,
    "dfs": dfs,
    "dijkstra": dijkstra,
}
