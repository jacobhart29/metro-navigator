"""Unit tests for the array-based MinHeap."""
import random
import time
import unittest

from min_heap import MinHeap


def priorities(heap):
    return [pair[0] for pair in heap.to_list()]


class TestMinHeap(unittest.TestCase):
    def test_MH_01(self):
        heap = MinHeap()
        self.assertEqual(len(heap), 0)
        self.assertTrue(heap.is_empty())
        self.assertEqual(heap.to_list(), [])
        self.assertTrue(heap.is_valid_heap())

    def test_MH_02(self):
        heap = MinHeap()
        with self.assertRaises(IndexError):
            heap.pop()
        with self.assertRaises(IndexError):
            heap.peek()

    def test_MH_03(self):
        heap = MinHeap()
        heap.push(4, "x")
        self.assertEqual(heap.peek(), (4, "x"))
        self.assertEqual(len(heap), 1)
        self.assertEqual(heap.pop(), (4, "x"))
        self.assertTrue(heap.is_empty())

    def test_MH_04(self):
        heap = MinHeap()
        for priority in [5, 3, 8, 1]:
            heap.push(priority, str(priority))
        self.assertEqual(priorities(heap), [1, 3, 8, 5])

    def test_MH_05(self):
        heap = MinHeap()
        for priority in [5, 3, 8, 1, 9, 2, 7]:
            heap.push(priority, f"item-{priority}")
        output = [heap.pop() for _ in range(7)]
        self.assertEqual([p for p, _ in output], [1, 2, 3, 5, 7, 8, 9])
        self.assertEqual([item for _, item in output], [f"item-{p}" for p, _ in output])

    def test_MH_06(self):
        heap = MinHeap()
        for priority in [5, 3, 8, 1]:
            heap.push(priority, str(priority))
        self.assertEqual(heap.pop(), (1, "1"))
        self.assertEqual(priorities(heap), [3, 5, 8])

    def test_MH_07(self):
        pairs = [(p, str(p)) for p in [1, 5, 2, 6, 7, 3, 4]]
        heap = MinHeap.build_heap(pairs)
        self.assertEqual(priorities(heap), [1, 5, 2, 6, 7, 3, 4])
        self.assertEqual(heap.pop(), (1, "1"))
        self.assertEqual(priorities(heap), [2, 5, 3, 6, 7, 4])

    def test_MH_08(self):
        heap = MinHeap()
        items = ["alpha", "beta", "gamma", "delta", "epsilon"]
        for item in items:
            heap.push(5, item)
        popped = [heap.pop()[1] for _ in items]
        self.assertEqual(sorted(popped), sorted(items))
        self.assertEqual(len(popped), len(set(items)))

    def test_MH_09(self):
        heap = MinHeap()
        heap.push(2, {})
        heap.push(2, {"x": 1})
        output = [heap.pop(), heap.pop()]
        self.assertEqual([priority for priority, _ in output], [2, 2])
        self.assertEqual(len(output), 2)

    def test_MH_10(self):
        heap = MinHeap()
        inputs = [(2.5, "two-five"), (-3, "negative"), (0, None), (2, "two"), (0.5, "half")]
        rng = random.Random(1001)
        rng.shuffle(inputs)
        for priority, item in inputs:
            heap.push(priority, item)
        output = [heap.pop() for _ in inputs]
        self.assertEqual([p for p, _ in output], [-3, 0, 0.5, 2, 2.5])
        self.assertIsNone(output[1][1])

    def test_MH_11(self):
        pairs = [(p, f"v{p}") for p in [5, 4, 3, 2, 1]]
        original = pairs[:]
        heap = MinHeap.build_heap(pairs)
        self.assertEqual(priorities(heap), [1, 2, 3, 5, 4])
        self.assertTrue(heap.is_valid_heap())
        self.assertEqual(pairs, original)

    def test_MH_12(self):
        heap = MinHeap.build_heap([])
        self.assertTrue(heap.is_empty())
        one = MinHeap.build_heap([(9, "nine")])
        self.assertEqual(one.pop(), (9, "nine"))
        one.push(2, "two")
        self.assertEqual(one.pop(), (2, "two"))

    def test_MH_13(self):
        rng = random.Random(1301)
        heap = MinHeap()
        model = []
        for _ in range(200):
            if not model or rng.random() < 0.63:
                priority = rng.randint(-30, 30)
                item = f"item-{rng.randrange(1000)}"
                heap.push(priority, item)
                model.append((priority, item))
            else:
                expected_priority = min(p for p, _ in model)
                popped = heap.pop()
                self.assertEqual(popped[0], expected_priority)
                model.remove(popped)
            self.assertTrue(heap.is_valid_heap())
        broken = MinHeap()
        for p in [3, 5, 8, 1, 9]:
            broken.push(p, str(p))
        broken._data[0] = (99, "broken")
        self.assertFalse(broken.is_valid_heap())

    def test_MH_14(self):
        heap = MinHeap()
        for p in [5, 1, 3, 2]:
            heap.push(p, str(p))
        self.assertEqual([p for p, _ in heap.drain()], [1, 2, 3, 5])
        self.assertTrue(heap.is_empty())
        self.assertEqual(MinHeap().drain(), [])

    def test_MH_15(self):
        rng = random.Random(1501)
        values = [rng.randint(-1_000_000, 1_000_000) for _ in range(1_000)]
        heap = MinHeap()
        for value in values:
            heap.push(value, value)
        self.assertEqual([p for p, _ in heap.drain()], sorted(values))

    def test_MH_16(self):
        heap = MinHeap()
        heap.push(5, "five")
        heap.push(1, "one")
        self.assertEqual(heap.pop(), (1, "one"))
        heap.push(0, "zero")
        heap.push(7, "seven")
        self.assertEqual(heap.pop(), (0, "zero"))
        self.assertEqual(heap.pop(), (5, "five"))
        self.assertEqual(heap.pop(), (7, "seven"))
        self.assertTrue(heap.is_empty())

    def test_MH_17(self):
        rng = random.Random(1701)
        heap = MinHeap()
        start = time.perf_counter()
        for i in range(50_000):
            heap.push(rng.randint(-1_000_000, 1_000_000), i)
        for _ in range(50_000):
            heap.pop()
        elapsed = time.perf_counter() - start
        self.assertLess(elapsed, 2.0)

    def test_MH_18(self):
        rng = random.Random(1801)
        heap = MinHeap()
        model = []
        next_item = 0
        for _ in range(2_000):
            if not model or rng.random() < 0.65:
                priority = rng.randint(-100, 100)
                heap.push(priority, next_item)
                model.append((priority, next_item))
                next_item += 1
            else:
                expected = min(priority for priority, _ in model)
                popped = heap.pop()
                self.assertEqual(popped[0], expected)
                model.remove(popped)
            self.assertTrue(heap.is_valid_heap())

    def test_MH_19(self):
        heap = MinHeap()
        for p in [4, 2, 8, 1]:
            heap.push(p, str(p))
        before = heap.to_list()
        self.assertEqual(heap.peek(), (1, "1"))
        self.assertEqual(heap.to_list(), before)
        copy = heap.to_list()
        copy.clear()
        self.assertEqual(heap.to_list(), before)

    def test_MH_EXTRA_01_build_heap_does_not_reuse_the_input_list(self):
        pairs = [(4, "a"), (1, "b"), (3, "c")]
        heap = MinHeap.build_heap(pairs)
        heap.push(0, "new")
        self.assertEqual(pairs, [(4, "a"), (1, "b"), (3, "c")])

    def test_MH_EXTRA_02_duplicate_priorities_do_not_lose_items(self):
        heap = MinHeap()
        for i in range(20):
            heap.push(i % 3, i)
        output = [item for _, item in heap.drain()]
        self.assertEqual(sorted(output), list(range(20)))


if __name__ == "__main__":
    unittest.main()
