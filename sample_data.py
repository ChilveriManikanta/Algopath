"""A small sample "city road network" graph used as the default demo."""

from .graph import Graph

SAMPLE_EDGES = [
    ("Hyderabad", "Warangal", 150),
    ("Hyderabad", "Nizamabad", 175),
    ("Hyderabad", "Vijayawada", 275),
    ("Hyderabad", "Karimnagar", 165),
    ("Warangal", "Karimnagar", 70),
    ("Warangal", "Khammam", 130),
    ("Khammam", "Vijayawada", 195),
    ("Nizamabad", "Karimnagar", 120),
    ("Vijayawada", "Guntur", 35),
    ("Vijayawada", "Visakhapatnam", 350),
    ("Guntur", "Nellore", 210),
    ("Nellore", "Chennai", 175),
    ("Visakhapatnam", "Chennai", 800),
    ("Karimnagar", "Khammam", 210),
]


def build_sample_graph() -> Graph:
    g = Graph(directed=False)
    for u, v, w in SAMPLE_EDGES:
        g.add_edge(u, v, w)
    return g
