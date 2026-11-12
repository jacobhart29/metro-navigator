
from linked_list import LinkedList
from hash_table import HashTable
from bst import BST
from min_heap import MinHeap
from graph import Graph
from linked_stack import Stack, is_balanced
from linked_queue import Queue, hot_potato
from hash_set import HashSet


def main():

    metro = Graph(directed=False)

    stations = [
        "Downtown", "Beach", "Factory", "Airport",
        "Campus", "Eastside", "Garden"
    ]

    for station in stations:
        metro.add_vertex(station)

    connections = [
        ("Downtown", "Airport"),
        ("Downtown", "Campus"),
        ("Downtown", "Eastside"),
        ("Downtown", "Factory"),
        ("Airport", "Eastside"),
        ("Factory", "Eastside"),
        ("Beach", "Campus"),
        ("Beach", "Garden")
    ]

    for connection in connections:
        metro.add_edge(*connection)

    print(metro)


    directory = BST()

    for station in [
        "Downtown", "Beach", "Factory", "Airport",
        "Campus", "Eastside", "Garden"
    ]:
        directory.insert(station)

    print("BST inorder:", directory.inorder())
    print("BST level order:", directory.level_order())


    fares = HashTable()

    fare_zones = {
        "Airport": 1,
        "Beach": 3,
        "Campus": 2,
        "Downtown": 1,
        "Eastside": 2,
        "Factory": 2,
        "Garden": 3
    }

    for station, zone in fare_zones.items():
        fares.put(station, zone)

    for station in stations:
        print(station, "Zone:", fares.get(station))


    trip = LinkedList()

    for station in ["Airport", "Downtown", "Campus", "Beach"]:
        trip.append(station)

    print("Trip:", trip)

    trip.reverse()

    print("Reversed trip:", trip)


    maintenance = MinHeap()

    maintenance.push(3, "Inspect Beach-Campus sign")
    maintenance.push(1, "Repair Eastside crossing")
    maintenance.push(2, "Replace Downtown display")

    while not maintenance.is_empty():
        print(maintenance.pop())


    history = Stack()

    for station in ["Airport", "Downtown", "Campus", "Beach"]:
        history.push(station)

    print("Back:", history.pop())
    print("Back:", history.pop())
    print("Current station:", history.peek())

    print("Balanced:", is_balanced("([]{})"))
    print("Balanced:", is_balanced("([)]"))


    line = Queue()

    for passenger in ["Ana", "Ben", "Cy"]:
        line.enqueue(passenger)

    print("Served:", line.dequeue())
    print("Next passenger:", line.peek())
    print("Waiting:", line.to_list())

    eliminated, winner = hot_potato(["A", "B", "C", "D", "E"], 3)
    print("Eliminated:", eliminated)
    print("Winner:", winner)


    airport_stops = HashSet()
    factory_stops = HashSet()
    beach_stops = HashSet()

    for station in metro.neighbors("Airport"):
        airport_stops.add(station)

    for station in metro.neighbors("Factory"):
        factory_stops.add(station)

    for station in metro.neighbors("Beach"):
        beach_stops.add(station)

    print("Airport and Factory common stops:",
          sorted(airport_stops.intersection(factory_stops).to_list()))

    print("Airport and Beach combined stops:",
          sorted(airport_stops.union(beach_stops).to_list()))

    print("Airport and Beach common stops:",
          sorted(airport_stops.intersection(beach_stops).to_list()))


if __name__ == "__main__":
    main()
