#!/usr/bin/env python3
"""
Comprehensive test suite for the Enhanced Advanced Calculator
Tests all features including graphing, equation solving, matrix operations, and conversions.
"""

import unittest
import math
import numpy as np
from calculator import AdvancedCalculator, safe_eval


class TestSafeEval(unittest.TestCase):
    """Test the safe_eval function."""
    
    def test_basic_arithmetic(self):
        """Test basic arithmetic operations."""
        self.assertEqual(safe_eval("5+3"), 8)
        self.assertEqual(safe_eval("10-4"), 6)
        self.assertEqual(safe_eval("6*7"), 42)
        self.assertEqual(safe_eval("20/5"), 4)
    
    def test_complex_expressions(self):
        """Test complex expressions."""
        self.assertEqual(safe_eval("(5+3)*2-4"), 12)
        self.assertEqual(safe_eval("2**3"), 8)
        self.assertEqual(safe_eval("10%3"), 1)
    
    def test_security(self):
        """Test that malicious code is blocked."""
        with self.assertRaises(ValueError):
            safe_eval("__import__('os').system('echo hack')")


class TestCalculatorCore(unittest.TestCase):
    """Test core calculator functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.calc = AdvancedCalculator()
        self.calc.withdraw()
    
    def tearDown(self):
        """Clean up after tests."""
        try:
            self.calc.destroy()
        except Exception:
            pass
    
    def test_basic_operations(self):
        """Test basic arithmetic operations."""
        self.calc.current_input = "15+27"
        self.calc.calculate()
        self.assertEqual(self.calc.current_input, "42")
        
        self.calc.current_input = "100-50"
        self.calc.calculate()
        self.assertEqual(self.calc.current_input, "50")
    
    def test_scientific_functions(self):
        """Test scientific functions."""
        # Square root
        self.calc.current_input = "16"
        self.calc.square_root()
        self.assertEqual(float(self.calc.current_input), 4.0)
        
        # Square
        self.calc.current_input = "5"
        self.calc.square()
        self.assertEqual(float(self.calc.current_input), 25.0)
        
        # Cube root
        self.calc.current_input = "27"
        self.calc.cube_root()
        self.assertAlmostEqual(float(self.calc.current_input), 3.0, places=10)
        
        # Factorial
        self.calc.current_input = "5"
        self.calc.factorial()
        self.assertEqual(float(self.calc.current_input), 120.0)
    
    def test_trig_functions_deg(self):
        """Test trigonometric functions in degree mode."""
        self.calc.angle_mode = "deg"
        
        # sin(30°) = 0.5
        self.calc.current_input = "30"
        self.calc.trig_function('sin')
        self.assertAlmostEqual(float(self.calc.current_input), 0.5, places=10)
        
        # cos(60°) = 0.5
        self.calc.current_input = "60"
        self.calc.trig_function('cos')
        self.assertAlmostEqual(float(self.calc.current_input), 0.5, places=10)
    
    def test_trig_functions_rad(self):
        """Test trigonometric functions in radian mode."""
        self.calc.angle_mode = "rad"
        
        # sin(π/6) = 0.5
        self.calc.current_input = str(math.pi/6)
        self.calc.trig_function('sin')
        self.assertAlmostEqual(float(self.calc.current_input), 0.5, places=10)
    
    def test_inverse_trig_functions(self):
        """Test inverse trigonometric functions."""
        self.calc.angle_mode = "deg"
        
        # asin(0.5) = 30°
        self.calc.current_input = "0.5"
        self.calc.trig_function('asin')
        self.assertAlmostEqual(float(self.calc.current_input), 30.0, places=10)
    
    def test_log_functions(self):
        """Test logarithmic functions."""
        # log10(100) = 2
        self.calc.current_input = "100"
        self.calc.log_function('log10')
        self.assertEqual(float(self.calc.current_input), 2.0)
        
        # ln(e) = 1
        self.calc.current_input = str(math.e)
        self.calc.log_function('log')
        self.assertAlmostEqual(float(self.calc.current_input), 1.0, places=10)
    
    def test_exp_function(self):
        """Test exponential function."""
        self.calc.current_input = "0"
        self.calc.exp_function()
        self.assertEqual(float(self.calc.current_input), 1.0)
        
        self.calc.current_input = "1"
        self.calc.exp_function()
        self.assertAlmostEqual(float(self.calc.current_input), math.e, places=10)
    
    def test_memory_operations(self):
        """Test memory functions."""
        self.calc.memory_clear()
        self.assertEqual(self.calc.memory, 0)
        
        self.calc.current_input = "100"
        self.calc.memory_add()
        self.assertEqual(self.calc.memory, 100)
        
        self.calc.current_input = "50"
        self.calc.memory_subtract()
        self.assertEqual(self.calc.memory, 50)
        
        self.calc.memory_recall()
        self.assertEqual(self.calc.current_input, "50")
    
    def test_angle_mode_toggle(self):
        """Test angle mode toggle."""
        initial_mode = self.calc.angle_mode
        self.calc.toggle_angle_mode()
        self.assertNotEqual(self.calc.angle_mode, initial_mode)
    
    def test_error_handling(self):
        """Test error handling."""
        # Division by zero
        self.calc.current_input = "5/0"
        self.calc.calculate()
        self.assertEqual(self.calc.current_input, "")
        
        # Square root of negative
        self.calc.current_input = "-4"
        self.calc.square_root()
        self.assertEqual(self.calc.current_input, "")


class TestMatrixOperations(unittest.TestCase):
    """Test matrix operations."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.calc = AdvancedCalculator()
        self.calc.withdraw()
    
    def tearDown(self):
        """Clean up after tests."""
        try:
            self.calc.destroy()
        except Exception:
            pass
    
    def test_parse_matrix(self):
        """Test matrix parsing."""
        matrix_str = "1,2,3;4,5,6;7,8,9"
        matrix = self.calc.parse_matrix(matrix_str)
        expected = np.array([[1,2,3],[4,5,6],[7,8,9]])
        np.testing.assert_array_equal(matrix, expected)
    
    def test_matrix_addition(self):
        """Test matrix addition."""
        self.calc.matrix_a_entry.delete("1.0", "end")
        self.calc.matrix_a_entry.insert("1.0", "1,2;3,4")
        self.calc.matrix_b_entry.delete("1.0", "end")
        self.calc.matrix_b_entry.insert("1.0", "5,6;7,8")
        self.calc.matrix_operation("add")
        # Result should be in matrix_result textbox
        result_text = self.calc.matrix_result.get("1.0", "end")
        self.assertIn("A + B", result_text)
    
    def test_matrix_multiplication(self):
        """Test matrix multiplication."""
        self.calc.matrix_a_entry.delete("1.0", "end")
        self.calc.matrix_a_entry.insert("1.0", "1,2;3,4")
        self.calc.matrix_b_entry.delete("1.0", "end")
        self.calc.matrix_b_entry.insert("1.0", "2,0;1,3")
        self.calc.matrix_operation("multiply")
        result_text = self.calc.matrix_result.get("1.0", "end")
        self.assertIn("A × B", result_text)
    
    def test_matrix_transpose(self):
        """Test matrix transpose."""
        self.calc.matrix_a_entry.delete("1.0", "end")
        self.calc.matrix_a_entry.insert("1.0", "1,2,3;4,5,6")
        self.calc.matrix_operation("transpose_a")
        result_text = self.calc.matrix_result.get("1.0", "end")
        self.assertIn("Transpose", result_text)
    
    def test_matrix_determinant(self):
        """Test matrix determinant."""
        self.calc.matrix_a_entry.delete("1.0", "end")
        self.calc.matrix_a_entry.insert("1.0", "1,2;3,4")
        self.calc.matrix_operation("det_a")
        result_text = self.calc.matrix_result.get("1.0", "end")
        self.assertIn("Determinant", result_text)


