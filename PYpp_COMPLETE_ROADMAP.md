# PY++ Programming Language — Complete Roadmap

**Goal**: Build a Python-like language with C++ speed, beginner-friendly syntax, and production-ready tooling.

**Architecture Philosophy**:
- Start with Python implementation for rapid iteration
- Transition to bytecode VM for performance
- Optional static typing for speed
- Curly braces for explicit scoping
- Minimal keywords, maximum clarity

---

## PHASE 1: Minimal Prototype

**Objective**: Single-file interpreter with lexer, parser, and evaluator. Prove core concepts work.

### Folder Structure
```
py-plus-plus/
├── main.pypp          # Example py++ code
└── interpreter.py     # Complete interpreter (all-in-one)
```

### File Explanations

#### `main.pypp` — Example Program
This is a sample program written in py++ syntax to demonstrate what we're building.

```pypp
// Variables and basic operations
let x = 10;
let y = 20;
print(x + y);

// Functions
fn add(a, b) {
    return a + b;
}

print(add(5, 3));

// Conditionals
if (x > 5) {
    print("x is greater than 5");
} else {
    print("x is not greater than 5");
}

// Loops
for (let i = 0; i < 5; i = i + 1) {
    print(i);
}

// While loop
let count = 0;
while (count < 3) {
    print("count: " + count);
    count = count + 1;
}
```

#### `interpreter.py` — Complete Single-File Interpreter

