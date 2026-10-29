"""Integration tests: all required data structures working together."""
import unittest

from bst import BST
from graph import Graph
from hash_set import HashSet
from hash_table import HashTable
from linked_list import LinkedList
from linked_queue import Queue
from linked_stack import Stack
from min_heap import MinHeap


STATIONS = ["Airport", "Beach", "Campus", "Downtown", "Eastside", "Factory", "Garden"]
CONNECTIONS = [
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
FARE_ZONES = {
    "Airport": 1,
    "Beach": 3,
    "Campus": 2,
    "Downtown": 1,
    "Eastside": 2,
    "Factory": 2,
    "Garden": 3,
}


def city_graph():
    graph = Graph(directed=False)
    for station in STATIONS:
        graph.add_vertex(station)
    for u, v in CONNECTIONS:
        graph.add_edge(u, v)
    return graph


class TestMetroNavigatorIntegration(unittest.TestCase):
    def test_INT_01(self):
        directory = BST()
        for station in ["Downtown", "Beach", "Factory", "Airport", "Campus", "Eastside", "Garden"]:
            directory.insert(station, station)
        self.assertEqual(directory.inorder(), ["Airport", "Beach", "Campus", "Downtown", "Eastside", "Factory", "Garden"])
        self.assertEqual(directory.height(), 3)
        self.assertEqual(directory.count_leaves(), 4)
        self.assertEqual(directory.preorder(), ["Downtown", "Beach", "Airport", "Campus", "Factory", "Eastside", "Garden"])

    def test_INT_02(self):
        fares = HashTable()
        for station, zone in FARE_ZONES.items():
            fares.put(station, zone)
        for station, zone in FARE_ZONES.items():
            self.assertEqual(fares.get(station), zone)
        self.assertEqual(len(fares), 7)

    def test_INT_03(self):
        trip = LinkedList()
        for station in ["Airport", "Downtown", "Campus", "Beach"]:
            trip.append(station)
        self.assertEqual(str(trip), "Airport -> Downtown -> Campus -> Beach -> None")
        trip.reverse()
        self.assertEqual(str(trip), "Beach -> Campus -> Downtown -> Airport -> None")

    def test_INT_04(self):
        tasks = MinHeap()
        tasks.push(3, "Inspect Beach-Campus sign")
        tasks.push(1, "Repair Eastside crossing")
        tasks.push(2, "Replace Downtown display")
        output = [tasks.pop() for _ in range(3)]
        self.assertEqual(output, [
            (1, "Repair Eastside crossing"),
            (2, "Replace Downtown display"),
            (3, "Inspect Beach-Campus sign"),
        ])
        self.assertTrue(tasks.is_empty())

    def test_INT_05(self):
        graph = city_graph()
        airport_neighbors = HashSet()
        factory_neighbors = HashSet()
        beach_neighbors = HashSet()
        for station in graph.neighbors("Airport"):
            airport_neighbors.add(station)
        for station in graph.neighbors("Factory"):
            factory_neighbors.add(station)
        for station in graph.neighbors("Beach"):
            beach_neighbors.add(station)
        self.assertEqual(sorted(airport_neighbors.intersection(factory_neighbors).to_list()), ["Downtown", "Eastside"])
        self.assertEqual(sorted(airport_neighbors.union(beach_neighbors).to_list()), ["Campus", "Downtown", "Eastside", "Garden"])
        self.assertEqual(airport_neighbors.intersection(beach_neighbors).to_list(), [])

    def test_INT_06(self):
        back = Stack()
        for station in ["Airport", "Downtown", "Campus", "Beach"]:
            back.push(station)
        self.assertEqual(back.pop(), "Beach")
        self.assertEqual(back.pop(), "Campus")
        self.assertEqual(back.peek(), "Downtown")
        self.assertEqual(back.to_list(), ["Downtown", "Airport"])

    def test_INT_07(self):
        line = Queue()
        for name in ["Ana", "Ben", "Cy"]:
            line.enqueue(name)
        self.assertEqual(line.dequeue(), "Ana")
        self.assertEqual(line.peek(), "Ben")
        self.assertEqual(len(line), 2)
        self.assertEqual(line.to_list(), ["Ben", "Cy"])

    def test_INT_08(self):
        graph = city_graph()
        neighbors = graph.neighbors("Downtown")
        self.assertEqual(neighbors, ["Airport", "Campus", "Eastside", "Factory"])
        line = Queue()
        for station in neighbors:
            line.enqueue(station)
        queue_output = [line.dequeue() for _ in range(len(line))]
        self.assertEqual(queue_output, ["Airport", "Campus", "Eastside", "Factory"])
        stack = Stack()
        for station in neighbors:
            stack.push(station)
        stack_output = [stack.pop() for _ in range(len(stack))]
        self.assertEqual(stack_output, ["Factory", "Eastside", "Campus", "Airport"])


if __name__ == "__main__":
    unittest.main()
