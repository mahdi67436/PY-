# API Reference

## Core Modules

### `src.lexer`

Tokenizes py++ source code into tokens.

```python
from src.lexer import Lexer, TokenType

lexer = Lexer("let x = 10;")
tokens = lexer.tokenize()
```

**Classes**:
- `Lexer(source: str)` — Tokenizer
- `Token(type, value, line, col)` — Token representation
- `TokenType` — Enum of token types

### `src.parser`

Parses tokens into an Abstract Syntax Tree (AST).

```python
from src.parser import Parser

parser = Parser(tokens)
ast = parser.parse()
```

**Classes**:
- `Parser(tokens: List[Token])` — Parser

### `src.ast_nodes`

AST node definitions for py++.

**Statement nodes**:
- `Program(statements)` — Root node
- `LetStatement(name, value, type_annotation)`
- `FunctionDecl(name, params, body, return_type, param_types)`
- `ReturnStatement(value)`
- `IfStatement(condition, then_block, else_block)`
- `ForStatement(init, condition, update, body)`
- `WhileStatement(condition, body)`
- `BlockStatement(statements)`
- `BreakStatement()`
- `ContinueStatement()`
- `ImportStatement(module_name)`

**Expression nodes**:
- `BinaryOp(left, op, right)` — Binary operation
- `UnaryOp(op, operand)` — Unary operation
- `CallExpression(func, args)` — Function call
- `Identifier(name)` — Variable reference
- `Literal(value)` — Literal value
- `AssignmentExpression(target, value)` — Assignment
- `MemberAccess(obj, member)` — Member access

### `src.evaluator`

Evaluates the AST and executes the program.

```python
from src.evaluator import Evaluator

evaluator = Evaluator()
result = evaluator.eval(ast)
```

**Classes**:
- `Evaluator()` — AST interpreter
  - `eval(node)` — Evaluate AST node
  - `call_function(func, args)` — Call py++ function
  - `check_type(value, type)` — Type checking
  - `get_variable(name)` — Get variable value
  - `set_variable(name, value)` — Set variable value

### `src.module_loader`

Loads and caches py++ modules.

```python
from src.module_loader import ModuleLoader

loader = ModuleLoader(['./stdlib'])
module = loader.load_module('math', evaluator)
```

**Classes**:
- `ModuleLoader(search_paths)` — Module loader
  - `load_module(name, evaluator)` — Load a module
  - `find_module(name)` — Find module file

### `src.errors`

Error classes for py++ runtime.

**Exception classes**:
- `PyPPError` — Base exception
- `LexerError` — Tokenization error
- `ParserError` — Parsing error
- `RuntimeError` — Runtime error
- `NameError` — Undefined variable
- `TypeError` — Type mismatch
- `ReturnValue` — Control flow (return)
- `BreakException` — Control flow (break)
- `ContinueException` — Control flow (continue)

### `src.builtins`

Built-in functions available in py++.

**Functions**:
- `builtin_print(*args)` — Print to stdout
- `builtin_len(obj)` — Get length
- `builtin_range(*args)` — Generate range
- `builtin_int(x)`, `builtin_float(x)`, `builtin_str(x)`, `builtin_bool(x)` — Type conversions
- `builtin_type(obj)` — Get object type
- `builtin_time()` — Current timestamp
- `builtin_sleep(seconds)` — Sleep
- `builtin_random()` — Random float
- `builtin_randint(a, b)` — Random int

**Classes**:
- `PyPPFunction(params, body, closure)` — py++ function object

## Top-Level Functions

### `interpreter.interpret(source: str)`

Complete pipeline: source → tokens → AST → evaluation.

```python
from interpreter import interpret

result = interpret("let x = 10; print(x);")
```

## Command-Line Interface

### `pypp_cli.PyPPCLI`

Command-line interface for py++.

```python
from pypp_cli import PyPPCLI

cli = PyPPCLI()
cli.run(['run', 'program.pypp'])
```

**Methods**:
- `run_command(args)` — Execute a py++ file
- `build_command(args)` — Build a project
- `new_command(args)` — Create new project
- `version_command()` — Show version
- `help_command()` — Show help

**Usage**:

```bash
pypp run <file>              # Run a file
pypp build [project]         # Build project
pypp new <name>              # Create new project
pypp version                 # Show version
pypp help                    # Show help
```

## Examples

### Basic Interpretation

```python
from interpreter import interpret
import io
from contextlib import redirect_stdout

code = """
fn fibonacci(n) {
    if (n <= 1) return n;
    return fibonacci(n - 1) + fibonacci(n - 2);
}

for (let i = 0; i < 10; i = i + 1) {
    print(fibonacci(i));
}
"""

f = io.StringIO()
with redirect_stdout(f):
    interpret(code)
print(f.getvalue())
```

### Custom Module Loading

```python
from interpreter import interpret
from src.module_loader import ModuleLoader

code = """
import math;
print(math.square(5));
"""

# Set up evaluator with custom module paths
from src.evaluator import Evaluator
from src.lexer import Lexer
from src.parser import Parser

lexer = Lexer(code)
tokens = lexer.tokenize()
parser = Parser(tokens)
ast = parser.parse()

evaluator = Evaluator()
evaluator.module_loader = ModuleLoader(['./stdlib', './custom_modules'])
evaluator.eval(ast)
```

### Testing Integration

```python
import unittest
from interpreter import interpret
import io
from contextlib import redirect_stdout

class TestProgram(unittest.TestCase):
    def test_addition(self):
        code = "let x = 5 + 3; print(x);"
        f = io.StringIO()
        with redirect_stdout(f):
            interpret(code)
        self.assertIn("8", f.getvalue())
```

## Performance Notes

- **Interpreter**: Tree-walking interpreter, suitable for scripts and development
- **Bytecode VM** (Phase 7): Planned 10-50x speedup for production
- **Module caching**: Loaded modules are cached to avoid re-execution
- **Scope chain**: Variables searched from innermost to outermost scope

## Future API Additions

- Bytecode compiler API
- VM execution API
- Type system API for static checking
- FFI for C/C++ integration
- Package manager API