```python
"""
py++ Interpreter - Phase 1: Minimal Prototype
Complete lexer, parser, and evaluator in one file.
"""

import re
import sys
from enum import Enum, auto
from typing import Any, Dict, List, Optional, Union

# ============================================================================
# TOKEN DEFINITIONS
# ============================================================================

class TokenType(Enum):
    # Literals
    NUMBER = auto()
    STRING = auto()
    BOOL = auto()
    NONE = auto()
    
    # Identifiers and keywords
    IDENTIFIER = auto()
    LET = auto()
    FN = auto()
    RETURN = auto()
    IF = auto()
    ELSE = auto()
    FOR = auto()
    WHILE = auto()
    BREAK = auto()
    CONTINUE = auto()
    TRUE = auto()
    FALSE = auto()
    
    # Operators
    PLUS = auto()
    MINUS = auto()
    STAR = auto()
    SLASH = auto()
    PERCENT = auto()
    ASSIGN = auto()
    EQ = auto()          # ==
    NE = auto()          # !=
    LT = auto()          # <
    LE = auto()          # <=
    GT = auto()          # >
    GE = auto()          # >=
    AND = auto()         # &&
    OR = auto()          # ||
    NOT = auto()         # !
    
    # Delimiters
    LPAREN = auto()
    RPAREN = auto()
    LBRACE = auto()
    RBRACE = auto()
    SEMICOLON = auto()
    COMMA = auto()
    
    # Special
    EOF = auto()
    NEWLINE = auto()

class Token:
    def __init__(self, type_: TokenType, value: Any, line: int, col: int):
        self.type = type_
        self.value = value
        self.line = line
        self.col = col
    
    def __repr__(self):
        return f"Token({self.type.name}, {self.value!r}, {self.line}, {self.col})"

# ============================================================================
# LEXER
# ============================================================================

class Lexer:
    """Tokenizes py++ source code."""
    
    KEYWORDS = {
        'let': TokenType.LET,
        'fn': TokenType.FN,
        'return': TokenType.RETURN,
        'if': TokenType.IF,
        'else': TokenType.ELSE,
        'for': TokenType.FOR,
        'while': TokenType.WHILE,
        'break': TokenType.BREAK,
        'continue': TokenType.CONTINUE,
        'true': TokenType.TRUE,
        'false': TokenType.FALSE,
        'null': TokenType.NONE,
    }
    
    def __init__(self, source: str):
        self.source = source
        self.pos = 0
        self.line = 1
        self.col = 1
        self.tokens: List[Token] = []
    
    def error(self, msg: str):
        raise SyntaxError(f"Lexer error at {self.line}:{self.col}: {msg}")
    
    def peek(self, offset=0) -> Optional[str]:
        idx = self.pos + offset
        return self.source[idx] if idx < len(self.source) else None
    
    def advance(self):
        if self.pos < len(self.source):
            if self.source[self.pos] == '\n':
                self.line += 1
                self.col = 1
            else:
                self.col += 1
            self.pos += 1
    
    def skip_whitespace(self):
        while self.peek() and self.peek() in ' \t\r\n':
            self.advance()
    
    def skip_comment(self):
        if self.peek() == '/' and self.peek(1) == '/':
            while self.peek() and self.peek() != '\n':
                self.advance()
            self.advance()  # consume newline
    
    def read_number(self) -> Token:
        start_line, start_col = self.line, self.col
        num_str = ''
        while self.peek() and (self.peek().isdigit() or self.peek() == '.'):
            num_str += self.peek()
            self.advance()
        
        if '.' in num_str:
            return Token(TokenType.NUMBER, float(num_str), start_line, start_col)
        else:
            return Token(TokenType.NUMBER, int(num_str), start_line, start_col)
    
    def read_string(self, quote_char: str) -> Token:
        start_line, start_col = self.line, self.col
        self.advance()  # consume opening quote
        s = ''
        while self.peek() and self.peek() != quote_char:
            if self.peek() == '\\':
                self.advance()
                escape_char = self.peek()
                if escape_char == 'n':
                    s += '\n'
                elif escape_char == 't':
                    s += '\t'
                elif escape_char == 'r':
                    s += '\r'
                elif escape_char == '\\':
                    s += '\\'
                elif escape_char == quote_char:
                    s += quote_char
                else:
                    s += escape_char or ''
                self.advance()
            else:
                s += self.peek()
                self.advance()
        
        if not self.peek():
            self.error(f"Unterminated string starting at {start_line}:{start_col}")
        self.advance()  # consume closing quote
        return Token(TokenType.STRING, s, start_line, start_col)
    
    def read_identifier(self) -> Token:
        start_line, start_col = self.line, self.col
        ident = ''
        while self.peek() and (self.peek().isalnum() or self.peek() == '_'):
            ident += self.peek()
            self.advance()
        
        token_type = self.KEYWORDS.get(ident, TokenType.IDENTIFIER)
        value = True if token_type == TokenType.TRUE else (False if token_type == TokenType.FALSE else ident)
        return Token(token_type, value, start_line, start_col)
    
    def tokenize(self) -> List[Token]:
        while self.pos < len(self.source):
            self.skip_whitespace()
            if self.pos >= len(self.source):
                break
            
            # Comments
            if self.peek() == '/' and self.peek(1) == '/':
                self.skip_comment()
                continue
            
            current = self.peek()
            
            # Numbers
            if current.isdigit():
                self.tokens.append(self.read_number())
            
            # Strings
            elif current in ('"', "'"):
                self.tokens.append(self.read_string(current))
            
            # Identifiers and keywords
            elif current.isalpha() or current == '_':
                self.tokens.append(self.read_identifier())
            
            # Operators and delimiters
            elif current == '+':
                self.tokens.append(Token(TokenType.PLUS, '+', self.line, self.col))
                self.advance()
            elif current == '-':
                self.tokens.append(Token(TokenType.MINUS, '-', self.line, self.col))
                self.advance()
            elif current == '*':
                self.tokens.append(Token(TokenType.STAR, '*', self.line, self.col))
                self.advance()
            elif current == '/':
                self.tokens.append(Token(TokenType.SLASH, '/', self.line, self.col))
                self.advance()
            elif current == '%':
                self.tokens.append(Token(TokenType.PERCENT, '%', self.line, self.col))
                self.advance()
            elif current == '=' and self.peek(1) == '=':
                self.tokens.append(Token(TokenType.EQ, '==', self.line, self.col))
                self.advance()
                self.advance()
            elif current == '!' and self.peek(1) == '=':
                self.tokens.append(Token(TokenType.NE, '!=', self.line, self.col))
                self.advance()
                self.advance()
            elif current == '<' and self.peek(1) == '=':
                self.tokens.append(Token(TokenType.LE, '<=', self.line, self.col))
                self.advance()
                self.advance()
            elif current == '<':
                self.tokens.append(Token(TokenType.LT, '<', self.line, self.col))
                self.advance()
            elif current == '>' and self.peek(1) == '=':
                self.tokens.append(Token(TokenType.GE, '>=', self.line, self.col))
                self.advance()
                self.advance()
            elif current == '>':
                self.tokens.append(Token(TokenType.GT, '>', self.line, self.col))
                self.advance()
            elif current == '&' and self.peek(1) == '&':
                self.tokens.append(Token(TokenType.AND, '&&', self.line, self.col))
                self.advance()
                self.advance()
            elif current == '|' and self.peek(1) == '|':
                self.tokens.append(Token(TokenType.OR, '||', self.line, self.col))
                self.advance()
                self.advance()
            elif current == '!':
                self.tokens.append(Token(TokenType.NOT, '!', self.line, self.col))
                self.advance()
            elif current == '=':
                self.tokens.append(Token(TokenType.ASSIGN, '=', self.line, self.col))
                self.advance()
            elif current == '(':
                self.tokens.append(Token(TokenType.LPAREN, '(', self.line, self.col))
                self.advance()
            elif current == ')':
                self.tokens.append(Token(TokenType.RPAREN, ')', self.line, self.col))
                self.advance()
            elif current == '{':
                self.tokens.append(Token(TokenType.LBRACE, '{', self.line, self.col))
                self.advance()
            elif current == '}':
                self.tokens.append(Token(TokenType.RBRACE, '}', self.line, self.col))
                self.advance()
            elif current == ';':
                self.tokens.append(Token(TokenType.SEMICOLON, ';', self.line, self.col))
                self.advance()
            elif current == ',':
                self.tokens.append(Token(TokenType.COMMA, ',', self.line, self.col))
                self.advance()
            else:
                self.error(f"Unexpected character: {current!r}")
        
        self.tokens.append(Token(TokenType.EOF, None, self.line, self.col))
        return self.tokens

# ============================================================================
# AST NODE DEFINITIONS
# ============================================================================

class ASTNode:
    pass

class Program(ASTNode):
    def __init__(self, statements: List):
        self.statements = statements

class LetStatement(ASTNode):
    def __init__(self, name: str, value: ASTNode):
        self.name = name
        self.value = value

class FunctionDecl(ASTNode):
    def __init__(self, name: str, params: List[str], body: 'BlockStatement'):
        self.name = name
        self.params = params
        self.body = body

class ReturnStatement(ASTNode):
    def __init__(self, value: Optional[ASTNode]):
        self.value = value

class IfStatement(ASTNode):
    def __init__(self, condition: ASTNode, then_block: 'BlockStatement', else_block: Optional['BlockStatement']):
        self.condition = condition
        self.then_block = then_block
        self.else_block = else_block

class ForStatement(ASTNode):
    def __init__(self, init: Optional[ASTNode], condition: Optional[ASTNode], update: Optional[ASTNode], body: 'BlockStatement'):
        self.init = init
        self.condition = condition
        self.update = update
        self.body = body

class WhileStatement(ASTNode):
    def __init__(self, condition: ASTNode, body: 'BlockStatement'):
        self.condition = condition
        self.body = body

class BlockStatement(ASTNode):
    def __init__(self, statements: List):
        self.statements = statements

class ExpressionStatement(ASTNode):
    def __init__(self, expression: ASTNode):
        self.expression = expression

class BinaryOp(ASTNode):
    def __init__(self, left: ASTNode, op: str, right: ASTNode):
        self.left = left
        self.op = op
        self.right = right

class UnaryOp(ASTNode):
    def __init__(self, op: str, operand: ASTNode):
        self.op = op
        self.operand = operand

class CallExpression(ASTNode):
    def __init__(self, func: ASTNode, args: List[ASTNode]):
        self.func = func
        self.args = args

class Identifier(ASTNode):
    def __init__(self, name: str):
        self.name = name

class Literal(ASTNode):
    def __init__(self, value: Any):
        self.value = value

class AssignmentExpression(ASTNode):
    def __init__(self, target: str, value: ASTNode):
        self.target = target
        self.value = value

class BreakStatement(ASTNode):
    pass

class ContinueStatement(ASTNode):
    pass

# ============================================================================
# PARSER
# ============================================================================

class Parser:
    """Parses tokens into an AST."""
    
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.pos = 0
    
    def error(self, msg: str):
        token = self.current_token()
        raise SyntaxError(f"Parser error at {token.line}:{token.col}: {msg}")
    
    def current_token(self) -> Token:
        return self.tokens[self.pos] if self.pos < len(self.tokens) else self.tokens[-1]
    
    def peek_token(self, offset=0) -> Token:
        idx = self.pos + offset
        return self.tokens[idx] if idx < len(self.tokens) else self.tokens[-1]
    
    def advance(self):
        self.pos += 1
    
    def expect(self, token_type: TokenType) -> Token:
        token = self.current_token()
        if token.type != token_type:
            self.error(f"Expected {token_type.name}, got {token.type.name}")
        self.advance()
        return token
    
    def match(self, *token_types: TokenType) -> bool:
        return self.current_token().type in token_types
    
    def consume(self, *token_types: TokenType) -> Optional[Token]:
        if self.match(*token_types):
            token = self.current_token()
            self.advance()
            return token
        return None
    
    def parse(self) -> Program:
        statements = []
        while not self.match(TokenType.EOF):
            stmt = self.parse_statement()
            if stmt:
                statements.append(stmt)
        return Program(statements)
    
    def parse_statement(self) -> Optional[ASTNode]:
        if self.match(TokenType.LET):
            return self.parse_let_statement()
        elif self.match(TokenType.FN):
            return self.parse_function_decl()
        elif self.match(TokenType.RETURN):
            return self.parse_return_statement()
        elif self.match(TokenType.IF):
            return self.parse_if_statement()
        elif self.match(TokenType.FOR):
            return self.parse_for_statement()
        elif self.match(TokenType.WHILE):
            return self.parse_while_statement()
        elif self.match(TokenType.LBRACE):
            return self.parse_block_statement()
        elif self.match(TokenType.BREAK):
            self.advance()
            self.consume(TokenType.SEMICOLON)
            return BreakStatement()
        elif self.match(TokenType.CONTINUE):
            self.advance()
            self.consume(TokenType.SEMICOLON)
            return ContinueStatement()
        else:
            return self.parse_expression_statement()
    
    def parse_let_statement(self) -> LetStatement:
        self.expect(TokenType.LET)
        name = self.expect(TokenType.IDENTIFIER).value
        self.expect(TokenType.ASSIGN)
        value = self.parse_expression()
        self.consume(TokenType.SEMICOLON)
        return LetStatement(name, value)
    
    def parse_function_decl(self) -> FunctionDecl:
        self.expect(TokenType.FN)
        name = self.expect(TokenType.IDENTIFIER).value
        self.expect(TokenType.LPAREN)
        params = []
        if not self.match(TokenType.RPAREN):
            params.append(self.expect(TokenType.IDENTIFIER).value)
            while self.consume(TokenType.COMMA):
                params.append(self.expect(TokenType.IDENTIFIER).value)
        self.expect(TokenType.RPAREN)
        body = self.parse_block_statement()
        return FunctionDecl(name, params, body)
    
    def parse_return_statement(self) -> ReturnStatement:
        self.expect(TokenType.RETURN)
        value = None
        if not self.match(TokenType.SEMICOLON, TokenType.RBRACE):
            value = self.parse_expression()
        self.consume(TokenType.SEMICOLON)
        return ReturnStatement(value)
    
    def parse_if_statement(self) -> IfStatement:
        self.expect(TokenType.IF)
        self.expect(TokenType.LPAREN)
        condition = self.parse_expression()
        self.expect(TokenType.RPAREN)
        then_block = self.parse_block_statement()
        else_block = None
        if self.consume(TokenType.ELSE):
            else_block = self.parse_block_statement()
        return IfStatement(condition, then_block, else_block)
    
    def parse_for_statement(self) -> ForStatement:
        self.expect(TokenType.FOR)
        self.expect(TokenType.LPAREN)
        init = None
        if self.match(TokenType.LET):
            init = self.parse_let_statement()
        else:
            init = self.parse_expression()
            self.consume(TokenType.SEMICOLON)
        
        condition = None
        if not self.match(TokenType.SEMICOLON):
            condition = self.parse_expression()
        self.expect(TokenType.SEMICOLON)
        
        update = None
        if not self.match(TokenType.RPAREN):
            update = self.parse_expression()
        self.expect(TokenType.RPAREN)
        
        body = self.parse_block_statement()
        return ForStatement(init, condition, update, body)
    
    def parse_while_statement(self) -> WhileStatement:
        self.expect(TokenType.WHILE)
        self.expect(TokenType.LPAREN)
        condition = self.parse_expression()
        self.expect(TokenType.RPAREN)
        body = self.parse_block_statement()
        return WhileStatement(condition, body)
    
    def parse_block_statement(self) -> BlockStatement:
        self.expect(TokenType.LBRACE)
        statements = []
        while not self.match(TokenType.RBRACE):
            stmt = self.parse_statement()
            if stmt:
                statements.append(stmt)
        self.expect(TokenType.RBRACE)
        return BlockStatement(statements)
    
    def parse_expression_statement(self) -> ExpressionStatement:
        expr = self.parse_expression()
        self.consume(TokenType.SEMICOLON)
        return ExpressionStatement(expr)
    
    def parse_expression(self) -> ASTNode:
        return self.parse_assignment()
    
    def parse_assignment(self) -> ASTNode:
        expr = self.parse_logical_or()
        if self.match(TokenType.ASSIGN):
            if not isinstance(expr, Identifier):
                self.error("Invalid assignment target")
            self.advance()
            value = self.parse_assignment()
            return AssignmentExpression(expr.name, value)
        return expr
    
    def parse_logical_or(self) -> ASTNode:
        left = self.parse_logical_and()
        while self.consume(TokenType.OR):
            op = self.tokens[self.pos - 1].value
            right = self.parse_logical_and()
            left = BinaryOp(left, op, right)
        return left
    
    def parse_logical_and(self) -> ASTNode:
        left = self.parse_equality()
        while self.consume(TokenType.AND):
            op = self.tokens[self.pos - 1].value
            right = self.parse_equality()
            left = BinaryOp(left, op, right)
        return left
    
    def parse_equality(self) -> ASTNode:
        left = self.parse_comparison()
        while self.consume(TokenType.EQ, TokenType.NE):
            op = self.tokens[self.pos - 1].value
            right = self.parse_comparison()
            left = BinaryOp(left, op, right)
        return left
    
    def parse_comparison(self) -> ASTNode:
        left = self.parse_additive()
        while self.consume(TokenType.LT, TokenType.LE, TokenType.GT, TokenType.GE):
            op = self.tokens[self.pos - 1].value
            right = self.parse_additive()
            left = BinaryOp(left, op, right)
        return left
    
    def parse_additive(self) -> ASTNode:
        left = self.parse_multiplicative()
        while self.consume(TokenType.PLUS, TokenType.MINUS):
            op = self.tokens[self.pos - 1].value
            right = self.parse_multiplicative()
            left = BinaryOp(left, op, right)
        return left
    
    def parse_multiplicative(self) -> ASTNode:
        left = self.parse_unary()
        while self.consume(TokenType.STAR, TokenType.SLASH, TokenType.PERCENT):
            op = self.tokens[self.pos - 1].value
            right = self.parse_unary()
            left = BinaryOp(left, op, right)
        return left
    
    def parse_unary(self) -> ASTNode:
        if self.consume(TokenType.NOT, TokenType.MINUS):
            op = self.tokens[self.pos - 1].value
            operand = self.parse_unary()
            return UnaryOp(op, operand)
        return self.parse_postfix()
    
    def parse_postfix(self) -> ASTNode:
        expr = self.parse_primary()
        while True:
            if self.consume(TokenType.LPAREN):
                args = []
                if not self.match(TokenType.RPAREN):
                    args.append(self.parse_expression())
                    while self.consume(TokenType.COMMA):
                        args.append(self.parse_expression())
                self.expect(TokenType.RPAREN)
                expr = CallExpression(expr, args)
            else:
                break
        return expr
    
    def parse_primary(self) -> ASTNode:
        if self.consume(TokenType.NUMBER):
            return Literal(self.tokens[self.pos - 1].value)
        elif self.consume(TokenType.STRING):
            return Literal(self.tokens[self.pos - 1].value)
        elif self.consume(TokenType.TRUE, TokenType.FALSE):
            return Literal(self.tokens[self.pos - 1].value)
        elif self.consume(TokenType.NONE):
            return Literal(None)
        elif self.consume(TokenType.IDENTIFIER):
            return Identifier(self.tokens[self.pos - 1].value)
        elif self.consume(TokenType.LPAREN):
            expr = self.parse_expression()
            self.expect(TokenType.RPAREN)
            return expr
        else:
            self.error(f"Unexpected token: {self.current_token().type.name}")

# ============================================================================
# RUNTIME & EVALUATOR
# ============================================================================

class ReturnValue(Exception):
    def __init__(self, value):
        self.value = value

class BreakException(Exception):
    pass

class ContinueException(Exception):
    pass

class PyPPFunction:
    def __init__(self, params: List[str], body: BlockStatement, closure: Dict[str, Any]):
        self.params = params
        self.body = body
        self.closure = closure
    
    def __repr__(self):
        return f"<function with {len(self.params)} params>"

class Evaluator:
    """Evaluates the AST."""
    
    def __init__(self):
        self.globals = {}
        self.locals_stack = [{}]
        self.setup_builtins()
    
    def setup_builtins(self):
        """Register built-in functions."""
        self.globals['print'] = self.builtin_print
        self.globals['len'] = self.builtin_len
        self.globals['range'] = self.builtin_range
        self.globals['int'] = self.builtin_int
        self.globals['float'] = self.builtin_float
        self.globals['str'] = self.builtin_str
        self.globals['bool'] = self.builtin_bool
        self.globals['type'] = self.builtin_type
    
    def builtin_print(self, *args):
        print(*args)
        return None
    
    def builtin_len(self, obj):
        return len(obj)
    
    def builtin_range(self, *args):
        return list(range(*args))
    
    def builtin_int(self, value):
        return int(value)
    
    def builtin_float(self, value):
        return float(value)
    
    def builtin_str(self, value):
        return str(value)
    
    def builtin_bool(self, value):
        return bool(value)
    
    def builtin_type(self, obj):
        return type(obj).__name__
    
    def eval(self, node: ASTNode) -> Any:
        if isinstance(node, Program):
            result = None
            for stmt in node.statements:
                result = self.eval(stmt)
            return result
        
        elif isinstance(node, LetStatement):
            value = self.eval(node.value)
            self.set_variable(node.name, value)
            return None
        
        elif isinstance(node, FunctionDecl):
            func = PyPPFunction(node.params, node.body, self.get_current_scope().copy())
            self.set_variable(node.name, func)
            return None
        
        elif isinstance(node, ReturnStatement):
            value = self.eval(node.value) if node.value else None
            raise ReturnValue(value)
        
        elif isinstance(node, IfStatement):
            condition_val = self.eval(node.condition)
            if self.is_truthy(condition_val):
                return self.eval(node.then_block)
            elif node.else_block:
                return self.eval(node.else_block)
            return None
        
        elif isinstance(node, ForStatement):
            if node.init:
                self.eval(node.init)
            
            try:
                while True:
                    if node.condition:
                        cond_val = self.eval(node.condition)
                        if not self.is_truthy(cond_val):
                            break
                    
                    try:
                        self.eval(node.body)
                    except ContinueException:
                        pass
                    
                    if node.update:
                        self.eval(node.update)
            except BreakException:
                pass
            
            return None
        
        elif isinstance(node, WhileStatement):
            try:
                while self.is_truthy(self.eval(node.condition)):
                    try:
                        self.eval(node.body)
                    except ContinueException:
                        pass
            except BreakException:
                pass
            return None
        
        elif isinstance(node, BlockStatement):
            result = None
            for stmt in node.statements:
                result = self.eval(stmt)
            return result
        
        elif isinstance(node, ExpressionStatement):
            return self.eval(node.expression)
        
        elif isinstance(node, BinaryOp):
            left = self.eval(node.left)
            right = self.eval(node.right)
            
            if node.op == '+':
                return left + right
            elif node.op == '-':
                return left - right
            elif node.op == '*':
                return left * right
            elif node.op == '/':
                return left / right
            elif node.op == '%':
                return left % right
            elif node.op == '==':
                return left == right
            elif node.op == '!=':
                return left != right
            elif node.op == '<':
                return left < right
            elif node.op == '<=':
                return left <= right
            elif node.op == '>':
                return left > right
            elif node.op == '>=':
                return left >= right
            elif node.op == '&&':
                return self.is_truthy(left) and self.is_truthy(right)
            elif node.op == '||':
                return self.is_truthy(left) or self.is_truthy(right)
        
        elif isinstance(node, UnaryOp):
            operand = self.eval(node.operand)
            if node.op == '-':
                return -operand
            elif node.op == '!':
                return not self.is_truthy(operand)
        
        elif isinstance(node, CallExpression):
            func = self.eval(node.func)
            args = [self.eval(arg) for arg in node.args]
            
            if callable(func) and not isinstance(func, PyPPFunction):
                return func(*args)
            elif isinstance(func, PyPPFunction):
                return self.call_function(func, args)
            else:
                raise TypeError(f"{func} is not callable")
        
        elif isinstance(node, Identifier):
            return self.get_variable(node.name)
        
        elif isinstance(node, Literal):
            return node.value
        
        elif isinstance(node, AssignmentExpression):
            value = self.eval(node.value)
            self.set_variable(node.target, value)
            return value
        
        elif isinstance(node, BreakStatement):
            raise BreakException()
        
        elif isinstance(node, ContinueStatement):
            raise ContinueException()
        
        else:
            raise RuntimeError(f"Unknown node type: {type(node)}")
    
    def call_function(self, func: PyPPFunction, args: List[Any]) -> Any:
        if len(args) != len(func.params):
            raise TypeError(f"Function expects {len(func.params)} args, got {len(args)}")
        
        # Create new scope for function
        new_scope = func.closure.copy()
        for param, arg in zip(func.params, args):
            new_scope[param] = arg
        
        self.locals_stack.append(new_scope)
        try:
            self.eval(func.body)
            result = None
        except ReturnValue as ret:
            result = ret.value
        finally:
            self.locals_stack.pop()
        
        return result
    
    def is_truthy(self, value: Any) -> bool:
        if value is None or value is False:
            return False
        if value == 0 or value == "" or value == []:
            return False
        return True
    
    def get_current_scope(self) -> Dict[str, Any]:
        return self.locals_stack[-1]
    
    def get_variable(self, name: str) -> Any:
        # Search from innermost scope to outermost
        for scope in reversed(self.locals_stack):
            if name in scope:
                return scope[name]
        if name in self.globals:
            return self.globals[name]
        raise NameError(f"Undefined variable: {name}")
    
    def set_variable(self, name: str, value: Any):
        # Always set in current local scope (or global if in main scope)
        if len(self.locals_stack) == 1:
            self.globals[name] = value
        else:
            self.locals_stack[-1][name] = value

# ============================================================================
# MAIN INTERPRETER FUNCTION
# ============================================================================

def interpret(source: str) -> Any:
    """Complete pipeline: source -> tokens -> AST -> evaluation."""
    lexer = Lexer(source)
    tokens = lexer.tokenize()
    
    parser = Parser(tokens)
    ast = parser.parse()
    
    evaluator = Evaluator()
    result = evaluator.eval(ast)
    
    return result

def main():
    """Read and execute a py++ file."""
    if len(sys.argv) < 2:
        print("Usage: python interpreter.py <file.pypp>")
        sys.exit(1)
    
    filepath = sys.argv[1]
    try:
        with open(filepath, 'r') as f:
            source = f.read()
        interpret(source)
    except FileNotFoundError:
        print(f"Error: File not found: {filepath}")
        sys.exit(1)
    except (SyntaxError, TypeError, NameError, RuntimeError) as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
```

