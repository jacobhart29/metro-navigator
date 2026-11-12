from hash_table import HashTable
from linked_list import LinkedList

class Edge:
    def __init__(self, to):
        self.to = to

class Graph:
    def __init__(self, directed=False):
        self.directed = directed
        self._adj = HashTable()
        self._edge_count = 0

    def add_vertex(self, vertex):
        if not isinstance(vertex, str):
            raise TypeError
        if not vertex:
            raise ValueError
        if self.has_vertex(vertex):
            return False
        self._adj.put(vertex, LinkedList())
        return True

    def add_edge(self, start, end):
        if not self.has_vertex(start) or not self.has_vertex(end):
            raise KeyError
        if start == end:
            raise ValueError
        if self.has_edge(start, end):
            return False
        self._adj.get(start).append(Edge(end))
        if not self.directed:
            self._adj.get(end).append(Edge(start))
        self._edge_count += 1
        return True

    def has_edge(self, start, end):
        if not self.has_vertex(start) or not self.has_vertex(end):
            return False
        return self._edge_index(start, end) != -1

    def _edge_index(self, start, end):
        index = 0
        for edge in self._adj.get(start):
            if edge.to == end:
                return index
            index += 1
        return -1

    def remove_edge(self, start, end):
        if not self.has_vertex(start) or not self.has_vertex(end):
            raise KeyError
        index = self._edge_index(start, end)
        if index == -1:
            return False
        self._adj.get(start).remove_at(index)
        if not self.directed:
            self._adj.get(end).remove_at(self._edge_index(end, start))
        self._edge_count -= 1
        return True

    def remove_vertex(self, vertex):
        if not self.has_vertex(vertex):
            return False
        removed = 0
        for other in self._adj.keys():
            if other != vertex:
                index = self._edge_index(other, vertex)
                if index != -1:
                    self._adj.get(other).remove_at(index)
                    removed += 1
        outgoing = len(self._adj.get(vertex))
        self._adj.remove(vertex)
        if self.directed:
            self._edge_count -= removed + outgoing
        else:
            self._edge_count -= outgoing
        return True

    def has_vertex(self, vertex):
        return self._adj.contains(vertex)

    def neighbors(self, vertex):
        if not self.has_vertex(vertex):
            raise KeyError
        result = []
        for edge in self._adj.get(vertex):
            result.append(edge.to)
        return result

    def degree(self, vertex):
        if not self.has_vertex(vertex):
            raise KeyError
        return len(self._adj.get(vertex))

    def vertex_count(self):
        return len(self._adj)

    def edge_count(self):
        return self._edge_count

    def vertices(self):
        return self._adj.keys()

    def edges(self):
        result = []
        for start in self._adj.keys():
            for edge in self._adj.get(start):
                if self.directed or start < edge.to:
                    result.append((start, edge.to))
        return result

    def __str__(self):
        lines = []
        for vertex in self._adj.keys():
            lines.append(vertex + ": " + ", ".join(self.neighbors(vertex)))
        return "\n".join(lines)
