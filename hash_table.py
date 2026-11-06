
class HashTable:
    def __init__(self, capacity=8):
        self.capacity = capacity
        self.size = 0
        self.buckets = [[] for _ in range(capacity)]

    def __len__(self):
        return self.size

    def _hash(self, key):
        if not isinstance(key, str):
            raise TypeError
        return hash(key) % self.capacity

    def put(self, key, value):
        index = self._hash(key)
        bucket = self.buckets[index]

        for i, (k, _) in enumerate(bucket):
            if k == key:
                bucket[i] = (key, value)
                return

        if (self.size + 1) / self.capacity > 0.75:
            self._resize()
            index = self._hash(key)

        self.buckets[index].append((key, value))
        self.size += 1

    def get(self, key, default=None):
        for k, value in self.buckets[self._hash(key)]:
            if k == key:
                return value
        return default

    def remove(self, key):
        bucket = self.buckets[self._hash(key)]

        for i, (k, value) in enumerate(bucket):
            if k == key:
                bucket.pop(i)
                self.size -= 1
                return value

        raise KeyError(key)

    def contains(self, key):
        return any(k == key for k, _ in self.buckets[self._hash(key)])

    def keys(self):
        return [k for bucket in self.buckets for k, _ in bucket]

    def values(self):
        return [v for bucket in self.buckets for _, v in bucket]

    def items(self):
        return [(k, v) for bucket in self.buckets for k, v in bucket]

    def load_factor(self):
        return self.size / self.capacity

    def _resize(self):
        old = self.buckets
        self.capacity *= 2
        self.buckets = [[] for _ in range(self.capacity)]

        for bucket in old:
            for key, value in bucket:
                self.buckets[self._hash(key)].append((key, value))

    def __getitem__(self, key):
        value = self.get(key)
        if value is None and not self.contains(key):
            raise KeyError(key)
        return value

    def __setitem__(self, key, value):
        self.put(key, value)

    def __contains__(self, key):
        return self.contains(key)
