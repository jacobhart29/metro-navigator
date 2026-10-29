"""Unit tests for HashSet. Built-in sets are used only as test-side models."""
import random
import time
import unittest

from hash_set import HashSet


class TestHashSet(unittest.TestCase):
    def test_SET_01(self):
        s = HashSet()
        self.assertEqual(len(s), 0)
        self.assertTrue(s.is_empty())
        self.assertEqual(s.to_list(), [])
        self.assertFalse(s.contains("a"))

    def test_SET_02(self):
        s = HashSet()
        self.assertTrue(s.add("a"))
        self.assertFalse(s.add("a"))
        self.assertEqual(len(s), 1)

    def test_SET_03(self):
        s = HashSet()
        s.add("")
        s.add("A")
        s.add("a")
        self.assertIn("", s)
        self.assertIn("A", s)
        self.assertIn("a", s)
        self.assertEqual(len(s), 3)
        s.remove("A")
        self.assertNotIn("A", s)

    def test_SET_04(self):
        s = HashSet()
        s.add("a")
        s.add("b")
        s.remove("a")
        self.assertNotIn("a", s)
        self.assertEqual(len(s), 1)
        with self.assertRaises(KeyError):
            s.remove("missing")
        self.assertTrue(s.discard("b"))
        self.assertFalse(s.discard("b"))
        self.assertFalse(s.discard("never-there"))

    def test_SET_05(self):
        s = HashSet()
        for bad in (5, None, ("a",)):
            for method in (s.add, s.remove, s.discard, s.contains):
                with self.subTest(value=bad, method=method.__name__):
                    with self.assertRaises(TypeError):
                        method(bad)

    def test_SET_06(self):
        a, b = HashSet(), HashSet()
        for value in ["a", "b", "c"]:
            a.add(value)
        for value in ["c", "d"]:
            b.add(value)
        a_before, b_before = sorted(a.to_list()), sorted(b.to_list())
        union = a.union(b)
        self.assertEqual(sorted(union.to_list()), ["a", "b", "c", "d"])
        self.assertEqual(sorted(a.to_list()), a_before)
        self.assertEqual(sorted(b.to_list()), b_before)
        self.assertEqual(sorted(a.union(HashSet()).to_list()), ["a", "b", "c"])
        self.assertEqual(sorted(HashSet().union(a).to_list()), ["a", "b", "c"])
        self.assertEqual(len(a.union(a)), 3)

    def test_SET_07(self):
        a, b = HashSet(), HashSet()
        for value in ["a", "b", "c"]:
            a.add(value)
        for value in ["b", "c", "d"]:
            b.add(value)
        self.assertEqual(sorted(a.intersection(b).to_list()), ["b", "c"])
        self.assertEqual(sorted(a.to_list()), ["a", "b", "c"])
        self.assertEqual(HashSet().intersection(a).to_list(), [])
        disjoint = HashSet()
        disjoint.add("z")
        self.assertEqual(a.intersection(disjoint).to_list(), [])

    def test_SET_08(self):
        a, b = HashSet(), HashSet()
        for value in ["a", "b", "c"]:
            a.add(value)
        for value in ["b", "d"]:
            b.add(value)
        self.assertEqual(sorted(a.difference(b).to_list()), ["a", "c"])
        self.assertEqual(sorted(b.difference(a).to_list()), ["d"])
        self.assertEqual(a.difference(a).to_list(), [])
        self.assertEqual(sorted(a.difference(HashSet()).to_list()), ["a", "b", "c"])

    def test_SET_09(self):
        a, b = HashSet(), HashSet()
        for value in ["a", "b", "c"]:
            a.add(value)
        for value in ["b", "c", "d"]:
            b.add(value)
        self.assertEqual(sorted(a.symmetric_difference(b).to_list()), ["a", "d"])
        self.assertEqual(a.symmetric_difference(a).to_list(), [])

    def test_SET_10(self):
        a, b, empty = HashSet(), HashSet(), HashSet()
        for value in ["a", "b"]:
            a.add(value)
        for value in ["a", "b", "c"]:
            b.add(value)
        self.assertTrue(a.is_subset(b))
        self.assertFalse(b.is_subset(a))
        self.assertTrue(a.is_subset(a))
        self.assertTrue(empty.is_subset(a))
        self.assertFalse(a.is_subset(empty))

    def test_SET_11(self):
        s = HashSet()
        operations = [s.union, s.intersection, s.difference, s.symmetric_difference, s.is_subset]
        bad_values = [["a"], "abc", None, {"a"}]
        for method in operations:
            for other in bad_values:
                with self.subTest(method=method.__name__, other_type=type(other).__name__):
                    with self.assertRaises(TypeError):
                        method(other)

    def test_SET_12(self):
        start = time.perf_counter()
        a, b = HashSet(), HashSet()
        for i in range(3_000):
            a.add(f"item_{i}")
            a.add(f"item_{i}")
        for i in range(2_000, 5_000):
            b.add(f"item_{i}")
        self.assertEqual(len(a.union(b)), 5_000)
        self.assertEqual(len(a.intersection(b)), 1_000)
        self.assertEqual(len(a.difference(b)), 2_000)
        self.assertEqual(len(a.symmetric_difference(b)), 4_000)
        self.assertEqual(len(a), 3_000)
        self.assertLess(time.perf_counter() - start, 1.0)

    def test_SET_13(self):
        rng = random.Random(1301)
        s = HashSet()
        model = set()
        names = [f"name{i}" for i in range(40)]
        for _ in range(2_000):
            value = rng.choice(names)
            op = rng.choice(["add", "remove", "discard"])
            if op == "add":
                self.assertEqual(s.add(value), value not in model)
                model.add(value)
            elif op == "remove":
                if value in model:
                    s.remove(value)
                    model.remove(value)
                else:
                    with self.assertRaises(KeyError):
                        s.remove(value)
            else:
                self.assertEqual(s.discard(value), value in model)
                model.discard(value)
            self.assertEqual(sorted(s.to_list()), sorted(model))
            self.assertEqual(len(s), len(model))

    def test_SET_EXTRA_01_clear_makes_the_set_reusable(self):
        s = HashSet()
        s.add("station")
        s.clear()
        self.assertTrue(s.is_empty())
        self.assertTrue(s.add("again"))
        self.assertIn("again", s)

    def test_SET_EXTRA_02_result_is_a_separate_hash_set(self):
        a, b = HashSet(), HashSet()
        a.add("a")
        b.add("b")
        result = a.union(b)
        result.add("c")
        self.assertNotIn("c", a)
        self.assertNotIn("c", b)


if __name__ == "__main__":
    unittest.main()
