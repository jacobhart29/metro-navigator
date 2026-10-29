"""Unit tests for LinkedList. Test names correspond to the project check IDs."""
import random
import time
import unittest

from linked_list import LinkedList


class TestLinkedList(unittest.TestCase):
    def test_LL_01(self):
        ll = LinkedList()
        self.assertEqual(len(ll), 0)
        self.assertTrue(ll.is_empty())
        self.assertEqual(ll.to_list(), [])
        self.assertEqual(str(ll), "None")
        self.assertIsNone(ll.head)
        self.assertIsNone(ll.tail)

    def test_LL_02(self):
        ll = LinkedList()
        for value in (1, 2, 3):
            ll.append(value)
        self.assertEqual(ll.to_list(), [1, 2, 3])
        self.assertEqual(len(ll), 3)
        self.assertEqual(ll.head.value, 1)
        self.assertEqual(ll.tail.value, 3)

    def test_LL_03(self):
        ll = LinkedList()
        for value in (1, 2, 3):
            ll.prepend(value)
        self.assertEqual(ll.to_list(), [3, 2, 1])
        self.assertEqual(ll.head.value, 3)
        self.assertEqual(ll.tail.value, 1)

    def test_LL_04(self):
        ll = LinkedList()
        ll.append(5)
        self.assertEqual((ll.head.value, ll.tail.value), (5, 5))
        ll.prepend(4)
        self.assertEqual((ll.head.value, ll.tail.value), (4, 5))
        ll.append(6)
        self.assertEqual(ll.to_list(), [4, 5, 6])
        self.assertEqual((ll.head.value, ll.tail.value), (4, 6))

    def test_LL_05(self):
        ll = LinkedList()
        ll.insert_at(0, "b")
        ll.insert_at(0, "a")
        ll.insert_at(2, "d")
        ll.insert_at(2, "c")
        self.assertEqual(ll.to_list(), ["a", "b", "c", "d"])
        self.assertEqual(ll.tail.value, "d")

    def test_LL_06(self):
        ll = LinkedList()
        for x in [1, 2, 3]:
            ll.append(x)
        before = ll.to_list()
        with self.assertRaises(IndexError):
            ll.insert_at(-1, 9)
        with self.assertRaises(IndexError):
            ll.insert_at(4, 9)
        self.assertEqual(ll.to_list(), before)

    def test_LL_07(self):
        ll = LinkedList()
        for x in [10, 20, 30, 40]:
            ll.append(x)
        self.assertEqual(ll.get(0), 10)
        self.assertEqual(ll.get(2), 30)
        self.assertEqual(ll.get(3), 40)
        for index in (-1, 4):
            with self.assertRaises(IndexError):
                ll.get(index)
        with self.assertRaises(IndexError):
            LinkedList().get(0)

    def test_LL_08(self):
        ll = LinkedList()
        for x in [1, 2, 1]:
            ll.append(x)
        self.assertEqual(ll.find(1), 0)
        self.assertEqual(ll.find(2), 1)
        self.assertEqual(ll.find(99), -1)
        self.assertEqual(LinkedList().find(1), -1)

    def test_LL_09(self):
        ll = LinkedList()
        for x in [1, 2, 1]:
            ll.append(x)
        self.assertTrue(ll.remove(1))
        self.assertEqual(ll.to_list(), [2, 1])
        self.assertEqual(len(ll), 2)

    def test_LL_10(self):
        ll = LinkedList()
        ll.append("kept")
        before = ll.to_list()
        self.assertFalse(ll.remove("missing"))
        self.assertEqual(ll.to_list(), before)
        self.assertEqual(len(ll), 1)
        self.assertFalse(LinkedList().remove("missing"))

    def test_LL_11(self):
        ll = LinkedList()
        for x in [1, 2, 3]:
            ll.append(x)
        self.assertTrue(ll.remove(1))
        self.assertEqual(ll.to_list(), [2, 3])
        self.assertTrue(ll.remove(3))
        self.assertEqual(ll.to_list(), [2])
        ll.append(9)
        self.assertEqual(ll.to_list(), [2, 9])
        self.assertEqual(ll.tail.value, 9)

    def test_LL_12(self):
        ll = LinkedList()
        ll.append("only")
        self.assertEqual(ll.remove_at(0), "only")
        self.assertIsNone(ll.head)
        self.assertIsNone(ll.tail)
        self.assertEqual(len(ll), 0)
        ll.append("again")
        self.assertEqual(ll.to_list(), ["again"])

    def test_LL_13(self):
        ll = LinkedList()
        for x in [10, 20, 30, 40]:
            ll.append(x)
        self.assertEqual(ll.remove_at(0), 10)
        self.assertEqual(ll.remove_at(2), 40)
        self.assertEqual(ll.remove_at(1), 30)
        self.assertEqual(ll.to_list(), [20])
        for index in (-1, 1):
            with self.assertRaises(IndexError):
                ll.remove_at(index)

    def test_LL_14(self):
        ll = LinkedList()
        for x in [1, 2, 3, 4]:
            ll.append(x)
        old_head, old_tail = ll.head, ll.tail
        ll.reverse()
        self.assertEqual(ll.to_list(), [4, 3, 2, 1])
        self.assertIs(ll.head, old_tail)
        self.assertIs(ll.tail, old_head)
        ll.append(5)
        self.assertEqual(ll.to_list(), [4, 3, 2, 1, 5])
        empty = LinkedList()
        empty.reverse()
        single = LinkedList()
        single.append(7)
        single.reverse()
        self.assertEqual(empty.to_list(), [])
        self.assertEqual(single.to_list(), [7])

    def test_LL_15(self):
        ll = LinkedList()
        for x in [1, 2, 3]:
            ll.append(x)
        self.assertEqual([x for x in ll], [1, 2, 3])
        self.assertEqual(list(ll), [1, 2, 3])
        self.assertEqual(str(ll), "1 -> 2 -> 3 -> None")
        self.assertEqual(list(LinkedList()), [])

    def test_LL_16(self):
        ll = LinkedList()
        for x in (1, "two", (3,), [4], None):
            ll.append(x)
        self.assertEqual(len(ll), 5)
        self.assertEqual(ll.find(None), 4)
        ll.clear()
        self.assertTrue(ll.is_empty())
        self.assertIsNone(ll.head)
        self.assertIsNone(ll.tail)
        ll.append("usable")
        other = LinkedList()
        other.append("separate")
        self.assertEqual(ll.to_list(), ["usable"])
        self.assertEqual(other.to_list(), ["separate"])

    def test_LL_17(self):
        ll = LinkedList()
        start = time.perf_counter()
        for x in range(20_000):
            ll.append(x)
        elapsed = time.perf_counter() - start
        self.assertLess(elapsed, 1.0, "append should use the tail pointer")
        self.assertEqual(ll.get(19_999), 19_999)

    def test_LL_18(self):
        rng = random.Random(1801)
        ll = LinkedList()
        model = []
        for _ in range(1_000):
            operation = rng.choice(["append", "prepend", "insert", "remove", "remove_at", "reverse"])
            value = rng.randint(-10, 10)
            if operation == "append":
                ll.append(value)
                model.append(value)
            elif operation == "prepend":
                ll.prepend(value)
                model.insert(0, value)
            elif operation == "insert":
                index = rng.randint(0, len(model))
                ll.insert_at(index, value)
                model.insert(index, value)
            elif operation == "remove":
                expected = value in model
                self.assertEqual(ll.remove(value), expected)
                if expected:
                    model.remove(value)
            elif operation == "remove_at" and model:
                index = rng.randrange(len(model))
                self.assertEqual(ll.remove_at(index), model.pop(index))
            elif operation == "reverse":
                ll.reverse()
                model.reverse()
            self.assertEqual(ll.to_list(), model)
            self.assertEqual(len(ll), len(model))

    def test_LL_19(self):
        ll = LinkedList()
        for x in range(20_000):
            ll.append(x)
        start = time.perf_counter()
        output = [ll.remove_at(0) for _ in range(20_000)]
        elapsed = time.perf_counter() - start
        self.assertLess(elapsed, 1.0, "remove_at(0) should not traverse the list")
        self.assertEqual(output, list(range(20_000)))
        self.assertTrue(ll.is_empty())

    def test_LL_EXTRA_01_remove_matches_value_not_identity(self):
        ll = LinkedList()
        ll.append("same")
        ll.append("same")
        self.assertTrue(ll.remove("same"))
        self.assertEqual(ll.to_list(), ["same"])

    def test_LL_EXTRA_02_to_list_is_a_copy(self):
        ll = LinkedList()
        ll.append(1)
        copy = ll.to_list()
        copy.append(2)
        self.assertEqual(ll.to_list(), [1])


if __name__ == "__main__":
    unittest.main()
