class TreeNode:
    def __init__(self, key, value=None):
        self.key = key
        self.value = value
        self.left = None
        self.right = None


class BST:
    def __init__(self):
        self.root = None
        self._size = 0

    def __len__(self):
        return self._size

    def is_empty(self):
        return self._size == 0

    def insert(self, key, value=None):
        if self.root is None:
            self.root = TreeNode(key, value)
            self._size += 1
            return
        node = self.root
        while True:
            if key == node.key:
                node.value = value
                return
            if key < node.key:
                if node.left is None:
                    node.left = TreeNode(key, value)
                    self._size += 1
                    return
                node = node.left
            else:
                if node.right is None:
                    node.right = TreeNode(key, value)
                    self._size += 1
                    return
                node = node.right

    def _find(self, key):
        node = self.root
        while node is not None:
            if key == node.key:
                return node
            if key < node.key:
                node = node.left
            else:
                node = node.right
        return None

    def contains(self, key):
        return self._find(key) is not None

    def get(self, key):
        node = self._find(key)
        if node is None:
            raise KeyError(key)
        return node.value

    def inorder(self):
        result = []
        self._inorder(self.root, result)
        return result

    def _inorder(self, node, result):
        if node is None:
            return
        self._inorder(node.left, result)
        result.append(node.key)
        self._inorder(node.right, result)

    def level_order(self):
        result = []
        if self.root is None:
            return result
        queue = [self.root]
        i = 0
        while i < len(queue):
            node = queue[i]
            i += 1
            result.append(node.key)
            if node.left is not None:
                queue.append(node.left)
            if node.right is not None:
                queue.append(node.right)
        return result

    def height(self):
        return self._height(self.root)

    def _height(self, node):
        if node is None:
            return 0
        return 1 + max(self._height(node.left), self._height(node.right))

    def min_key(self):
        if self.root is None:
            raise ValueError("min_key from empty BST")
        node = self.root
        while node.left is not None:
            node = node.left
        return node.key

    def count_leaves(self):
        return self._leaves(self.root)

    def _leaves(self, node):
        if node is None:
            return 0
        if node.left is None and node.right is None:
            return 1
        return self._leaves(node.left) + self._leaves(node.right)

    def range_query(self, low, high):
        result = []
        if low > high:
            return result
        self._range(self.root, low, high, result)
        return result

    def _range(self, node, low, high, result):
        if node is None:
            return
        if low < node.key:
            self._range(node.left, low, high, result)
        if low <= node.key <= high:
            result.append(node.key)
        if node.key < high:
            self._range(node.right, low, high, result)

    def is_valid_bst(self):
        return self._valid(self.root, None, None)

    def _valid(self, node, low, high):
        if node is None:
            return True
        if low is not None and node.key <= low:
            return False
        if high is not None and node.key >= high:
            return False
        return self._valid(node.left, low, node.key) and self._valid(node.right, node.key, high)

    def delete(self, key):
        if self._find(key) is None:
            return False
        self.root = self._delete(self.root, key)
        self._size -= 1
        return True

    def _delete(self, node, key):
        if node is None:
            return None
        if key < node.key:
            node.left = self._delete(node.left, key)
        elif key > node.key:
            node.right = self._delete(node.right, key)
        else:
            if node.left is None:
                return node.right
            if node.right is None:
                return node.left
            successor = node.right
            while successor.left is not None:
                successor = successor.left
            node.key = successor.key
            node.value = successor.value
            node.right = self._delete(node.right, successor.key)
        return node

    def preorder(self):
        result = []
        self._preorder(self.root, result)
        return result

    def _preorder(self, node, result):
        if node is None:
            return
        result.append(node.key)
        self._preorder(node.left, result)
        self._preorder(node.right, result)


    def postorder(self):
        result = []
        self._postorder(self.root, result)
        return result

    def _postorder(self, node, result):
        if node is None:
            return
        self._postorder(node.left, result)
        self._postorder(node.right, result)
        result.append(node.key)

    def max_key(self):
        if self.root is None:
            raise ValueError("max_key from empty BST")

        node = self.root
        while node.right is not None:
            node = node.right

        return node.key