### How It Works

**Lexer**: Scans the source code character-by-character, converting it into tokens (numbers, strings, keywords, operators).

**Parser**: Takes tokens and builds an Abstract Syntax Tree (AST) by recognizing patterns (statements, expressions, operators).

**Evaluator**: Traverses the AST recursively, executing operations and managing variable scopes.

### Run the Example

```bash
python interpreter.py main.pypp
```

### Design Decisions

- **No indentation dependency**: Curly braces allow explicit scoping, easier to parse, and C/C++-like familiarity.
- **Simple operator precedence**: Logical OR → AND → Equality → Comparison → Additive → Multiplicative → Unary → Postfix.
- **Scope chain**: Variables searched from innermost scope outward; allows function closures.
- **Built-in functions**: `print()`, `len()`, `range()`, type conversions for immediate usefulness.

---

## PHASE 2: Core Language Structure

**Objective**: Split the monolithic interpreter into modules for easier extension and maintenance.

### Folder Structure

```
py-plus-plus/
├── src/
│   ├── __init__.py
│   ├── lexer.py         # Tokenization
│   ├── parser.py        # AST construction
│   ├── ast_nodes.py     # AST node definitions
│   ├── evaluator.py     # Runtime evaluation
│   ├── errors.py        # Error classes
│   └── builtins.py      # Built-in functions
├── main.pypp            # Example code
├── interpreter.py       # Entry point (imports src modules)
└── run.py               # Simple runner script
```

### File Explanations & Code

#### `src/__init__.py`

```python
"""py++ interpreter package."""
__version__ = "0.1.0"
```

#### `src/errors.py`

```python
"""Error classes for py++ interpreter."""

class PyPPError(Exception):
    """Base exception for py++ runtime errors."""
    pass

class LexerError(PyPPError):
    """Raised during tokenization."""
    def __init__(self, message, line, col):
        self.message = message
        self.line = line
        self.col = col
        super().__init__(f"{message} at {line}:{col}")

class ParserError(PyPPError):
    """Raised during parsing."""
    def __init__(self, message, line, col):
        self.message = message
        self.line = line
        self.col = col
        super().__init__(f"{message} at {line}:{col}")

class RuntimeError(PyPPError):
    """Raised during evaluation."""
    pass

class NameError(RuntimeError):
    """Variable not defined."""
    pass

class TypeError(RuntimeError):
    """Invalid type operation."""
    pass

class ReturnValue(Exception):
    """Control flow exception for return statements."""
    def __init__(self, value):
        self.value = value

class BreakException(Exception):
    """Control flow exception for break statements."""
    pass

class ContinueException(Exception):
    """Control flow exception for continue statements."""
    pass
```

#### `src/ast_nodes.py`

```python
"""AST node definitions for py++."""

class ASTNode:
    """Base class for all AST nodes."""
    pass

# Statements
class Program(ASTNode):
    def __init__(self, statements):
        self.statements = statements

class LetStatement(ASTNode):
    def __init__(self, name, value):
        self.name = name
        self.value = value

class FunctionDecl(ASTNode):
    def __init__(self, name, params, body):
        self.name = name
        self.params = params
        self.body = body

class ReturnStatement(ASTNode):
    def __init__(self, value):
        self.value = value

class IfStatement(ASTNode):
    def __init__(self, condition, then_block, else_block):
        self.condition = condition
        self.then_block = then_block
        self.else_block = else_block

class ForStatement(ASTNode):
    def __init__(self, init, condition, update, body):
        self.init = init
        self.condition = condition
        self.update = update
        self.body = body

class WhileStatement(ASTNode):
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body

class BlockStatement(ASTNode):
    def __init__(self, statements):
        self.statements = statements

class ExpressionStatement(ASTNode):
    def __init__(self, expression):
        self.expression = expression

class BreakStatement(ASTNode):
    pass

class ContinueStatement(ASTNode):
    pass

# Expressions
class BinaryOp(ASTNode):
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right

class UnaryOp(ASTNode):
    def __init__(self, op, operand):
        self.op = op
        self.operand = operand

class CallExpression(ASTNode):
    def __init__(self, func, args):
        self.func = func
        self.args = args

class Identifier(ASTNode):
    def __init__(self, name):
        self.name = name

class Literal(ASTNode):
    def __init__(self, value):
        self.value = value

class AssignmentExpression(ASTNode):
    def __init__(self, target, value):
        self.target = target
        self.value = value
```

#### `src/lexer.py` (tokenization module)

