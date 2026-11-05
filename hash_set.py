class HashSet:
    def __init__(self, capacity=16):
        self.capacity = capacity
        self.size = 0
        self.buckets = [[] for _ in range(capacity)]

    def __len__(self):
        return self.size

    def __contains__(self, item):
        index = hash(item) % self.capacity
        return item in self.buckets[index]

    def is_empty(self):
        return self.size == 0

    def add(self, value):
        if not isinstance(value, str):
            raise TypeError("HashSet only accepts strings")
        index = hash(value) % self.capacity
        if value not in self.buckets[index]:
            self.buckets[index].append(value)
            self.size += 1
            return True
        else:
            return False

    def contains(self, value):
        if not isinstance(value, str):
            raise TypeError("HashSet only accepts strings")
        index = hash(value) % self.capacity
        return value in self.buckets[index]

    def remove(self, value):
        if not isinstance(value, str):
            raise TypeError("HashSet only accepts strings")
        index = hash(value) % self.capacity
        if value in self.buckets[index]:
            self.buckets[index].remove(value)
            self.size -= 1
            return True
        else:
            raise KeyError(value)

    def discard(self, value):
        if not isinstance(value, str):
            raise TypeError("HashSet only accepts strings")
        index = hash(value) % self.capacity
        if value in self.buckets[index]:
            self.buckets[index].remove(value)
            self.size -= 1
            return True
        return False

    def clear(self):
        self.buckets = [[] for _ in range(self.capacity)]
        self.size = 0

    def to_list(self):
        result = []
        for bucket in self.buckets:
            result.extend(bucket)
        return result

    def union(self, other_set):
        if not isinstance(other_set, HashSet):
            raise TypeError("Argument must be a HashSet")
        result_set = HashSet(max(self.capacity, other_set.capacity))
        for value in self.to_list():
            result_set.add(value)
        for value in other_set.to_list():
            result_set.add(value)
        return result_set

    def intersection(self, other_set):
        if not isinstance(other_set, HashSet):
            raise TypeError("Argument must be a HashSet")
        result_set = HashSet(min(self.capacity, other_set.capacity))
        for value in self.to_list():
            if other_set.contains(value):
                result_set.add(value)
        return result_set

    def difference(self, other_set):
        if not isinstance(other_set, HashSet):
            raise TypeError("Argument must be a HashSet")
        result_set = HashSet(self.capacity)
        for value in self.to_list():
            if not other_set.contains(value):
                result_set.add(value)
        return result_set

    def symmetric_difference(self, other_set):
        if not isinstance(other_set, HashSet):
            raise TypeError("Argument must be a HashSet")
        result_set = HashSet(max(self.capacity, other_set.capacity))
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