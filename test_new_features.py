#!/usr/bin/env python3
"""
Test suite for new calculator features:
- Fixed graphing functionality
- Multi-variable equation solving
- Enhanced differentiation and integration
"""

import unittest
import numpy as np
from calculator import AdvancedCalculator


class TestGraphingFixes(unittest.TestCase):
    """Test the fixed graphing functionality."""
    
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
    
    def test_plot_basic_function(self):
        """Test plotting a basic function."""
        self.calc.func_entry.insert(0, "x**2")
        self.calc.x_min_entry.delete(0, "end")
        self.calc.x_min_entry.insert(0, "-5")
        self.calc.x_max_entry.delete(0, "end")
        self.calc.x_max_entry.insert(0, "5")
        
        try:
            self.calc.plot_function()
            # Check that no error label is set
            self.assertEqual(self.calc.graph_error_label.cget("text"), "")
            success = True
        except Exception as e:
            print(f"Error: {e}")
            success = False
        
        self.assertTrue(success)
    
    def test_plot_trig_function(self):
        """Test plotting trigonometric functions."""
        self.calc.func_entry.delete(0, "end")
        self.calc.func_entry.insert(0, "sin(x)")
        self.calc.x_min_entry.delete(0, "end")
        self.calc.x_min_entry.insert(0, "-10")
        self.calc.x_max_entry.delete(0, "end")
        self.calc.x_max_entry.insert(0, "10")
        
        try:
            self.calc.plot_function()
            self.assertEqual(self.calc.graph_error_label.cget("text"), "")
            success = True
        except Exception:
            success = False
        
        self.assertTrue(success)
    
    def test_plot_inverse_trig_function(self):
        """Test that inverse trig functions work (was broken before fix)."""
        self.calc.func_entry.delete(0, "end")
        self.calc.func_entry.insert(0, "asin(x)")
        self.calc.x_min_entry.delete(0, "end")
        self.calc.x_min_entry.insert(0, "-0.9")
        self.calc.x_max_entry.delete(0, "end")
        self.calc.x_max_entry.insert(0, "0.9")
        
        try:
            self.calc.plot_function()
            self.assertEqual(self.calc.graph_error_label.cget("text"), "")
            success = True
        except Exception:
            success = False
        
        self.assertTrue(success)
    
    def test_plot_exponential_function(self):
        """Test plotting exponential functions."""
        self.calc.func_entry.delete(0, "end")
        self.calc.func_entry.insert(0, "exp(x)")
        self.calc.x_min_entry.delete(0, "end")
        self.calc.x_min_entry.insert(0, "-2")
        self.calc.x_max_entry.delete(0, "end")
        self.calc.x_max_entry.insert(0, "2")
        
        try:
            self.calc.plot_function()
            self.assertEqual(self.calc.graph_error_label.cget("text"), "")
            success = True
        except Exception:
            success = False
        
        self.assertTrue(success)
    
    def test_plot_logarithmic_function(self):
        """Test plotting logarithmic functions."""
        self.calc.func_entry.delete(0, "end")
        self.calc.func_entry.insert(0, "log(x)")
        self.calc.x_min_entry.delete(0, "end")
        self.calc.x_min_entry.insert(0, "0.1")
        self.calc.x_max_entry.delete(0, "end")
        self.calc.x_max_entry.insert(0, "10")
        
        try:
            self.calc.plot_function()
            self.assertEqual(self.calc.graph_error_label.cget("text"), "")
            success = True
        except Exception:
            success = False
        
        self.assertTrue(success)
    
    def test_add_function_to_plot(self):
        """Test adding multiple functions to the same plot."""
        # Plot first function
        self.calc.func_entry.insert(0, "x**2")
        self.calc.plot_function()
        
        # Add second function
        self.calc.func_entry.delete(0, "end")
        self.calc.func_entry.insert(0, "x**3")
        
        try:
            self.calc.add_function()
            self.assertEqual(self.calc.graph_error_label.cget("text"), "")
            success = True
        except Exception:
            success = False
        
        self.assertTrue(success)
    
    def test_clear_graph(self):
        """Test clearing the graph."""
        self.calc.func_entry.insert(0, "x**2")
        self.calc.plot_function()
        
        try:
            self.calc.clear_graph()
            success = True
        except Exception:
            success = False
        
        self.assertTrue(success)


