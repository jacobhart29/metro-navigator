class Node:
    def __init__(self, value):
        self.value = value
        self.next = None


class LinkedList:
    def __init__(self):
        self.head = None
        self.tail = None
        self.size = 0

    def __len__(self):
        return self.size

    def is_empty(self):
        return self.size == 0

    def prepend(self, value):
        new_node = Node(value)
        if self.is_empty():
            self.head = new_node
            self.tail = new_node
        else:
            new_node.next = self.head
            self.head = new_node
        self.size += 1

    def append(self, value):
        new_node = Node(value)
        if self.is_empty():
            self.head = new_node
            self.tail = new_node
        else:
            self.tail.next = new_node
            self.tail = new_node
        self.size += 1

    def to_list(self):
        result = []
        current = self.head
        while current:
            result.append(current.value)
            current = current.next
        return result

    def insert_at(self, index, value):
        if index < 0 or index > self.size:
            raise IndexError("Index out of bounds")
        if index == 0:
            self.prepend(value)
        elif index == self.size:
            self.append(value)
        else:
            new_node = Node(value)
            current = self.head
            for _ in range(index - 1):
                current = current.next
            new_node.next = current.next
            current.next = new_node
            self.size += 1

    def get(self, index):
        if index < 0 or index >= self.size:
            raise IndexError("Index out of bounds")
        current = self.head
        for _ in range(index):
            current = current.next
        return current.value

    def find(self, target):
        current = self.head
        index = 0
        while current:
            if current.value == target:
                return index
            current = current.next
            index += 1
        return -1

    def clear(self):
        self.head = None
        self.tail = None
        self.size = 0

    def remove(self, value) -> bool:
        if self.is_empty():
            return False

        if self.head.value == value:
            self.head = self.head.next
            if self.head is None:
                self.tail = None
            self.size -= 1
            return True

        current = self.head
        while current.next:
            if current.next.value == value:
                if current.next == self.tail:
                    self.tail = current
                current.next = current.next.next
                self.size -= 1
                return True
            current = current.next

        return False

    def remove_at(self, index):
        if index < 0 or index >= self.size:
            raise IndexError("Index out of bounds")

        if index == 0:
            popped_value = self.head.value
            self.head = self.head.next
            if self.head is None:
                self.tail = None
            self.size -= 1
            return popped_value

        current = self.head
        for _ in range(index - 1):
            current = current.next

        popped_value = current.next.value
        if current.next == self.tail:
            self.tail = current
        current.next = current.next.next
        self.size -= 1
        return popped_value

    def reverse(self):
        if self.size <= 1:
            return
        
        prev = None
        current = self.head
        self.tail = current 
        
        while current:
            next_node = current.next
            current.next = prev
            prev = current
            current = next_node
            
        self.head = prev

    def __iter__(self):
        current = self.head
        while current:
            yield current.value
            current = current.next

    def __str__(self):
        if self.is_empty():
            return "None"
        result = []
        current = self.head
        while current:
            result.append(str(current.value))
            current = current.next
        result.append("None")
        return " -> ".join(result)
