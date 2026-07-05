import java.util.*;

/**
 * AlgoPath (Java edition) — run BFS, DFS, and Dijkstra on the sample city
 * graph and print a comparison table.
 *
 * Usage:
 *   java Main                          (uses default start/goal)
 *   java Main Hyderabad Chennai        (custom start/goal)
 *   java Main --benchmark              (runtime/operations across graph sizes)
 */
public class Main {
    public static void main(String[] args) {
        if (args.length > 0 && args[0].equals("--benchmark")) {
            runBenchmark();
            return;
        }

        Graph graph = Graph.sampleCityGraph();
        String start = args.length > 0 ? args[0] : "Hyderabad";
        String goal = args.length > 1 ? args[1] : "Chennai";

        if (!graph.hasNode(start) || !graph.hasNode(goal)) {
            System.out.println("Unknown node. Available nodes: " + graph.nodes());
            return;
        }

        System.out.printf("Graph: %d nodes, %d edges%n", graph.nodeCount(), graph.edgeCount());
        System.out.printf("Finding path from '%s' to '%s'...%n%n", start, goal);

        List<Algorithms.SearchResult> results = List.of(
                Algorithms.bfs(graph, start, goal),
                Algorithms.dfs(graph, start, goal),
                Algorithms.dijkstra(graph, start, goal)
        );
        for (var r : results) {
            System.out.println(r);
        }
    }

    private static void runBenchmark() {
        int[] sizes = {10, 25, 50, 100, 200, 400};
        System.out.println("Nodes  Edges |      BFS       |      DFS       |    DIJKSTRA");
        System.out.println("-".repeat(70));
        for (int n : sizes) {
            Graph g = Graph.randomGraph(n, Math.max(0.08, 6.0 / n), 7);
            List<String> nodes = new ArrayList<>(g.nodes());
            String start = nodes.get(0), goal = nodes.get(nodes.size() - 1);

            StringBuilder row = new StringBuilder(String.format("%5d %6d |", n, g.edgeCount()));
            for (var fn : List.of("bfs", "dfs", "dijkstra")) {
                long t0 = System.nanoTime();
                Algorithms.SearchResult r = switch (fn) {
                    case "bfs" -> Algorithms.bfs(g, start, goal);
                    case "dfs" -> Algorithms.dfs(g, start, goal);
                    default -> Algorithms.dijkstra(g, start, goal);
                };
                double ms = (System.nanoTime() - t0) / 1_000_000.0;
                row.append(String.format(" %6.3f ms/%4d ops |", ms, r.operations));
            }
            System.out.println(row);
        }
    }
}
