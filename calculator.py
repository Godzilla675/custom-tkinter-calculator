#!/usr/bin/env python3
"""
Advanced Scientific Calculator with Graphing and Equation Solving
Features:
- Enhanced modern UI with tabs
- Basic and advanced arithmetic operations
- Complete scientific functions
- Graphing capabilities (2D function plotting)
- Equation solver (algebraic, quadratic, polynomial)
- Matrix operations
- Unit conversions
- Memory functions
- Calculation history
- Dark/Light theme switching
- Keyboard support
"""

import customtkinter as ctk
import math
import ast
import operator
from typing import List, Optional, Tuple
import numpy as np
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import sympy as sp
from sympy import symbols, solve, simplify, expand, factor, diff, integrate


def preprocess_math_input(expression: str) -> str:
    """
    Preprocess mathematical expressions to make them more user-friendly.
    Handles implicit multiplication, common notations, etc.
    
    Examples:
        '2x' -> '2*x'
        'x^2' -> 'x**2'
        '2(x+1)' -> '2*(x+1)'
        '(x)(y)' -> '(x)*(y)'
        'sin x' -> 'sin(x)'
        '2sin(x)' -> '2*sin(x)'
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
    # But avoid breaking function names
    # We'll do this carefully by only splitting isolated single letters
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


def safe_eval(expression: str) -> float:
    """
    Safely evaluate a mathematical expression without using eval().
    Only allows mathematical operations and prevents code injection.
    """
    allowed_operators = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.Pow: operator.pow,
        ast.Mod: operator.mod,
        ast.USub: operator.neg,
    }
    
    def eval_node(node):
        """Recursively evaluate AST nodes."""
        if isinstance(node, ast.Constant):
            return node.value
        elif isinstance(node, ast.Num):
            return node.n
        elif isinstance(node, ast.BinOp):
            left = eval_node(node.left)
            right = eval_node(node.right)
            op = allowed_operators.get(type(node.op))
            if op is None:
                raise ValueError(f"Unsupported operator: {type(node.op).__name__}")
            return op(left, right)
        elif isinstance(node, ast.UnaryOp):
            operand = eval_node(node.operand)
            op = allowed_operators.get(type(node.op))
            if op is None:
                raise ValueError(f"Unsupported unary operator: {type(node.op).__name__}")
            return op(operand)
        else:
            raise ValueError(f"Unsupported expression: {type(node).__name__}")
    
    try:
        tree = ast.parse(expression, mode='eval')
        return eval_node(tree.body)
    except (SyntaxError, ValueError, TypeError) as e:
        raise ValueError(f"Invalid expression: {str(e)}")


class AdvancedCalculator(ctk.CTk):
    """Main advanced calculator application class with tabs."""
    
    def __init__(self):
        super().__init__()
        
        # Window configuration
        self.title("Advanced Scientific Calculator")
        self.geometry("900x750")
        
        # Set theme
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        # Calculator state
        self.current_input = ""
        self.result_displayed = False
        self.memory = 0
        self.history: List[str] = []
        self.angle_mode = "deg"  # deg or rad
        
        # Create main UI
        self.create_main_ui()
        
        # Bind keyboard events
        self.bind('<Key>', self.handle_keypress)
        
    def create_main_ui(self):
        """Create the main tabbed interface."""
        # Header with theme toggle
        header = ctk.CTkFrame(self, height=50)
        header.pack(fill="x", padx=10, pady=(10, 5))
        
        title_label = ctk.CTkLabel(
            header,
            text="Advanced Scientific Calculator",
            font=("Arial", 20, "bold")
        )
        title_label.pack(side="left", padx=10)
        
        theme_btn = ctk.CTkButton(
            header,
            text="🌓 Theme",
            width=100,
            command=self.toggle_theme
        )
        theme_btn.pack(side="right", padx=10)
        
        # Create tabview
        self.tabview = ctk.CTkTabview(self, width=880, height=680)
        self.tabview.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Add tabs
        self.tabview.add("Calculator")
        self.tabview.add("Graphing")
        self.tabview.add("Equation Solver")
        self.tabview.add("Matrix")
        self.tabview.add("Conversions")
        
        # Setup each tab
        self.setup_calculator_tab()
        self.setup_graphing_tab()
        self.setup_solver_tab()
        self.setup_matrix_tab()
        self.setup_conversion_tab()
        
    def setup_calculator_tab(self):
        """Setup the main calculator tab with enhanced UI."""
        calc_tab = self.tabview.tab("Calculator")
        
        # Left side - Display and buttons
        left_frame = ctk.CTkFrame(calc_tab)
        left_frame.pack(side="left", fill="both", expand=True, padx=5, pady=5)
        
        # Display frame with memory indicator
        display_frame = ctk.CTkFrame(left_frame)
        display_frame.pack(fill="x", padx=5, pady=5)
        
        # Mode and memory indicators
        indicators_frame = ctk.CTkFrame(display_frame)
        indicators_frame.pack(fill="x", padx=5, pady=(5, 0))
        
        self.angle_label = ctk.CTkLabel(
            indicators_frame,
            text=f"Angle: {self.angle_mode.upper()}",
            font=("Arial", 11)
        )
        self.angle_label.pack(side="left", padx=5)
        
        self.memory_label = ctk.CTkLabel(
            indicators_frame,
            text="",
            font=("Arial", 11)
        )
        self.memory_label.pack(side="right", padx=5)
        
        # Main display
        self.display = ctk.CTkEntry(
            display_frame,
            font=("Arial", 32, "bold"),
            height=80,
            justify="right"
        )
        self.display.pack(fill="x", padx=5, pady=5)
        self.display.insert(0, "0")
        
        # Secondary display for expression
        self.expr_display = ctk.CTkEntry(
            display_frame,
            font=("Arial", 14),
            height=35,
            justify="right",
            fg_color="transparent"
        )
        self.expr_display.pack(fill="x", padx=5, pady=(0, 5))
        
        # Calculator buttons
        buttons_frame = ctk.CTkFrame(left_frame)
        buttons_frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Enhanced button layout with more functions
        self.calc_buttons = [
            ['2nd', 'π', 'e', 'C', '⌫'],
            ['x²', '√', 'xʸ', '∛', 'log'],
            ['sin', 'cos', 'tan', 'ln', '('],
            ['asin', 'acos', 'atan', 'eˣ', ')'],
            ['7', '8', '9', '÷', 'x!'],
            ['4', '5', '6', '×', '1/x'],
            ['1', '2', '3', '-', '%'],
            ['0', '.', '±', '+', '=']
        ]
        
        for i, row in enumerate(self.calc_buttons):
            for j, btn_text in enumerate(row):
                self.create_calc_button(buttons_frame, i, j, btn_text)
        
        # Configure grid weights
        for i in range(8):
            buttons_frame.grid_rowconfigure(i, weight=1)
        for j in range(5):
            buttons_frame.grid_columnconfigure(j, weight=1)
        
        # Right side - Quick functions and history
        right_frame = ctk.CTkFrame(calc_tab, width=250)
        right_frame.pack(side="right", fill="both", padx=5, pady=5)
        right_frame.pack_propagate(False)
        
        # Quick functions
        quick_label = ctk.CTkLabel(
            right_frame,
            text="Quick Functions",
            font=("Arial", 14, "bold")
        )
        quick_label.pack(pady=5)
        
        quick_btns = [
            ("MC", self.memory_clear),
            ("MR", self.memory_recall),
            ("M+", self.memory_add),
            ("M-", self.memory_subtract),
            ("DEG/RAD", self.toggle_angle_mode),
            ("History", self.show_history)
        ]
        
        for text, cmd in quick_btns:
            btn = ctk.CTkButton(
                right_frame,
                text=text,
                command=cmd,
                height=35
            )
            btn.pack(fill="x", padx=10, pady=2)
        
        # History display
        hist_label = ctk.CTkLabel(
            right_frame,
            text="Recent History",
            font=("Arial", 14, "bold")
        )
        hist_label.pack(pady=(15, 5))
        
        self.history_text = ctk.CTkTextbox(
            right_frame,
            font=("Courier", 11),
            height=300
        )
        self.history_text.pack(fill="both", expand=True, padx=10, pady=5)
        
    def setup_graphing_tab(self):
        """Setup the graphing tab."""
        graph_tab = self.tabview.tab("Graphing")
        
        # Control panel
        control_frame = ctk.CTkFrame(graph_tab, height=180)
        control_frame.pack(fill="x", padx=5, pady=5)
        control_frame.pack_propagate(False)
        
        # Function input
        ctk.CTkLabel(
            control_frame,
            text="Enter function f(x):",
            font=("Arial", 12, "bold")
        ).grid(row=0, column=0, padx=5, pady=5, sticky="w")
        
        self.func_entry = ctk.CTkEntry(
            control_frame,
            placeholder_text="e.g., sin(x), x^2, 2x+1, exp(x)",
            width=400,
            font=("Arial", 12)
        )
        self.func_entry.grid(row=0, column=1, padx=5, pady=5)
        
        # Range inputs
        ctk.CTkLabel(
            control_frame,
            text="X Range:",
            font=("Arial", 12)
        ).grid(row=1, column=0, padx=5, pady=5, sticky="w")
        
        range_frame = ctk.CTkFrame(control_frame)
        range_frame.grid(row=1, column=1, padx=5, pady=5, sticky="w")
        
        ctk.CTkLabel(range_frame, text="From:").pack(side="left", padx=2)
        self.x_min_entry = ctk.CTkEntry(range_frame, width=80)
        self.x_min_entry.pack(side="left", padx=2)
        self.x_min_entry.insert(0, "-10")
        
        ctk.CTkLabel(range_frame, text="To:").pack(side="left", padx=2)
        self.x_max_entry = ctk.CTkEntry(range_frame, width=80)
        self.x_max_entry.pack(side="left", padx=2)
        self.x_max_entry.insert(0, "10")
        
        # Buttons
        btn_frame = ctk.CTkFrame(control_frame)
        btn_frame.grid(row=2, column=0, columnspan=2, pady=10)
        
        ctk.CTkButton(
            btn_frame,
            text="Plot Function",
            command=self.plot_function,
            width=120
        ).pack(side="left", padx=5)
        
        ctk.CTkButton(
            btn_frame,
            text="Clear Graph",
            command=self.clear_graph,
            width=120
        ).pack(side="left", padx=5)
        
        ctk.CTkButton(
            btn_frame,
            text="Add Function",
            command=self.add_function,
            width=120
        ).pack(side="left", padx=5)
        
        # Error/Status label
        self.graph_error_label = ctk.CTkLabel(
            control_frame,
            text="",
            font=("Arial", 11),
            text_color="red"
        )
        self.graph_error_label.grid(row=3, column=0, columnspan=2, padx=5, pady=5)
        
        # Graph canvas
        self.graph_frame = ctk.CTkFrame(graph_tab)
        self.graph_frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Create matplotlib figure
        self.fig = Figure(figsize=(8, 5), dpi=100)
        self.ax = self.fig.add_subplot(111)
        self.ax.grid(True, alpha=0.3)
        self.ax.set_xlabel('x')
        self.ax.set_ylabel('f(x)')
        self.ax.set_title('Function Graph')
        
        self.canvas = FigureCanvasTkAgg(self.fig, self.graph_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill="both", expand=True)
        
    def setup_solver_tab(self):
        """Setup the equation solver tab."""
        solver_tab = self.tabview.tab("Equation Solver")
        
        # Instructions
        info_label = ctk.CTkLabel(
            solver_tab,
            text="Equation Solver - Solve algebraic equations",
            font=("Arial", 16, "bold")
        )
        info_label.pack(pady=10)
        
        # Input frame
        input_frame = ctk.CTkFrame(solver_tab)
        input_frame.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(
            input_frame,
            text="Enter equation (use x as variable):",
            font=("Arial", 12, "bold")
        ).pack(anchor="w", padx=10, pady=5)
        
        self.equation_entry = ctk.CTkEntry(
            input_frame,
            placeholder_text="e.g., x^2 - 4x + 4 = 0, 2x + 5 = 11",
            font=("Arial", 14),
            height=40
        )
        self.equation_entry.pack(fill="x", padx=10, pady=5)
        
        # Solver type
        type_frame = ctk.CTkFrame(input_frame)
        type_frame.pack(fill="x", padx=10, pady=5)
        
        ctk.CTkLabel(
            type_frame,
            text="Equation Type:",
            font=("Arial", 12)
        ).pack(side="left", padx=5)
        
        self.solver_type = ctk.CTkSegmentedButton(
            type_frame,
            values=["Algebraic", "Quadratic", "Polynomial", "Simplify"]
        )
        self.solver_type.pack(side="left", padx=10)
        self.solver_type.set("Algebraic")
        
        # Solve button
        ctk.CTkButton(
            input_frame,
            text="Solve Equation",
            command=self.solve_equation,
            height=40,
            font=("Arial", 13, "bold")
        ).pack(pady=10)
        
        # Operations frame
        ops_frame = ctk.CTkFrame(solver_tab)
        ops_frame.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(
            ops_frame,
            text="Expression Operations:",
            font=("Arial", 12, "bold")
        ).pack(anchor="w", padx=10, pady=5)
        
        ops_btn_frame = ctk.CTkFrame(ops_frame)
        ops_btn_frame.pack(fill="x", padx=10, pady=5)
        
        operations = [
            ("Expand", self.expand_expression),
            ("Factor", self.factor_expression),
            ("Differentiate", self.differentiate),
            ("Integrate", self.integrate_expression)
        ]
        
        for text, cmd in operations:
            ctk.CTkButton(
                ops_btn_frame,
                text=text,
                command=cmd,
                width=150
            ).pack(side="left", padx=5)
        
        # Result display
        ctk.CTkLabel(
            solver_tab,
            text="Solution:",
            font=("Arial", 12, "bold")
        ).pack(anchor="w", padx=20, pady=(10, 5))
        
        self.solver_result = ctk.CTkTextbox(
            solver_tab,
            font=("Courier", 13),
            height=300
        )
        self.solver_result.pack(fill="both", expand=True, padx=20, pady=(0, 10))
        
    def setup_matrix_tab(self):
        """Setup the matrix operations tab."""
        matrix_tab = self.tabview.tab("Matrix")
        
        ctk.CTkLabel(
            matrix_tab,
            text="Matrix Operations",
            font=("Arial", 16, "bold")
        ).pack(pady=10)
        
        # Matrix input frame
        input_frame = ctk.CTkFrame(matrix_tab)
        input_frame.pack(fill="x", padx=20, pady=10)
        
        # Matrix A
        matrix_a_frame = ctk.CTkFrame(input_frame)
        matrix_a_frame.pack(side="left", fill="both", expand=True, padx=5)
        
        ctk.CTkLabel(
            matrix_a_frame,
            text="Matrix A (rows separated by ; columns by ,):",
            font=("Arial", 11, "bold")
        ).pack(pady=5)
        
        self.matrix_a_entry = ctk.CTkTextbox(
            matrix_a_frame,
            height=100,
            font=("Courier", 11)
        )
        self.matrix_a_entry.pack(fill="both", expand=True, padx=5, pady=5)
        self.matrix_a_entry.insert("1.0", "1,2,3;4,5,6;7,8,9")
        
        # Matrix B
        matrix_b_frame = ctk.CTkFrame(input_frame)
        matrix_b_frame.pack(side="left", fill="both", expand=True, padx=5)
        
        ctk.CTkLabel(
            matrix_b_frame,
            text="Matrix B:",
            font=("Arial", 11, "bold")
        ).pack(pady=5)
        
        self.matrix_b_entry = ctk.CTkTextbox(
            matrix_b_frame,
            height=100,
            font=("Courier", 11)
        )
        self.matrix_b_entry.pack(fill="both", expand=True, padx=5, pady=5)
        self.matrix_b_entry.insert("1.0", "9,8,7;6,5,4;3,2,1")
        
        # Operations
        ops_frame = ctk.CTkFrame(matrix_tab)
        ops_frame.pack(fill="x", padx=20, pady=10)
        
        operations = [
            ("Add (A+B)", lambda: self.matrix_operation("add")),
            ("Subtract (A-B)", lambda: self.matrix_operation("subtract")),
            ("Multiply (A×B)", lambda: self.matrix_operation("multiply")),
            ("Transpose A", lambda: self.matrix_operation("transpose_a")),
            ("Determinant A", lambda: self.matrix_operation("det_a")),
            ("Inverse A", lambda: self.matrix_operation("inverse_a"))
        ]
        
        for i, (text, cmd) in enumerate(operations):
            btn = ctk.CTkButton(
                ops_frame,
                text=text,
                command=cmd,
                width=140
            )
            btn.grid(row=i//3, column=i%3, padx=5, pady=5)
        
        # Result
        ctk.CTkLabel(
            matrix_tab,
            text="Result:",
            font=("Arial", 12, "bold")
        ).pack(anchor="w", padx=20, pady=(10, 5))
        
        self.matrix_result = ctk.CTkTextbox(
            matrix_tab,
            font=("Courier", 12),
            height=200
        )
        self.matrix_result.pack(fill="both", expand=True, padx=20, pady=(0, 10))
        
    def setup_conversion_tab(self):
        """Setup the unit conversion tab."""
        conv_tab = self.tabview.tab("Conversions")
        
        ctk.CTkLabel(
            conv_tab,
            text="Unit Converter",
            font=("Arial", 16, "bold")
        ).pack(pady=10)
        
        # Conversion categories
        categories = {
            "Length": {
                "meter": 1,
                "kilometer": 1000,
                "centimeter": 0.01,
                "millimeter": 0.001,
                "mile": 1609.34,
                "yard": 0.9144,
                "foot": 0.3048,
                "inch": 0.0254
            },
            "Weight": {
                "kilogram": 1,
                "gram": 0.001,
                "milligram": 0.000001,
                "pound": 0.453592,
                "ounce": 0.0283495,
                "ton": 1000
            },
            "Temperature": {
                "celsius": "C",
                "fahrenheit": "F",
                "kelvin": "K"
            },
            "Area": {
                "sq_meter": 1,
                "sq_kilometer": 1000000,
                "sq_mile": 2589988,
                "sq_yard": 0.836127,
                "sq_foot": 0.092903,
                "acre": 4046.86,
                "hectare": 10000
            }
        }
        
        self.conversion_data = categories
        
        # Category selection
        cat_frame = ctk.CTkFrame(conv_tab)
        cat_frame.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(
            cat_frame,
            text="Category:",
            font=("Arial", 12, "bold")
        ).pack(side="left", padx=10)
        
        self.conv_category = ctk.CTkSegmentedButton(
            cat_frame,
            values=list(categories.keys()),
            command=self.update_conversion_units
        )
        self.conv_category.pack(side="left", padx=10)
        self.conv_category.set("Length")
        
        # Conversion frame
        convert_frame = ctk.CTkFrame(conv_tab)
        convert_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # From
        from_frame = ctk.CTkFrame(convert_frame)
        from_frame.pack(fill="x", pady=10)
        
        ctk.CTkLabel(
            from_frame,
            text="From:",
            font=("Arial", 12, "bold")
        ).pack(side="left", padx=10)
        
        self.from_value = ctk.CTkEntry(
            from_frame,
            placeholder_text="Enter value",
            width=150,
            font=("Arial", 13)
        )
        self.from_value.pack(side="left", padx=5)
        
        self.from_unit = ctk.CTkComboBox(
            from_frame,
            values=list(categories["Length"].keys()),
            width=150
        )
        self.from_unit.pack(side="left", padx=5)
        
        # To
        to_frame = ctk.CTkFrame(convert_frame)
        to_frame.pack(fill="x", pady=10)
        
        ctk.CTkLabel(
            to_frame,
            text="To:",
            font=("Arial", 12, "bold"),
            width=50
        ).pack(side="left", padx=10)
        
        self.to_value = ctk.CTkEntry(
            to_frame,
            width=150,
            font=("Arial", 13),
            state="readonly"
        )
        self.to_value.pack(side="left", padx=5)
        
        self.to_unit = ctk.CTkComboBox(
            to_frame,
            values=list(categories["Length"].keys()),
            width=150
        )
        self.to_unit.pack(side="left", padx=5)
        
        # Convert button
        ctk.CTkButton(
            convert_frame,
            text="Convert",
            command=self.perform_conversion,
            height=40,
            font=("Arial", 13, "bold")
        ).pack(pady=20)
        
        # Result display
        self.conversion_result = ctk.CTkLabel(
            convert_frame,
            text="",
            font=("Arial", 14)
        )
        self.conversion_result.pack(pady=10)
        
    def create_calc_button(self, parent, row: int, col: int, text: str):
        """Create a calculator button with enhanced styling."""
        # Determine button color based on type
        if text == '=':
            fg_color = "#1f6aa5"
            hover_color = "#1a5a8f"
        elif text in ['C', '⌫']:
            fg_color = "#c93d3d"
            hover_color = "#b03535"
        elif text in ['+', '-', '×', '÷', '%']:
            fg_color = "#6a6a6a"
            hover_color = "#5a5a5a"
        elif text in ['sin', 'cos', 'tan', 'asin', 'acos', 'atan', 'log', 'ln', 'eˣ', 
                      'x²', '√', 'xʸ', '∛', 'x!', '1/x', '2nd']:
            fg_color = "#2b7a3d"
            hover_color = "#246830"
        elif text in ['π', 'e']:
            fg_color = "#8b5a8b"
            hover_color = "#7a4a7a"
        else:
            fg_color = "#3b3b3b"
            hover_color = "#2b2b2b"
        
        button = ctk.CTkButton(
            parent,
            text=text,
            font=("Arial", 16, "bold"),
            fg_color=fg_color,
            hover_color=hover_color,
            command=lambda t=text: self.calc_button_click(t)
        )
        button.grid(row=row, column=col, padx=2, pady=2, sticky="nsew")
        
    def calc_button_click(self, text: str):
        """Handle calculator button clicks."""
        try:
            if text == 'C':
                self.clear()
            elif text == '⌫':
                self.backspace()
            elif text == '=':
                self.calculate()
            elif text == '±':
                self.toggle_sign()
            elif text == '%':
                self.percentage()
            elif text == '√':
                self.square_root()
            elif text == '∛':
                self.cube_root()
            elif text == 'x²':
                self.square()
            elif text == 'xʸ':
                self.append_to_input('**')
            elif text == '1/x':
                self.reciprocal()
            elif text == 'x!':
                self.factorial()
            elif text == 'sin':
                self.trig_function('sin')
            elif text == 'cos':
                self.trig_function('cos')
            elif text == 'tan':
                self.trig_function('tan')
            elif text == 'asin':
                self.trig_function('asin')
            elif text == 'acos':
                self.trig_function('acos')
            elif text == 'atan':
                self.trig_function('atan')
            elif text == 'log':
                self.log_function('log10')
            elif text == 'ln':
                self.log_function('log')
            elif text == 'eˣ':
                self.exp_function()
            elif text == 'π':
                self.append_to_input(str(math.pi))
            elif text == 'e':
                self.append_to_input(str(math.e))
            elif text in ['(', ')']:
                self.append_to_input(text)
            elif text == '×':
                self.append_to_input('*')
            elif text == '÷':
                self.append_to_input('/')
            elif text == '2nd':
                pass  # Toggle secondary functions
            else:
                self.append_to_input(text)
                
            # Update expression display
            self.expr_display.delete(0, "end")
            self.expr_display.insert(0, self.current_input)
                
        except Exception as e:
            self.display_error(str(e))
    
    def append_to_input(self, text: str):
        """Append text to current input."""
        if self.result_displayed:
            self.current_input = ""
            self.result_displayed = False
        
        self.current_input += text
        self.update_display(self.current_input)
    
    def clear(self):
        """Clear the display."""
        self.current_input = ""
        self.result_displayed = False
        self.update_display("0")
        self.expr_display.delete(0, "end")
    
    def backspace(self):
        """Delete last character."""
        if not self.result_displayed and self.current_input:
            self.current_input = self.current_input[:-1]
            self.update_display(self.current_input if self.current_input else "0")
    
    def calculate(self):
        """Evaluate the current expression."""
        if not self.current_input:
            return
        
        try:
            result = safe_eval(self.current_input)
            
            if isinstance(result, float):
                if result.is_integer():
                    result = int(result)
                else:
                    result = round(result, 10)
            
            self.add_to_history(f"{self.current_input} = {result}")
            self.current_input = str(result)
            self.update_display(self.current_input)
            self.result_displayed = True
            
        except ZeroDivisionError:
            self.display_error("Division by zero")
        except (ValueError, TypeError, SyntaxError):
            self.display_error("Error")
    
    def toggle_sign(self):
        """Toggle the sign of the current number."""
        if self.current_input:
            try:
                value = safe_eval(self.current_input)
                self.current_input = str(-value)
                self.update_display(self.current_input)
                self.result_displayed = True
            except (ValueError, TypeError, ZeroDivisionError):
                pass
    
    def percentage(self):
        """Calculate percentage."""
        if self.current_input:
            try:
                value = safe_eval(self.current_input)
                result = value / 100
                self.current_input = str(result)
                self.update_display(self.current_input)
                self.result_displayed = True
            except (ValueError, TypeError, ZeroDivisionError):
                self.display_error("Error")
    
    def square_root(self):
        """Calculate square root."""
        if self.current_input:
            try:
                value = safe_eval(self.current_input)
                if value < 0:
                    self.display_error("Invalid input")
                    return
                result = math.sqrt(value)
                self.add_to_history(f"√({self.current_input}) = {result}")
                self.current_input = str(result)
                self.update_display(self.current_input)
                self.result_displayed = True
            except (ValueError, TypeError, ZeroDivisionError):
                self.display_error("Error")
    
    def cube_root(self):
        """Calculate cube root."""
        if self.current_input:
            try:
                value = safe_eval(self.current_input)
                result = value ** (1/3)
                self.add_to_history(f"∛({self.current_input}) = {result}")
                self.current_input = str(result)
                self.update_display(self.current_input)
                self.result_displayed = True
            except (ValueError, TypeError, ZeroDivisionError):
                self.display_error("Error")
    
    def square(self):
        """Calculate square."""
        if self.current_input:
            try:
                value = safe_eval(self.current_input)
                result = value ** 2
                self.add_to_history(f"({self.current_input})² = {result}")
                self.current_input = str(result)
                self.update_display(self.current_input)
                self.result_displayed = True
            except (ValueError, TypeError, ZeroDivisionError):
                self.display_error("Error")
    
    def reciprocal(self):
        """Calculate reciprocal."""
        if self.current_input:
            try:
                value = safe_eval(self.current_input)
                if value == 0:
                    self.display_error("Division by zero")
                    return
                result = 1 / value
                self.add_to_history(f"1/({self.current_input}) = {result}")
                self.current_input = str(result)
                self.update_display(self.current_input)
                self.result_displayed = True
            except (ValueError, TypeError, ZeroDivisionError):
                self.display_error("Error")
    
    def factorial(self):
        """Calculate factorial."""
        if self.current_input:
            try:
                value = safe_eval(self.current_input)
                if value < 0 or not float(value).is_integer():
                    self.display_error("Invalid input")
                    return
                result = math.factorial(int(value))
                self.add_to_history(f"{self.current_input}! = {result}")
                self.current_input = str(result)
                self.update_display(self.current_input)
                self.result_displayed = True
            except (ValueError, TypeError, ZeroDivisionError):
                self.display_error("Error")
    
    def trig_function(self, func: str):
        """Calculate trigonometric function."""
        if self.current_input:
            try:
                value = safe_eval(self.current_input)
                
                if func in ['sin', 'cos', 'tan']:
                    if self.angle_mode == "deg":
                        radians = math.radians(value)
                    else:
                        radians = value
                    
                    if func == 'sin':
                        result = math.sin(radians)
                    elif func == 'cos':
                        result = math.cos(radians)
                    elif func == 'tan':
                        result = math.tan(radians)
                else:  # Inverse trig functions
                    if func == 'asin':
                        result = math.asin(value)
                    elif func == 'acos':
                        result = math.acos(value)
                    elif func == 'atan':
                        result = math.atan(value)
                    
                    if self.angle_mode == "deg":
                        result = math.degrees(result)
                
                mode_str = "°" if self.angle_mode == "deg" else "rad"
                self.add_to_history(f"{func}({self.current_input}{mode_str}) = {result}")
                self.current_input = str(result)
                self.update_display(self.current_input)
                self.result_displayed = True
            except (ValueError, TypeError, ZeroDivisionError):
                self.display_error("Error")
    
    def log_function(self, func: str):
        """Calculate logarithm."""
        if self.current_input:
            try:
                value = safe_eval(self.current_input)
                if value <= 0:
                    self.display_error("Invalid input")
                    return
                
                if func == 'log10':
                    result = math.log10(value)
                    func_name = "log"
                elif func == 'log':
                    result = math.log(value)
                    func_name = "ln"
                
                self.add_to_history(f"{func_name}({self.current_input}) = {result}")
                self.current_input = str(result)
                self.update_display(self.current_input)
                self.result_displayed = True
            except (ValueError, TypeError, ZeroDivisionError):
                self.display_error("Error")
    
    def exp_function(self):
        """Calculate e^x."""
        if self.current_input:
            try:
                value = safe_eval(self.current_input)
                result = math.exp(value)
                self.add_to_history(f"e^({self.current_input}) = {result}")
                self.current_input = str(result)
                self.update_display(self.current_input)
                self.result_displayed = True
            except (ValueError, TypeError, ZeroDivisionError):
                self.display_error("Error")
    
    def memory_clear(self):
        """Clear memory."""
        self.memory = 0
        self.update_memory_indicator()
    
    def memory_recall(self):
        """Recall memory value."""
        self.current_input = str(self.memory)
        self.update_display(self.current_input)
        self.result_displayed = True
    
    def memory_add(self):
        """Add current value to memory."""
        if self.current_input:
            try:
                value = safe_eval(self.current_input)
                self.memory += value
                self.update_memory_indicator()
            except (ValueError, TypeError, ZeroDivisionError):
                pass
    
    def memory_subtract(self):
        """Subtract current value from memory."""
        if self.current_input:
            try:
                value = safe_eval(self.current_input)
                self.memory -= value
                self.update_memory_indicator()
            except (ValueError, TypeError, ZeroDivisionError):
                pass
    
    def toggle_angle_mode(self):
        """Toggle between degrees and radians."""
        self.angle_mode = "rad" if self.angle_mode == "deg" else "deg"
        self.angle_label.configure(text=f"Angle: {self.angle_mode.upper()}")
    
    def update_memory_indicator(self):
        """Update memory indicator label."""
        if self.memory != 0:
            self.memory_label.configure(text=f"M: {self.memory}")
        else:
            self.memory_label.configure(text="")
    
    def update_display(self, text: str):
        """Update the display."""
        self.display.delete(0, "end")
        self.display.insert(0, text)
    
    def display_error(self, message: str):
        """Display error message."""
        self.update_display(message)
        self.after(2000, lambda: self.update_display("0"))
        self.current_input = ""
        self.result_displayed = False
    
    def add_to_history(self, entry: str):
        """Add calculation to history."""
        self.history.append(entry)
        if len(self.history) > 50:
            self.history.pop(0)
        
        # Update history display
        self.history_text.delete("1.0", "end")
        for item in reversed(self.history[-10:]):  # Show last 10
            self.history_text.insert("1.0", item + "\n")
    
    def show_history(self):
        """Show full calculation history in a new window."""
        history_window = ctk.CTkToplevel(self)
        history_window.title("Calculation History")
        history_window.geometry("500x600")
        
        history_text = ctk.CTkTextbox(history_window, font=("Courier", 12))
        history_text.pack(fill="both", expand=True, padx=10, pady=10)
        
        if self.history:
            for entry in reversed(self.history):
                history_text.insert("1.0", entry + "\n")
        else:
            history_text.insert("1.0", "No history available")
        
        history_text.configure(state="disabled")
        
        ctk.CTkButton(
            history_window,
            text="Clear History",
            command=lambda: self.clear_history(history_window)
        ).pack(pady=5)
    
    def clear_history(self, window):
        """Clear calculation history."""
        self.history.clear()
        self.history_text.delete("1.0", "end")
        window.destroy()
    
    def toggle_theme(self):
        """Toggle between light and dark theme."""
        current_mode = ctk.get_appearance_mode()
        if current_mode == "Dark":
            ctk.set_appearance_mode("light")
        else:
            ctk.set_appearance_mode("dark")
    
    # Graphing functions
    def plot_function(self):
        """Plot the function entered by user."""
        try:
            func_str = self.func_entry.get()
            x_min = float(self.x_min_entry.get())
            x_max = float(self.x_max_entry.get())
            
            if not func_str:
                return
            
            # Create x values
            x_vals = np.linspace(x_min, x_max, 1000)
            
            # Use sympy to evaluate the function safely
            x = sp.Symbol('x')
            
            # Preprocess the function string for user-friendly input
            func_str_clean = preprocess_math_input(func_str)
            expr = sp.sympify(func_str_clean)
            
            # Convert to numpy function for vectorized evaluation
            func = sp.lambdify(x, expr, modules=['numpy'])
            
            # Evaluate function
            y_vals = func(x_vals)
            
            # Clear and plot
            self.ax.clear()
            self.ax.grid(True, alpha=0.3)
            self.ax.plot(x_vals, y_vals, 'b-', linewidth=2, label=self.func_entry.get())
            self.ax.axhline(y=0, color='k', linewidth=0.5)
            self.ax.axvline(x=0, color='k', linewidth=0.5)
            self.ax.set_xlabel('x', fontsize=11)
            self.ax.set_ylabel('f(x)', fontsize=11)
            self.ax.set_title(f'Graph of f(x) = {self.func_entry.get()}', fontsize=12)
            self.ax.legend()
            self.canvas.draw()
            
            # Clear any previous error
            self.graph_error_label.configure(text="")
            
        except Exception as e:
            # Display error in the error label
            self.graph_error_label.configure(text=f"Error: {str(e)}")
    
    def add_function(self):
        """Add another function to the existing plot."""
        try:
            func_str = self.func_entry.get()
            x_min = float(self.x_min_entry.get())
            x_max = float(self.x_max_entry.get())
            
            if not func_str:
                return
            
            # Create x values
            x_vals = np.linspace(x_min, x_max, 1000)
            
            # Use sympy to evaluate the function safely
            x = sp.Symbol('x')
            
            # Preprocess the function string for user-friendly input
            func_str_clean = preprocess_math_input(func_str)
            expr = sp.sympify(func_str_clean)
            
            # Convert to numpy function for vectorized evaluation
            func = sp.lambdify(x, expr, modules=['numpy'])
            
            # Evaluate function
            y_vals = func(x_vals)
            
            # Add to existing plot
            self.ax.plot(x_vals, y_vals, linewidth=2, label=self.func_entry.get())
            self.ax.legend()
            self.canvas.draw()
            
            # Clear any previous error
            self.graph_error_label.configure(text="")
            
        except Exception as e:
            self.graph_error_label.configure(text=f"Error: {str(e)}")
    
    def clear_graph(self):
        """Clear the graph."""
        self.ax.clear()
        self.ax.grid(True, alpha=0.3)
        self.ax.set_xlabel('x')
        self.ax.set_ylabel('f(x)')
        self.ax.set_title('Function Graph')
        self.canvas.draw()
    
    # Equation solver functions
    def solve_equation(self):
        """Solve the equation entered by user."""
        try:
            equation_str = self.equation_entry.get()
            if not equation_str:
                return
            
            # Preprocess the equation string for user-friendly input
            equation_str_clean = preprocess_math_input(equation_str)
            
            # Parse equation
            if '=' in equation_str_clean:
                left, right = equation_str_clean.split('=')
                equation = sp.sympify(left) - sp.sympify(right)
            else:
                equation = sp.sympify(equation_str_clean)
            
            # Detect all variables in the equation
            variables = list(equation.free_symbols)
            
            # Display result
            self.solver_result.delete("1.0", "end")
            self.solver_result.insert("1.0", f"Equation: {equation_str}\n\n")
            
            if len(variables) == 0:
                self.solver_result.insert("end", "No variables found in equation.\n")
                return
            
            # Sort variables by name for consistent display
            variables = sorted(variables, key=lambda s: str(s))
            
            solver_type = self.solver_type.get()
            
            if len(variables) == 1:
                # Single variable equation
                var = variables[0]
                self.solver_result.insert("end", f"Solving for {var}:\n\n")
                
                if solver_type == "Simplify":
                    solutions = simplify(equation)
                    self.solver_result.insert("end", f"Simplified: {solutions}\n")
                else:
                    solutions = solve(equation, var)
                    self.solver_result.insert("end", f"Solution(s):\n")
                    if isinstance(solutions, list):
                        if len(solutions) == 0:
                            self.solver_result.insert("end", "  No solutions found\n")
                        else:
                            for i, sol in enumerate(solutions, 1):
                                self.solver_result.insert("end", f"  {var}{i} = {sol}\n")
                    else:
                        self.solver_result.insert("end", f"  {var} = {solutions}\n")
            else:
                # Multiple variables - solve for each variable
                self.solver_result.insert("end", f"Variables detected: {', '.join(str(v) for v in variables)}\n\n")
                
                if solver_type == "Simplify":
                    solutions = simplify(equation)
                    self.solver_result.insert("end", f"Simplified: {solutions}\n")
                else:
                    # Try to solve for each variable in terms of others
                    for var in variables:
                        try:
                            solutions = solve(equation, var)
                            self.solver_result.insert("end", f"Solving for {var}:\n")
                            if isinstance(solutions, list):
                                if len(solutions) == 0:
                                    self.solver_result.insert("end", "  No solutions found\n")
                                else:
                                    for i, sol in enumerate(solutions, 1):
                                        self.solver_result.insert("end", f"  {var} = {sol}\n")
                            else:
                                self.solver_result.insert("end", f"  {var} = {solutions}\n")
                            self.solver_result.insert("end", "\n")
                        except Exception as e:
                            self.solver_result.insert("end", f"  Cannot solve for {var}: {str(e)}\n\n")
            
        except Exception as e:
            self.solver_result.delete("1.0", "end")
            self.solver_result.insert("1.0", f"Error solving equation: {str(e)}\n\n")
            self.solver_result.insert("end", "Make sure your equation is properly formatted.\n")
            self.solver_result.insert("end", "Example: x^2 - 4x + 4 = 0 or x + 2y = 10")
    
    def expand_expression(self):
        """Expand the expression."""
        try:
            expr_str = self.equation_entry.get().split('=')[0]
            expr_str_clean = preprocess_math_input(expr_str)
            expr = sp.sympify(expr_str_clean)
            result = expand(expr)
            
            self.solver_result.delete("1.0", "end")
            self.solver_result.insert("1.0", f"Original: {expr_str}\n\n")
            self.solver_result.insert("end", f"Expanded: {result}")
        except Exception as e:
            self.solver_result.delete("1.0", "end")
            self.solver_result.insert("1.0", f"Error: {str(e)}")
    
    def factor_expression(self):
        """Factor the expression."""
        try:
            expr_str = self.equation_entry.get().split('=')[0]
            expr_str_clean = preprocess_math_input(expr_str)
            expr = sp.sympify(expr_str_clean)
            result = factor(expr)
            
            self.solver_result.delete("1.0", "end")
            self.solver_result.insert("1.0", f"Original: {expr_str}\n\n")
            self.solver_result.insert("end", f"Factored: {result}")
        except Exception as e:
            self.solver_result.delete("1.0", "end")
            self.solver_result.insert("1.0", f"Error: {str(e)}")
    
    def differentiate(self):
        """Differentiate the expression."""
        try:
            expr_str = self.equation_entry.get().split('=')[0]
            expr_str_clean = preprocess_math_input(expr_str)
            expr = sp.sympify(expr_str_clean)
            
            # Detect all variables
            variables = list(expr.free_symbols)
            
            if len(variables) == 0:
                self.solver_result.delete("1.0", "end")
                self.solver_result.insert("1.0", "No variables found in expression.")
                return
            
            # Sort variables by name for consistent display
            variables = sorted(variables, key=lambda s: str(s))
            
            self.solver_result.delete("1.0", "end")
            self.solver_result.insert("1.0", f"f({', '.join(str(v) for v in variables)}) = {expr_str}\n\n")
            
            # Differentiate with respect to each variable
            if len(variables) == 1:
                var = variables[0]
                result = diff(expr, var)
                self.solver_result.insert("end", f"f'({var}) = {result}")
            else:
                self.solver_result.insert("end", "Partial derivatives:\n\n")
                for var in variables:
                    result = diff(expr, var)
                    self.solver_result.insert("end", f"∂f/∂{var} = {result}\n")
                    
        except Exception as e:
            self.solver_result.delete("1.0", "end")
            self.solver_result.insert("1.0", f"Error: {str(e)}")
    
    def integrate_expression(self):
        """Integrate the expression."""
        try:
            expr_str = self.equation_entry.get().split('=')[0]
            expr_str_clean = preprocess_math_input(expr_str)
            expr = sp.sympify(expr_str_clean)
            
            # Detect all variables
            variables = list(expr.free_symbols)
            
            if len(variables) == 0:
                self.solver_result.delete("1.0", "end")
                self.solver_result.insert("1.0", "No variables found in expression.")
                return
            
            # Sort variables by name for consistent display
            variables = sorted(variables, key=lambda s: str(s))
            
            self.solver_result.delete("1.0", "end")
            self.solver_result.insert("1.0", f"f({', '.join(str(v) for v in variables)}) = {expr_str}\n\n")
            
            # Integrate with respect to each variable
            if len(variables) == 1:
                var = variables[0]
                result = integrate(expr, var)
                self.solver_result.insert("end", f"∫f({var})d{var} = {result} + C")
            else:
                self.solver_result.insert("end", "Integrals with respect to each variable:\n\n")
                for var in variables:
                    result = integrate(expr, var)
                    self.solver_result.insert("end", f"∫f(...)d{var} = {result} + C\n")
                    
        except Exception as e:
            self.solver_result.delete("1.0", "end")
            self.solver_result.insert("1.0", f"Error: {str(e)}")
    
    # Matrix operations
    def parse_matrix(self, matrix_str: str) -> np.ndarray:
        """Parse matrix from string."""
        rows = matrix_str.strip().split(';')
        matrix = []
        for row in rows:
            cols = [float(x.strip()) for x in row.split(',')]
            matrix.append(cols)
        return np.array(matrix)
    
    def matrix_operation(self, operation: str):
        """Perform matrix operation."""
        try:
            self.matrix_result.delete("1.0", "end")
            
            matrix_a_str = self.matrix_a_entry.get("1.0", "end").strip()
            matrix_a = self.parse_matrix(matrix_a_str)
            
            if operation == "add":
                matrix_b_str = self.matrix_b_entry.get("1.0", "end").strip()
                matrix_b = self.parse_matrix(matrix_b_str)
                result = matrix_a + matrix_b
                self.matrix_result.insert("1.0", f"A + B =\n{result}")
                
            elif operation == "subtract":
                matrix_b_str = self.matrix_b_entry.get("1.0", "end").strip()
                matrix_b = self.parse_matrix(matrix_b_str)
                result = matrix_a - matrix_b
                self.matrix_result.insert("1.0", f"A - B =\n{result}")
                
            elif operation == "multiply":
                matrix_b_str = self.matrix_b_entry.get("1.0", "end").strip()
                matrix_b = self.parse_matrix(matrix_b_str)
                result = np.matmul(matrix_a, matrix_b)
                self.matrix_result.insert("1.0", f"A × B =\n{result}")
                
            elif operation == "transpose_a":
                result = matrix_a.T
                self.matrix_result.insert("1.0", f"Transpose of A =\n{result}")
                
            elif operation == "det_a":
                det = np.linalg.det(matrix_a)
                self.matrix_result.insert("1.0", f"Determinant of A = {det}")
                
            elif operation == "inverse_a":
                inv = np.linalg.inv(matrix_a)
                self.matrix_result.insert("1.0", f"Inverse of A =\n{inv}")
                
        except Exception as e:
            self.matrix_result.delete("1.0", "end")
            self.matrix_result.insert("1.0", f"Error: {str(e)}\n\n")
            self.matrix_result.insert("end", "Make sure matrices are properly formatted.\n")
            self.matrix_result.insert("end", "Example: 1,2,3;4,5,6;7,8,9")
    
    # Conversion functions
    def update_conversion_units(self, category: str):
        """Update unit dropdowns based on selected category."""
        units = list(self.conversion_data[category].keys())
        self.from_unit.configure(values=units)
        self.to_unit.configure(values=units)
        self.from_unit.set(units[0])
        self.to_unit.set(units[1] if len(units) > 1 else units[0])
    
    def perform_conversion(self):
        """Perform unit conversion."""
        try:
            value = float(self.from_value.get())
            category = self.conv_category.get()
            from_unit = self.from_unit.get()
            to_unit = self.to_unit.get()
            
            if category == "Temperature":
                result = self.convert_temperature(value, from_unit, to_unit)
            else:
                # Get conversion factors
                from_factor = self.conversion_data[category][from_unit]
                to_factor = self.conversion_data[category][to_unit]
                
                # Convert to base unit then to target unit
                base_value = value * from_factor
                result = base_value / to_factor
            
            self.to_value.configure(state="normal")
            self.to_value.delete(0, "end")
            self.to_value.insert(0, f"{result:.6f}")
            self.to_value.configure(state="readonly")
            
            self.conversion_result.configure(
                text=f"{value} {from_unit} = {result:.6f} {to_unit}"
            )
            
        except Exception as e:
            self.conversion_result.configure(text=f"Error: {str(e)}")
    
    def convert_temperature(self, value: float, from_unit: str, to_unit: str) -> float:
        """Convert temperature between units."""
        # Convert to Celsius first
        if from_unit == "celsius":
            celsius = value
        elif from_unit == "fahrenheit":
            celsius = (value - 32) * 5/9
        elif from_unit == "kelvin":
            celsius = value - 273.15
        
        # Convert from Celsius to target
        if to_unit == "celsius":
            return celsius
        elif to_unit == "fahrenheit":
            return celsius * 9/5 + 32
        elif to_unit == "kelvin":
            return celsius + 273.15
    
    def handle_keypress(self, event):
        """Handle keyboard input."""
        # Only handle keyboard in calculator tab
        if self.tabview.get() != "Calculator":
            return
        
        key = event.char
        
        if key in '0123456789.+-*/()':
            if key == '*':
                self.append_to_input('*')
            elif key == '/':
                self.append_to_input('/')
            else:
                self.append_to_input(key)
        elif event.keysym == 'Return':
            self.calculate()
        elif event.keysym == 'BackSpace':
            self.backspace()
        elif event.keysym == 'Escape':
            self.clear()
        elif key == '%':
            self.percentage()


def main():
    """Main entry point."""
    app = AdvancedCalculator()
    app.mainloop()


if __name__ == "__main__":
    main()
