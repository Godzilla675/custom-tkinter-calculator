# Advanced Custom Tkinter Calculator

A feature-rich, modern calculator built with CustomTkinter in Python. This calculator supports both basic and advanced scientific operations, with a beautiful, theme-switchable interface.

![Calculator](https://img.shields.io/badge/Python-3.8+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

## Features

### Core Functionality
- **Basic Arithmetic**: Addition, subtraction, multiplication, and division
- **Scientific Functions**:
  - Trigonometric: sin, cos, tan (in degrees)
  - Logarithmic: log (base 10) and ln (natural log)
  - Power operations: square (x²), power (xʸ)
  - Root: square root (√)
  - Other: factorial (n!), absolute value (abs), modulo (mod), reciprocal (1/x)
  - Constants: π (pi) and e (Euler's number)

### Memory Functions
- **MC**: Memory Clear
- **MR**: Memory Recall
- **M+**: Memory Add
- **M-**: Memory Subtract

### User Interface Features
- **Dual Mode**: Switch between Standard and Scientific calculator modes
- **Theme Switching**: Toggle between light and dark themes
- **Calculation History**: View and manage your calculation history
- **Keyboard Support**: Full keyboard input support for faster calculations
- **Error Handling**: Graceful error messages for invalid operations
- **Responsive Design**: Clean, modern interface built with CustomTkinter

## Installation

### Prerequisites
- Python 3.8 or higher
- tkinter (usually comes with Python)

### Setup

1. Clone the repository:
```bash
git clone https://github.com/Godzilla675/custom-tkinter-calculator.git
cd custom-tkinter-calculator
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the calculator:
```bash
python calculator.py
```

## Usage

### Basic Operations
- Click number buttons to input numbers
- Click operator buttons (+, -, ×, ÷) for basic arithmetic
- Press `=` or Enter key to calculate the result
- Use `C` to clear the display
- Use `⌫` (backspace) to delete the last character

### Scientific Mode
1. Click the **Scientific** button to switch to scientific mode
2. Additional buttons will appear for advanced functions
3. Click **Standard** to return to basic mode

### Memory Functions
1. Perform a calculation
2. Click `M+` to add the result to memory
3. Click `MR` to recall the memory value
4. Click `M-` to subtract from memory
5. Click `MC` to clear memory

### Keyboard Shortcuts
- **Numbers (0-9)**: Input numbers
- **Operators (+, -, *, /)**: Perform operations
- **Enter**: Calculate result
- **Backspace**: Delete last character
- **Escape**: Clear display
- **%**: Percentage
- **( )**: Parentheses for grouping

### Theme Switching
Click the **Theme** button to toggle between light and dark themes.

### Viewing History
1. Click the **History** button to view your calculation history
2. The history shows the last 50 calculations
3. Click **Clear History** to reset the history

## Examples

### Basic Calculation
```
Input: 15 + 27
Output: 42
```

### Scientific Calculation
```
Input: sin(30)
Output: 0.5 (sine of 30 degrees)
```

### Complex Expression
```
Input: (5 + 3) * 2 - 4
Output: 12
```

### Power Operation
```
Input: 2 xʸ 8
(or: 2**8)
Output: 256
```

## Testing

The calculator includes a comprehensive test suite covering all major functionality.

### Running Tests

```bash
# Run with virtual display (for headless environments)
xvfb-run -a python test_calculator.py

# Run directly (if you have a display)
python test_calculator.py
```

### Test Coverage
- Basic arithmetic operations
- Scientific functions (trigonometric, logarithmic, etc.)
- Memory operations
- Error handling (division by zero, invalid inputs)
- UI functionality (mode toggle, input handling)

All 32 tests pass successfully! ✅

## Project Structure

```
custom-tkinter-calculator/
├── calculator.py          # Main calculator application
├── test_calculator.py     # Comprehensive test suite
├── requirements.txt       # Python dependencies
└── README.md             # This file
```

## Technical Details

### Built With
- **Python 3.12**: Programming language
- **CustomTkinter 5.2.2**: Modern UI framework
- **tkinter**: Base GUI framework (included with Python)
- **math**: Mathematical operations

### Key Classes
- `Calculator`: Main application class inheriting from `ctk.CTk`
  - Handles all UI creation and event management
  - Manages calculator state and operations
  - Implements keyboard and button event handlers

### Architecture Highlights
- Clean separation of UI and logic
- Comprehensive error handling
- Event-driven architecture
- Modular button creation system
- Dynamic mode switching (Standard/Scientific)

## Features in Detail

### Error Handling
The calculator handles various error cases gracefully:
- Division by zero
- Invalid mathematical operations (e.g., square root of negative numbers)
- Logarithm of non-positive numbers
- Factorial of negative or non-integer numbers
- Syntax errors in expressions

### Expression Evaluation
- Uses Python's `eval()` function for expression evaluation
- Supports parentheses for complex expressions
- Handles operator precedence correctly
- Supports decimal numbers and negative numbers

### UI Design
- Color-coded buttons for easy identification:
  - Blue: Equals button
  - Red: Clear and delete buttons
  - Gray: Basic operators
  - Purple: Memory functions
  - Green: Scientific functions
  - Dark gray: Number buttons
- Responsive button grid layout
- Large, readable display
- Memory indicator shows current memory value

## Contributing

Contributions are welcome! Here are some ways you can contribute:
- Report bugs
- Suggest new features
- Submit pull requests
- Improve documentation

## License

This project is open source and available under the MIT License.

## Acknowledgments

- Built with [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter) by Tom Schimansky
- Inspired by modern calculator designs
- Thanks to the Python community for excellent documentation

## Future Enhancements

Potential features for future versions:
- Radian/Degree mode toggle for trigonometric functions
- Hyperbolic functions (sinh, cosh, tanh)
- Statistical functions (mean, median, standard deviation)
- Unit conversions
- Equation solver
- Graphing capabilities
- Export history to file
- Custom color themes
- Resizable window

## Contact

For questions, issues, or suggestions, please open an issue on GitHub.

---

Made with ❤️ using Python and CustomTkinter