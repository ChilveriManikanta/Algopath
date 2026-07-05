import java.util.*;

/**
 * A weighted, undirected graph backed by an adjacency-list representation
 * (a Map of Maps), mirroring the Python implementation in algopath.graph.
 */
public class Graph {
    private final Map<String, Map<String, Double>> adjacency = new LinkedHashMap<>();

    public void addNode(String node) {
        adjacency.computeIfAbsent(node, k -> new LinkedHashMap<>());
    }

    public void addEdge(String u, String v, double weight) {
        if (weight < 0) {
            throw new IllegalArgumentException("AlgoPath assumes non-negative edge weights.");
        }
        addNode(u);
        addNode(v);
        adjacency.get(u).put(v, weight);
        adjacency.get(v).put(u, weight);
    }

    public Map<String, Double> neighbors(String node) {
        return adjacency.getOrDefault(node, Collections.emptyMap());
    }

    public Set<String> nodes() {
        return adjacency.keySet();
    }

    public boolean hasNode(String node) {
        return adjacency.containsKey(node);
    }

    public int nodeCount() {
        return adjacency.size();
    }

    public int edgeCount() {
        Set<String> seen = new HashSet<>();
        int count = 0;
        for (var entry : adjacency.entrySet()) {
            for (String v : entry.getValue().keySet()) {
                String key = entry.getKey().compareTo(v) < 0
                        ? entry.getKey() + "|" + v
                        : v + "|" + entry.getKey();
                if (!seen.contains(key)) {
                    seen.add(key);
                    count++;
                }
            }
        }
        return count;
    }

    /** Build the same sample "city road network" used by the Python demo. */
    public static Graph sampleCityGraph() {
        Graph g = new Graph();
        Object[][] edges = {
            {"Hyderabad", "Warangal", 150.0}, {"Hyderabad", "Nizamabad", 175.0},
            {"Hyderabad", "Vijayawada", 275.0}, {"Hyderabad", "Karimnagar", 165.0},
            {"Warangal", "Karimnagar", 70.0}, {"Warangal", "Khammam", 130.0},
            {"Khammam", "Vijayawada", 195.0}, {"Nizamabad", "Karimnagar", 120.0},
            {"Vijayawada", "Guntur", 35.0}, {"Vijayawada", "Visakhapatnam", 350.0},
            {"Guntur", "Nellore", 210.0}, {"Nellore", "Chennai", 175.0},
            {"Visakhapatnam", "Chennai", 800.0}, {"Karimnagar", "Khammam", 210.0},
        };
        for (Object[] e : edges) {
            g.addEdge((String) e[0], (String) e[1], (Double) e[2]);
        }
        return g;
    }

    /** Random connected graph generator, for benchmarking. */
    public static Graph randomGraph(int numNodes, double edgeProbability, long seed) {
        Random rng = new Random(seed);
        Graph g = new Graph();
        List<String> names = new ArrayList<>();
        for (int i = 0; i < numNodes; i++) {
            names.add("N" + i);
            g.addNode("N" + i);
        }
        List<String> shuffled = new ArrayList<>(names);
        Collections.shuffle(shuffled, rng);
        for (int i = 0; i < shuffled.size() - 1; i++) {
            g.addEdge(shuffled.get(i), shuffled.get(i + 1), 1 + rng.nextInt(20));
        }
        for (int i = 0; i < names.size(); i++) {
            for (int j = i + 1; j < names.size(); j++) {
                String a = names.get(i), b = names.get(j);
                if (g.neighbors(a).containsKey(b)) continue;
                if (rng.nextDouble() < edgeProbability) {
                    g.addEdge(a, b, 1 + rng.nextInt(20));
                }
            }
        }
        return g;
    }
}
