import java.util.*;

public class Algorithms {

    public static class SearchResult {
        public final String algorithm;
        public final List<String> path;
        public final double cost;
        public final int operations;
        public final String complexity;
        public final boolean found;

        public SearchResult(String algorithm, List<String> path, double cost,
                             int operations, String complexity) {
            this.algorithm = algorithm;
            this.path = path;
            this.cost = cost;
            this.operations = operations;
            this.complexity = complexity;
            this.found = !path.isEmpty();
        }

        @Override
        public String toString() {
            String pathStr = found ? String.join(" -> ", path) : "(no path)";
            return String.format("%-9s found=%-6s cost=%-8s expanded=%-5d complexity=%-16s path=%s",
                    algorithm, found, cost, operations, complexity, pathStr);
        }
    }

    private static List<String> reconstructPath(Map<String, String> cameFrom, String start, String goal) {
        if (!cameFrom.containsKey(goal) && !goal.equals(start)) return new ArrayList<>();
        LinkedList<String> path = new LinkedList<>();
        String current = goal;
        path.addFirst(current);
        while (!current.equals(start)) {
            String prev = cameFrom.get(current);
            if (prev == null) return new ArrayList<>();
            path.addFirst(prev);
            current = prev;
        }
        return path;
    }

    private static double pathCost(Graph graph, List<String> path) {
        double cost = 0;
        for (int i = 0; i < path.size() - 1; i++) {
            cost += graph.neighbors(path.get(i)).get(path.get(i + 1));
        }
        return cost;
    }

    /** Breadth-First Search — shortest path by edge count (unweighted). */
    public static SearchResult bfs(Graph graph, String start, String goal) {
        Set<String> visited = new HashSet<>(List.of(start));
        Map<String, String> cameFrom = new HashMap<>();
        Deque<String> queue = new ArrayDeque<>();
        queue.add(start);
        int operations = 0;

        while (!queue.isEmpty()) {
            String node = queue.poll();
            operations++;
            if (node.equals(goal)) break;
            for (String neighbor : graph.neighbors(node).keySet()) {
                if (!visited.contains(neighbor)) {
                    visited.add(neighbor);
                    cameFrom.put(neighbor, node);
                    queue.add(neighbor);
                }
            }
        }
        List<String> path = reconstructPath(cameFrom, start, goal);
        double cost = path.isEmpty() ? 0 : pathCost(graph, path);
        return new SearchResult("BFS", path, cost, operations, "O(V + E)");
    }

    /** Depth-First Search — finds *a* path, not guaranteed shortest. */
    public static SearchResult dfs(Graph graph, String start, String goal) {
        Set<String> visited = new HashSet<>();
        Map<String, String> cameFrom = new HashMap<>();
        Deque<String> stack = new ArrayDeque<>();
        stack.push(start);
        int operations = 0;

        while (!stack.isEmpty()) {
            String node = stack.pop();
            if (visited.contains(node)) continue;
            visited.add(node);
            operations++;
            if (node.equals(goal)) break;
            for (String neighbor : graph.neighbors(node).keySet()) {
                if (!visited.contains(neighbor)) {
                    cameFrom.putIfAbsent(neighbor, node);
                    stack.push(neighbor);
                }
            }
        }
        List<String> path = reconstructPath(cameFrom, start, goal);
        double cost = path.isEmpty() ? 0 : pathCost(graph, path);
        return new SearchResult("DFS", path, cost, operations, "O(V + E)");
    }

    /** Dijkstra's algorithm using Java's built-in PriorityQueue (binary heap). */
    public static SearchResult dijkstra(Graph graph, String start, String goal) {
        Map<String, Double> dist = new HashMap<>();
        for (String n : graph.nodes()) dist.put(n, Double.POSITIVE_INFINITY);
        dist.put(start, 0.0);
        Map<String, String> cameFrom = new HashMap<>();
        Set<String> visited = new HashSet<>();
        int operations = 0;

        PriorityQueue<double[]> pq = new PriorityQueue<>(Comparator.comparingDouble(a -> a[0]));
        Map<Integer, String> idToNode = new HashMap<>();
        Map<String, Integer> nodeToId = new HashMap<>();
        int idCounter = 0;
        for (String n : graph.nodes()) {
            idToNode.put(idCounter, n);
            nodeToId.put(n, idCounter);
            idCounter++;
        }
        pq.add(new double[]{0.0, nodeToId.get(start)});

        while (!pq.isEmpty()) {
            double[] top = pq.poll();
            String node = idToNode.get((int) top[1]);
            if (visited.contains(node)) continue;
            visited.add(node);
            operations++;
            if (node.equals(goal)) break;

            for (var entry : graph.neighbors(node).entrySet()) {
                String neighbor = entry.getKey();
                double weight = entry.getValue();
                double newDist = top[0] + weight;
                if (newDist < dist.getOrDefault(neighbor, Double.POSITIVE_INFINITY)) {
                    dist.put(neighbor, newDist);
                    cameFrom.put(neighbor, node);
                    pq.add(new double[]{newDist, nodeToId.get(neighbor)});
                }
            }
        }

        List<String> path = reconstructPath(cameFrom, start, goal);
        double cost = dist.getOrDefault(goal, Double.POSITIVE_INFINITY);
        if (Double.isInfinite(cost)) cost = 0;
        return new SearchResult("Dijkstra", path, cost, operations, "O((V + E) log V)");
    }
}
