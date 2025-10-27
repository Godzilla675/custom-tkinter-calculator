# Advanced Scientific Calculator - Enhanced Edition

A professional-grade scientific calculator with graphing capabilities, equation solving, matrix operations, and unit conversions. Built with CustomTkinter for a modern, beautiful interface.

![Calculator](https://github.com/user-attachments/assets/7309193d-63c5-4ac1-bff2-35c8bd3cc24b)

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![CustomTkinter](https://img.shields.io/badge/CustomTkinter-5.2+-green.svg)](https://github.com/TomSchimansky/CustomTkinter)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

## 🚀 New Features (Enhanced Version)

### Tabbed Interface
- **5 Different Modes**: Calculator, Graphing, Equation Solver, Matrix Operations, and Unit Conversions
- **Modern UI**: Enhanced styling with better color schemes and layout
- **Real-time History**: Live display of recent calculations

### Calculator Tab
- **Extended Scientific Functions**:
  - Trigonometric: sin, cos, tan, asin, acos, atan
  - Logarithmic: log (base 10) and ln (natural log)
  - Exponential: e^x
  - Power: x², x^y, √x, ∛x
  - Other: factorial (x!), reciprocal (1/x), percentage (%)
  - Constants: π and e
- **Angle Mode**: Toggle between degrees and radians
- **Memory Functions**: MC, MR, M+, M- with visual indicator
- **Dual Display**: Main display + expression display

### Graphing Tab  
- **2D Function Plotting**: Plot any mathematical function
- **Customizable Range**: Set X-axis min and max values
- **Multiple Functions**: Add multiple functions to the same graph
- **Interactive Controls**: Plot, Clear, and Add Function buttons
- **Professional Graphs**: Using matplotlib for high-quality visualization

### Equation Solver Tab
- **Solve Equations**: Algebraic, Quadratic, and Polynomial equations
- **Expression Operations**:
  - **Expand**: Expand algebraic expressions
  - **Factor**: Factor polynomials
  - **Differentiate**: Calculate derivatives
  - **Integrate**: Calculate integrals (indefinite)
- **Simplify**: Simplify complex expressions
- **Step-by-step Solutions**: Clear display of solutions

### Matrix Operations Tab
- **Matrix Arithmetic**: Addition, Subtraction, Multiplication
- **Matrix Properties**:
  - Transpose
  - Determinant
  - Inverse
- **Easy Input Format**: rows separated by `;` columns by `,`
- **Example**: `1,2,3;4,5,6;7,8,9`

### Unit Conversions Tab
- **Length**: meter, kilometer, mile, foot, inch, etc.
- **Weight**: kilogram, gram, pound, ounce, ton, etc.
- **Temperature**: Celsius, Fahrenheit, Kelvin
- **Area**: square meter, acre, hectare, etc.
- **Real-time Conversion**: Instant results

## 📋 Features Summary

| Feature | Description |
|---------|-------------|
| 🧮 Basic Operations | +, -, ×, ÷, %, parentheses |
| 🔬 Scientific Functions | 20+ mathematical functions |
| 📊 Graphing | Plot mathematical functions with matplotlib |
| ⚖️ Equation Solver | Solve algebraic equations, simplify, factor, differentiate, integrate |
| 🔢 Matrix Operations | Full matrix support (add, multiply, transpose, determinant, inverse) |
| 🔄 Unit Conversions | Convert between multiple units |
| 💾 Memory | M+, M-, MR, MC |
| 📜 History | Last 50 calculations with live display |
| 🎨 Themes | Light/Dark mode toggle |
| ⌨️ Keyboard Support | Full keyboard input |
| 🔐 Security | Safe expression evaluation (no eval vulnerabilities) |

## 🔧 Installation

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

## 📖 Usage Guide

### Basic Calculator
1. Click number buttons or type on keyboard
2. Use operator buttons or keyboard shortcuts
3. Press `=` or Enter to calculate
4. Press `C` or Escape to clear

### Graphing Functions
1. Go to "Graphing" tab
2. Enter a function (e.g., `sin(x)`, `x**2`, `exp(x)`)
3. Set X range (from/to)
4. Click "Plot Function"
5. Use "Add Function" to plot multiple functions
6. Click "Clear Graph" to reset

### Solving Equations
1. Go to "Equation Solver" tab
2. Enter equation (e.g., `x**2 - 4*x + 4 = 0`)
3. Select equation type
4. Click "Solve Equation"
5. Use operation buttons for expand, factor, differentiate, or integrate

### Matrix Operations
1. Go to "Matrix" tab
2. Enter matrices in format: `1,2,3;4,5,6;7,8,9`
3. Click desired operation button
4. View result

### Unit Conversions
1. Go to "Conversions" tab
2. Select category (Length, Weight, Temperature, Area)
3. Enter value and select units
4. Click "Convert"

## ⌨️ Keyboard Shortcuts

| Key | Action |
|-----|--------|
| 0-9 | Numbers |
| +, -, *, / | Operators |
| Enter | Calculate |
| Backspace | Delete last character |
| Escape | Clear |
| % | Percentage |
| ( ) | Parentheses |

## 🧪 Testing

The calculator includes a comprehensive test suite with 30+ tests covering all features.

### Run Tests

```bash
# With virtual display (for headless environments)
xvfb-run -a python test_enhanced_calculator.py

# Direct run (if you have a display)
python test_enhanced_calculator.py
```

### Test Coverage
✅ Safe expression evaluation (security)
✅ Basic arithmetic operations  
✅ Scientific functions (trig, log, exp)  
✅ Angle mode (degrees/radians)  
✅ Memory operations  
✅ Matrix operations (all types)  
✅ Unit conversions  
✅ Graphing functionality  
✅ Equation solver  
✅ Expression operations (expand, factor, differentiate, integrate)  
✅ UI components and tab switching  
✅ Error handling  

**All 30 tests passing! ✅**

## 📁 Project Structure

```
custom-tkinter-calculator/
├── calculator.py              # Main enhanced calculator application (1400+ lines)
├── test_enhanced_calculator.py # Comprehensive test suite (30 tests)
├── demo.py                    # Demo script
├── requirements.txt           # Python dependencies
├── .gitignore                 # Git ignore configuration
└── README.md                  # This file
```

## 🔬 Technical Details

### Built With
- **Python 3.12**: Programming language
- **CustomTkinter 5.2.2**: Modern UI framework
- **Matplotlib 3.10**: Graphing and visualization
- **NumPy 2.3**: Numerical computations and matrices
- **SymPy 1.14**: Symbolic mathematics and equation solving
- **AST Module**: Safe expression parsing (security)

### Architecture
- **Tabbed Interface**: Clean separation of functionality
- **Event-driven**: Responsive UI with callback-based interactions
- **Secure Evaluation**: Custom safe_eval() using AST parsing
- **Modular Design**: Each feature in separate methods
- **Professional UI**: Color-coded buttons, dual displays, indicators

### Security
- ✅ **No eval() vulnerabilities**: All user input parsed with AST
- ✅ **Input validation**: Expressions validated before execution
- ✅ **Whitelist approach**: Only mathematical operations allowed
- ✅ **CodeQL verified**: 0 security alerts
- ✅ **Exception handling**: Specific exception types throughout

Example of blocked malicious input:
```python
__import__('os').system('malicious_command')
# Result: ValueError - Unsupported expression ✅
```

## 📊 Performance

- **Lines of Code**: 1,400+ (main application)
- **Test Suite**: 30 comprehensive tests
- **Test Pass Rate**: 100%
- **Security Rating**: A+ (0 CodeQL alerts)
- **Features**: 40+ distinct capabilities

## 🎯 Use Cases

- **Students**: Learn mathematics with visual graphing
- **Engineers**: Quick calculations and matrix operations
- **Scientists**: Advanced functions and equation solving
- **Everyday Users**: Unit conversions and basic arithmetic
- **Developers**: Study secure expression evaluation

## 🔜 Potential Enhancements

- [ ] 3D graphing capabilities
- [ ] Parametric and polar plots
- [ ] Statistics functions (mean, median, std dev)
- [ ] Complex number support
- [ ] Programmable functions
- [ ] Export graphs and history
- [ ] Custom themes and colors
- [ ] Equation solver for systems of equations
- [ ] Numerical integration and derivatives

## 🤝 Contributing

Contributions are welcome! Areas for contribution:
- Bug fixes
- New features
- UI improvements
- Documentation
- Test coverage
- Performance optimizations

## 📄 License

This project is open source and available under the MIT License.

## 🙏 Acknowledgments

- [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter) by Tom Schimansky
- [Matplotlib](https://matplotlib.org/) for graphing
- [NumPy](https://numpy.org/) for numerical operations
- [SymPy](https://www.sympy.org/) for symbolic mathematics
- Python community for excellent documentation

## 📞 Support

For questions, issues, or suggestions:
- Open an issue on GitHub
- Check existing issues for solutions
- Review documentation and examples

---

**Made with ❤️ using Python, CustomTkinter, Matplotlib, NumPy, and SymPy**

*Transform your calculations with professional-grade tools* 🚀