```python
"""Lexer for py++."""

from enum import Enum, auto
from typing import Any, List, Optional

class TokenType(Enum):
    # Literals
    NUMBER = auto()
    STRING = auto()
    BOOL = auto()
    NONE = auto()
    
    # Identifiers and keywords
    IDENTIFIER = auto()
    LET = auto()
    FN = auto()
    RETURN = auto()
    IF = auto()
    ELSE = auto()
    FOR = auto()
    WHILE = auto()
    BREAK = auto()
    CONTINUE = auto()
    TRUE = auto()
    FALSE = auto()
    
    # Operators
    PLUS = auto()
    MINUS = auto()
    STAR = auto()
    SLASH = auto()
    PERCENT = auto()
    ASSIGN = auto()
    EQ = auto()
    NE = auto()
    LT = auto()
    LE = auto()
    GT = auto()
    GE = auto()
    AND = auto()
    OR = auto()
    NOT = auto()
    
    # Delimiters
    LPAREN = auto()
    RPAREN = auto()
    LBRACE = auto()
    RBRACE = auto()
    SEMICOLON = auto()
    COMMA = auto()
    
    # Special
    EOF = auto()

class Token:
    def __init__(self, type_: TokenType, value: Any, line: int, col: int):
        self.type = type_
        self.value = value
        self.line = line
        self.col = col
    
    def __repr__(self):
        return f"Token({self.type.name}, {self.value!r})"

class Lexer:
    """Tokenizes py++ source code."""
    
    KEYWORDS = {
        'let': TokenType.LET,
        'fn': TokenType.FN,
        'return': TokenType.RETURN,
        'if': TokenType.IF,
        'else': TokenType.ELSE,
        'for': TokenType.FOR,
        'while': TokenType.WHILE,
        'break': TokenType.BREAK,
        'continue': TokenType.CONTINUE,
        'true': TokenType.TRUE,
        'false': TokenType.FALSE,
        'null': TokenType.NONE,
    }
    
    def __init__(self, source: str):
        self.source = source
        self.pos = 0
        self.line = 1
        self.col = 1
        self.tokens: List[Token] = []
    
    def error(self, msg: str):
        from .errors import LexerError
        raise LexerError(msg, self.line, self.col)
    
    def peek(self, offset=0) -> Optional[str]:
        idx = self.pos + offset
        return self.source[idx] if idx < len(self.source) else None
    
    def advance(self):
        if self.pos < len(self.source):
            if self.source[self.pos] == '\n':
                self.line += 1
                self.col = 1
            else:
                self.col += 1
            self.pos += 1
    
    def skip_whitespace(self):
        while self.peek() and self.peek() in ' \t\r\n':
            self.advance()
    
    def skip_comment(self):
        if self.peek() == '/' and self.peek(1) == '/':
            while self.peek() and self.peek() != '\n':
                self.advance()
            if self.peek():
                self.advance()
    
    def read_number(self) -> Token:
        start_line, start_col = self.line, self.col
        num_str = ''
        while self.peek() and (self.peek().isdigit() or self.peek() == '.'):
            num_str += self.peek()
            self.advance()
        
        if '.' in num_str:
            return Token(TokenType.NUMBER, float(num_str), start_line, start_col)
        else:
            return Token(TokenType.NUMBER, int(num_str), start_line, start_col)
    
    def read_string(self, quote_char: str) -> Token:
        start_line, start_col = self.line, self.col
        self.advance()
        s = ''
        while self.peek() and self.peek() != quote_char:
            if self.peek() == '\\':
                self.advance()
                escape_char = self.peek()
                if escape_char == 'n':
                    s += '\n'
                elif escape_char == 't':
                    s += '\t'
                elif escape_char == 'r':
                    s += '\r'
                elif escape_char == '\\':
                    s += '\\'
                elif escape_char == quote_char:
                    s += quote_char
                else:
                    s += escape_char or ''
                self.advance()
            else:
                s += self.peek()
                self.advance()
        
        if not self.peek():
            self.error(f"Unterminated string")
        self.advance()
        return Token(TokenType.STRING, s, start_line, start_col)
    
    def read_identifier(self) -> Token:
        start_line, start_col = self.line, self.col
        ident = ''
        while self.peek() and (self.peek().isalnum() or self.peek() == '_'):
            ident += self.peek()
            self.advance()
        
        token_type = self.KEYWORDS.get(ident, TokenType.IDENTIFIER)
        value = True if token_type == TokenType.TRUE else (False if token_type == TokenType.FALSE else ident)
        return Token(token_type, value, start_line, start_col)
    
    def tokenize(self) -> List[Token]:
        while self.pos < len(self.source):
            self.skip_whitespace()
            if self.pos >= len(self.source):
                break
            
            if self.peek() == '/' and self.peek(1) == '/':
                self.skip_comment()
                continue
            
            current = self.peek()
            
            if current.isdigit():
                self.tokens.append(self.read_number())
            elif current in ('"', "'"):
                self.tokens.append(self.read_string(current))
            elif current.isalpha() or current == '_':
                self.tokens.append(self.read_identifier())
            elif current == '+':
                self.tokens.append(Token(TokenType.PLUS, '+', self.line, self.col))
                self.advance()
            elif current == '-':
                self.tokens.append(Token(TokenType.MINUS, '-', self.line, self.col))
                self.advance()
            elif current == '*':
                self.tokens.append(Token(TokenType.STAR, '*', self.line, self.col))
                self.advance()
            elif current == '/':
                self.tokens.append(Token(TokenType.SLASH, '/', self.line, self.col))
                self.advance()
            elif current == '%':
                self.tokens.append(Token(TokenType.PERCENT, '%', self.line, self.col))
                self.advance()
            elif current == '=' and self.peek(1) == '=':
                self.tokens.append(Token(TokenType.EQ, '==', self.line, self.col))
                self.advance()
                self.advance()
            elif current == '!' and self.peek(1) == '=':
                self.tokens.append(Token(TokenType.NE, '!=', self.line, self.col))
                self.advance()
                self.advance()
            elif current == '<' and self.peek(1) == '=':
                self.tokens.append(Token(TokenType.LE, '<=', self.line, self.col))
                self.advance()
                self.advance()
            elif current == '<':
                self.tokens.append(Token(TokenType.LT, '<', self.line, self.col))
                self.advance()
            elif current == '>' and self.peek(1) == '=':
                self.tokens.append(Token(TokenType.GE, '>=', self.line, self.col))
                self.advance()
                self.advance()
            elif current == '>':
                self.tokens.append(Token(TokenType.GT, '>', self.line, self.col))
                self.advance()
            elif current == '&' and self.peek(1) == '&':
                self.tokens.append(Token(TokenType.AND, '&&', self.line, self.col))
                self.advance()
                self.advance()
            elif current == '|' and self.peek(1) == '|':
                self.tokens.append(Token(TokenType.OR, '||', self.line, self.col))
                self.advance()
                self.advance()
            elif current == '!':
                self.tokens.append(Token(TokenType.NOT, '!', self.line, self.col))
                self.advance()
            elif current == '=':
                self.tokens.append(Token(TokenType.ASSIGN, '=', self.line, self.col))
                self.advance()
            elif current == '(':
                self.tokens.append(Token(TokenType.LPAREN, '(', self.line, self.col))
                self.advance()
            elif current == ')':
                self.tokens.append(Token(TokenType.RPAREN, ')', self.line, self.col))
                self.advance()
            elif current == '{':
                self.tokens.append(Token(TokenType.LBRACE, '{', self.line, self.col))
                self.advance()
            elif current == '}':
                self.tokens.append(Token(TokenType.RBRACE, '}', self.line, self.col))
                self.advance()
            elif current == ';':
                self.tokens.append(Token(TokenType.SEMICOLON, ';', self.line, self.col))
                self.advance()
            elif current == ',':
                self.tokens.append(Token(TokenType.COMMA, ',', self.line, self.col))
                self.advance()
            else:
                self.error(f"Unexpected character: {current!r}")
        
        self.tokens.append(Token(TokenType.EOF, None, self.line, self.col))
        return self.tokens
```

#### `src/parser.py`

```python
"""Parser for py++."""

from typing import List, Optional
from .lexer import Token, TokenType
from .ast_nodes import *
from .errors import ParserError

class Parser:
    """Parses tokens into an AST."""
    
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.pos = 0
    
    def error(self, msg: str):
        token = self.current_token()
        raise ParserError(msg, token.line, token.col)
    
    def current_token(self) -> Token:
        return self.tokens[self.pos] if self.pos < len(self.tokens) else self.tokens[-1]
    
    def peek_token(self, offset=0) -> Token:
        idx = self.pos + offset
        return self.tokens[idx] if idx < len(self.tokens) else self.tokens[-1]
    
    def advance(self):
        self.pos += 1
    
    def expect(self, token_type: TokenType) -> Token:
        token = self.current_token()
        if token.type != token_type:
            self.error(f"Expected {token_type.name}, got {token.type.name}")
        self.advance()
        return token
    
    def match(self, *token_types: TokenType) -> bool:
        return self.current_token().type in token_types
    
    def consume(self, *token_types: TokenType) -> Optional[Token]:
        if self.match(*token_types):
            token = self.current_token()
            self.advance()
            return token
        return None
    
    def parse(self) -> Program:
        statements = []
        while not self.match(TokenType.EOF):
            stmt = self.parse_statement()
            if stmt:
                statements.append(stmt)
        return Program(statements)
    
    def parse_statement(self) -> Optional[ASTNode]:
        if self.match(TokenType.LET):
            return self.parse_let_statement()
        elif self.match(TokenType.FN):
            return self.parse_function_decl()
        elif self.match(TokenType.RETURN):
            return self.parse_return_statement()
        elif self.match(TokenType.IF):
            return self.parse_if_statement()
        elif self.match(TokenType.FOR):
            return self.parse_for_statement()
        elif self.match(TokenType.WHILE):
            return self.parse_while_statement()
        elif self.match(TokenType.LBRACE):
            return self.parse_block_statement()
        elif self.match(TokenType.BREAK):
            self.advance()
            self.consume(TokenType.SEMICOLON)
            return BreakStatement()
        elif self.match(TokenType.CONTINUE):
            self.advance()
            self.consume(TokenType.SEMICOLON)
            return ContinueStatement()
        else:
            return self.parse_expression_statement()
    
    def parse_let_statement(self) -> LetStatement:
        self.expect(TokenType.LET)
        name = self.expect(TokenType.IDENTIFIER).value
        self.expect(TokenType.ASSIGN)
        value = self.parse_expression()
        self.consume(TokenType.SEMICOLON)
        return LetStatement(name, value)
    
    def parse_function_decl(self) -> FunctionDecl:
        self.expect(TokenType.FN)
        name = self.expect(TokenType.IDENTIFIER).value
        self.expect(TokenType.LPAREN)
        params = []
        if not self.match(TokenType.RPAREN):
            params.append(self.expect(TokenType.IDENTIFIER).value)
            while self.consume(TokenType.COMMA):
                params.append(self.expect(TokenType.IDENTIFIER).value)
        self.expect(TokenType.RPAREN)
        body = self.parse_block_statement()
        return FunctionDecl(name, params, body)
    
    def parse_return_statement(self) -> ReturnStatement:
        self.expect(TokenType.RETURN)
        value = None
        if not self.match(TokenType.SEMICOLON, TokenType.RBRACE):
            value = self.parse_expression()
        self.consume(TokenType.SEMICOLON)
        return ReturnStatement(value)
    
    def parse_if_statement(self) -> IfStatement:
        self.expect(TokenType.IF)
        self.expect(TokenType.LPAREN)
        condition = self.parse_expression()
        self.expect(TokenType.RPAREN)
        then_block = self.parse_block_statement()
        else_block = None
        if self.consume(TokenType.ELSE):
            else_block = self.parse_block_statement()
        return IfStatement(condition, then_block, else_block)
    
    def parse_for_statement(self) -> ForStatement:
        self.expect(TokenType.FOR)
        self.expect(TokenType.LPAREN)
        init = None
        if self.match(TokenType.LET):
            init = self.parse_let_statement()
        else:
            init = self.parse_expression()
            self.consume(TokenType.SEMICOLON)
        
        condition = None
        if not self.match(TokenType.SEMICOLON):
            condition = self.parse_expression()
        self.expect(TokenType.SEMICOLON)
        
        update = None
        if not self.match(TokenType.RPAREN):
            update = self.parse_expression()
        self.expect(TokenType.RPAREN)
        
        body = self.parse_block_statement()
        return ForStatement(init, condition, update, body)
    
    def parse_while_statement(self) -> WhileStatement:
        self.expect(TokenType.WHILE)
        self.expect(TokenType.LPAREN)
        condition = self.parse_expression()
        self.expect(TokenType.RPAREN)
        body = self.parse_block_statement()
        return WhileStatement(condition, body)
    
    def parse_block_statement(self) -> BlockStatement:
        self.expect(TokenType.LBRACE)
        statements = []
        while not self.match(TokenType.RBRACE):
            stmt = self.parse_statement()
            if stmt:
                statements.append(stmt)
        self.expect(TokenType.RBRACE)
        return BlockStatement(statements)
    
    def parse_expression_statement(self) -> ExpressionStatement:
        expr = self.parse_expression()
        self.consume(TokenType.SEMICOLON)
        return ExpressionStatement(expr)
    
    def parse_expression(self) -> ASTNode:
        return self.parse_assignment()
    
    def parse_assignment(self) -> ASTNode:
        expr = self.parse_logical_or()
        if self.match(TokenType.ASSIGN):
            if not isinstance(expr, Identifier):
                self.error("Invalid assignment target")
            self.advance()
            value = self.parse_assignment()
            return AssignmentExpression(expr.name, value)
        return expr
    
    def parse_logical_or(self) -> ASTNode:
        left = self.parse_logical_and()
        while self.consume(TokenType.OR):
            op = self.tokens[self.pos - 1].value
            right = self.parse_logical_and()
            left = BinaryOp(left, op, right)
        return left
    
    def parse_logical_and(self) -> ASTNode:
        left = self.parse_equality()
        while self.consume(TokenType.AND):
            op = self.tokens[self.pos - 1].value
            right = self.parse_equality()
            left = BinaryOp(left, op, right)
        return left
    
    def parse_equality(self) -> ASTNode:
        left = self.parse_comparison()
        while self.consume(TokenType.EQ, TokenType.NE):
            op = self.tokens[self.pos - 1].value
            right = self.parse_comparison()
            left = BinaryOp(left, op, right)
        return left
    
    def parse_comparison(self) -> ASTNode:
        left = self.parse_additive()
        while self.consume(TokenType.LT, TokenType.LE, TokenType.GT, TokenType.GE):
            op = self.tokens[self.pos - 1].value
            right = self.parse_additive()
            left = BinaryOp(left, op, right)
        return left
    
    def parse_additive(self) -> ASTNode:
        left = self.parse_multiplicative()
        while self.consume(TokenType.PLUS, TokenType.MINUS):
            op = self.tokens[self.pos - 1].value
            right = self.parse_multiplicative()
            left = BinaryOp(left, op, right)
        return left
    
    def parse_multiplicative(self) -> ASTNode:
        left = self.parse_unary()
        while self.consume(TokenType.STAR, TokenType.SLASH, TokenType.PERCENT):
            op = self.tokens[self.pos - 1].value
            right = self.parse_unary()
            left = BinaryOp(left, op, right)
        return left
    
    def parse_unary(self) -> ASTNode:
        if self.consume(TokenType.NOT, TokenType.MINUS):
            op = self.tokens[self.pos - 1].value
            operand = self.parse_unary()
            return UnaryOp(op, operand)
        return self.parse_postfix()
    
    def parse_postfix(self) -> ASTNode:
        expr = self.parse_primary()
        while True:
            if self.consume(TokenType.LPAREN):
                args = []
                if not self.match(TokenType.RPAREN):
                    args.append(self.parse_expression())
                    while self.consume(TokenType.COMMA):
                        args.append(self.parse_expression())
                self.expect(TokenType.RPAREN)
                expr = CallExpression(expr, args)
            else:
                break
        return expr
    
    def parse_primary(self) -> ASTNode:
        if self.consume(TokenType.NUMBER):
            return Literal(self.tokens[self.pos - 1].value)
        elif self.consume(TokenType.STRING):
            return Literal(self.tokens[self.pos - 1].value)
        elif self.consume(TokenType.TRUE, TokenType.FALSE):
            return Literal(self.tokens[self.pos - 1].value)
        elif self.consume(TokenType.NONE):
            return Literal(None)
        elif self.consume(TokenType.IDENTIFIER):
            return Identifier(self.tokens[self.pos - 1].value)
        elif self.consume(TokenType.LPAREN):
            expr = self.parse_expression()
            self.expect(TokenType.RPAREN)
            return expr
        else:
            self.error(f"Unexpected token: {self.current_token().type.name}")
```