class TestConversions(unittest.TestCase):
    """Test unit conversion functions."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.calc = AdvancedCalculator()
        self.calc.withdraw()
    
    def tearDown(self):
        """Clean up after tests."""
        try:
            self.calc.destroy()
        except Exception:
            pass
    
    def test_length_conversion(self):
        """Test length conversions."""
        # 1 meter = 100 centimeters
        self.calc.from_value.insert(0, "1")
        self.calc.from_unit.set("meter")
        self.calc.to_unit.set("centimeter")
        self.calc.perform_conversion()
        result = float(self.calc.to_value.get())
        self.assertAlmostEqual(result, 100.0, places=5)
    
    def test_temperature_conversion(self):
        """Test temperature conversions."""
        # 0°C = 32°F
        result = self.calc.convert_temperature(0, "celsius", "fahrenheit")
        self.assertEqual(result, 32.0)
        
        # 100°C = 212°F
        result = self.calc.convert_temperature(100, "celsius", "fahrenheit")
        self.assertEqual(result, 212.0)
        
        # 0°C = 273.15K
        result = self.calc.convert_temperature(0, "celsius", "kelvin")
        self.assertEqual(result, 273.15)


class TestGraphing(unittest.TestCase):
    """Test graphing functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.calc = AdvancedCalculator()
        self.calc.withdraw()
    
    def tearDown(self):
        """Clean up after tests."""
        try:
            self.calc.destroy()
        except Exception:
            pass
    
    def test_plot_function(self):
        """Test function plotting."""
        self.calc.func_entry.insert(0, "x**2")
        self.calc.x_min_entry.delete(0, "end")
        self.calc.x_min_entry.insert(0, "-5")
        self.calc.x_max_entry.delete(0, "end")
        self.calc.x_max_entry.insert(0, "5")
        
        # Should not raise an error
        try:
            self.calc.plot_function()
            success = True
        except Exception:
            success = False
        
        self.assertTrue(success)
    
    def test_clear_graph(self):
        """Test clearing the graph."""
        try:
            self.calc.clear_graph()
            success = True
        except Exception:
            success = False
        
        self.assertTrue(success)


