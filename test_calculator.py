#!/usr/bin/env python3
"""
Test suite for the Advanced Custom Tkinter Calculator
Tests all major functionality including:
- Basic arithmetic
- Scientific functions
- Memory operations
- Error handling
"""

import unittest
import math
from calculator import Calculator


class TestCalculator(unittest.TestCase):
    """Test cases for the calculator."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.calc = Calculator()
        # Don't actually show the window
        self.calc.withdraw()
    
    def tearDown(self):
        """Clean up after tests."""
        try:
            self.calc.destroy()
        except Exception:
            pass
    
    def test_basic_addition(self):
        """Test basic addition."""
        self.calc.current_input = "5+3"
        self.calc.calculate()
        self.assertEqual(self.calc.current_input, "8")
    
    def test_basic_subtraction(self):
        """Test basic subtraction."""
        self.calc.current_input = "10-4"
        self.calc.calculate()
        self.assertEqual(self.calc.current_input, "6")
    
    def test_basic_multiplication(self):
        """Test basic multiplication."""
        self.calc.current_input = "6*7"
        self.calc.calculate()
        self.assertEqual(self.calc.current_input, "42")
    
    def test_basic_division(self):
        """Test basic division."""
        self.calc.current_input = "20/5"
        self.calc.calculate()
        self.assertEqual(self.calc.current_input, "4")
    
    def test_complex_expression(self):
        """Test complex arithmetic expression."""
        self.calc.current_input = "(5+3)*2-4"
        self.calc.calculate()
        self.assertEqual(self.calc.current_input, "12")
    
    def test_division_by_zero(self):
        """Test division by zero error handling."""
        self.calc.current_input = "5/0"
        self.calc.calculate()
        # Should display error and reset
        self.assertEqual(self.calc.current_input, "")
    
    def test_square_root(self):
        """Test square root function."""
        self.calc.current_input = "16"
        self.calc.square_root()
        self.assertEqual(float(self.calc.current_input), 4.0)
    
    def test_square_root_negative(self):
        """Test square root of negative number."""
        self.calc.current_input = "-4"
        self.calc.square_root()
        # Should show error and reset
        self.assertEqual(self.calc.current_input, "")
    
    def test_square(self):
        """Test square function."""
        self.calc.current_input = "5"
        self.calc.square()
        self.assertEqual(float(self.calc.current_input), 25.0)
    
    def test_reciprocal(self):
        """Test reciprocal function."""
        self.calc.current_input = "4"
        self.calc.reciprocal()
        self.assertEqual(float(self.calc.current_input), 0.25)
    
    def test_reciprocal_zero(self):
        """Test reciprocal of zero."""
        self.calc.current_input = "0"
        self.calc.reciprocal()
        # Should show error and reset
        self.assertEqual(self.calc.current_input, "")
    
    def test_percentage(self):
        """Test percentage function."""
        self.calc.current_input = "50"
        self.calc.percentage()
        self.assertEqual(float(self.calc.current_input), 0.5)
    
    def test_toggle_sign(self):
        """Test sign toggle."""
        self.calc.current_input = "42"
        self.calc.toggle_sign()
        self.assertEqual(self.calc.current_input, "-42")
        
        self.calc.toggle_sign()
        self.assertEqual(self.calc.current_input, "42")
    
    def test_factorial(self):
        """Test factorial function."""
        self.calc.current_input = "5"
        self.calc.factorial()
        self.assertEqual(float(self.calc.current_input), 120.0)
    
    def test_factorial_negative(self):
        """Test factorial of negative number."""
        self.calc.current_input = "-5"
        self.calc.factorial()
        # Should show error and reset
        self.assertEqual(self.calc.current_input, "")
    
    def test_absolute_value(self):
        """Test absolute value function."""
        self.calc.current_input = "-15"
        self.calc.absolute()
        self.assertEqual(float(self.calc.current_input), 15.0)
    
    def test_sin_function(self):
        """Test sine function."""
        self.calc.current_input = "30"
        self.calc.trig_function('sin')
        result = float(self.calc.current_input)
        expected = math.sin(math.radians(30))
        self.assertAlmostEqual(result, expected, places=10)
    
    def test_cos_function(self):
        """Test cosine function."""
        self.calc.current_input = "60"
        self.calc.trig_function('cos')
        result = float(self.calc.current_input)
        expected = math.cos(math.radians(60))
        self.assertAlmostEqual(result, expected, places=10)
    
    def test_tan_function(self):
        """Test tangent function."""
        self.calc.current_input = "45"
        self.calc.trig_function('tan')
        result = float(self.calc.current_input)
        expected = math.tan(math.radians(45))
        self.assertAlmostEqual(result, expected, places=10)
    
    def test_log10_function(self):
        """Test log base 10 function."""
        self.calc.current_input = "100"
        self.calc.log_function('log10')
        self.assertEqual(float(self.calc.current_input), 2.0)
    
    def test_ln_function(self):
        """Test natural log function."""
        self.calc.current_input = str(math.e)
        self.calc.log_function('log')
        result = float(self.calc.current_input)
        self.assertAlmostEqual(result, 1.0, places=10)
    
    def test_log_negative(self):
        """Test log of negative number."""
        self.calc.current_input = "-10"
        self.calc.log_function('log10')
        # Should show error and reset
        self.assertEqual(self.calc.current_input, "")
    
    def test_memory_operations(self):
        """Test memory functions."""
        # Clear memory
        self.calc.memory_clear()
        self.assertEqual(self.calc.memory, 0)
        
        # Add to memory
        self.calc.current_input = "10"
        self.calc.memory_add()
        self.assertEqual(self.calc.memory, 10)
        
        # Add more
        self.calc.current_input = "5"
        self.calc.memory_add()
        self.assertEqual(self.calc.memory, 15)
        
        # Subtract from memory
        self.calc.current_input = "3"
        self.calc.memory_subtract()
        self.assertEqual(self.calc.memory, 12)
        
        # Recall memory
        self.calc.memory_recall()
        self.assertEqual(self.calc.current_input, "12")
        
        # Clear memory
        self.calc.memory_clear()
        self.assertEqual(self.calc.memory, 0)
    
    def test_clear_function(self):
        """Test clear function."""
        self.calc.current_input = "12345"
        self.calc.clear()
        self.assertEqual(self.calc.current_input, "")
        self.assertFalse(self.calc.result_displayed)
    
    def test_backspace(self):
        """Test backspace function."""
        self.calc.current_input = "12345"
        self.calc.backspace()
        self.assertEqual(self.calc.current_input, "1234")
        
        self.calc.backspace()
        self.assertEqual(self.calc.current_input, "123")
    
    def test_history(self):
        """Test history functionality."""
        self.calc.add_to_history("5+3=8")
        self.assertEqual(len(self.calc.history), 1)
        self.assertEqual(self.calc.history[0], "5+3=8")
        
        self.calc.add_to_history("10-2=8")
        self.assertEqual(len(self.calc.history), 2)
    
    def test_power_operation(self):
        """Test power operation."""
        self.calc.current_input = "2**3"
        self.calc.calculate()
        self.assertEqual(float(self.calc.current_input), 8.0)
    
    def test_decimal_operations(self):
        """Test operations with decimal numbers."""
        self.calc.current_input = "3.5+2.5"
        self.calc.calculate()
        self.assertEqual(float(self.calc.current_input), 6.0)
    
    def test_negative_numbers(self):
        """Test operations with negative numbers."""
        self.calc.current_input = "-5+3"
        self.calc.calculate()
        self.assertEqual(float(self.calc.current_input), -2.0)


class TestCalculatorUI(unittest.TestCase):
    """Test UI-related functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.calc = Calculator()
        self.calc.withdraw()
    
    def tearDown(self):
        """Clean up after tests."""
        try:
            self.calc.destroy()
        except Exception:
            pass
    
    def test_mode_toggle(self):
        """Test mode toggle between standard and scientific."""
        initial_mode = self.calc.scientific_mode
        self.calc.toggle_mode()
        self.assertNotEqual(self.calc.scientific_mode, initial_mode)
    
    def test_append_to_input(self):
        """Test appending to input."""
        self.calc.append_to_input("5")
        self.assertEqual(self.calc.current_input, "5")
        
        self.calc.append_to_input("+")
        self.assertEqual(self.calc.current_input, "5+")
        
        self.calc.append_to_input("3")
        self.assertEqual(self.calc.current_input, "5+3")
    
    def test_result_displayed_flag(self):
        """Test that result_displayed flag works correctly."""
        self.calc.current_input = "5+5"
        self.calc.calculate()
        self.assertTrue(self.calc.result_displayed)
        
        # After calculation, appending should clear and start fresh
        self.calc.append_to_input("2")
        self.assertEqual(self.calc.current_input, "2")
        self.assertFalse(self.calc.result_displayed)


def run_tests():
    """Run all tests."""
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all tests
    suite.addTests(loader.loadTestsFromTestCase(TestCalculator))
    suite.addTests(loader.loadTestsFromTestCase(TestCalculatorUI))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_tests()
    exit(0 if success else 1)
