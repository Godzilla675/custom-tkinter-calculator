#!/usr/bin/env python3
"""
Advanced Custom Tkinter Calculator
Features:
- Basic arithmetic operations
- Scientific functions (sin, cos, tan, log, ln, etc.)
- Memory functions (M+, M-, MR, MC)
- Calculation history
- Dark/Light theme switching
- Keyboard support
- Error handling
"""

import customtkinter as ctk
import math
from typing import List, Optional


class Calculator(ctk.CTk):
    """Main calculator application class."""
    
    def __init__(self):
        super().__init__()
        
        # Window configuration
        self.title("Advanced Calculator")
        self.geometry("500x700")
        self.resizable(False, False)
        
        # Set theme
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        # Calculator state
        self.current_input = ""
        self.result_displayed = False
        self.memory = 0
        self.history: List[str] = []
        self.scientific_mode = False
        
        # Create UI
        self.create_widgets()
        
        # Bind keyboard events
        self.bind('<Key>', self.handle_keypress)
        
    def create_widgets(self):
        """Create all UI widgets."""
        # Main container
        main_frame = ctk.CTkFrame(self)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Top bar with mode toggle and theme toggle
        top_bar = ctk.CTkFrame(main_frame)
        top_bar.pack(fill="x", padx=5, pady=5)
        
        self.mode_button = ctk.CTkButton(
            top_bar,
            text="Scientific",
            width=100,
            command=self.toggle_mode
        )
        self.mode_button.pack(side="left", padx=5)
        
        self.theme_button = ctk.CTkButton(
            top_bar,
            text="Theme",
            width=100,
            command=self.toggle_theme
        )
        self.theme_button.pack(side="left", padx=5)
        
        self.history_button = ctk.CTkButton(
            top_bar,
            text="History",
            width=100,
            command=self.show_history
        )
        self.history_button.pack(side="left", padx=5)
        
        # Display frame
        display_frame = ctk.CTkFrame(main_frame)
        display_frame.pack(fill="x", padx=5, pady=5)
        
        # Memory indicator
        self.memory_label = ctk.CTkLabel(
            display_frame,
            text="",
            font=("Arial", 12),
            anchor="w"
        )
        self.memory_label.pack(fill="x", padx=5, pady=(5, 0))
        
        # Display
        self.display = ctk.CTkEntry(
            display_frame,
            font=("Arial", 28),
            height=60,
            justify="right"
        )
        self.display.pack(fill="x", padx=5, pady=5)
        self.display.insert(0, "0")
        
        # Buttons frame
        buttons_frame = ctk.CTkFrame(main_frame)
        buttons_frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Standard calculator buttons
        self.standard_buttons = [
            ['MC', 'MR', 'M+', 'M-'],
            ['C', '⌫', '%', '÷'],
            ['7', '8', '9', '×'],
            ['4', '5', '6', '-'],
            ['1', '2', '3', '+'],
            ['±', '0', '.', '=']
        ]
        
        # Scientific calculator buttons
        self.scientific_buttons = [
            ['sin', 'cos', 'tan', 'π'],
            ['log', 'ln', 'e', '√'],
            ['x²', 'xʸ', '(', ')'],
            ['1/x', 'n!', 'abs', 'mod']
        ]
        
        self.button_grid_frame = ctk.CTkFrame(buttons_frame)
        self.button_grid_frame.pack(fill="both", expand=True)
        
        self.create_button_grid()
        
    def create_button_grid(self):
        """Create the button grid based on current mode."""
        # Clear existing buttons
        for widget in self.button_grid_frame.winfo_children():
            widget.destroy()
        
        buttons = self.standard_buttons
        if self.scientific_mode:
            # Add scientific buttons at the top
            all_buttons = self.scientific_buttons + self.standard_buttons
            buttons = all_buttons
        
        # Create buttons
        for i, row in enumerate(buttons):
            for j, btn_text in enumerate(row):
                self.create_button(i, j, btn_text)
    
    def create_button(self, row: int, col: int, text: str):
        """Create a single button."""
        # Determine button color based on type
        if text in ['=']:
            fg_color = "#1f6aa5"  # Blue for equals
        elif text in ['C', '⌫']:
            fg_color = "#c93d3d"  # Red for clear/delete
        elif text in ['+', '-', '×', '÷', '%', '±']:
            fg_color = "#5a5a5a"  # Gray for operators
        elif text in ['MC', 'MR', 'M+', 'M-']:
            fg_color = "#8b5a8b"  # Purple for memory
        elif text in self.scientific_buttons[0] + self.scientific_buttons[1] + \
                     self.scientific_buttons[2] + self.scientific_buttons[3]:
            fg_color = "#2b7a3d"  # Green for scientific
        else:
            fg_color = "#3b3b3b"  # Default dark gray
        
        button = ctk.CTkButton(
            self.button_grid_frame,
            text=text,
            font=("Arial", 18, "bold"),
            height=60,
            fg_color=fg_color,
            command=lambda t=text: self.button_click(t)
        )
        button.grid(row=row, column=col, padx=3, pady=3, sticky="nsew")
        
        # Configure grid weights
        self.button_grid_frame.grid_rowconfigure(row, weight=1)
        self.button_grid_frame.grid_columnconfigure(col, weight=1)
    
    def button_click(self, text: str):
        """Handle button clicks."""
        try:
            if text == 'C':
                self.clear()
            elif text == '⌫':
                self.backspace()
            elif text == '=':
                self.calculate()
            elif text == 'MC':
                self.memory_clear()
            elif text == 'MR':
                self.memory_recall()
            elif text == 'M+':
                self.memory_add()
            elif text == 'M-':
                self.memory_subtract()
            elif text == '±':
                self.toggle_sign()
            elif text == '%':
                self.percentage()
            elif text == '√':
                self.square_root()
            elif text == 'x²':
                self.square()
            elif text == 'xʸ':
                self.append_to_input('**')
            elif text == '1/x':
                self.reciprocal()
            elif text == 'sin':
                self.trig_function('sin')
            elif text == 'cos':
                self.trig_function('cos')
            elif text == 'tan':
                self.trig_function('tan')
            elif text == 'log':
                self.log_function('log10')
            elif text == 'ln':
                self.log_function('log')
            elif text == 'π':
                self.append_to_input(str(math.pi))
            elif text == 'e':
                self.append_to_input(str(math.e))
            elif text == 'n!':
                self.factorial()
            elif text == 'abs':
                self.absolute()
            elif text == 'mod':
                self.append_to_input('%')
            elif text in ['(', ')']:
                self.append_to_input(text)
            elif text == '×':
                self.append_to_input('*')
            elif text == '÷':
                self.append_to_input('/')
            else:
                self.append_to_input(text)
        except Exception as e:
            self.display_error(str(e))
    
    def append_to_input(self, text: str):
        """Append text to current input."""
        if self.result_displayed:
            self.current_input = ""
            self.result_displayed = False
        
        # Don't allow multiple decimal points in a number
        if text == '.':
            # Get the last number in the expression
            parts = self.current_input.replace('+', ' ').replace('-', ' ').replace('*', ' ').replace('/', ' ').split()
            if parts and '.' in parts[-1]:
                return
        
        self.current_input += text
        self.update_display(self.current_input)
    
    def clear(self):
        """Clear the display."""
        self.current_input = ""
        self.result_displayed = False
        self.update_display("0")
    
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
            # Replace visual operators with Python operators
            expression = self.current_input
            
            # Add support for implicit multiplication (e.g., 2π -> 2*π)
            # This is a simplified version
            
            # Evaluate the expression
            result = eval(expression)
            
            # Format result
            if isinstance(result, float):
                if result.is_integer():
                    result = int(result)
                else:
                    result = round(result, 10)
            
            # Add to history
            self.add_to_history(f"{self.current_input} = {result}")
            
            # Update display
            self.current_input = str(result)
            self.update_display(self.current_input)
            self.result_displayed = True
            
        except ZeroDivisionError:
            self.display_error("Division by zero")
        except Exception as e:
            self.display_error("Error")
    
    def toggle_sign(self):
        """Toggle the sign of the current number."""
        if self.current_input:
            try:
                value = eval(self.current_input)
                self.current_input = str(-value)
                self.update_display(self.current_input)
                self.result_displayed = True
            except:
                pass
    
    def percentage(self):
        """Calculate percentage."""
        if self.current_input:
            try:
                value = eval(self.current_input)
                result = value / 100
                self.current_input = str(result)
                self.update_display(self.current_input)
                self.result_displayed = True
            except:
                self.display_error("Error")
    
    def square_root(self):
        """Calculate square root."""
        if self.current_input:
            try:
                value = eval(self.current_input)
                if value < 0:
                    self.display_error("Invalid input")
                    return
                result = math.sqrt(value)
                self.add_to_history(f"√({self.current_input}) = {result}")
                self.current_input = str(result)
                self.update_display(self.current_input)
                self.result_displayed = True
            except:
                self.display_error("Error")
    
    def square(self):
        """Calculate square."""
        if self.current_input:
            try:
                value = eval(self.current_input)
                result = value ** 2
                self.add_to_history(f"({self.current_input})² = {result}")
                self.current_input = str(result)
                self.update_display(self.current_input)
                self.result_displayed = True
            except:
                self.display_error("Error")
    
    def reciprocal(self):
        """Calculate reciprocal."""
        if self.current_input:
            try:
                value = eval(self.current_input)
                if value == 0:
                    self.display_error("Division by zero")
                    return
                result = 1 / value
                self.add_to_history(f"1/({self.current_input}) = {result}")
                self.current_input = str(result)
                self.update_display(self.current_input)
                self.result_displayed = True
            except:
                self.display_error("Error")
    
    def trig_function(self, func: str):
        """Calculate trigonometric function."""
        if self.current_input:
            try:
                value = eval(self.current_input)
                # Convert to radians (assume input is in degrees)
                radians = math.radians(value)
                
                if func == 'sin':
                    result = math.sin(radians)
                elif func == 'cos':
                    result = math.cos(radians)
                elif func == 'tan':
                    result = math.tan(radians)
                
                self.add_to_history(f"{func}({self.current_input}°) = {result}")
                self.current_input = str(result)
                self.update_display(self.current_input)
                self.result_displayed = True
            except:
                self.display_error("Error")
    
    def log_function(self, func: str):
        """Calculate logarithm."""
        if self.current_input:
            try:
                value = eval(self.current_input)
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
            except:
                self.display_error("Error")
    
    def factorial(self):
        """Calculate factorial."""
        if self.current_input:
            try:
                value = eval(self.current_input)
                if value < 0 or not float(value).is_integer():
                    self.display_error("Invalid input")
                    return
                result = math.factorial(int(value))
                self.add_to_history(f"{self.current_input}! = {result}")
                self.current_input = str(result)
                self.update_display(self.current_input)
                self.result_displayed = True
            except:
                self.display_error("Error")
    
    def absolute(self):
        """Calculate absolute value."""
        if self.current_input:
            try:
                value = eval(self.current_input)
                result = abs(value)
                self.add_to_history(f"abs({self.current_input}) = {result}")
                self.current_input = str(result)
                self.update_display(self.current_input)
                self.result_displayed = True
            except:
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
                value = eval(self.current_input)
                self.memory += value
                self.update_memory_indicator()
            except:
                pass
    
    def memory_subtract(self):
        """Subtract current value from memory."""
        if self.current_input:
            try:
                value = eval(self.current_input)
                self.memory -= value
                self.update_memory_indicator()
            except:
                pass
    
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
        if len(self.history) > 50:  # Keep last 50 entries
            self.history.pop(0)
    
    def show_history(self):
        """Show calculation history in a new window."""
        history_window = ctk.CTkToplevel(self)
        history_window.title("Calculation History")
        history_window.geometry("400x500")
        
        # Create text widget for history
        history_text = ctk.CTkTextbox(history_window, font=("Arial", 12))
        history_text.pack(fill="both", expand=True, padx=10, pady=10)
        
        if self.history:
            for entry in reversed(self.history):
                history_text.insert("1.0", entry + "\n")
        else:
            history_text.insert("1.0", "No history available")
        
        history_text.configure(state="disabled")
        
        # Clear history button
        clear_btn = ctk.CTkButton(
            history_window,
            text="Clear History",
            command=lambda: self.clear_history(history_window)
        )
        clear_btn.pack(pady=5)
    
    def clear_history(self, window):
        """Clear calculation history."""
        self.history.clear()
        window.destroy()
    
    def toggle_mode(self):
        """Toggle between standard and scientific mode."""
        self.scientific_mode = not self.scientific_mode
        
        if self.scientific_mode:
            self.geometry("500x900")
            self.mode_button.configure(text="Standard")
        else:
            self.geometry("500x700")
            self.mode_button.configure(text="Scientific")
        
        self.create_button_grid()
    
    def toggle_theme(self):
        """Toggle between light and dark theme."""
        current_mode = ctk.get_appearance_mode()
        if current_mode == "Dark":
            ctk.set_appearance_mode("light")
        else:
            ctk.set_appearance_mode("dark")
    
    def handle_keypress(self, event):
        """Handle keyboard input."""
        key = event.char
        
        # Number and operator keys
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
    app = Calculator()
    app.mainloop()


if __name__ == "__main__":
    main()
