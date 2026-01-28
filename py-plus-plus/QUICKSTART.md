# py++ Quick Reference Guide

## Installation & Running

```bash
# Navigate to project
cd py-plus-plus

# Run a program
python run.py program.pypp

# Or use CLI
python pypp_cli.py run program.pypp

# Show version
python pypp_cli.py version
```

---

## Syntax Quick Reference

### Variables
```pypp
let x = 10;
let name = "Alice";
let pi: float = 3.14;
let active: bool = true;
```

### Functions
```pypp
fn add(a, b) {
    return a + b;
}

fn multiply(x: int, y: int) -> int {
    return x * y;
}

// Call functions
print(add(5, 3));
```

### Control Flow
```pypp
// If statement
if (x > 0) {
    print("positive");
} else {
    print("non-positive");
}

// For loop
for (let i = 0; i < 10; i = i + 1) {
    print(i);
}

// While loop
while (count < 5) {
    print(count);
    count = count + 1;
}

// Break and continue
for (let i = 0; i < 10; i = i + 1) {
    if (i == 5) break;
    if (i == 2) continue;
    print(i);
}
```

### Operators
```pypp
// Arithmetic
5 + 3    // Addition
5 - 3    // Subtraction
5 * 3    // Multiplication
5 / 3    // Division
5 % 3    // Modulo

// Comparison
x == y   // Equal
x != y   // Not equal
x < y    // Less than
x <= y   // Less or equal
x > y    // Greater than
x >= y   // Greater or equal

// Logical
x && y   // AND
x || y   // OR
!x       // NOT
```

### Comments
```pypp
// This is a comment
let x = 5; // Inline comment
```

### Modules
```pypp
import math;
import string;
import sys;

// Use module functions
print(math.square(5));
print(string.length("hello"));
```

---

## Built-in Functions

```pypp
print(x)        // Print output
len(s)          // Length of string
range(n)        // Numbers 0 to n-1
int(x)          // Convert to integer
float(x)        // Convert to float
str(x)          // Convert to string
bool(x)         // Convert to boolean
type(x)         // Get type name
time()          // Current timestamp
sleep(s)        // Sleep for s seconds
random()        // Random 0.0-1.0
randint(a, b)   // Random integer [a, b]
```

---

## Standard Library Modules

### math module
```pypp
import math;

math.abs(-5)        // 5
math.min(3, 7)      // 3
math.max(3, 7)      // 7
math.square(4)      // 16
math.cube(3)        // 27
math.power(2, 8)    // 256
```

### string module
```pypp
import string;

string.length("hello")      // 5
string.concat("a", "b")     // "ab"
string.repeat("x", 3)       // "xxx"
```

### sys module
```pypp
import sys;

sys.print_version()   // Print py++ version
sys.info()            // Print info
```

---

## Examples

### Hello World
```pypp
print("Hello, py++!");
```

### Fibonacci
```pypp
fn fib(n: int) -> int {
    if (n <= 1) return n;
    return fib(n - 1) + fib(n - 2);
}

for (let i = 0; i < 10; i = i + 1) {
    print(fib(i));
}
```

### Calculator
```pypp
fn add(a, b) { return a + b; }
fn sub(a, b) { return a - b; }
fn mul(a, b) { return a * b; }
fn div(a, b) { return a / b; }

let x = 100;
let y = 25;

print(add(x, y));   // 125
print(sub(x, y));   // 75
print(mul(x, y));   // 2500
print(div(x, y));   // 4.0
```

### Loop Examples
```pypp
// Count to 10
for (let i = 1; i <= 10; i = i + 1) {
    print(i);
}

// Process list
for (let i = 0; i < len(items); i = i + 1) {
    print(items[i]);  // Note: Array indexing coming soon
}

// Skip and break
for (let i = 0; i < 10; i = i + 1) {
    if (i == 5) break;      // Exit loop
    if (i == 2) continue;   // Skip to next
    print(i);
}
```

---

