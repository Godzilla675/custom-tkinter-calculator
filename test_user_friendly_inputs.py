#!/usr/bin/env python3
"""
Manual test script to verify graphing and equation solving functionality
This script tests the preprocessing function with various user-friendly inputs
"""

import re

# Copy of the preprocess_math_input function for testing
def preprocess_math_input(expression: str) -> str:
    """
    Preprocess mathematical expressions to make them more user-friendly.
    """
    import re
    
    # First, replace ^ with **
    expr = expression.replace('^', '**')
    
    # List of known mathematical functions  
    known_funcs = ['sin', 'cos', 'tan', 'asin', 'acos', 'atan', 
                   'sinh', 'cosh', 'tanh', 'log', 'ln', 'exp', 
                   'sqrt', 'abs']
    
    # Step 1: Handle functions without parentheses (sin x -> sin(x))
    for func in known_funcs:
        pattern = rf'\b{func}\s+(?!\()([a-zA-Z_]\w*|\d+\.?\d*)'
        expr = re.sub(pattern, rf'{func}(\1)', expr)
    
    # Step 2: Add multiplication for number followed by letter/function
    # 2x -> 2*x, 2sin -> 2*sin
    expr = re.sub(r'(\d)([a-zA-Z_])', r'\1*\2', expr)
    
    # Step 3: Add multiplication for number followed by opening paren
    # 2(x) -> 2*(x)
    expr = re.sub(r'(\d)\(', r'\1*(', expr)
    
    # Step 4: Add multiplication for closing paren followed by opening paren
    # (x)(y) -> (x)*(y)
    expr = re.sub(r'\)\s*\(', r')*(', expr)
    
    # Step 5: Add multiplication for closing paren followed by letter/digit
    # )x -> )*x, )2 -> )*2
    expr = re.sub(r'\)([a-zA-Z_0-9])', r')*\1', expr)
    
    # Step 6: Add multiplication for letter followed by opening paren (not a function)
    # We do this by scanning and checking if identifier is not a function
    parts = []
    i = 0
    while i < len(expr):
        if expr[i] == '(' and i > 0:
            # Look back to find the identifier
            j = i - 1
            while j >= 0 and (expr[j].isalnum() or expr[j] == '_'):
                j -= 1
            identifier = expr[j+1:i]
            if identifier and identifier not in known_funcs and identifier.isalpha():
                # Insert * before (
                parts.append('*')
        parts.append(expr[i])
        i += 1
    expr = ''.join(parts)
    
    # Step 7: Add multiplication between consecutive single letters (xy -> x*y)
    result = []
    i = 0
    while i < len(expr):
        result.append(expr[i])
        if i < len(expr) - 1:
            curr = expr[i]
            next_char = expr[i + 1]
            
            # Check if we have two consecutive single letters
            if curr.isalpha() and next_char.isalpha():
                # Make sure current is not part of a longer identifier
                prev_is_alnum = i > 0 and expr[i-1].isalnum()
                next_next_is_alnum = i + 2 < len(expr) and expr[i+2].isalnum()
                
                # Only insert * if both are standalone single letters
                if not prev_is_alnum and not next_next_is_alnum:
                    result.append('*')
        i += 1
    
    return ''.join(result)


def test_graphing_inputs():
    """Test graphing function inputs"""
    print("=" * 80)
    print("TESTING GRAPHING FUNCTION INPUTS")
    print("=" * 80)
    
    graphing_tests = [
        # User-friendly input -> What it becomes
        ("x^2", "x**2", "Simple quadratic"),
        ("2x + 1", "2*x + 1", "Linear with coefficient"),
        ("x^3 - 2x^2 + x - 1", "x**3 - 2*x**2 + x - 1", "Cubic polynomial"),
        ("sin(x)", "sin(x)", "Sine function (unchanged)"),
        ("sin x", "sin(x)", "Sine without parentheses"),
        ("2sin(x)", "2*sin(x)", "Scaled sine"),
        ("cos(x) + sin(x)", "cos(x) + sin(x)", "Multiple trig functions"),
        ("x^2 * sin(x)", "x**2 * sin(x)", "Product of polynomial and trig"),
        ("(x-1)(x+1)", "(x-1)*(x+1)", "Factored form"),
        ("exp(x)", "exp(x)", "Exponential"),
        ("log(x)", "log(x)", "Logarithm"),
        ("sqrt(x)", "sqrt(x)", "Square root"),
        ("1/x", "1/x", "Reciprocal"),
        ("x^(-1)", "x**(-1)", "Negative exponent"),
    ]
    
    print("\nTest cases:")
    print("-" * 80)
    passed = 0
    failed = 0
    
    for user_input, expected, description in graphing_tests:
        result = preprocess_math_input(user_input)
        status = "✓ PASS" if result == expected else "✗ FAIL"
        
        if result == expected:
            passed += 1
        else:
            failed += 1
        
        print(f"{status}: {description}")
        print(f"  User input:  '{user_input}'")
        print(f"  Expected:    '{expected}'")
        print(f"  Got:         '{result}'")
        print()
    
    print("-" * 80)
    print(f"Results: {passed} passed, {failed} failed out of {len(graphing_tests)} tests\n")
    return failed == 0


