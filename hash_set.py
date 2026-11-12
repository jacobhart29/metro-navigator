from hash_table import HashTable


class HashSet:
    def __init__(self):
        self._table = HashTable()

    def __len__(self):
        return len(self._table)

    def __contains__(self, item):
        return item in self._table
    def is_empty(self):
        return len(self._table) == 0

    def add(self, value):
        if not isinstance(value, str):
            raise TypeError("HashSet only accepts strings")
        if self._table.contains(value):
            return False
        self._table.put(value, True)
        return True

    def contains(self, value):
        if not isinstance(value, str):
            raise TypeError("HashSet only accepts strings")
        return self._table.contains(value)

    def remove(self, value):
        if not isinstance(value, str):
            raise TypeError("HashSet only accepts strings")
        return self._table.remove(value)

    def discard(self, value):
        if not isinstance(value, str):
            raise TypeError("HashSet only accepts strings")
        try:
            self._table.remove(value)
            return True
        except KeyError:
            return False

    def clear(self):
        self._table = HashTable()

    def to_list(self):
        return self._table.keys()

    def union(self, other_set):
        if not isinstance(other_set, HashSet):
            raise TypeError("Argument must be a HashSet")
        result_set = HashSet()
        for value in self.to_list():
            result_set.add(value)
        for value in other_set.to_list():
            result_set.add(value)
        return result_set

    def intersection(self, other_set):
        if not isinstance(other_set, HashSet):
            raise TypeError("Argument must be a HashSet")
        result_set = HashSet()
        for value in self.to_list():
            if other_set.contains(value):
                result_set.add(value)
        return result_set

    def difference(self, other_set):
        if not isinstance(other_set, HashSet):
            raise TypeError("Argument must be a HashSet")
        result_set = HashSet()
        for value in self.to_list():
            if not other_set.contains(value):
                result_set.add(value)
        return result_set

    def symmetric_difference(self, other_set):
        if not isinstance(other_set, HashSet):
            raise TypeError("Argument must be a HashSet")
        result_set = HashSet()
        for value in self.to_list():
            if not other_set.contains(value):
                result_set.add(value)
        for value in other_set.to_list():
            if not self.contains(value):
                result_set.add(value)
        return result_set

    def is_subset(self, other_set):
        if not isinstance(other_set, HashSet):
            raise TypeError("Argument must be a HashSet")
        for value in self.to_list():
            if not other_set.contains(value):
                return False
        return True