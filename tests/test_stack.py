"""Unit tests for Stack and is_balanced()."""
import random
import time
import unittest

from linked_list import LinkedList
from linked_stack import Stack, is_balanced


class TestStack(unittest.TestCase):
    def test_ST_01(self):
        stack = Stack()
        self.assertEqual(len(stack), 0)
        self.assertTrue(stack.is_empty())
        self.assertEqual(stack.to_list(), [])
        with self.assertRaises(IndexError):
            stack.pop()
        with self.assertRaises(IndexError):
            stack.peek()

    def test_ST_02(self):
        stack = Stack()
        for x in [1, 2, 3]:
            stack.push(x)
        self.assertEqual(stack.peek(), 3)
        self.assertEqual(len(stack), 3)
        self.assertEqual(stack.to_list(), [3, 2, 1])

    def test_ST_03(self):
        stack = Stack()
        for x in [1, 2, 3]:
            stack.push(x)
        self.assertEqual([stack.pop(), stack.pop(), stack.pop()], [3, 2, 1])
        self.assertTrue(stack.is_empty())
        with self.assertRaises(IndexError):
            stack.pop()

    def test_ST_04(self):
        stack = Stack()
        for x in [1, 2, 3]:
            stack.push(x)
        for _ in range(3):
            self.assertEqual(stack.peek(), 3)
        self.assertEqual(len(stack), 3)

    def test_ST_05(self):
        stack = Stack()
        stack.push("a")
        stack.push("b")
        self.assertEqual(stack.pop(), "b")
        stack.push("c")
        self.assertEqual(stack.pop(), "c")
        self.assertEqual(stack.pop(), "a")
        self.assertTrue(stack.is_empty())

    def test_ST_06(self):
        stack = Stack()
        values = [None, 0, [], ("x",)]
        for value in values:
            stack.push(value)
        self.assertEqual([stack.pop() for _ in values], list(reversed(values)))

    def test_ST_07(self):
        stack = Stack()
        stack.push(1)
        stack.push(2)
        stack.clear()
        self.assertTrue(stack.is_empty())
        stack.push(3)
        other = Stack()
        other.push(9)
        self.assertEqual(stack.to_list(), [3])
        self.assertEqual(other.to_list(), [9])

    def test_ST_08(self):
        stack = Stack()
        self.assertIsInstance(stack._list, LinkedList)
        start = time.perf_counter()
        for i in range(20_000):
            stack.push(i)
        for i in range(19_999, -1, -1):
            self.assertEqual(stack.pop(), i)
        self.assertLess(time.perf_counter() - start, 1.0)

    def test_ST_09(self):
        for text in ["", "()", "([]{})", "a(b[c]d)e"]:
            with self.subTest(text=text):
                self.assertTrue(is_balanced(text))
        for text in ["(", ")(", "([)]", "((())", "}{"]:
            with self.subTest(text=text):
                self.assertFalse(is_balanced(text))
        with self.assertRaises(TypeError):
            is_balanced(5)

    def test_ST_10(self):
        rng = random.Random(1001)
        stack = Stack()
        model = []
        for _ in range(1_000):
            if not model or rng.random() < 0.6:
                value = rng.randint(-100, 100)
                stack.push(value)
                model.append(value)
            else:
                self.assertEqual(stack.pop(), model.pop())
            self.assertEqual(stack.to_list(), list(reversed(model)))
            self.assertEqual(len(stack), len(model))

    def test_ST_EXTRA_01_multiple_stacks_do_not_share_storage(self):
        a, b = Stack(), Stack()
        a.push("A")
        self.assertTrue(b.is_empty())

    def test_ST_EXTRA_02_non_bracket_characters_are_ignored(self):
        self.assertTrue(is_balanced("robot_01: [x + (y * z)] # ok"))


if __name__ == "__main__":
    unittest.main()