def test_equation_inputs():
    """Test equation solver inputs"""
    print("=" * 80)
    print("TESTING EQUATION SOLVER INPUTS")
    print("=" * 80)
    
    equation_tests = [
        # User-friendly input -> What it becomes
        ("x^2 - 4x + 4 = 0", "x**2 - 4*x + 4 = 0", "Quadratic equation"),
        ("2x + 5 = 11", "2*x + 5 = 11", "Simple linear equation"),
        ("x^2 = 9", "x**2 = 9", "Simple quadratic"),
        ("(x-2)(x+3) = 0", "(x-2)*(x+3) = 0", "Factored quadratic"),
        ("2x + 3y = 10", "2*x + 3*y = 10", "Linear equation with two variables"),
        ("x^2 + y^2 = 25", "x**2 + y**2 = 25", "Circle equation"),
        ("sin(x) = 0.5", "sin(x) = 0.5", "Trigonometric equation"),
        ("xy = 12", "x*y = 12", "Product of variables"),
        ("x^3 - 8 = 0", "x**3 - 8 = 0", "Cubic equation"),
        ("exp(x) = 10", "exp(x) = 10", "Exponential equation"),
    ]
    
    print("\nTest cases:")
    print("-" * 80)
    passed = 0
    failed = 0
    
    for user_input, expected, description in equation_tests:
        result = preprocess_math_input(user_input)
        status = "✓ PASS" if result == expected else "✗ FAIL"
        
        if result == expected:
            passed += 1
        else:
            failed += 1
        
        print(f"{status}: {description}")
        print(f"  User input:  '{user_input}'")
        print(f"  Expected:    '{expected}'")
        print(f"  Got:         '{result}'")
        print()
    
    print("-" * 80)
    print(f"Results: {passed} passed, {failed} failed out of {len(equation_tests)} tests\n")
    return failed == 0


def test_expression_operations():
    """Test expression operations (expand, factor, differentiate, integrate)"""
    print("=" * 80)
    print("TESTING EXPRESSION OPERATIONS")
    print("=" * 80)
    
    expression_tests = [
        # User-friendly input -> What it becomes
        ("(x+1)(x-1)", "(x+1)*(x-1)", "Expand/Factor test"),
        ("x^2 + 2x + 1", "x**2 + 2*x + 1", "Expand test"),
        ("2x^3 + 3x^2", "2*x**3 + 3*x**2", "Differentiate test"),
        ("sin(x)", "sin(x)", "Differentiate trig"),
        ("x^2 + y^2", "x**2 + y**2", "Partial derivatives"),
        ("xy", "x*y", "Simple product"),
        ("2xy + 3x", "2*x*y + 3*x", "Multiple terms"),
    ]
    
    print("\nTest cases:")
    print("-" * 80)
    passed = 0
    failed = 0
    
    for user_input, expected, description in expression_tests:
        result = preprocess_math_input(user_input)
        status = "✓ PASS" if result == expected else "✗ FAIL"
        
        if result == expected:
            passed += 1
        else:
            failed += 1
        
        print(f"{status}: {description}")
        print(f"  User input:  '{user_input}'")
        print(f"  Expected:    '{expected}'")
        print(f"  Got:         '{result}'")
        print()
    
    print("-" * 80)
    print(f"Results: {passed} passed, {failed} failed out of {len(expression_tests)} tests\n")
    return failed == 0


def main():
    """Run all tests"""
    print("\n" + "=" * 80)
    print(" MANUAL TEST SUITE FOR USER-FRIENDLY INPUT PREPROCESSING")
    print("=" * 80 + "\n")
    
    all_passed = True
    
    all_passed = test_graphing_inputs() and all_passed
    all_passed = test_equation_inputs() and all_passed
    all_passed = test_expression_operations() and all_passed
    
    print("=" * 80)
    if all_passed:
        print("✓ ALL TESTS PASSED!")
    else:
        print("✗ SOME TESTS FAILED - Please review")
    print("=" * 80)
    
    print("\nUsage Examples:")
    print("-" * 80)
    print("\nGraphing:")
    print("  • x^2              (instead of x**2)")
    print("  • 2x + 1           (instead of 2*x + 1)")
    print("  • sin(x)           (standard notation)")
    print("  • 2sin(x)          (instead of 2*sin(x))")
    print("  • (x-1)(x+1)       (instead of (x-1)*(x+1))")
    
    print("\nEquation Solving:")
    print("  • x^2 - 4x + 4 = 0 (instead of x**2 - 4*x + 4 = 0)")
    print("  • 2x + 3y = 10     (instead of 2*x + 3*y = 10)")
    print("  • xy = 12          (instead of x*y = 12)")
    
    print("\nExpression Operations:")
    print("  • (x+1)(x-1)       (for expansion)")
    print("  • x^2 + 2x + 1     (for factoring)")
    print("  • 2x^3             (for differentiation)")
    print("-" * 80)


if __name__ == "__main__":
    main()
