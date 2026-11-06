class Graph:
    def __init__(self, directed=False):
        self.directed = directed
        self.adjacency_list = {}

    def add_vertex(self, vertex):
        if not isinstance(vertex, str):
            raise TypeError
        if not vertex:
            raise ValueError
        if vertex in self.adjacency_list:
            return False
        self.adjacency_list[vertex] = []
        return True

    def add_edge(self, start, end):
        if start not in self.adjacency_list or end not in self.adjacency_list:
            raise KeyError
        if start == end:
            raise ValueError
        if end in self.adjacency_list[start]:
            return False
        self.adjacency_list[start].append(end)
        if not self.directed:
            self.adjacency_list[end].append(start)
        return True

    def remove_edge(self, start, end):
        if start not in self.adjacency_list or end not in self.adjacency_list:
            raise KeyError
        if end not in self.adjacency_list[start]:
            return False
        self.adjacency_list[start].remove(end)
        if not self.directed:
            self.adjacency_list[end].remove(start)
        return True

    def remove_vertex(self, vertex):
        if vertex not in self.adjacency_list:
            return False
        del self.adjacency_list[vertex]
        for neighbors in self.adjacency_list.values():
            if vertex in neighbors:
                neighbors.remove(vertex)
        return True

    def has_vertex(self, vertex):
        return vertex in self.adjacency_list

    def has_edge(self, start, end):
        return start in self.adjacency_list and end in self.adjacency_list[start]

    def neighbors(self, vertex):
        if vertex not in self.adjacency_list:
            raise KeyError
        return self.adjacency_list[vertex].copy()

    def degree(self, vertex):
        if vertex not in self.adjacency_list:
            raise KeyError
        return len(self.adjacency_list[vertex])

    def vertex_count(self):
        return len(self.adjacency_list)

    def edge_count(self):
        total = sum(len(neighbors) for neighbors in self.adjacency_list.values())
        return total if self.directed else total // 2

    def vertices(self):
        return list(self.adjacency_list)

    def edges(self):
        if self.directed:
            return [(start, end) for start in self.adjacency_list for end in self.adjacency_list[start]]
        return [(start, end) for start in self.adjacency_list for end in self.adjacency_list[start] if start < end]

    def __str__(self):
        return str(self.adjacency_list)