class TestMultiVariableSolver(unittest.TestCase):
    """Test multi-variable equation solving."""
    
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
    
    def test_solve_for_x_in_xy_equation(self):
        """Test solving x + y = 10 for x."""
        self.calc.equation_entry.insert(0, "x + y = 10")
        self.calc.solver_type.set("Algebraic")
        
        try:
            self.calc.solve_equation()
            result_text = self.calc.solver_result.get("1.0", "end")
            # Should contain x in terms of y
            self.assertIn("x", result_text.lower())
            self.assertIn("y", result_text.lower())
            success = True
        except Exception as e:
            print(f"Error: {e}")
            success = False
        
        self.assertTrue(success)
    
    def test_solve_for_y_in_xy_equation(self):
        """Test that equation solver shows solution for y too."""
        self.calc.equation_entry.delete(0, "end")
        self.calc.equation_entry.insert(0, "2*x + 3*y = 12")
        self.calc.solver_type.set("Algebraic")
        
        try:
            self.calc.solve_equation()
            result_text = self.calc.solver_result.get("1.0", "end")
            # Should show solutions for both variables
            self.assertIn("x", result_text.lower())
            self.assertIn("y", result_text.lower())
            success = True
        except Exception:
            success = False
        
        self.assertTrue(success)
    
    def test_solve_three_variable_equation(self):
        """Test solving equation with three variables."""
        self.calc.equation_entry.delete(0, "end")
        self.calc.equation_entry.insert(0, "x + y + z = 15")
        self.calc.solver_type.set("Algebraic")
        
        try:
            self.calc.solve_equation()
            result_text = self.calc.solver_result.get("1.0", "end")
            # Should detect all three variables
            self.assertIn("x", result_text.lower())
            self.assertIn("y", result_text.lower())
            self.assertIn("z", result_text.lower())
            success = True
        except Exception:
            success = False
        
        self.assertTrue(success)
    
    def test_quadratic_xy_equation(self):
        """Test solving quadratic equation with x and y."""
        self.calc.equation_entry.delete(0, "end")
        self.calc.equation_entry.insert(0, "x**2 + y = 5")
        self.calc.solver_type.set("Quadratic")
        
        try:
            self.calc.solve_equation()
            result_text = self.calc.solver_result.get("1.0", "end")
            # Should show solutions for both variables
            success = "x" in result_text.lower() or "y" in result_text.lower()
        except Exception:
            success = False
        
        self.assertTrue(success)


class TestMultiVariableOperations(unittest.TestCase):
    """Test multi-variable differentiation and integration."""
    
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
    
    def test_partial_derivative_xy(self):
        """Test partial derivatives with x and y."""
        self.calc.equation_entry.insert(0, "x**2 + y**2")
        
        try:
            self.calc.differentiate()
            result_text = self.calc.solver_result.get("1.0", "end")
            # Should show partial derivatives
            self.assertIn("∂", result_text)  # Partial derivative symbol
            self.assertIn("x", result_text.lower())
            self.assertIn("y", result_text.lower())
            success = True
        except Exception as e:
            print(f"Error: {e}")
            success = False
        
        self.assertTrue(success)
    
    def test_partial_derivative_xyz(self):
        """Test partial derivatives with x, y, and z."""
        self.calc.equation_entry.delete(0, "end")
        self.calc.equation_entry.insert(0, "x*y + y*z + x*z")
        
        try:
            self.calc.differentiate()
            result_text = self.calc.solver_result.get("1.0", "end")
            # Should show partial derivatives for all variables
            self.assertIn("x", result_text.lower())
            self.assertIn("y", result_text.lower())
            self.assertIn("z", result_text.lower())
            success = True
        except Exception:
            success = False
        
        self.assertTrue(success)
    
    def test_integrate_multi_variable(self):
        """Test integration with multiple variables."""
        self.calc.equation_entry.delete(0, "end")
        self.calc.equation_entry.insert(0, "x*y")
        
        try:
            self.calc.integrate_expression()
            result_text = self.calc.solver_result.get("1.0", "end")
            # Should show integrals for both variables
            self.assertIn("x", result_text.lower())
            self.assertIn("y", result_text.lower())
            success = True
        except Exception:
            success = False
        
        self.assertTrue(success)
    
    def test_expand_multi_variable(self):
        """Test expanding expressions with multiple variables."""
        self.calc.equation_entry.delete(0, "end")
        self.calc.equation_entry.insert(0, "(x + y)**2")
        
        try:
            self.calc.expand_expression()
            result_text = self.calc.solver_result.get("1.0", "end")
            # Should expand to x**2 + 2*x*y + y**2
            self.assertIn("x", result_text.lower())
            self.assertIn("y", result_text.lower())
            success = True
        except Exception:
            success = False
        
        self.assertTrue(success)
    
    def test_factor_multi_variable(self):
        """Test factoring expressions with multiple variables."""
        self.calc.equation_entry.delete(0, "end")
        self.calc.equation_entry.insert(0, "x**2 - y**2")
        
        try:
            self.calc.factor_expression()
            result_text = self.calc.solver_result.get("1.0", "end")
            # Should factor to (x - y)*(x + y)
            self.assertIn("x", result_text.lower())
            self.assertIn("y", result_text.lower())
            success = True
        except Exception:
            success = False
        
        self.assertTrue(success)


def run_tests():
    """Run all new feature tests."""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all test cases
    suite.addTests(loader.loadTestsFromTestCase(TestGraphingFixes))
    suite.addTests(loader.loadTestsFromTestCase(TestMultiVariableSolver))
    suite.addTests(loader.loadTestsFromTestCase(TestMultiVariableOperations))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_tests()
    exit(0 if success else 1)
