"""Unit tests for the unweighted Graph used by Metro Navigator."""
import random
import time
import unittest

from graph import Graph


METRO_STATIONS = ["Airport", "Beach", "Campus", "Downtown", "Eastside", "Factory", "Garden"]
METRO_CONNECTIONS = [
    ("Airport", "Downtown"),
    ("Airport", "Eastside"),
    ("Beach", "Campus"),
    ("Beach", "Garden"),
    ("Campus", "Downtown"),
    ("Downtown", "Eastside"),
    ("Downtown", "Factory"),
    ("Eastside", "Factory"),
    ("Factory", "Garden"),
]


def build_metro_graph():
    graph = Graph(directed=False)
    for station in METRO_STATIONS:
        graph.add_vertex(station)
    for u, v in METRO_CONNECTIONS:
        graph.add_edge(u, v)
    return graph


def canonical_edges(graph):
    return {tuple(edge) for edge in graph.edges()}


class TestGraph(unittest.TestCase):
    def test_G_01(self):
        graph = Graph()
        self.assertEqual(graph.vertex_count(), 0)
        self.assertEqual(graph.edge_count(), 0)
        self.assertEqual(graph.vertices(), [])
        self.assertEqual(graph.edges(), [])

    def test_G_02(self):
        graph = Graph()
        self.assertTrue(graph.add_vertex("A"))
        self.assertFalse(graph.add_vertex("A"))
        self.assertEqual(graph.vertex_count(), 1)
        self.assertTrue(graph.has_vertex("A"))
        self.assertFalse(graph.has_vertex("B"))

    def test_G_03(self):
        graph = Graph()
        with self.assertRaises(TypeError):
            graph.add_vertex(5)
        with self.assertRaises(ValueError):
            graph.add_vertex("")

    def test_G_04(self):
        graph = Graph(directed=False)
        graph.add_vertex("A")
        graph.add_vertex("B")
        self.assertTrue(graph.add_edge("A", "B"))
        self.assertTrue(graph.has_edge("A", "B"))
        self.assertTrue(graph.has_edge("B", "A"))
        self.assertEqual(graph.degree("A"), 1)
        self.assertEqual(graph.degree("B"), 1)
        self.assertEqual(graph.edge_count(), 1)

    def test_G_05(self):
        graph = Graph()
        graph.add_vertex("A")
        with self.assertRaises(KeyError):
            graph.add_edge("A", "missing")
        with self.assertRaises(KeyError):
            graph.add_edge("missing", "A")
        self.assertEqual(graph.vertex_count(), 1)
        self.assertEqual(graph.edge_count(), 0)
        self.assertEqual(graph.vertices(), ["A"])

    def test_G_06(self):
        graph = Graph()
        graph.add_vertex("A")
        graph.add_vertex("B")
        with self.assertRaises(ValueError):
            graph.add_edge("A", "A")
        self.assertTrue(graph.add_edge("A", "B"))
        self.assertFalse(graph.add_edge("A", "B"))
        self.assertFalse(graph.add_edge("B", "A"))
        self.assertEqual(graph.edge_count(), 1)
        self.assertEqual(graph.neighbors("A"), ["B"])

    def test_G_07(self):
        graph = Graph(directed=True)
        graph.add_vertex("A")
        graph.add_vertex("B")
        self.assertTrue(graph.add_edge("A", "B"))
        self.assertTrue(graph.has_edge("A", "B"))
        self.assertFalse(graph.has_edge("B", "A"))
        self.assertTrue(graph.add_edge("B", "A"))
        self.assertEqual(graph.edge_count(), 2)
        self.assertEqual(graph.neighbors("A"), ["B"])
        self.assertEqual(graph.neighbors("B"), ["A"])

    def test_G_08(self):
        graph = Graph()
        for name in ["A", "B", "C", "D"]:
            graph.add_vertex(name)
        for u, v in [("A", "C"), ("A", "B"), ("A", "D")]:
            graph.add_edge(u, v)
        neighbors = graph.neighbors("A")
        self.assertEqual(neighbors, ["C", "B", "D"])
        neighbors.clear()
        self.assertEqual(graph.neighbors("A"), ["C", "B", "D"])

    def test_G_09(self):
        graph = Graph()
        graph.add_vertex("isolated")
        self.assertEqual(graph.neighbors("isolated"), [])
        self.assertEqual(graph.degree("isolated"), 0)
        with self.assertRaises(KeyError):
            graph.neighbors("missing")
        with self.assertRaises(KeyError):
            graph.degree("missing")

    def test_G_10(self):
        graph = Graph()
        for name in ["A", "B", "C"]:
            graph.add_vertex(name)
        graph.add_edge("A", "B")
        graph.add_edge("A", "C")
        self.assertTrue(graph.remove_edge("A", "B"))
        self.assertFalse(graph.has_edge("A", "B"))
        self.assertFalse(graph.has_edge("B", "A"))
        self.assertTrue(graph.has_edge("A", "C"))
        self.assertTrue(graph.has_vertex("A"))
        self.assertEqual(graph.edge_count(), 1)
        self.assertFalse(graph.remove_edge("A", "B"))

    def test_G_11(self):
        graph = Graph(directed=True)
        graph.add_vertex("A")
        graph.add_vertex("B")
        graph.add_edge("A", "B")
        graph.add_edge("B", "A")
        self.assertTrue(graph.remove_edge("A", "B"))
        self.assertFalse(graph.has_edge("A", "B"))
        self.assertTrue(graph.has_edge("B", "A"))
        self.assertEqual(graph.edge_count(), 1)

    def test_G_12(self):
        graph = Graph()
        graph.add_vertex("A")
        graph.add_vertex("B")
        with self.assertRaises(KeyError):
            graph.remove_edge("A", "missing")
        with self.assertRaises(KeyError):
            graph.remove_edge("missing", "A")
        self.assertFalse(graph.remove_edge("A", "B"))

    def test_G_13(self):
        graph = Graph()
        for name in ["A", "B", "C"]:
            graph.add_vertex(name)
        graph.add_edge("A", "B")
        graph.add_edge("B", "C")
        graph.add_edge("A", "C")
        self.assertTrue(graph.remove_vertex("B"))
        self.assertEqual(graph.vertex_count(), 2)
        self.assertEqual(graph.edge_count(), 1)
        self.assertEqual(graph.neighbors("A"), ["C"])
        self.assertFalse(graph.remove_vertex("B"))
        self.assertTrue(graph.add_vertex("B"))
        self.assertEqual(graph.neighbors("B"), [])

    def test_G_14(self):
        graph = Graph(directed=True)
        for name in ["A", "B", "C"]:
            graph.add_vertex(name)
        graph.add_edge("A", "B")
        graph.add_edge("B", "C")
        graph.add_edge("C", "B")
        self.assertTrue(graph.remove_vertex("B"))
        self.assertEqual(graph.edge_count(), 0)
        self.assertEqual(graph.neighbors("A"), [])
        self.assertEqual(graph.vertex_count(), 2)

    def test_G_15(self):
        graph = Graph()
        for name in ["A", "B", "C"]:
            graph.add_vertex(name)
        graph.add_edge("B", "C")
        graph.add_edge("A", "C")
        graph.add_edge("A", "B")
        self.assertEqual(canonical_edges(graph), {("A", "B"), ("A", "C"), ("B", "C")})
        directed = Graph(directed=True)
        directed.add_vertex("A")
        directed.add_vertex("B")
        directed.add_edge("A", "B")
        directed.add_edge("B", "A")
        self.assertEqual(canonical_edges(directed), {("A", "B"), ("B", "A")})

    def test_G_16(self):
        graph = Graph()
        graph.add_vertex("A")
        self.assertFalse(graph.has_edge("A", "missing"))
        self.assertFalse(graph.has_edge("missing", "A"))
        self.assertFalse(graph.has_edge("missing", "also-missing"))

    def test_G_17(self):
        graph = Graph()
        graph.add_vertex("center")
        for i in range(5):
            name = f"leaf{i}"
            graph.add_vertex(name)
            graph.add_edge("center", name)
        self.assertEqual(graph.degree("center"), 5)
        for i in range(5):
            self.assertEqual(graph.degree(f"leaf{i}"), 1)
        directed = Graph(directed=True)
        for name in ["A", "B", "C"]:
            directed.add_vertex(name)
        directed.add_edge("A", "B")
        directed.add_edge("C", "A")
        self.assertEqual(directed.degree("A"), 1)
        self.assertEqual(directed.degree("C"), 1)
        self.assertEqual(directed.degree("B"), 0)

    def test_G_18(self):
        graph = build_metro_graph()
        self.assertEqual(graph.vertex_count(), 7)
        self.assertEqual(graph.edge_count(), 9)
        expected_degrees = {
            "Airport": 2, "Beach": 2, "Campus": 2, "Downtown": 4,
            "Eastside": 3, "Factory": 3, "Garden": 2,
        }
        for station, degree in expected_degrees.items():
            self.assertEqual(graph.degree(station), degree)
        for u, v in METRO_CONNECTIONS:
            self.assertTrue(graph.has_edge(u, v))
            self.assertTrue(graph.has_edge(v, u))
        self.assertEqual(sum(graph.degree(s) for s in METRO_STATIONS), 18)
        self.assertEqual(len(graph.edges()), 9)

    def test_G_19(self):
        start = time.perf_counter()
        path = Graph()
        for i in range(1_000):
            path.add_vertex(f"v{i}")
        for i in range(999):
            path.add_edge(f"v{i}", f"v{i + 1}")
        self.assertEqual(path.edge_count(), 999)
        self.assertEqual(path.degree("v500"), 2)
        for i in range(0, 1_000, 2):
            self.assertTrue(path.remove_vertex(f"v{i}"))
        self.assertEqual(path.vertex_count(), 500)
        self.assertEqual(path.edge_count(), 0)

        complete = Graph()
        for i in range(60):
            complete.add_vertex(f"n{i}")
        for i in range(60):
            for j in range(i + 1, 60):
                complete.add_edge(f"n{i}", f"n{j}")
        self.assertEqual(complete.edge_count(), 1_770)
        for i in range(60):
            self.assertEqual(complete.degree(f"n{i}"), 59)
        self.assertLess(time.perf_counter() - start, 2.0)

    def test_G_20(self):
        rng = random.Random(2001)
        graph = Graph()
        model = {}  # test-only dict of dicts; implementations may not use dict.
        names = [f"v{i}" for i in range(30)]

        def check_model():
            self.assertEqual(set(graph.vertices()), set(model))
            self.assertEqual(graph.vertex_count(), len(model))
            expected_edges = {
                (u, v) for u, neighbors in model.items() for v in neighbors if u < v
            }
            self.assertEqual(canonical_edges(graph), expected_edges)
            self.assertEqual(graph.edge_count(), len(expected_edges))
            for u in model:
                self.assertEqual(set(graph.neighbors(u)), set(model[u]))
                for v in model:
                    self.assertEqual(graph.has_edge(u, v), v in model[u])

        for step in range(1_500):
            op = rng.choice(["add_vertex", "remove_vertex", "add_edge", "remove_edge"])
            u, v = rng.choice(names), rng.choice(names)
            if op == "add_vertex":
                expected = u not in model
                self.assertEqual(graph.add_vertex(u), expected)
                if expected:
                    model[u] = {}
            elif op == "remove_vertex":
                expected = u in model
                self.assertEqual(graph.remove_vertex(u), expected)
                if expected:
                    del model[u]
                    for neighbors in model.values():
                        neighbors.pop(u, None)
            elif op == "add_edge":
                if u not in model or v not in model:
                    with self.assertRaises(KeyError):
                        graph.add_edge(u, v)
                elif u == v:
                    with self.assertRaises(ValueError):
                        graph.add_edge(u, v)
                else:
                    expected = v not in model[u]
                    self.assertEqual(graph.add_edge(u, v), expected)
                    model[u][v] = True
                    model[v][u] = True
            else:
                if u not in model or v not in model:
                    with self.assertRaises(KeyError):
                        graph.remove_edge(u, v)
                else:
                    expected = v in model[u]
                    self.assertEqual(graph.remove_edge(u, v), expected)
                    model[u].pop(v, None)
                    model[v].pop(u, None)
            if step % 50 == 0:
                check_model()
        check_model()

    def test_G_EXTRA_01_graph_string_is_readable(self):
        graph = build_metro_graph()
        self.assertIsInstance(str(graph), str)
        self.assertTrue(str(graph).strip())

    def test_G_EXTRA_02_no_numeric_edge_costs_are_required(self):
        graph = build_metro_graph()
        self.assertTrue(all(isinstance(name, str) for name in graph.neighbors("Downtown")))
        for edge in graph.edges():
            self.assertEqual(len(edge), 2)


if __name__ == "__main__":
    unittest.main()
