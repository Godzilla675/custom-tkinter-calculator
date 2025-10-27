#!/usr/bin/env python3
"""
Demo script to showcase the calculator features.
Run this to see the calculator in action.
"""

from calculator import Calculator


def main():
    """Launch the calculator application."""
    print("=" * 60)
    print("Advanced Custom Tkinter Calculator")
    print("=" * 60)
    print()
    print("Features:")
    print("  • Basic arithmetic (+, -, ×, ÷)")
    print("  • Scientific functions (sin, cos, tan, log, ln, √, etc.)")
    print("  • Memory functions (MC, MR, M+, M-)")
    print("  • Calculation history")
    print("  • Light/Dark theme switching")
    print("  • Keyboard support")
    print()
    print("Keyboard shortcuts:")
    print("  • 0-9: Numbers")
    print("  • +, -, *, /: Operators")
    print("  • Enter: Calculate")
    print("  • Backspace: Delete")
    print("  • Escape: Clear")
    print()
    print("Launching calculator...")
    print("=" * 60)
    print()
    
    app = Calculator()
    app.mainloop()


if __name__ == "__main__":
    main()
