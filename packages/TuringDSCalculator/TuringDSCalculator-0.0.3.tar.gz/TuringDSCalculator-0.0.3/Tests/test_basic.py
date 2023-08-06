# BASIC TEST FOR CALCULATOR
# ----------------------------------------------------------------------------------------------------------------


# START --------
import unittest
from TuringDSCalculator import Calculator
from math import nan, inf


# EXECUTION ----
class TestCalculator(unittest.TestCase):
    def setUp(self):
        self.calculator = Calculator()
    
    # Tests for functionalities of individual methods
    def test_add(self):
        self.calculator.add(2)
        self.assertEqual(self.calculator.getResult(), 2)
        self.calculator.add(3)
        self.assertEqual(self.calculator.getResult(), 5)

    def test_subtract(self):
        self.calculator.subtract(2)
        self.assertEqual(self.calculator.getResult(), -2)
        self.calculator.subtract(3)
        self.assertEqual(self.calculator.getResult(), -5)

    def test_multiply(self):
        self.calculator.add(2)
        self.calculator.multiply(3)
        self.assertEqual(self.calculator.getResult(), 6)

    def test_divide(self):
        self.calculator.add(6)
        self.calculator.divided(3)
        self.assertEqual(self.calculator.getResult(), 2)

    def test_root(self):
        self.calculator.add(8)
        self.calculator.root(3)
        self.assertAlmostEqual(self.calculator.getResult(), 2.0)

    def test_reset(self):
        self.calculator.add(2)
        self.calculator.reset()
        self.assertEqual(self.calculator.getResult(), 0)
        
    # Tests for types of arguments
    def test_add_arg_type(self):
        with self.assertRaises(TypeError):
            self.calculator.add('2')

    def test_subtract_arg_type(self):
        with self.assertRaises(TypeError):
            self.calculator.subtract('2')

    def test_multiply_arg_type(self):
        with self.assertRaises(TypeError):
            self.calculator.multiply('2')

    def test_divide_arg_type(self):
        with self.assertRaises(TypeError):
            self.calculator.divided('2')

    def test_root_arg_type(self):
        with self.assertRaises(TypeError):
            self.calculator.root('3')

    # Tests for number of arguments
    def test_add_n_args(self):
        with self.assertRaises(TypeError):
            self.calculator.add(2, 3)

    def test_subtract_n_args(self):
        with self.assertRaises(TypeError):
            self.calculator.subtract(2, 3)

    def test_multiply_n_args(self):
        with self.assertRaises(TypeError):
            self.calculator.multiply(2, 3)

    def test_divide_n_args(self):
        with self.assertRaises(TypeError):
            self.calculator.divided(2, 3)

    def test_root_n_args(self):
        with self.assertRaises(TypeError):
            self.calculator.root(2, 3)

    # Test for division by 0
    def test_divide_zero(self):
        with self.assertRaises(ZeroDivisionError):
            self.calculator.divided(0)


# END ----------
if __name__ == '__main__':
    unittest.main()
