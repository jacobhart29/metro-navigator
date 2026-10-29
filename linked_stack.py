class Node:
    def __init__(self, data):
        self.data = data
        self.next = None
        self.value = None

class Stack:
    def __init__(self):
        self.top = None
        self.size = 0

    def __len__(self):
        return self.size

    def is_empty(self):
        return self.size == 0

    def push(self, data):
        new_node = Node(data)
        new_node.next = self.top
        self.top = new_node
        self.size += 1

    def pop(self):
        if self.is_empty():
            raise IndexError("Pop from empty stack")
        popped_node = self.top
        self.top = self.top.next
        self.size -= 1
        return popped_node.data

    def peek(self):
        if self.is_empty():
            raise IndexError("Peek from empty stack")
        return self.top.data

    def to_list(self):
        result = []
        current = self.top
        while current:
            result.append(current.data)
            current = current.next
        return result

def is_balanced(expression):
    stack = Stack()
    opening = "({["
    closing = ")}]"
    matching = {')': '(', '}': '{', ']': '['}

    for char in expression:
        if char in opening:
            stack.push(char)
        elif char in closing:
            if stack.is_empty() or stack.pop() != matching[char]:
                return False

    return stack.is_empty()
