import unittest
from automixy import binding, reactive, profile
from unittest.mock import Mock




class TestAutomixy(unittest.TestCase):
    def test_binding(self):
        b = binding(5)
        self.assertEqual(b.value, 5)
        b.set(10)
        self.assertEqual(b.value, 10)

    def test_reactive_lazy(self):
        b = binding(5)
        @profile
        def PLUS_ONE(x):
            print(f"PLUS_ONE called with {x}")
            return x + 1
        
        r = reactive(PLUS_ONE, b)
        
        self.assertEqual(PLUS_ONE.call_count, 0)  # Function not called on creation
        self.assertEqual(r(), 6)
        self.assertEqual(PLUS_ONE.call_count, 1)  # Function called on first access
        
        self.assertEqual(r(), 6)
        self.assertEqual(PLUS_ONE.call_count, 1)  # Function not called again for same value
        
        b.set(10)
        self.assertEqual(PLUS_ONE.call_count, 1)  # Function not called on dependency update
        self.assertEqual(r(), 11)
        self.assertEqual(PLUS_ONE.call_count, 2)  # Function called on access after update

    def test_reactive_eager(self):
        b = binding(5)

        @profile
        def PLUS_ONE(x):
            print(f"PLUS_ONE called with {x}")
            return x + 1
        
        r = reactive(PLUS_ONE, b, is_lazy=False)
        
        self.assertEqual(PLUS_ONE.call_count, 1)  # Function called on creation
        self.assertEqual(r.value, 6)
        self.assertEqual(PLUS_ONE.call_count, 1)  # Function not called on access
        
        b.set(10)
        self.assertEqual(PLUS_ONE.call_count, 2)  # Function called immediately on dependency update
        self.assertEqual(r.value, 11)
        self.assertEqual(PLUS_ONE.call_count, 2)  # Function not called on access

    def test_reactive_lazy_multiple_dependencies(self):
        b1 = binding(5)
        b2 = binding(10)
        
        @profile
        def SUM_TWO(x, y):
            print(f"SUM_TWO called with {x}, {y}")
            return x + y

        r = reactive(SUM_TWO, b1, b2)
        
        self.assertEqual(SUM_TWO.call_count, 0)  # Function not called on creation
        self.assertEqual(r(), 15)
        self.assertEqual(SUM_TWO.call_count, 1)  # Function called on first access
        
        b1.set(7)
        self.assertEqual(SUM_TWO.call_count, 1)  # Function not called on first dependency update
        b2.set(13)
        self.assertEqual(SUM_TWO.call_count, 1)  # Function not called on second dependency update
        self.assertEqual(r(), 20)
        self.assertEqual(SUM_TWO.call_count, 2)  # Function called on access after updates

    def test_reactive_chain(self):
        b = binding(5)

        @profile
        def DOUBLE(x):
            print("DOUBLE called")
            return x * 2
        
        @profile
        def PLUS_ONE(x):
            print("PLUS_ONE called")
            return x + 1
        
        r1 = reactive(DOUBLE, b)
        r2 = reactive(PLUS_ONE, r1)
        
        self.assertEqual(DOUBLE.call_count, 0)
        self.assertEqual(PLUS_ONE.call_count, 0)
        self.assertEqual(r2(), 11)
        self.assertEqual(DOUBLE.call_count, 1)
        self.assertEqual(PLUS_ONE.call_count, 1)
        
        b.set(10)
        self.assertEqual(DOUBLE.call_count, 1)
        self.assertEqual(PLUS_ONE.call_count, 1)
        self.assertEqual(r2(), 21)
        self.assertEqual(DOUBLE.call_count, 2)
        self.assertEqual(PLUS_ONE.call_count, 2)

    def test_reactive_with_constant(self):
        b = binding(5)
        r = reactive(lambda x, y: x + y, b, 3)
        self.assertEqual(r(), 8)
        b.set(10)
        self.assertEqual(r(), 13)

    def test_reactive_eager_chain_with_constant(self):
        # reactive evaluation based on another reactive
        # here a is a reactive function of b, 
        # and P is a reactive function of a and B, 
        # therefore P is a reactive function of b and B
        # when we set b, a is called, and therefore P is called, and the value of P is cached
        
        @profile
        def PLUS_ONE(x):
            print("PLUS_ONE called")
            return x + 1

        @profile
        def SUM_TRIPLE(x, y, z):
            print("SUM_TRIPLE called")
            return x + y + z

        b = binding(5)
        B = binding(2)

        a = reactive(PLUS_ONE, b, is_lazy=False)
        P = reactive(SUM_TRIPLE, a, B, 2, is_lazy=False)

        self.assertEqual(PLUS_ONE.call_count, 1)
        self.assertEqual(SUM_TRIPLE.call_count, 1)

        b.set(10)
        self.assertEqual(PLUS_ONE.call_count, 2)
        self.assertEqual(SUM_TRIPLE.call_count, 2)
        self.assertEqual(P(), 15)

if __name__ == '__main__':
    unittest.main()