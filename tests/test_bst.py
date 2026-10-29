"""Unit tests for BST."""
import random
import unittest

from bst import BST


def reference_tree():
    tree = BST()
    for key in [50, 30, 70, 20, 40, 60, 80]:
        tree.insert(key, str(key))
    return tree


class TestBST(unittest.TestCase):
    def test_BST_01(self):
        tree = BST()
        self.assertEqual(len(tree), 0)
        self.assertTrue(tree.is_empty())
        self.assertEqual(tree.height(), 0)
        self.assertEqual(tree.count_leaves(), 0)
        self.assertEqual(tree.inorder(), [])
        self.assertEqual(tree.preorder(), [])
        self.assertEqual(tree.postorder(), [])
        self.assertEqual(tree.level_order(), [])
        self.assertFalse(tree.contains(1))
        self.assertIsNone(tree.root)

    def test_BST_02(self):
        tree = BST()
        with self.assertRaises(ValueError):
            tree.min_key()
        with self.assertRaises(ValueError):
            tree.max_key()

    def test_BST_03(self):
        tree = BST()
        tree.insert(7, "seven")
        self.assertEqual(len(tree), 1)
        self.assertEqual(tree.height(), 1)
        self.assertEqual(tree.count_leaves(), 1)
        self.assertEqual(tree.min_key(), 7)
        self.assertEqual(tree.max_key(), 7)

    def test_BST_04(self):
        tree = reference_tree()
        self.assertEqual(tree.inorder(), [20, 30, 40, 50, 60, 70, 80])
        self.assertEqual(tree.preorder(), [50, 30, 20, 40, 70, 60, 80])
        self.assertEqual(tree.postorder(), [20, 40, 30, 60, 80, 70, 50])
        self.assertEqual(tree.level_order(), [50, 30, 70, 20, 40, 60, 80])
        self.assertEqual(tree.height(), 3)
        self.assertEqual(tree.count_leaves(), 4)
        self.assertEqual(len(tree), 7)

    def test_BST_05(self):
        tree = BST()
        tree.insert(50, "a")
        tree.insert(50, "b")
        self.assertEqual(len(tree), 1)
        self.assertEqual(tree.get(50), "b")

    def test_BST_06(self):
        tree = reference_tree()
        for key in [20, 30, 40, 50, 60, 70, 80]:
            self.assertTrue(tree.contains(key))
            self.assertEqual(tree.get(key), str(key))
        for key in [10, 55, 100]:
            self.assertFalse(tree.contains(key))
        with self.assertRaises(KeyError):
            tree.get(99)

    def test_BST_07(self):
        ascending = BST()
        for key in range(1, 501):
            ascending.insert(key, key)
        self.assertEqual(ascending.height(), 500)
        self.assertEqual(ascending.inorder(), list(range(1, 501)))
        self.assertTrue(ascending.is_valid_bst())
        descending = BST()
        for key in range(500, 0, -1):
            descending.insert(key, key)
        self.assertEqual(descending.height(), 500)
        self.assertEqual(descending.inorder(), list(range(1, 501)))
        self.assertTrue(descending.is_valid_bst())

    def test_BST_08(self):
        tree = reference_tree()
        self.assertEqual(tree.min_key(), 20)
        self.assertEqual(tree.max_key(), 80)
        tree.delete(20)
        tree.delete(80)
        self.assertEqual(tree.min_key(), 30)
        self.assertEqual(tree.max_key(), 70)

    def test_BST_09(self):
        tree = reference_tree()
        self.assertTrue(tree.delete(20))
        self.assertEqual(tree.inorder(), [30, 40, 50, 60, 70, 80])
        self.assertEqual(len(tree), 6)

    def test_BST_10(self):
        left_child_case = BST()
        for key in [50, 30, 70, 20]:
            left_child_case.insert(key, key)
        self.assertTrue(left_child_case.delete(30))
        self.assertEqual(left_child_case.preorder(), [50, 20, 70])
        right_child_case = BST()
        for key in [50, 30, 70, 80]:
            right_child_case.insert(key, key)
        self.assertTrue(right_child_case.delete(70))
        self.assertEqual(right_child_case.preorder(), [50, 30, 80])

    def test_BST_11(self):
        tree = reference_tree()
        self.assertTrue(tree.delete(70))
        self.assertEqual(tree.preorder(), [50, 30, 20, 40, 80, 60])
        self.assertEqual(tree.inorder(), [20, 30, 40, 50, 60, 80])

    def test_BST_12(self):
        tree = reference_tree()
        self.assertTrue(tree.delete(50))
        self.assertEqual(tree.root.key, 60)
        self.assertEqual(tree.preorder(), [60, 30, 20, 40, 70, 80])

    def test_BST_13(self):
        tree = BST()
        tree.insert(50, 50)
        tree.insert(30, 30)
        self.assertTrue(tree.delete(50))
        self.assertEqual(tree.root.key, 30)
        self.assertTrue(tree.delete(30))
        self.assertIsNone(tree.root)
        tree.insert(42, 42)
        self.assertEqual(tree.inorder(), [42])

    def test_BST_14(self):
        tree = reference_tree()
        before = tree.inorder()
        self.assertFalse(tree.delete(999))
        self.assertEqual(tree.inorder(), before)
        self.assertEqual(len(tree), 7)
        self.assertFalse(BST().delete(1))

    def test_BST_15(self):
        tree = BST()
        for key in [50, 30, 70, 60, 65]:
            tree.insert(key, key)
        self.assertTrue(tree.delete(50))
        self.assertEqual(tree.preorder(), [60, 30, 70, 65])
        self.assertTrue(tree.is_valid_bst())

    def test_BST_16(self):
        keys = [50, 30, 70, 20, 40, 60, 80]
        for deletion_order in (keys, list(reversed(keys))):
            tree = reference_tree()
            remaining = set(keys)
            for key in deletion_order:
                self.assertTrue(tree.delete(key))
                remaining.remove(key)
                self.assertTrue(tree.is_valid_bst())
                self.assertEqual(len(tree), len(remaining))
                self.assertEqual(tree.inorder(), sorted(remaining))

    def test_BST_17(self):
        tree = reference_tree()
        self.assertEqual(tree.range_query(35, 65), [40, 50, 60])
        self.assertEqual(tree.range_query(30, 70), [30, 40, 50, 60, 70])
        self.assertEqual(tree.range_query(0, 100), [20, 30, 40, 50, 60, 70, 80])
        self.assertEqual(tree.range_query(51, 59), [])
        self.assertEqual(tree.range_query(70, 30), [])
        self.assertEqual(BST().range_query(0, 10), [])

    def test_BST_18(self):
        tree = BST()
        for key in ["dog", "cat", "emu", "ant"]:
            tree.insert(key, key.upper())
        self.assertEqual(tree.inorder(), ["ant", "cat", "dog", "emu"])
        self.assertEqual(tree.min_key(), "ant")
        self.assertEqual(tree.max_key(), "emu")

    def test_BST_19(self):
        tree = reference_tree()
        self.assertTrue(tree.is_valid_bst())
        tree.root.left.right.key = 55
        self.assertFalse(tree.is_valid_bst())

    def test_BST_20(self):
        rng = random.Random(2001)
        tree = BST()
        model = {}
        for _ in range(1_000):
            key = rng.randrange(201)
            if rng.random() < 0.58:
                value = rng.randint(-1_000, 1_000)
                tree.insert(key, value)
                model[key] = value
            else:
                result = tree.delete(key)
                expected = key in model
                self.assertEqual(result, expected)
                model.pop(key, None)
            self.assertEqual(tree.inorder(), sorted(model))
            self.assertEqual(len(tree), len(model))
            self.assertTrue(tree.is_valid_bst())
            for sample in rng.sample(list(model), min(3, len(model))):
                self.assertEqual(tree.get(sample), model[sample])

    def test_BST_21(self):
        tree = BST()
        for key in [1, 2, 3, 4]:
            tree.insert(key, key)
        self.assertEqual(tree.level_order(), [1, 2, 3, 4])
        other = BST()
        other.insert(5, 5)
        other.insert(3, 3)
        self.assertEqual(other.level_order(), [5, 3])

    def test_BST_EXTRA_01_empty_range_is_safe(self):
        self.assertEqual(BST().range_query(0, 0), [])

    def test_BST_EXTRA_02_duplicate_insert_does_not_change_height(self):
        tree = reference_tree()
        old_height = tree.height()
        tree.insert(40, "updated")
        self.assertEqual(tree.height(), old_height)
        self.assertEqual(len(tree), 7)
        self.assertEqual(tree.get(40), "updated")


if __name__ == "__main__":
    unittest.main()
