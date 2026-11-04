from linked_list import LinkedList

class Stack:
    def __init__(self):
        self._list = LinkedList()

    def push(self, value):
        self._list.prepend(value)

    def pop(self):
        if self.is_empty():
            raise IndexError("pop from empty stack")
        return self._list.remove_at(0)

    def peek(self):
        if self.is_empty():
            raise IndexError("peek from empty stack")
        return self._list.head.value

    def is_empty(self):
        return self._list.is_empty()

    def __len__(self):
        return len(self._list)

    def clear(self):
        self._list.clear()

    def to_list(self):
        return self._list.to_list()

def is_balanced(text):
    if not isinstance(text, str):
        raise TypeError("text must be a string")

    stack = Stack()
    pairs = {
        ")": "(",
        "]": "[",
        "}": "{"
    }

    for char in text:
        if char in "([{":
            stack.push(char)
        elif char in ")]}":
            if stack.is_empty():
                return False
            if stack.pop() != pairs[char]:
                return False
    return stack.is_empty()