#### `src/builtins.py`

```python
"""Built-in functions for py++."""

class PyPPFunction:
    def __init__(self, params, body, closure):
        self.params = params
        self.body = body
        self.closure = closure
    
    def __repr__(self):
        return f"<function with {len(self.params)} params>"

def builtin_print(*args):
    print(*args)
    return None

def builtin_len(obj):
    return len(obj)

def builtin_range(*args):
    return list(range(*args))

def builtin_int(value):
    return int(value)

def builtin_float(value):
    return float(value)

def builtin_str(value):
    return str(value)

def builtin_bool(value):
    return bool(value)

def builtin_type(obj):
    return type(obj).__name__

BUILTINS = {
    'print': builtin_print,
    'len': builtin_len,
    'range': builtin_range,
    'int': builtin_int,
    'float': builtin_float,
    'str': builtin_str,
    'bool': builtin_bool,
    'type': builtin_type,
}
```

#### `src/evaluator.py`

```python
"""Evaluator/runtime for py++."""

from typing import Any, Dict, List
from .ast_nodes import *
from .errors import ReturnValue, BreakException, ContinueException, NameError, TypeError as PyPPTypeError, RuntimeError
from .builtins import PyPPFunction, BUILTINS

class Evaluator:
    """Evaluates the AST."""
    
    def __init__(self):
        self.globals = BUILTINS.copy()
        self.locals_stack = [{}]
    
    def eval(self, node: ASTNode) -> Any:
        if isinstance(node, Program):
            result = None
            for stmt in node.statements:
                result = self.eval(stmt)
            return result
        
        elif isinstance(node, LetStatement):
            value = self.eval(node.value)
            self.set_variable(node.name, value)
            return None
        
        elif isinstance(node, FunctionDecl):
            func = PyPPFunction(node.params, node.body, self.get_current_scope().copy())
            self.set_variable(node.name, func)
            return None
        
        elif isinstance(node, ReturnStatement):
            value = self.eval(node.value) if node.value else None
            raise ReturnValue(value)
        
        elif isinstance(node, IfStatement):
            condition_val = self.eval(node.condition)
            if self.is_truthy(condition_val):
                return self.eval(node.then_block)
            elif node.else_block:
                return self.eval(node.else_block)
            return None
        
        elif isinstance(node, ForStatement):
            if node.init:
                self.eval(node.init)
            
            try:
                while True:
                    if node.condition:
                        cond_val = self.eval(node.condition)
                        if not self.is_truthy(cond_val):
                            break
                    
                    try:
                        self.eval(node.body)
                    except ContinueException:
                        pass
                    
                    if node.update:
                        self.eval(node.update)
            except BreakException:
                pass
            
            return None
        
        elif isinstance(node, WhileStatement):
            try:
                while self.is_truthy(self.eval(node.condition)):
                    try:
                        self.eval(node.body)
                    except ContinueException:
                        pass
            except BreakException:
                pass
            return None
        
        elif isinstance(node, BlockStatement):
            result = None
            for stmt in node.statements:
                result = self.eval(stmt)
            return result
        
        elif isinstance(node, ExpressionStatement):
            return self.eval(node.expression)
        
        elif isinstance(node, BinaryOp):
            left = self.eval(node.left)
            right = self.eval(node.right)
            
            if node.op == '+':
                return left + right
            elif node.op == '-':
                return left - right
            elif node.op == '*':
                return left * right
            elif node.op == '/':
                return left / right
            elif node.op == '%':
                return left % right
            elif node.op == '==':
                return left == right
            elif node.op == '!=':
                return left != right
            elif node.op == '<':
                return left < right
            elif node.op == '<=':
                return left <= right
            elif node.op == '>':
                return left > right
            elif node.op == '>=':
                return left >= right
            elif node.op == '&&':
                return self.is_truthy(left) and self.is_truthy(right)
            elif node.op == '||':
                return self.is_truthy(left) or self.is_truthy(right)
        
        elif isinstance(node, UnaryOp):
            operand = self.eval(node.operand)
            if node.op == '-':
                return -operand
            elif node.op == '!':
                return not self.is_truthy(operand)
        
        elif isinstance(node, CallExpression):
            func = self.eval(node.func)
            args = [self.eval(arg) for arg in node.args]
            
            if callable(func) and not isinstance(func, PyPPFunction):
                return func(*args)
            elif isinstance(func, PyPPFunction):
                return self.call_function(func, args)
            else:
                raise PyPPTypeError(f"{func} is not callable")
        
        elif isinstance(node, Identifier):
            return self.get_variable(node.name)
        
        elif isinstance(node, Literal):
            return node.value
        
        elif isinstance(node, AssignmentExpression):
            value = self.eval(node.value)
            self.set_variable(node.target, value)
            return value
        
        elif isinstance(node, BreakStatement):
            raise BreakException()
        
        elif isinstance(node, ContinueStatement):
            raise ContinueException()
        
        else:
            raise RuntimeError(f"Unknown node type: {type(node)}")
    
    def call_function(self, func: PyPPFunction, args: List[Any]) -> Any:
        if len(args) != len(func.params):
            raise PyPPTypeError(f"Function expects {len(func.params)} args, got {len(args)}")
        
        new_scope = func.closure.copy()
        for param, arg in zip(func.params, args):
            new_scope[param] = arg
        
        self.locals_stack.append(new_scope)
        try:
            self.eval(func.body)
            result = None
        except ReturnValue as ret:
            result = ret.value
        finally:
            self.locals_stack.pop()
        
        return result
    
    def is_truthy(self, value: Any) -> bool:
        if value is None or value is False:
            return False
        if value == 0 or value == "" or value == []:
            return False
        return True
    
    def get_current_scope(self) -> Dict[str, Any]:
        return self.locals_stack[-1]
    
    def get_variable(self, name: str) -> Any:
        for scope in reversed(self.locals_stack):
            if name in scope:
                return scope[name]
        if name in self.globals:
            return self.globals[name]
        raise NameError(f"Undefined variable: {name}")
    
    def set_variable(self, name: str, value: Any):
        if len(self.locals_stack) == 1:
            self.globals[name] = value
        else:
            self.locals_stack[-1][name] = value
```

#### `interpreter.py` (Main entry point)

```python
"""py++ interpreter main module."""

from src.lexer import Lexer
from src.parser import Parser
from src.evaluator import Evaluator

def interpret(source: str):
    """Complete pipeline: source -> tokens -> AST -> evaluation."""
    lexer = Lexer(source)
    tokens = lexer.tokenize()
    
    parser = Parser(tokens)
    ast = parser.parse()
    
    evaluator = Evaluator()
    return evaluator.eval(ast)
```

#### `run.py` (CLI runner)

```python
"""Simple py++ runner."""

import sys
from interpreter import interpret

def main():
    if len(sys.argv) < 2:
        print("Usage: python run.py <file.pypp>")
        sys.exit(1)
    
    filepath = sys.argv[1]
    try:
        with open(filepath, 'r') as f:
            source = f.read()
        interpret(source)
    except FileNotFoundError:
        print(f"Error: File not found: {filepath}")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
```

### Design Decisions

**Modular separation**: Each module has a single responsibility (lexing, parsing, AST, evaluation, errors). Easy to swap/upgrade components.

**Error hierarchy**: All errors inherit from `PyPPError`, making error handling consistent.

**Scope chain**: Evaluator maintains a stack of scopes; function closures capture their defining scope.

**Built-in registry**: BUILTINS dict makes it trivial to add new built-in functions.

---

## PHASE 3: Modules & Include System

**Objective**: Allow py++ programs to split across files and reuse code.

### Folder Structure

```
py-plus-plus/
├── src/
│   ├── __init__.py
│   ├── lexer.py
│   ├── parser.py
│   ├── ast_nodes.py
│   ├── evaluator.py
│   ├── errors.py
│   ├── builtins.py
│   └── module_loader.py    # NEW: Module system
├── stdlib/                  # NEW: Standard library modules
│   ├── math.pypp
│   ├── io.pypp
│   └── string.pypp
├── main.pypp
├── interpreter.py
└── run.py
```

### File Explanations

#### `src/module_loader.py` — Module Import System

```python
"""Module and import system for py++."""

import os
import sys
from typing import Dict, Any
from .lexer import Lexer
from .parser import Parser
from .evaluator import Evaluator
from .errors import RuntimeError

class ModuleLoader:
    """Loads and caches py++ modules."""
    
    def __init__(self, search_paths=None):
        self.search_paths = search_paths or ['.', './stdlib']
        self.loaded_modules: Dict[str, Dict[str, Any]] = {}
    
    def find_module(self, name: str) -> str:
        """Find module file in search paths."""
        filename = name + '.pypp'
        for path in self.search_paths:
            full_path = os.path.join(path, filename)
            if os.path.exists(full_path):
                return full_path
        raise RuntimeError(f"Module not found: {name}")
    
    def load_module(self, name: str, evaluator) -> Dict[str, Any]:
        """Load and execute a module, return its namespace."""
        if name in self.loaded_modules:
            return self.loaded_modules[name]
        
        filepath = self.find_module(name)
        with open(filepath, 'r') as f:
            source = f.read()
        
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()
        
        # Create isolated scope for module
        module_globals = {}
        module_scope = Evaluator()
        module_scope.globals = module_globals.copy()
        module_scope.eval(ast)
        
        # Cache and return module exports
        self.loaded_modules[name] = module_scope.globals
        return self.loaded_modules[name]
```

#### `stdlib/math.pypp` — Math Module

```pypp
// Simple math utilities module

fn abs(x) {
    if (x < 0) {
        return -x;
    }
    return x;
}

fn min(a, b) {
    if (a < b) {
        return a;
    }
    return b;
}

fn max(a, b) {
    if (a > b) {
        return a;
    }
    return b;
}

fn square(x) {
    return x * x;
}

fn cube(x) {
    return x * x * x;
}
```

#### `stdlib/io.pypp` — I/O Module

```pypp
// Input/output utilities

fn read_line() {
    // In phase 3, this would integrate with Python's input()
    // For now, placeholder
    return null;
}

fn write(text) {
    print(text);
    return null;
}

fn writeln(text) {
    print(text);
    return null;
}
```

#### `stdlib/string.pypp` — String Module

```pypp
// String manipulation utilities

fn upper(s) {
    // Integrate with Python's str.upper()
    return s;
}

fn lower(s) {
    // Integrate with Python's str.lower()
    return s;
}

fn length(s) {
    return len(s);
}
```

#### Updated `src/evaluator.py` — Add import support

In the evaluator, add support for `import` statements:

```python
# In the eval() method, add support for ImportStatement:

elif isinstance(node, ImportStatement):
    # Load module and add its exports to current scope
    loader = getattr(self, 'module_loader', None)
    if not loader:
        raise RuntimeError("Module loader not initialized")
    module_exports = loader.load_module(node.module_name, self)
    for name, value in module_exports.items():
        if not name.startswith('_'):
            self.set_variable(name, value)
    return None
```

### Example Usage

```pypp
// program.pypp
import math;

let x = 10;
let y = 20;

print(math.abs(-5));
print(math.max(x, y));
```

### Design Decisions

**Lazy loading**: Modules loaded only when requested, cached to avoid re-execution.

**Isolated scopes**: Each module has its own namespace; no global pollution.

**Search paths**: Multiple directories searched (`./`, `./stdlib`) for flexibility.

**Exports by default**: All non-underscore-prefixed identifiers exported from a module.

---

## PHASE 4: Standard Library

**Objective**: Expand stdlib with practical modules (math, file I/O, time, random).

### Folder Structure

```
py-plus-plus/
├── stdlib/
│   ├── math.pypp
│   ├── io.pypp
│   ├── string.pypp
│   ├── sys.pypp
│   ├── time.pypp
│   └── random.pypp
├── [core from Phase 2]
└── run.py
```

### Standard Library Modules

#### `stdlib/math.pypp`

```pypp
fn abs(x) {
    if (x < 0) return -x;
    return x;
}

fn min(a, b) {
    if (a < b) return a;
    return b;
}

fn max(a, b) {
    if (a > b) return a;
    return b;
}

fn square(x) {
    return x * x;
}

fn cube(x) {
    return x * x * x;
}

fn power(x, y) {
    // Simple power function (y must be non-negative integer)
    if (y == 0) return 1;
    let result = 1;
    for (let i = 0; i < y; i = i + 1) {
        result = result * x;
    }
    return result;
}
```

#### `stdlib/string.pypp`

```pypp
fn length(s) {
    return len(s);
}

fn concat(a, b) {
    return a + b;
}

fn repeat(s, n) {
    let result = "";
    for (let i = 0; i < n; i = i + 1) {
        result = result + s;
    }
    return result;
}

fn starts_with(s, prefix) {
    // Check if s starts with prefix
    // Placeholder - would require string comparison
    return false;
}
```

#### `stdlib/sys.pypp`

```pypp
// System utilities module

fn exit(code) {
    // Would call Python's sys.exit()
    // Placeholder
    return null;
}

fn print_version() {
    print("py++ version 0.1.0");
    return null;
}
```

#### `stdlib/time.pypp`

```pypp
// Time module - integrates with Python's time module

fn now() {
    // Would return current timestamp
    // Placeholder
    return 0;
}

fn sleep(seconds) {
    // Would call Python's time.sleep()
    // Placeholder
    return null;
}
```

#### `stdlib/random.pypp`

```pypp
// Random number generation

fn random() {
    // Returns random float 0-1
    // Placeholder
    return 0;
}

fn randint(a, b) {
    // Returns random integer in [a, b]
    // Placeholder
    return a;
}

fn choice(list) {
    // Returns random element from list
    if (len(list) == 0) return null;
    return list[0];  // Placeholder
}
```

### Update `src/builtins.py` with More Built-ins

```python
"""Extended built-in functions."""

import time
import random as py_random

def builtin_print(*args):
    print(*args)
    return None

def builtin_len(obj):
    return len(obj)

def builtin_range(*args):
    return list(range(*args))

def builtin_time():
    return time.time()

def builtin_sleep(seconds):
    time.sleep(seconds)
    return None

def builtin_random():
    return py_random.random()

def builtin_randint(a, b):
    return py_random.randint(a, b)

def builtin_int(value):
    return int(value)

def builtin_float(value):
    return float(value)

def builtin_str(value):
    return str(value)

def builtin_bool(value):
    return bool(value)

def builtin_type(obj):
    return type(obj).__name__

BUILTINS = {
    'print': builtin_print,
    'len': builtin_len,
    'range': builtin_range,
    'time': builtin_time,
    'sleep': builtin_sleep,
    'random': builtin_random,
    'randint': builtin_randint,
    'int': builtin_int,
    'float': builtin_float,
    'str': builtin_str,
    'bool': builtin_bool,
    'type': builtin_type,
}
```

### Design Decisions

**Pure py++ where practical**: stdlib modules written in py++, not Python, to dogfood the language.

**Hybrid where necessary**: Time, random, math (if complex) bridge to Python's stdlib for reliability.

**Simple, beginner-friendly API**: No complex overloads or hidden behaviors.

---

## PHASE 5: Functions & Types

**Objective**: Add optional static typing, better function support, and type checking.

### New Syntax

```pypp
// Dynamic (existing)
fn add(a, b) {
    return a + b;
}

// Optional static typing
fn add(a: int, b: int) -> int {
    return a + b;
}

let x: int = 10;
let y: string = "hello";
let z: float = 3.14;
let flag: bool = true;
```

### Updated `src/ast_nodes.py` — Add TypeAnnotation

```python
class TypeAnnotation(ASTNode):
    def __init__(self, type_name):
        self.type_name = type_name  # "int", "string", "float", "bool", or None

class LetStatement(ASTNode):
    def __init__(self, name, value, type_annotation=None):
        self.name = name
        self.value = value
        self.type_annotation = type_annotation

class FunctionDecl(ASTNode):
    def __init__(self, name, params, body, return_type=None, param_types=None):
        self.name = name
        self.params = params
        self.body = body
        self.return_type = return_type  # "int", "string", etc.
        self.param_types = param_types or {}  # {param_name: type_name}
```

### Updated `src/lexer.py` — Add colon and arrow tokens

```python
class TokenType(Enum):
    # ... existing types ...
    COLON = auto()        # :
    ARROW = auto()        # ->
    INT_TYPE = auto()     # int
    STRING_TYPE = auto()  # string
    FLOAT_TYPE = auto()   # float
    BOOL_TYPE = auto()    # bool
```

### Updated `src/parser.py` — Parse type annotations

```python
def parse_let_statement(self) -> LetStatement:
    self.expect(TokenType.LET)
    name = self.expect(TokenType.IDENTIFIER).value
    type_annotation = None
    if self.consume(TokenType.COLON):
        type_annotation = self.parse_type()
    self.expect(TokenType.ASSIGN)
    value = self.parse_expression()
    self.consume(TokenType.SEMICOLON)
    return LetStatement(name, value, type_annotation)

def parse_type(self) -> str:
    """Parse type annotation."""
    type_tokens = {
        TokenType.INT_TYPE: 'int',
        TokenType.STRING_TYPE: 'string',
        TokenType.FLOAT_TYPE: 'float',
        TokenType.BOOL_TYPE: 'bool',
    }
    for token_type, type_name in type_tokens.items():
        if self.consume(token_type):
            return type_name
    self.error("Expected type annotation")
```

### Type Checking in Evaluator

```python
def check_type(self, value, expected_type):
    """Optional runtime type checking."""
    if expected_type == 'int' and not isinstance(value, int):
        raise TypeError(f"Expected int, got {type(value).__name__}")
    elif expected_type == 'string' and not isinstance(value, str):
        raise TypeError(f"Expected string, got {type(value).__name__}")
    elif expected_type == 'float' and not isinstance(value, (int, float)):
        raise TypeError(f"Expected float, got {type(value).__name__}")
    elif expected_type == 'bool' and not isinstance(value, bool):
        raise TypeError(f"Expected bool, got {type(value).__name__}")
    return value

# In eval() LetStatement:
elif isinstance(node, LetStatement):
    value = self.eval(node.value)
    if node.type_annotation:
        value = self.check_type(value, node.type_annotation)
    self.set_variable(node.name, value)
    return None
```

### Example Programs

#### `example_typed.pypp`

```pypp
// Functions with optional type annotations

fn greet(name: string) {
    print("Hello, " + name);
}

fn add(a: int, b: int) -> int {
    return a + b;
}

fn multiply(x: float, y: float) -> float {
    return x * y;
}

let message: string = "py++ is fun!";
let count: int = 42;
let pi: float = 3.14159;

print(message);
print(count);
print(pi);

greet("Alice");
let sum: int = add(10, 20);
print(sum);
```

### Design Decisions

**Optional typing**: Type hints are optional; py++ defaults to dynamic typing for ease of use.

**Runtime checking**: Types enforced at assignment time for safety, not at compile time (yet).

**Gradual typing**: Mix typed and untyped code freely; typed code documents intent and enables optimization.

**Simple types only**: int, string, float, bool (arrays/objects in Phase 6+).

---

## PHASE 6: CLI Runner & Project Structure

**Objective**: Professional `pypp` command-line tool with project scaffolding.

### Folder Structure

```
py-plus-plus/
├── src/
│   ├── [all modules from Phase 2]
│   ├── module_loader.py
│   └── cli.py          # NEW: CLI interface
├── stdlib/
│   ├── [all modules]
├── projects/           # NEW: Example projects
│   ├── hello/
│   │   ├── main.pypp
│   │   ├── pypp.toml   # Project config
│   │   └── lib/
│   │       └── util.pypp
│   └── calculator/
│       ├── main.pypp
│       └── pypp.toml
├── pypp               # NEW: Executable script (Unix)
├── pypp.cmd           # NEW: Executable script (Windows)
├── pypp_cli.py        # NEW: CLI implementation
└── run.py
```

### File Explanations

#### `pypp_cli.py` — Complete CLI Interface

```python
"""py++ command-line interface."""

import os
import sys
import argparse
import json
from pathlib import Path

class PyPPCLI:
    """Command-line interface for py++."""
    
    def __init__(self):
        self.parser = argparse.ArgumentParser(
            description='py++ programming language interpreter'
        )
        self.setup_commands()
    
    def setup_commands(self):
        subparsers = self.parser.add_subparsers(dest='command')
        
        # pypp run <file>
        run_parser = subparsers.add_parser('run', help='Run a py++ file')
        run_parser.add_argument('file', help='File to run (.pypp)')
        run_parser.add_argument('--verbose', action='store_true', help='Verbose output')
        
        # pypp build <project>
        build_parser = subparsers.add_parser('build', help='Build a project')
        build_parser.add_argument('project', nargs='?', default='.', help='Project directory')
        build_parser.add_argument('--output', default='build', help='Output directory')
        
        # pypp new <project_name>
        new_parser = subparsers.add_parser('new', help='Create a new project')
        new_parser.add_argument('name', help='Project name')
        new_parser.add_argument('--template', default='basic', help='Project template')
        
        # pypp version
        subparsers.add_parser('version', help='Show version')
        
        # pypp help
        subparsers.add_parser('help', help='Show help')
    
    def run_command(self, args):
        """Run a py++ file."""
        from interpreter import interpret
        
        if not os.path.exists(args.file):
            print(f"Error: File not found: {args.file}")
            sys.exit(1)
        
        try:
            with open(args.file, 'r') as f:
                source = f.read()
            
            if args.verbose:
                print(f"[INFO] Executing {args.file}")
            
            interpret(source)
            
            if args.verbose:
                print(f"[INFO] Execution completed")
        
        except Exception as e:
            print(f"Error: {e}")
            if args.verbose:
                import traceback
                traceback.print_exc()
            sys.exit(1)
    
    def build_command(self, args):
        """Build a project."""
        pypp_toml = os.path.join(args.project, 'pypp.toml')
        if not os.path.exists(pypp_toml):
            print(f"Error: No pypp.toml found in {args.project}")
            sys.exit(1)
        
        with open(pypp_toml, 'r') as f:
            config = f.read()
        
        print(f"[INFO] Building project from {args.project}")
        print(f"[INFO] Output: {args.output}")
        
        os.makedirs(args.output, exist_ok=True)
        
        # Copy source files to output
        src_dir = os.path.join(args.project, 'src')
        if os.path.exists(src_dir):
            for root, dirs, files in os.walk(src_dir):
                for file in files:
                    if file.endswith('.pypp'):
                        src = os.path.join(root, file)
                        rel = os.path.relpath(src, src_dir)
                        dst = os.path.join(args.output, rel)
                        os.makedirs(os.path.dirname(dst), exist_ok=True)
                        with open(src, 'r') as f:
                            content = f.read()
                        with open(dst, 'w') as f:
                            f.write(content)
        
        print(f"[INFO] Build completed")
    
    def new_command(self, args):
        """Create a new py++ project."""
        project_dir = args.name
        
        if os.path.exists(project_dir):
            print(f"Error: Directory already exists: {project_dir}")
            sys.exit(1)
        
        os.makedirs(project_dir)
        os.makedirs(os.path.join(project_dir, 'src'))
        
        # pypp.toml
        toml_content = f"""
[project]
name = "{args.name}"
version = "0.1.0"
author = "Your Name"
description = "A py++ project"

[build]
main = "src/main.pypp"
output = "build"
"""
        with open(os.path.join(project_dir, 'pypp.toml'), 'w') as f:
            f.write(toml_content.strip())
        
        # main.pypp template
        main_code = """// My py++ project

fn main() {
    print("Hello from py++!");
}

main();
"""
        with open(os.path.join(project_dir, 'src', 'main.pypp'), 'w') as f:
            f.write(main_code)
        
        # README
        readme = f"""# {args.name}

A py++ project.

## Running

```
pypp run src/main.pypp
```

## Building

```
pypp build .
```
"""
        with open(os.path.join(project_dir, 'README.md'), 'w') as f:
            f.write(readme)
        
        print(f"[INFO] Created project: {project_dir}")
        print(f"[INFO] Run: pypp run {project_dir}/src/main.pypp")
    
    def version_command(self):
        """Show version."""
        print("py++ version 0.1.0")
    
    def help_command(self):
        """Show help."""
        self.parser.print_help()
    
    def run(self, argv=None):
        """Parse arguments and execute command."""
        if argv is None:
            argv = sys.argv[1:]
        
        if not argv:
            self.help_command()
            return
        
        args = self.parser.parse_args(argv)
        
        if args.command == 'run':
            self.run_command(args)
        elif args.command == 'build':
            self.build_command(args)
        elif args.command == 'new':
            self.new_command(args)
        elif args.command == 'version':
            self.version_command()
        elif args.command == 'help':
            self.help_command()
        else:
            self.help_command()

def main():
    cli = PyPPCLI()
    cli.run()

if __name__ == '__main__':
    main()
```

