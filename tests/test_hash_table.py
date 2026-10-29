"""Unit tests for HashTable."""
import random
import time
import unittest

from hash_table import HashTable


class TestHashTable(unittest.TestCase):
    def test_HT_01(self):
        ht = HashTable()
        self.assertEqual(len(ht), 0)
        self.assertEqual(ht.capacity, 8)
        self.assertEqual(ht.keys(), [])
        self.assertFalse(ht.contains("a"))
        self.assertEqual(ht.load_factor(), 0)

    def test_HT_02(self):
        ht = HashTable()
        ht.put("a", 1)
        ht["b"] = 2
        self.assertIs(ht.get("a"), 1)
        self.assertEqual(ht["b"], 2)
        self.assertEqual(len(ht), 2)

    def test_HT_03(self):
        ht = HashTable()
        ht.put("a", 1)
        ht.put("a", 99)
        self.assertEqual(ht.get("a"), 99)
        self.assertEqual(len(ht), 1)

    def test_HT_04(self):
        ht = HashTable()
        self.assertIsNone(ht.get("zzz"))
        self.assertEqual(ht.get("zzz", 0), 0)
        with self.assertRaises(KeyError):
            _ = ht["zzz"]

    def test_HT_05(self):
        ht = HashTable()
        ht.put("a", 1)
        self.assertTrue(ht.contains("a"))
        self.assertIn("a", ht)
        self.assertFalse(ht.contains("missing"))
        self.assertEqual(ht.remove("a"), 1)
        self.assertNotIn("a", ht)

    def test_HT_06(self):
        ht = HashTable()
        ht.put("a", 10)
        self.assertEqual(ht.remove("a"), 10)
        self.assertEqual(len(ht), 0)
        with self.assertRaises(KeyError):
            ht.remove("a")
        ht.put("a", 20)
        self.assertEqual(ht.get("a"), 20)

    def test_HT_07(self):
        ht = HashTable()
        self.assertIsInstance(ht._hash("station"), int)
        self.assertEqual(ht._hash("station"), ht._hash("station"))
        self.assertGreaterEqual(ht._hash("station"), 0)
        self.assertLess(ht._hash("station"), ht.capacity)
        for i in range(20):
            ht.put(f"key{i}", i)
        self.assertGreater(ht.capacity, 8)
        self.assertLess(ht._hash("station"), ht.capacity)

    def test_HT_08(self):
        ht = HashTable()
        groups = {}
        colliding = None
        for i in range(10_000):
            key = f"collision_{i}"
            bucket = ht._hash(key)
            groups.setdefault(bucket, []).append(key)
            if len(groups[bucket]) == 3:
                colliding = groups[bucket]
                break
        self.assertIsNotNone(colliding, "should find three keys with the same bucket")
        for i, key in enumerate(colliding):
            ht.put(key, i)
        self.assertTrue(all(ht.get(key) == i for i, key in enumerate(colliding)))
        self.assertEqual(ht.remove(colliding[0]), 0)
        self.assertEqual(ht.get(colliding[1]), 1)
        self.assertEqual(ht.get(colliding[2]), 2)
        self.assertEqual(ht.remove(colliding[1]), 1)
        self.assertEqual(ht.get(colliding[2]), 2)
        self.assertEqual(ht.remove(colliding[2]), 2)
        self.assertEqual(len(ht), 0)

    def test_HT_09(self):
        ht = HashTable()
        for key, value in [("", 0), ("A", 1), ("a", 2), ("abc", 3), ("cba", 4)]:
            ht.put(key, value)
        self.assertEqual(len(ht), 5)
        self.assertEqual([ht.get(k) for k in ["", "A", "a", "abc", "cba"]], [0, 1, 2, 3, 4])

    def test_HT_10(self):
        ht = HashTable()
        for bad_key in (5, None, 3.14, ("a",)):
            for method in (ht.put, ht.get, ht.remove, ht.contains):
                with self.subTest(key=bad_key, method=method.__name__):
                    with self.assertRaises(TypeError):
                        if method == ht.put:
                            method(bad_key, 1)
                        else:
                            method(bad_key)

    def test_HT_11(self):
        ht = HashTable()
        values = [("none", None), ("zero", 0), ("false", False), ("list", [])]
        for key, value in values:
            ht.put(key, value)
        for key, value in values:
            self.assertEqual(ht.get(key, "default"), value)
            self.assertTrue(ht.contains(key))
        self.assertIsNone(ht.get("none", "default"))

    def test_HT_12(self):
        ht = HashTable()
        for i in range(6):
            ht.put(f"k{i}", i)
        self.assertEqual(ht.capacity, 8)
        ht.put("k6", 6)
        self.assertEqual(ht.capacity, 16)
        ht.put("k6", 99)
        self.assertEqual(ht.capacity, 16)
        self.assertEqual(len(ht), 7)
        self.assertEqual(ht.get("k6"), 99)

    def test_HT_13(self):
        ht = HashTable()
        for i in range(100):
            ht.put(f"key{i}", i)
            self.assertLessEqual(ht.load_factor(), 0.75)
        for i in range(100):
            self.assertEqual(ht.get(f"key{i}"), i)

    def test_HT_14(self):
        ht = HashTable()
        expected = {"Airport": 1, "Beach": 3, "Campus": 2}
        for key, value in expected.items():
            ht.put(key, value)
        keys, values, items = ht.keys(), ht.values(), ht.items()
        self.assertEqual(len(keys), len(ht))
        self.assertEqual(len(values), len(ht))
        self.assertEqual(len(items), len(ht))
        self.assertEqual(sorted(keys), sorted(expected))
        self.assertEqual(dict(items), expected)
        self.assertEqual(len(keys), len(values))
        for key, value, item in zip(keys, values, items):
            self.assertEqual((key, value), item)
        for key, value in items:
            self.assertEqual(ht.get(key), value)

    def test_HT_15(self):
        ht = HashTable()
        for i in range(7):
            ht.put(f"k{i}", i)
        cap = ht.capacity
        self.assertEqual(ht.load_factor(), len(ht) / ht.capacity)
        ht.remove("k0")
        self.assertEqual(ht.load_factor(), len(ht) / ht.capacity)
        self.assertEqual(ht.capacity, cap)

    def test_HT_16(self):
        ht = HashTable()
        start = time.perf_counter()
        for i in range(5_000):
            ht.put(f"station_{i}", i)
        for i in range(5_000):
            self.assertEqual(ht.get(f"station_{i}"), i)
        for i in range(0, 5_000, 2):
            self.assertEqual(ht.remove(f"station_{i}"), i)
        elapsed = time.perf_counter() - start
        self.assertLess(elapsed, 1.0)
        self.assertEqual(len(ht), 2_500)
        for i in range(5_000):
            self.assertEqual(ht.contains(f"station_{i}"), i % 2 == 1)

    def test_HT_17(self):
        rng = random.Random(1701)
        ht = HashTable()
        model = {}
        for _ in range(2_000):
            key = f"k{rng.randrange(50)}"
            op = rng.choice(["put", "put", "get", "remove"])
            if op == "put":
                value = rng.choice([None, 0, False, rng.randint(-20, 20)])
                ht.put(key, value)
                model[key] = value
            elif op == "get":
                self.assertEqual(ht.get(key, "MISSING"), model.get(key, "MISSING"))
            elif key in model:
                self.assertEqual(ht.remove(key), model.pop(key))
            else:
                with self.assertRaises(KeyError):
                    ht.remove(key)
            self.assertEqual(len(ht), len(model))
            for model_key, model_value in model.items():
                self.assertEqual(ht.get(model_key, "MISSING"), model_value)

    def test_HT_EXTRA_01_clear_not_required_but_instances_are_independent(self):
        a, b = HashTable(), HashTable()
        a.put("x", 1)
        self.assertFalse(b.contains("x"))

    def test_HT_EXTRA_02_returned_views_are_independent_lists(self):
        ht = HashTable()
        ht.put("x", 1)
        keys = ht.keys()
        values = ht.values()
        items = ht.items()
        keys.clear(); values.clear(); items.clear()
        self.assertEqual(ht.get("x"), 1)
        self.assertEqual(len(ht), 1)


if __name__ == "__main__":
    unittest.main()
