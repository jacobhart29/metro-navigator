class Node:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.next = None

class HashTable:
    def __init__(self, capacity=8):
        self.capacity = capacity
        self.size = 0
        self.buckets = [None] * capacity

    def __len__(self):
        return self.size

    def _hash(self, key):
        if not isinstance(key, str):
            raise TypeError
        hash_value = 0
        for char in key:
            hash_value = hash_value * 31 + ord(char)
        return hash_value % self.capacity

    def put(self, key, value):
        index = self._hash(key)
        entry = self.buckets[index]
        while entry is not None:
            if entry.key == key:
                entry.value = value
                return
            entry = entry.next

        if (self.size + 1) / self.capacity > 0.75:
            self._resize()
            index = self._hash(key)

        new_node = Node(key, value)
        new_node.next = self.buckets[index]
        self.buckets[index] = new_node
        self.size += 1

    def get(self, key, default=None):
        entry = self.buckets[self._hash(key)]
        while entry is not None:
            if entry.key == key:
                return entry.value
            entry = entry.next
        return default

    def remove(self, key):
        index = self._hash(key)
        entry = self.buckets[index]
        prev = None
        while entry is not None:
            if entry.key == key:
                if prev is None:
                    self.buckets[index] = entry.next
                else:
                    prev.next = entry.next
                self.size -= 1
                return entry.value
            prev = entry
            entry = entry.next
        raise KeyError(key)

    def contains(self, key):
        entry = self.buckets[self._hash(key)]
        while entry is not None:
            if entry.key == key:
                return True
            entry = entry.next
        return False

    def keys(self):
        result = []
        for slot in self.buckets:
            entry = slot
            while entry is not None:
                result.append(entry.key)
                entry = entry.next
        return result

    def values(self):
        result = []
        for slot in self.buckets:
            entry = slot
            while entry is not None:
                result.append(entry.value)
                entry = entry.next
        return result

    def items(self):
        result = []
        for slot in self.buckets:
            entry = slot
            while entry is not None:
                result.append((entry.key, entry.value))
                entry = entry.next
        return result

    def load_factor(self):
        return self.size / self.capacity

    def _resize(self):
        old = self.buckets
        self.capacity *= 2
        self.buckets = [None] * self.capacity

        for slot in old:
            entry = slot
            while entry is not None:
                next_entry = entry.next
                index = self._hash(entry.key)
                entry.next = self.buckets[index]
                self.buckets[index] = entry
                entry = next_entry

    def __getitem__(self, key):
        value = self.get(key)
        if value is None and not self.contains(key):
            raise KeyError(key)
        return value

    def __setitem__(self, key, value):
        self.put(key, value)

    def __contains__(self, key):
        return self.contains(key)