## Tips & Best Practices

1. **Use type annotations** for clarity:
   ```pypp
   fn process(data: string) -> int {
       return len(data);
   }
   ```

2. **Write small functions** for reusability:
   ```pypp
   fn double(x) { return x * 2; }
   fn triple(x) { return x * 3; }
   ```

3. **Use meaningful names**:
   ```pypp
   let total_price = price * quantity;  // Good
   let x = p * q;                       // Avoid
   ```

4. **Comment complex logic**:
   ```pypp
   // Calculate compound interest
   let result = principal * (1 + rate) ^ years;
   ```

5. **Test incrementally**:
   ```pypp
   let x = 10;
   print(x);  // Verify value
   ```

---

## Common Patterns

### Factorial
```pypp
fn factorial(n) {
    if (n <= 1) return 1;
    return n * factorial(n - 1);
}
```

### Sum of Numbers
```pypp
fn sum_to(n) {
    let total = 0;
    for (let i = 1; i <= n; i = i + 1) {
        total = total + i;
    }
    return total;
}
```

### Check if Prime
```pypp
fn is_prime(n) {
    if (n < 2) return false;
    for (let i = 2; i < n; i = i + 1) {
        if (n % i == 0) return false;
    }
    return true;
}
```

### String Building
```pypp
let message = "";
message = message + "Hello";
message = message + " ";
message = message + "World";
print(message);  // Hello World
```

---

## Debugging

### Print Debugging
```pypp
let x = 10;
print("x = " + str(x));  // Check values

fn test() {
    print("Entering test function");
    // ... code ...
    print("Exiting test function");
}
```

### Type Checking
```pypp
print(type(x));    // Get type name
print(type(5));    // int
print(type("hi")); // str
```

### Error Messages
If you get an error, check:
1. Syntax: Missing semicolons, braces, parentheses?
2. Variables: Declared before use?
3. Functions: Correct number of arguments?
4. Types: Using correct operations for types?

---

## Useful Files

```
py-plus-plus/
├── examples/          # Working example programs
│   ├── basic.pypp
│   ├── fibonacci.pypp
│   ├── control_flow.pypp
│   ├── math.pypp
│   └── calculator.pypp
├── projects/          # Template projects
│   ├── hello/
│   └── calculator/
├── docs/              # Documentation
│   ├── guide.md      # Complete language guide
│   └── api.md        # API reference
└── stdlib/            # Standard library modules
    ├── math.pypp
    ├── string.pypp
    └── sys.pypp
```

---

## CLI Commands

```bash
# Run a file
pypp run program.pypp

# Create new project
pypp new my_app
cd my_app
pypp run src/main.pypp

# Build project
pypp build .

# Show version
pypp version

# Show help
pypp help
```

---

## Next Steps

1. **Run examples**: `python run.py examples/fibonacci.pypp`
2. **Create program**: Write your first `.pypp` file
3. **Read guide**: `docs/guide.md` for complete syntax
4. **Check API**: `docs/api.md` for all functions
5. **Explore projects**: See working examples in `projects/`

---

## Common Errors & Solutions

| Error | Cause | Solution |
|-------|-------|----------|
| `Undefined variable: x` | Variable not declared | Use `let x = value;` |
| `Expected SEMICOLON` | Missing semicolon | Add `;` at end of statement |
| `Function expects N args` | Wrong number of arguments | Check function definition |
| `Cannot divide by zero` | Division by 0 | Check divisor is not 0 |
| `Unexpected token` | Syntax error | Check braces, parentheses |

---

## Learn More

- **Language Guide**: [docs/guide.md](docs/guide.md)
- **API Reference**: [docs/api.md](docs/api.md)
- **Complete Roadmap**: [../PYpp_COMPLETE_ROADMAP.md](../PYpp_COMPLETE_ROADMAP.md)
- **Build Summary**: [BUILD_SUMMARY.md](BUILD_SUMMARY.md)

---

**Happy coding with py++!** 🚀
