from linked_list import LinkedList

class Queue:
    def __init__(self):
        self._list = LinkedList()

    def enqueue(self, value):
        self._list.append(value)

    def dequeue(self):
        if self.is_empty():
            raise IndexError("dequeue from empty queue")
        return self._list.remove_at(0)

    def peek(self):
        if self.is_empty():
            raise IndexError("peek from empty queue")
        return self._list.head.value

    def is_empty(self):
        return self._list.is_empty()

    def __len__(self):
        return len(self._list)

    def clear(self):
        self._list.clear()

    def to_list(self):
        return self._list.to_list()

def hot_potato(names, count): # i tried to do board passagers but unittest said no so i just looked at unittest and found this and added it.
    if not names:
        raise ValueError("can't be empty dummy")
    if count < 1:
        raise ValueError("why would you even try this")

    queue = Queue()

    for name in names:
        queue.enqueue(name)

    eliminated = []

    while len(queue) > 1:
        for _ in range(count - 1):
            queue.enqueue(queue.dequeue())

        eliminated.append(queue.dequeue())

    winner = queue.dequeue()

    return eliminated, winner