#!/usr/bin/env python3
"""
Test script for the preprocess_math_input function
"""

from calculator import preprocess_math_input
import sympy as sp

def test_preprocessing():
    """Test various preprocessing scenarios."""
    
    test_cases = [
        # (input, expected_output, description)
        ("2x", "2*x", "Implicit multiplication: number and variable"),
        ("3y + 2x", "3*y + 2*x", "Multiple implicit multiplications"),
        ("x^2", "x**2", "Exponentiation with ^"),
        ("2^3", "2**3", "Number exponentiation"),
        ("2(x+1)", "2*(x+1)", "Number times parenthesis"),
        ("(x)(y)", "(x)*(y)", "Parenthesis times parenthesis"),
        ("(x+1)(y+2)", "(x+1)*(y+2)", "Complex parenthesis multiplication"),
        ("sin(x)", "sin(x)", "Function call should not change"),
        ("2sin(x)", "2*sin(x)", "Number times function"),
        ("cos(x)", "cos(x)", "Cosine function"),
        ("x(y+1)", "x*(y+1)", "Variable times parenthesis"),
        ("xy", "x*y", "Two variables"),
        ("2xy", "2*x*y", "Number and two variables"),
        ("sin x", "sin(x)", "Function without parentheses"),
        ("cos x", "cos(x)", "Cosine without parentheses"),
        ("log 10", "log(10)", "Log without parentheses"),
        ("exp 2", "exp(2)", "Exp without parentheses"),
        ("x^2 + 2x + 1", "x**2 + 2*x + 1", "Complete quadratic"),
        ("2x^2 + 3x + 4", "2*x**2 + 3*x + 4", "Quadratic with coefficients"),
    ]
    
    print("Testing preprocess_math_input function:\n")
    print("-" * 80)
    
    passed = 0
    failed = 0
    
    for input_str, expected, description in test_cases:
        result = preprocess_math_input(input_str)
        status = "✓ PASS" if result == expected else "✗ FAIL"
        
        if result == expected:
            passed += 1
        else:
            failed += 1
        
        print(f"{status}: {description}")
        print(f"  Input:    '{input_str}'")
        print(f"  Expected: '{expected}'")
        print(f"  Got:      '{result}'")
        
        # Also test if it can be parsed by sympy
        try:
            expr = sp.sympify(result)
            print(f"  SymPy:    ✓ Parseable -> {expr}")
        except Exception as e:
            print(f"  SymPy:    ✗ Error: {str(e)}")
        
        print()
    
    print("-" * 80)
    print(f"\nResults: {passed} passed, {failed} failed out of {len(test_cases)} tests")
    
    return failed == 0


def test_graphing_examples():
    """Test examples that would be used in graphing."""
    print("\n" + "=" * 80)
    print("Testing Graphing Examples:")
    print("=" * 80 + "\n")
    
    examples = [
        "sin(x)",
        "x^2",
        "2x + 1",
        "x^3 - 2x^2 + x - 1",
        "(x-1)(x+1)",
        "exp(x)",
        "log(x)",
        "1/x",
        "sqrt(x)",
    ]
    
    for example in examples:
        processed = preprocess_math_input(example)
        print(f"Input:      {example}")
        print(f"Processed:  {processed}")
        
        try:
            x = sp.Symbol('x')
            expr = sp.sympify(processed)
            func = sp.lambdify(x, expr, modules=['numpy'])
            print(f"SymPy expr: {expr}")
            print(f"Status:     ✓ Valid\n")
        except Exception as e:
            print(f"Error:      ✗ {str(e)}\n")


def test_equation_examples():
    """Test examples that would be used in equation solving."""
    print("\n" + "=" * 80)
    print("Testing Equation Solver Examples:")
    print("=" * 80 + "\n")
    
    examples = [
        "x^2 - 4x + 4 = 0",
        "2x + 5 = 11",
        "x^2 - 9 = 0",
        "(x-1)(x+1) = 0",
        "2x + 3y = 10",
        "sin(x) = 0.5",
    ]
    
    for example in examples:
        processed = preprocess_math_input(example)
        print(f"Input:      {example}")
        print(f"Processed:  {processed}")
        
        try:
            if '=' in processed:
                left, right = processed.split('=')
                equation = sp.sympify(left) - sp.sympify(right)
            else:
                equation = sp.sympify(processed)
            
            variables = list(equation.free_symbols)
            print(f"Equation:   {equation} = 0")
            print(f"Variables:  {', '.join(str(v) for v in variables)}")
            
            if len(variables) == 1:
                solutions = sp.solve(equation, variables[0])
                print(f"Solutions:  {solutions}")
            
            print(f"Status:     ✓ Valid\n")
        except Exception as e:
            print(f"Error:      ✗ {str(e)}\n")


if __name__ == "__main__":
    all_passed = test_preprocessing()
    test_graphing_examples()
    test_equation_examples()
    
    if all_passed:
        print("\n" + "=" * 80)
        print("All preprocessing tests passed! ✓")
        print("=" * 80)
    else:
        print("\n" + "=" * 80)
        print("Some tests failed! Please review.")
        print("=" * 80)