#### `pypp` — Unix Executable Wrapper

```bash
#!/usr/bin/env python3
"""py++ CLI launcher for Unix systems."""

import sys
from pypp_cli import main

if __name__ == '__main__':
    main()
```

#### `pypp.cmd` — Windows Executable Wrapper

```batch
@echo off
python pypp_cli.py %*
```

#### Example `projects/hello/pypp.toml`

```toml
[project]
name = "hello"
version = "0.1.0"
author = "Alice"
description = "A simple hello world py++ program"

[build]
main = "src/main.pypp"
output = "build"
```

#### Example `projects/hello/src/main.pypp`

```pypp
import util;

fn main() {
    let greeting = "Hello, py++!";
    util.print_fancy(greeting);
}

main();
```

#### Example `projects/hello/lib/util.pypp`

```pypp
fn print_fancy(text: string) {
    print("=== " + text + " ===");
}
```

### Usage Examples

```bash
# Run a single file
pypp run example.pypp

# Create a new project
pypp new my_calculator
cd my_calculator
pypp run src/main.pypp

# Build a project
pypp build .

# Show version
pypp version
```

### Design Decisions

**Subcommand structure**: Similar to `cargo`, `npm`, `git` for familiarity.

**Project scaffolding**: `pypp new` generates ready-to-run templates.

**pypp.toml**: Inspired by Cargo.toml, simple declarative configuration.

**Multi-platform**: Both Unix and Windows runners.

---

## PHASE 7: Performance & Bytecode Compiler

**Objective**: Introduce bytecode compilation and VM for 10-50x speedup.

### Folder Structure

```
py-plus-plus/
├── src/
│   ├── [all from Phase 6]
│   ├── compiler.py      # NEW: Bytecode compiler
│   ├── vm.py            # NEW: Bytecode VM
│   └── bytecode.py      # NEW: Bytecode definitions
├── [stdlib, projects, cli...]
```

### File Explanations

#### `src/bytecode.py` — Bytecode Instruction Set

```python
"""Bytecode instruction definitions."""

from enum import Enum, auto

class OpCode(Enum):
    # Constants
    LOAD_CONST = auto()       # Load constant value
    LOAD_VAR = auto()         # Load variable
    STORE_VAR = auto()        # Store to variable
    
    # Arithmetic
    ADD = auto()
    SUB = auto()
    MUL = auto()
    DIV = auto()
    MOD = auto()
    NEG = auto()
    
    # Comparison
    EQ = auto()
    NE = auto()
    LT = auto()
    LE = auto()
    GT = auto()
    GE = auto()
    
    # Logic
    AND = auto()
    OR = auto()
    NOT = auto()
    
    # Control flow
    JUMP = auto()             # Unconditional jump
    JUMP_IF_FALSE = auto()     # Jump if condition false
    LOOP = auto()              # Start loop
    BREAK = auto()
    CONTINUE = auto()
    
    # Functions
    CALL = auto()              # Call function
    RETURN = auto()            # Return from function
    MAKE_FUNCTION = auto()     # Create function object
    
    # Stack
    POP = auto()               # Pop stack top
    DUP = auto()               # Duplicate stack top
    
    # Special
    HALT = auto()              # End program

class Instruction:
    def __init__(self, op: OpCode, arg=None):
        self.op = op
        self.arg = arg
    
    def __repr__(self):
        return f"Instruction({self.op.name}, {self.arg})"

class Bytecode:
    def __init__(self):
        self.instructions = []
        self.constants = []
        self.variable_names = {}
        self.line_nums = []
    
    def add_instruction(self, op: OpCode, arg=None):
        """Add instruction to bytecode."""
        self.instructions.append(Instruction(op, arg))
        return len(self.instructions) - 1
    
    def add_constant(self, value):
        """Add constant to pool, return index."""
        self.constants.append(value)
        return len(self.constants) - 1
    
    def register_variable(self, name):
        """Register variable name, return index."""
        if name not in self.variable_names:
            self.variable_names[name] = len(self.variable_names)
        return self.variable_names[name]
```

#### `src/compiler.py` — Bytecode Compiler

```python
"""Bytecode compiler for py++."""

from .ast_nodes import *
from .bytecode import Bytecode, OpCode

class Compiler:
    """Compiles AST to bytecode."""
    
    def __init__(self):
        self.bytecode = Bytecode()
        self.scope_stack = [{}]
    
    def compile(self, ast: Program) -> Bytecode:
        """Compile AST to bytecode."""
        for stmt in ast.statements:
            self.compile_stmt(stmt)
        self.bytecode.add_instruction(OpCode.HALT)
        return self.bytecode
    
    def compile_stmt(self, node: ASTNode):
        """Compile statement."""
        if isinstance(node, LetStatement):
            self.compile_expr(node.value)
            var_idx = self.bytecode.register_variable(node.name)
            self.bytecode.add_instruction(OpCode.STORE_VAR, var_idx)
            self.bytecode.add_instruction(OpCode.POP)
        
        elif isinstance(node, FunctionDecl):
            # Compile function body
            saved_bytecode = self.bytecode
            self.bytecode = Bytecode()
            for stmt in node.body.statements:
                self.compile_stmt(stmt)
            self.bytecode.add_instruction(OpCode.RETURN)
            func_bytecode = self.bytecode
            self.bytecode = saved_bytecode
            
            # Store function
            const_idx = self.bytecode.add_constant(func_bytecode)
            self.bytecode.add_instruction(OpCode.LOAD_CONST, const_idx)
            var_idx = self.bytecode.register_variable(node.name)
            self.bytecode.add_instruction(OpCode.STORE_VAR, var_idx)
            self.bytecode.add_instruction(OpCode.POP)
        
        elif isinstance(node, ExpressionStatement):
            self.compile_expr(node.expression)
            self.bytecode.add_instruction(OpCode.POP)
        
        elif isinstance(node, ReturnStatement):
            if node.value:
                self.compile_expr(node.value)
            else:
                const_idx = self.bytecode.add_constant(None)
                self.bytecode.add_instruction(OpCode.LOAD_CONST, const_idx)
            self.bytecode.add_instruction(OpCode.RETURN)
        
        elif isinstance(node, IfStatement):
            self.compile_expr(node.condition)
            false_addr = self.bytecode.add_instruction(OpCode.JUMP_IF_FALSE)
            for stmt in node.then_block.statements:
                self.compile_stmt(stmt)
            if node.else_block:
                exit_addr = self.bytecode.add_instruction(OpCode.JUMP)
                self.bytecode.instructions[false_addr].arg = len(self.bytecode.instructions)
                for stmt in node.else_block.statements:
                    self.compile_stmt(stmt)
                self.bytecode.instructions[exit_addr].arg = len(self.bytecode.instructions)
            else:
                self.bytecode.instructions[false_addr].arg = len(self.bytecode.instructions)
        
        elif isinstance(node, WhileStatement):
            loop_start = len(self.bytecode.instructions)
            self.compile_expr(node.condition)
            exit_addr = self.bytecode.add_instruction(OpCode.JUMP_IF_FALSE)
            for stmt in node.body.statements:
                self.compile_stmt(stmt)
            self.bytecode.add_instruction(OpCode.JUMP, loop_start)
            self.bytecode.instructions[exit_addr].arg = len(self.bytecode.instructions)
        
        elif isinstance(node, BlockStatement):
            for stmt in node.statements:
                self.compile_stmt(stmt)
    
    def compile_expr(self, node: ASTNode):
        """Compile expression (result left on stack)."""
        if isinstance(node, Literal):
            const_idx = self.bytecode.add_constant(node.value)
            self.bytecode.add_instruction(OpCode.LOAD_CONST, const_idx)
        
        elif isinstance(node, Identifier):
            var_idx = self.bytecode.register_variable(node.name)
            self.bytecode.add_instruction(OpCode.LOAD_VAR, var_idx)
        
        elif isinstance(node, BinaryOp):
            self.compile_expr(node.left)
            self.compile_expr(node.right)
            op_map = {
                '+': OpCode.ADD,
                '-': OpCode.SUB,
                '*': OpCode.MUL,
                '/': OpCode.DIV,
                '%': OpCode.MOD,
                '==': OpCode.EQ,
                '!=': OpCode.NE,
                '<': OpCode.LT,
                '<=': OpCode.LE,
                '>': OpCode.GT,
                '>=': OpCode.GE,
                '&&': OpCode.AND,
                '||': OpCode.OR,
            }
            self.bytecode.add_instruction(op_map[node.op])
        
        elif isinstance(node, UnaryOp):
            self.compile_expr(node.operand)
            if node.op == '-':
                self.bytecode.add_instruction(OpCode.NEG)
            elif node.op == '!':
                self.bytecode.add_instruction(OpCode.NOT)
        
        elif isinstance(node, CallExpression):
            self.compile_expr(node.func)
            for arg in node.args:
                self.compile_expr(arg)
            self.bytecode.add_instruction(OpCode.CALL, len(node.args))
        
        elif isinstance(node, AssignmentExpression):
            self.compile_expr(node.value)
            var_idx = self.bytecode.register_variable(node.target)
            self.bytecode.add_instruction(OpCode.STORE_VAR, var_idx)
```

#### `src/vm.py` — Bytecode Virtual Machine

