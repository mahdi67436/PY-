# py++ Programming Language

A Python-like programming language with C++ speed.

## Overview

**py++** combines the simplicity and readability of Python with performance approaching C++. It features:

- **Python-like syntax**: Familiar, beginner-friendly syntax
- **Curly braces** for explicit scoping (C/C++ style)
- **Optional static typing** for safety and optimization
- **Minimal keywords**: Easy to learn and remember
- **Fast execution**: Bytecode VM (Phase 7) for 10-50x speedup
- **Modules and packages**: Built-in import system
- **Standard library**: Common utilities (math, string, sys)
- **CLI tools**: Professional command-line interface
- **Full project support**: Scaffolding, building, deployment

## Quick Start

### Installation

```bash
# Clone or download the repository
cd py-plus-plus

# Install dependencies (if any)
pip install -e .
```

### Run Your First Program

```bash
# Basic example
python run.py examples/basic.pypp

# Or use the CLI
pypp run examples/basic.pypp
```

### Create a Project

```bash
# Create new project
pypp new my_project
cd my_project

# Run the project
pypp run src/main.pypp

# Build the project
pypp build .
```

## Language Syntax

### Variables

```pypp
let name = "Alice";
let age = 30;
let score: float = 95.5;
```

### Functions

```pypp
fn greet(name: string) {
    print("Hello, " + name);
}

greet("World");
```

### Control Flow

```pypp
if (x > 0) {
    print("positive");
} else {
    print("non-positive");
}

for (let i = 0; i < 10; i = i + 1) {
    print(i);
}

while (condition) {
    break;  // or continue
}
```

### Modules

```pypp
import math;

let result = math.square(5);  // 25
```

## Project Structure

```
py-plus-plus/
├── src/                     # Core interpreter
│   ├── __init__.py
│   ├── lexer.py            # Tokenizer
│   ├── parser.py           # AST builder
│   ├── ast_nodes.py        # AST definitions
│   ├── evaluator.py        # Runtime
│   ├── builtins.py         # Built-in functions
│   ├── errors.py           # Error classes
│   └── module_loader.py    # Module system
├── stdlib/                 # Standard library
│   ├── math.pypp
│   ├── string.pypp
│   └── sys.pypp
├── examples/               # Example programs
│   ├── basic.pypp
│   ├── fibonacci.pypp
│   ├── control_flow.pypp
│   ├── math.pypp
│   └── calculator.pypp
├── projects/               # Template projects
│   ├── hello/
│   └── calculator/
├── tests/                  # Test suite
│   ├── test_lexer.py
│   ├── test_parser.py
│   └── test_evaluator.py
├── docs/                   # Documentation
│   ├── guide.md           # Language guide
│   └── api.md             # API reference
├── interpreter.py         # Main interpreter
├── pypp_cli.py           # Command-line interface
├── run.py                # Simple runner
├── setup.py              # Distribution setup
├── Makefile              # Build automation
└── README.md             # This file
```

## Usage

### Run a Single File

```bash
python run.py program.pypp
```

### Use the CLI

```bash
# Run a file
pypp run program.pypp

# Create a new project
pypp new my_app
cd my_app
pypp run src/main.pypp

# Build a project
pypp build .

# Show version
pypp version
```

### Run Tests

```bash
# With pytest (recommended)
python -m pytest tests/ -v

# Or with unittest
python -m unittest discover tests

# Using make
make test
```

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

print(add(10, 5));
print(sub(10, 5));
print(mul(10, 5));
print(div(10, 5));
```

See `examples/` and `projects/` for more.

## Built-in Functions

- **I/O**: `print(...)`, `len(obj)`
- **Type Conversion**: `int(x)`, `float(x)`, `str(x)`, `bool(x)`, `type(x)`
- **Utilities**: `range(n)`, `time()`, `sleep(s)`, `random()`, `randint(a, b)`

## Standard Library

### math module

```pypp
import math;
math.abs(-5)      // 5
math.min(3, 7)    // 3
math.max(3, 7)    // 7
math.square(4)    // 16
math.cube(3)      // 27
math.power(2, 8)  // 256
```

### string module

```pypp
import string;
string.length("hello")    // 5
string.concat("a", "b")   // "ab"
string.repeat("x", 3)     // "xxx"
```

### sys module

```pypp
import sys;
sys.print_version()
sys.info()
```

## Architecture

**Phase 1-2**: Lexer → Parser → AST → Evaluator (tree-walking interpreter)

**Phase 3-4**: Module system, standard library

**Phase 5**: Optional static typing with runtime checking

**Phase 6**: CLI tools and project structure

**Phase 7**: Bytecode compiler and VM (planned for 10-50x speedup)

**Phase 8+**: Package management, native extensions, async

## Development

### Running Examples

```bash
make examples
```

### Quick Tests

```bash
make test-quick
```

### Full Test Suite

```bash
make test
```

### Clean Build Artifacts

```bash
make clean
```

## Roadmap

- [x] Phase 1: Minimal interpreter
- [x] Phase 2: Modular structure
- [x] Phase 3: Module system
- [x] Phase 4: Standard library
- [x] Phase 5: Type system
- [x] Phase 6: CLI & projects
- [ ] Phase 7: Bytecode VM (in progress)
- [ ] Phase 8: Package management
- [ ] Phase 9: Native extensions
- [ ] Phase 10: Async/concurrency

## Documentation

- [Language Guide](docs/guide.md) — Syntax and features
- [API Reference](docs/api.md) — Module and function reference
- [Roadmap](../PYpp_COMPLETE_ROADMAP.md) — Complete development roadmap

## Performance

Current implementation is a tree-walking interpreter. Performance characteristics:

- **Development**: Instant feedback, ideal for learning
- **Scripts**: Suitable for automation and small programs
- **Production**: Phase 7 bytecode VM will provide 10-50x speedup

## Contributing

Contributions welcome! Areas for improvement:

- More stdlib modules
- Performance optimizations
- Error messages
- Documentation
- Examples

## License

MIT License - See LICENSE file

## Support

For issues, questions, or suggestions:

1. Check [Language Guide](docs/guide.md)
2. Review [examples/](examples/) and [projects/](projects/)
3. Examine the [complete roadmap](../PYpp_COMPLETE_ROADMAP.md)
4. Run tests to verify your environment

---

**py++**: Making fast programming fun!

Start with Phase 1 and scale up as needed. The complete architecture supports growth from scripts to production applications.
