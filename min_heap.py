class MinHeap:
    def __init__(self):
        self._data = []

    def __len__(self):
        return len(self._data)

    def is_empty(self):
        return len(self._data) == 0

    def push(self, priority, item):
        self._data.append((priority, item))
        i = len(self._data) - 1
        while i > 0:
            parent = (i - 1) // 2
            if self._data[i][0] < self._data[parent][0]:
                self._data[i], self._data[parent] = self._data[parent], self._data[i]
                i = parent
            else:
                break

    def peek(self):
        if self.is_empty():
            raise IndexError("peek from empty heap")
        return self._data[0]

    def to_list(self):
        return self._data.copy()

    def _sift_down(self, i):
        n = len(self._data)
        while True:
            left = 2 * i + 1
            right = 2 * i + 2
            smallest = i
            if left < n and self._data[left][0] < self._data[smallest][0]:
                smallest = left
            if right < n and self._data[right][0] < self._data[smallest][0]:
                smallest = right
            if smallest == i:
                break
            self._data[i], self._data[smallest] = self._data[smallest], self._data[i]
            i = smallest

    def pop(self):
        if self.is_empty():
            raise IndexError("pop from empty heap")
        top = self._data[0]
        last = self._data.pop()
        if self._data:
            self._data[0] = last
            self._sift_down(0)
        return top

    @staticmethod
    def build_heap(pairs):
        heap = MinHeap()
        heap._data = list(pairs)
        for i in range(len(heap._data) // 2 - 1, -1, -1):
            heap._sift_down(i)
        return heap

    def drain(self):
        result = []
        while not self.is_empty():
            result.append(self.pop())
        return result

    def is_valid_heap(self):
        for i in range(1, len(self._data)):
            parent = (i - 1) // 2
            if self._data[parent][0] > self._data[i][0]:
                return False
        return True