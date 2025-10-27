#!/usr/bin/env python3
"""
Demo script to showcase the Enhanced Advanced Calculator features.
Run this to see the calculator in action with all its new capabilities.
"""

from calculator import AdvancedCalculator


def main():
    """Launch the enhanced calculator application."""
    print("=" * 70)
    print("Advanced Scientific Calculator - Enhanced Edition")
    print("=" * 70)
    print()
    print("🚀 NEW FEATURES:")
    print("  • Tabbed interface with 5 different modes")
    print("  • 2D Function graphing with matplotlib")
    print("  • Equation solver (algebraic, quadratic, polynomial)")
    print("  • Expression operations (expand, factor, differentiate, integrate)")
    print("  • Matrix operations (add, subtract, multiply, transpose, det, inverse)")
    print("  • Unit conversions (length, weight, temperature, area)")
    print("  • Enhanced UI with better styling")
    print()
    print("📊 TABS:")
    print("  1. Calculator - Enhanced scientific calculator with 20+ functions")
    print("  2. Graphing - Plot mathematical functions")
    print("  3. Equation Solver - Solve equations and manipulate expressions")
    print("  4. Matrix - Matrix operations and calculations")
    print("  5. Conversions - Unit converter for various measurements")
    print()
    print("⌨️  KEYBOARD SHORTCUTS:")
    print("  • 0-9: Numbers")
    print("  • +, -, *, /: Operators")
    print("  • Enter: Calculate")
    print("  • Backspace: Delete")
    print("  • Escape: Clear")
    print("  • %: Percentage")
    print("  • ( ): Parentheses")
    print()
    print("🎨 FEATURES:")
    print("  • Angle mode toggle (DEG/RAD)")
    print("  • Memory functions (MC, MR, M+, M-)")
    print("  • Real-time calculation history")
    print("  • Light/Dark theme switching")
    print("  • Safe expression evaluation (secure)")
    print()
    print("Launching calculator...")
    print("=" * 70)
    print()
    
    app = AdvancedCalculator()
    app.mainloop()


if __name__ == "__main__":
    main()
