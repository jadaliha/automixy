import unittest
from automixy import binding, reactive

class TestAutomixy(unittest.TestCase):
    def test_binding(self):
        b = binding(5)
        self.assertEqual(b.value, 5)
        b.set(10)
        self.assertEqual(b.value, 10)

    def test_reactive_lazy(self):
        b = binding(5)
        r = reactive(lambda x: x + 1, b)
        self.assertEqual(r(), 6)
        b.set(10)
        self.assertEqual(r(), 11)

    def test_reactive_eager(self):
        b = binding(5)
        r = reactive(lambda x: x + 1, b, is_lazy=False)
        self.assertEqual(r.value, 6)
        b.set(10)
        self.assertEqual(r.value, 11)

    def test_reactive_multiple_dependencies(self):
        b1 = binding(5)
        b2 = binding(10)
        r = reactive(lambda x, y: x + y, b1, b2)
        self.assertEqual(r(), 15)
        b1.set(7)
        b2.set(13)
        self.assertEqual(r(), 20)

    def test_reactive_chain(self):
        b = binding(5)
        r1 = reactive(lambda x: x * 2, b)
        r2 = reactive(lambda x: x + 1, r1)
        self.assertEqual(r2(), 11)
        b.set(10)
        self.assertEqual(r2(), 21)

    def test_reactive_with_constant(self):
        b = binding(5)
        r = reactive(lambda x, y: x + y, b, 3)
        self.assertEqual(r(), 8)
        b.set(10)
        self.assertEqual(r(), 13)

if __name__ == '__main__':
    unittest.main()