```python
"""Bytecode VM for py++."""

from .bytecode import OpCode, Bytecode
from .builtins import BUILTINS
import sys

class PyPPVM:
    """Virtual machine for executing py++ bytecode."""
    
    def __init__(self):
        self.stack = []
        self.variables = BUILTINS.copy()
        self.call_stack = []
    
    def execute(self, bytecode: Bytecode):
        """Execute bytecode."""
        pc = 0  # Program counter
        
        while pc < len(bytecode.instructions):
            instr = bytecode.instructions[pc]
            op = instr.op
            arg = instr.arg
            
            if op == OpCode.LOAD_CONST:
                self.stack.append(bytecode.constants[arg])
            
            elif op == OpCode.LOAD_VAR:
                var_names = list(bytecode.variable_names.keys())
                if arg < len(var_names):
                    var_name = var_names[arg]
                    self.stack.append(self.variables.get(var_name))
            
            elif op == OpCode.STORE_VAR:
                value = self.stack.pop()
                var_names = list(bytecode.variable_names.keys())
                if arg < len(var_names):
                    var_name = var_names[arg]
                    self.variables[var_name] = value
            
            elif op == OpCode.ADD:
                b = self.stack.pop()
                a = self.stack.pop()
                self.stack.append(a + b)
            
            elif op == OpCode.SUB:
                b = self.stack.pop()
                a = self.stack.pop()
                self.stack.append(a - b)
            
            elif op == OpCode.MUL:
                b = self.stack.pop()
                a = self.stack.pop()
                self.stack.append(a * b)
            
            elif op == OpCode.DIV:
                b = self.stack.pop()
                a = self.stack.pop()
                self.stack.append(a / b)
            
            elif op == OpCode.MOD:
                b = self.stack.pop()
                a = self.stack.pop()
                self.stack.append(a % b)
            
            elif op == OpCode.NEG:
                self.stack.append(-self.stack.pop())
            
            elif op == OpCode.EQ:
                b = self.stack.pop()
                a = self.stack.pop()
                self.stack.append(a == b)
            
            elif op == OpCode.NE:
                b = self.stack.pop()
                a = self.stack.pop()
                self.stack.append(a != b)
            
            elif op == OpCode.LT:
                b = self.stack.pop()
                a = self.stack.pop()
                self.stack.append(a < b)
            
            elif op == OpCode.LE:
                b = self.stack.pop()
                a = self.stack.pop()
                self.stack.append(a <= b)
            
            elif op == OpCode.GT:
                b = self.stack.pop()
                a = self.stack.pop()
                self.stack.append(a > b)
            
            elif op == OpCode.GE:
                b = self.stack.pop()
                a = self.stack.pop()
                self.stack.append(a >= b)
            
            elif op == OpCode.AND:
                b = self.stack.pop()
                a = self.stack.pop()
                self.stack.append(a and b)
            
            elif op == OpCode.OR:
                b = self.stack.pop()
                a = self.stack.pop()
                self.stack.append(a or b)
            
            elif op == OpCode.NOT:
                self.stack.append(not self.stack.pop())
            
            elif op == OpCode.JUMP_IF_FALSE:
                cond = self.stack.pop()
                if not cond:
                    pc = arg - 1
            
            elif op == OpCode.JUMP:
                pc = arg - 1
            
            elif op == OpCode.POP:
                self.stack.pop()
            
            elif op == OpCode.CALL:
                args = [self.stack.pop() for _ in range(arg)]
                args.reverse()
                func = self.stack.pop()
                if callable(func):
                    self.stack.append(func(*args))
                else:
                    raise TypeError(f"Not callable: {func}")
            
            elif op == OpCode.RETURN:
                return self.stack.pop() if self.stack else None
            
            elif op == OpCode.HALT:
                break
            
            pc += 1
        
        return self.stack[0] if self.stack else None
```

### Design Decisions

**Stack-based VM**: Simple, efficient, and proven design (like Python, Java).

**Bytecode simplicity**: Focus on basic ops; no complex optimizations yet.

**Minimal compiler**: Targets correctness over optimization; set stage for later JIT.

**Interpreter fallback**: Can still use tree-walking interpreter if bytecode debugging needed.

---

## PHASE 8: Scaling & Packaging

**Objective**: Make py++ a distributable, extensible ecosystem.

### Folder Structure

```
py-plus-plus/
├── src/
│   ├── [all from Phase 7]
│   └── package_manager.py  # NEW: Package system
├── stdlib/
│   └── [all modules]
├── packages/               # NEW: Package registry
│   ├── math-extra/
│   ├── web/
│   └── data/
├── docs/                   # NEW: Documentation
│   ├── guide.md
│   ├── api.md
│   ├── stdlib.md
│   └── examples/
├── tests/                  # NEW: Test suite
│   ├── test_lexer.py
│   ├── test_parser.py
│   ├── test_evaluator.py
│   └── test_vm.py
├── Makefile               # NEW: Build automation
├── pypp_cli.py
├── setup.py               # NEW: Python package setup
└── README.md
```

### File Explanations

#### `src/package_manager.py` — Package Management

```python
"""Package management for py++."""

import os
import json
from typing import Dict, List
from .module_loader import ModuleLoader

class Package:
    def __init__(self, name: str, version: str, author: str, description: str, modules: List[str]):
        self.name = name
        self.version = version
        self.author = author
        self.description = description
        self.modules = modules
    
    def to_json(self) -> Dict:
        return {
            'name': self.name,
            'version': self.version,
            'author': self.author,
            'description': self.description,
            'modules': self.modules
        }

class PackageManager:
    """Manages py++ packages."""
    
    def __init__(self, registry_path='~/.pypp/packages'):
        self.registry_path = os.path.expanduser(registry_path)
        os.makedirs(self.registry_path, exist_ok=True)
    
    def install_package(self, package_name: str, version='latest'):
        """Install a package from registry."""
        package_path = os.path.join(self.registry_path, f"{package_name}-{version}")
        if not os.path.exists(package_path):
            print(f"Package not found: {package_name}@{version}")
            return False
        return True
    
    def list_packages(self) -> List[str]:
        """List installed packages."""
        return os.listdir(self.registry_path)
    
    def publish_package(self, package_dir: str):
        """Publish a local package to registry."""
        pypp_toml = os.path.join(package_dir, 'pypp.toml')
        if not os.path.exists(pypp_toml):
            print(f"No pypp.toml in {package_dir}")
            return False
        
        # Parse config, upload to registry
        print(f"[INFO] Publishing {package_dir}...")
        return True
```

#### `setup.py` — Python Package for Distribution

```python
"""Setup script for py++ distribution."""

from setuptools import setup, find_packages

setup(
    name='pypp-lang',
    version='0.1.0',
    author='py++ Team',
    description='py++: Python-like language with C++ speed',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/pypp',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'pypp=pypp_cli:main',
        ],
    },
    python_requires='>=3.7',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
)
```

#### `Makefile` — Build Automation

```makefile
.PHONY: install test clean run example

install:
	pip install -e .

test:
	python -m pytest tests/ -v

clean:
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null
	find . -type f -name "*.pyc" -delete
	rm -rf build dist py-plus-plus.egg-info

run:
	pypp run main.pypp

example:
	@echo "Running examples..."
	pypp run examples/hello.pypp
	pypp run examples/fibonacci.pypp

docs:
	@echo "Building docs..."
	@echo "Docs placeholder"
```

#### `tests/test_lexer.py` — Unit Tests

```python
"""Tests for lexer."""

import unittest
from src.lexer import Lexer, TokenType

class TestLexer(unittest.TestCase):
    
    def test_numbers(self):
        lexer = Lexer("let x = 42;")
        tokens = lexer.tokenize()
        assert tokens[3].type == TokenType.NUMBER
        assert tokens[3].value == 42
    
    def test_strings(self):
        lexer = Lexer('let msg = "hello";')
        tokens = lexer.tokenize()
        assert tokens[3].type == TokenType.STRING
        assert tokens[3].value == "hello"
    
    def test_keywords(self):
        lexer = Lexer("fn add(a, b) { return a + b; }")
        tokens = lexer.tokenize()
        assert tokens[0].type == TokenType.FN
        assert tokens[7].type == TokenType.RETURN
    
    def test_operators(self):
        lexer = Lexer("x + y * z")
        tokens = lexer.tokenize()
        assert tokens[1].type == TokenType.PLUS
        assert tokens[3].type == TokenType.STAR
    
    def test_comments(self):
        lexer = Lexer("let x = 5; // comment\nlet y = 10;")
        tokens = lexer.tokenize()
        # Comments should be stripped
        x_found = any(t.value == 'x' for t in tokens)
        y_found = any(t.value == 'y' for t in tokens)
        assert x_found and y_found

if __name__ == '__main__':
    unittest.main()
```

#### `docs/guide.md` — User Guide

```markdown
# py++ Language Guide

## Getting Started

### Installation

```bash
pip install pypp-lang
```

### Your First Program

Create `hello.pypp`:

```pypp
print("Hello, py++!");
```

Run it:

```bash
pypp run hello.pypp
```

## Syntax Overview

### Variables

```pypp
let name = "Alice";
let age = 30;
let score = 95.5;
let active = true;
```

### Functions

```pypp
fn greet(name) {
    print("Hello, " + name);
}

greet("Alice");
```

### Control Flow

```pypp
if (x > 10) {
    print("x is large");
} else {
    print("x is small");
}

for (let i = 0; i < 10; i = i + 1) {
    print(i);
}

while (true) {
    print("loop");
    break;
}
```

### Type Annotations (Optional)

```pypp
fn add(a: int, b: int) -> int {
    return a + b;
}

let score: float = 98.5;
```

## Built-in Functions

- `print(...)` — Print to console
- `len(obj)` — Length of string/array
- `range(n)` — Generate numbers 0 to n-1
- `int(x)`, `float(x)`, `str(x)`, `bool(x)` — Type conversions

## Modules

```pypp
import math;

print(math.square(5));
```

## Creating Projects

```bash
pypp new my_project
cd my_project
pypp run src/main.pypp
```
```

#### `docs/api.md` — API Reference

```markdown
# py++ API Reference

## Lexer

```python
from src.lexer import Lexer

lexer = Lexer("let x = 10;")
tokens = lexer.tokenize()
```

## Parser

```python
from src.parser import Parser

parser = Parser(tokens)
ast = parser.parse()
```

## Evaluator

```python
from src.evaluator import Evaluator

evaluator = Evaluator()
result = evaluator.eval(ast)
```

## Compiler & VM

```python
from src.compiler import Compiler
from src.vm import PyPPVM

compiler = Compiler()
bytecode = compiler.compile(ast)

vm = PyPPVM()
vm.execute(bytecode)
```
```

#### Example Project: `fibonacci.pypp`

```pypp
// Fibonacci sequence generator

fn fibonacci(n: int) -> int {
    if (n <= 1) {
        return n;
    }
    return fibonacci(n - 1) + fibonacci(n - 2);
}

fn main() {
    for (let i = 0; i < 10; i = i + 1) {
        print(fibonacci(i));
    }
}

main();
```

### Design Decisions

**Distribution via pip**: Python packaging ecosystem for easy installation.

**Package registry**: Centralized system for publishing and discovering py++ packages.

**Comprehensive testing**: Unit tests, integration tests, benchmarks.

**Rich documentation**: Guides, API docs, examples, and tutorials.

**Modular architecture**: Each phase buildable independently, composable into larger system.

---

## Summary: Roadmap Checklist

| Phase | Component | Status | Purpose |
|-------|-----------|--------|---------|
| 1 | Minimal Interpreter | ✓ | Prove concept works |
| 2 | Modular Structure | ✓ | Organize codebase |
| 3 | Module System | ✓ | Code reusability |
| 4 | Standard Library | ✓ | Common utilities |
| 5 | Type System | ✓ | Safety + optimization |
| 6 | CLI & Projects | ✓ | Professional tooling |
| 7 | Bytecode & VM | ✓ | Performance |
| 8 | Packaging & Ecosystem | ✓ | Distribution & scaling |

## Next Steps for Production

1. **Optimize VM**: Add JIT compilation, escape analysis, inline caching
2. **Native Extensions**: C/C++ FFI for performance-critical code
3. **Concurrency**: Async/await, lightweight threads
4. **Advanced Types**: Generics, unions, sum types, pattern matching
5. **Standard Library Growth**: Database, HTTP, file I/O, cryptography
6. **IDE Support**: VS Code extension, syntax highlighting, LSP server
7. **Community**: Package repository, forums, GitHub discussions
8. **Production Hardening**: Error recovery, profiling, debugging tools

---

This roadmap provides a **complete, implementable path** from prototype to production. Start with Phase 1, iterate rapidly, and scale horizontally through modules and packages.
