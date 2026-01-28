# py++ Language Documentation

## Getting Started

py++ is a Python-like programming language designed for speed and simplicity. It combines Python's readability with performance approaching C++.

### Installation

```bash
# Copy the py-plus-plus folder to your system
cd py-plus-plus
python run.py examples/basic.pypp
```

### Your First Program

Create `hello.pypp`:

```pypp
print("Hello, py++!");
```

Run it:

```bash
python run.py hello.pypp
```

## Language Syntax

### Variables

Declare variables with `let`:

```pypp
let name = "Alice";
let age = 30;
let score = 95.5;
let active = true;
```

**With type annotations (optional)**:

```pypp
let name: string = "Alice";
let age: int = 30;
let score: float = 95.5;
let active: bool = true;
```

### Functions

Define functions with `fn`:

```pypp
fn greet(name) {
    print("Hello, " + name);
}

greet("Alice");
```

**With type annotations**:

```pypp
fn add(a: int, b: int) -> int {
    return a + b;
}

let result = add(5, 3);  // result = 8
```

### Control Flow

**If/Else**:

```pypp
if (x > 10) {
    print("x is large");
} else {
    print("x is small");
}
```

**For Loops**:

```pypp
for (let i = 0; i < 10; i = i + 1) {
    print(i);
}
```

**While Loops**:

```pypp
let count = 0;
while (count < 5) {
    print(count);
    count = count + 1;
}
```

**Break and Continue**:

```pypp
for (let i = 0; i < 10; i = i + 1) {
    if (i == 5) break;
    if (i == 2) continue;
    print(i);
}
```

## Operators

**Arithmetic**: `+`, `-`, `*`, `/`, `%`

**Comparison**: `==`, `!=`, `<`, `<=`, `>`, `>=`

**Logical**: `&&` (AND), `||` (OR), `!` (NOT)

**Assignment**: `=`

## Built-in Functions

- `print(...)` — Print to console
- `len(obj)` — Length of string
- `range(n)` — Generate numbers 0 to n-1
- `int(x)` — Convert to integer
- `float(x)` — Convert to float
- `str(x)` — Convert to string
- `bool(x)` — Convert to boolean
- `type(x)` — Get type name
- `time()` — Get current timestamp
- `sleep(seconds)` — Sleep for seconds
- `random()` — Random float 0-1
- `randint(a, b)` — Random integer [a, b]

## Modules

Import modules with `import`:

```pypp
import math;

print(math.abs(-5));
print(math.square(4));
```

### Available Modules

**math**: `abs()`, `min()`, `max()`, `square()`, `cube()`, `power()`

**string**: `length()`, `concat()`, `repeat()`

**sys**: `exit()`, `print_version()`, `info()`

## Examples

### Fibonacci Sequence

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

print(add(10, 5));   // 15
print(sub(10, 5));   // 5
print(mul(10, 5));   // 50
print(div(10, 5));   // 2
```

## Command-Line Interface

### Run a file

```bash
python run.py program.pypp
```

Or use the CLI:

```bash
pypp run program.pypp
```

### Create a new project

```bash
pypp new my_project
cd my_project
pypp run src/main.pypp
```

### Build a project

```bash
pypp build .
```

### Show version

```bash
pypp version
```

## Error Handling

py++ will report syntax and runtime errors with line and column information:

```
Error: Unexpected token at 5:10
```

Common errors:

- **Undefined variable**: Variable used without declaration
- **Type mismatch**: Wrong type for operation
- **Division by zero**: Dividing by zero
- **Invalid syntax**: Unexpected character or token

## Tips & Best Practices

1. **Use type annotations** for documentation and early error detection
2. **Write small functions** for clarity and reusability
3. **Use meaningful names** for variables and functions
4. **Comment complex logic** with `// comment`
5. **Test incrementally** as you develop
6. **Use the CLI** for larger projects

## Advanced Features

### Optional Typing

Mix typed and untyped code:

```pypp
fn process(data) {  // dynamic
    return transform(data);
}

fn transform(x: int) -> int {  // typed
    return x * 2;
}
```

### Closures

Functions capture their defining scope:

```pypp
fn make_adder(x) {
    fn adder(y) {
        return x + y;
    }
    return adder;
}

let add5 = make_adder(5);
print(add5(3));  // 8
```

## Limitations & Future Plans

**Current (Phase 1-6)**:
- Interpreted only (Phase 7 adds bytecode VM)
- Dynamic arrays/objects coming soon
- No package manager yet (Phase 8)
- No async/concurrency (Phase 9+)

**Planned**:
- Bytecode compilation for 10-50x speedup
- Native C/C++ FFI
- Pattern matching
- Generics
- IDE support (VS Code extension)
- Community package registry

## Getting Help

- Check `examples/` folder for sample code
- Review the main roadmap documentation
- Examine project templates in `projects/`
- Run tests: `python -m pytest tests/`

Enjoy building with py++!
