import unittest

from calculator.calculator import add


class TestAddFunction(unittest.TestCase):
    
    def test_add_positive_numbers(self):
        self.assertEqual(add(3, 5), 8)
        
    def test_add_negative_numbers(self):
        self.assertEqual(add(-3, -5), -8)
        
    def test_add_positive_and_negative(self):
        self.assertEqual(add(3, -5), -2)
        
    def test_add_with_zero(self):
        self.assertEqual(add(0, 5), 5)
        self.assertEqual(add(3, 0), 3)
        
    def test_add_floats(self):
        self.assertAlmostEqual(add(3.5, 2.3), 5.8)