class TestEquationSolver(unittest.TestCase):
    """Test equation solver functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.calc = AdvancedCalculator()
        self.calc.withdraw()
    
    def tearDown(self):
        """Clean up after tests."""
        try:
            self.calc.destroy()
        except Exception:
            pass
    
    def test_solve_linear_equation(self):
        """Test solving linear equations."""
        self.calc.equation_entry.insert(0, "2*x + 5 = 11")
        self.calc.solver_type.set("Algebraic")
        
        try:
            self.calc.solve_equation()
            result_text = self.calc.solver_result.get("1.0", "end")
            # Should contain the solution x = 3
            self.assertIn("3", result_text)
        except Exception as e:
            self.fail(f"Equation solver failed: {e}")
    
    def test_solve_quadratic_equation(self):
        """Test solving quadratic equations."""
        self.calc.equation_entry.delete(0, "end")
        self.calc.equation_entry.insert(0, "x**2 - 5*x + 6 = 0")
        self.calc.solver_type.set("Quadratic")
        
        try:
            self.calc.solve_equation()
            result_text = self.calc.solver_result.get("1.0", "end")
            # Should contain solutions x = 2 and x = 3
            success = "2" in result_text and "3" in result_text
            self.assertTrue(success)
        except Exception as e:
            self.fail(f"Quadratic solver failed: {e}")
    
    def test_expand_expression(self):
        """Test expression expansion."""
        self.calc.equation_entry.delete(0, "end")
        self.calc.equation_entry.insert(0, "(x+2)*(x+3)")
        
        try:
            self.calc.expand_expression()
            result_text = self.calc.solver_result.get("1.0", "end")
            self.assertIn("Expanded", result_text)
        except Exception as e:
            self.fail(f"Expand failed: {e}")
    
    def test_differentiate(self):
        """Test differentiation."""
        self.calc.equation_entry.delete(0, "end")
        self.calc.equation_entry.insert(0, "x**2")
        
        try:
            self.calc.differentiate()
            result_text = self.calc.solver_result.get("1.0", "end")
            # Derivative of x^2 is 2*x
            self.assertIn("2*x", result_text)
        except Exception as e:
            self.fail(f"Differentiate failed: {e}")


class TestUIComponents(unittest.TestCase):
    """Test UI components and interactions."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.calc = AdvancedCalculator()
        self.calc.withdraw()
    
    def tearDown(self):
        """Clean up after tests."""
        try:
            self.calc.destroy()
        except Exception:
            pass
    
    def test_tab_switching(self):
        """Test switching between tabs."""
        tabs = ["Calculator", "Graphing", "Equation Solver", "Matrix", "Conversions"]
        
        for tab in tabs:
            self.calc.tabview.set(tab)
            self.assertEqual(self.calc.tabview.get(), tab)
    
    def test_theme_toggle(self):
        """Test theme toggling."""
        try:
            self.calc.toggle_theme()
            success = True
        except Exception:
            success = False
        
        self.assertTrue(success)
    
    def test_history_management(self):
        """Test history functionality."""
        self.calc.add_to_history("5+3=8")
        self.assertEqual(len(self.calc.history), 1)
        
        self.calc.add_to_history("10*2=20")
        self.assertEqual(len(self.calc.history), 2)
    
    def test_display_update(self):
        """Test display updates."""
        self.calc.update_display("42")
        self.assertEqual(self.calc.display.get(), "42")
        
        self.calc.update_display("3.14159")
        self.assertEqual(self.calc.display.get(), "3.14159")


def run_tests():
    """Run all tests."""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all test cases
    suite.addTests(loader.loadTestsFromTestCase(TestSafeEval))
    suite.addTests(loader.loadTestsFromTestCase(TestCalculatorCore))
    suite.addTests(loader.loadTestsFromTestCase(TestMatrixOperations))
    suite.addTests(loader.loadTestsFromTestCase(TestConversions))
    suite.addTests(loader.loadTestsFromTestCase(TestGraphing))
    suite.addTests(loader.loadTestsFromTestCase(TestEquationSolver))
    suite.addTests(loader.loadTestsFromTestCase(TestUIComponents))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_tests()
    exit(0 if success else 1)
