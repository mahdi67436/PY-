"""Lexer for py++."""

from enum import Enum, auto
from typing import Any, List, Optional
from .errors import LexerError

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
    IMPORT = auto()
    
    # Types
    INT_TYPE = auto()
    STRING_TYPE = auto()
    FLOAT_TYPE = auto()
    BOOL_TYPE = auto()
    
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
    DOT = auto()
    
    # Delimiters
    LPAREN = auto()
    RPAREN = auto()
    LBRACE = auto()
    RBRACE = auto()
    SEMICOLON = auto()
    COMMA = auto()
    COLON = auto()
    ARROW = auto()
    
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
        'import': TokenType.IMPORT,
        'int': TokenType.INT_TYPE,
        'string': TokenType.STRING_TYPE,
        'float': TokenType.FLOAT_TYPE,
        'bool': TokenType.BOOL_TYPE,
    }
    
    def __init__(self, source: str):
        self.source = source
        self.pos = 0
        self.line = 1
        self.col = 1
        self.tokens: List[Token] = []
    
    def error(self, msg: str):
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
            elif current == '-' and self.peek(1) == '>':
                self.tokens.append(Token(TokenType.ARROW, '->', self.line, self.col))
                self.advance()
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
            elif current == ':':
                self.tokens.append(Token(TokenType.COLON, ':', self.line, self.col))
                self.advance()
            elif current == '.':
                self.tokens.append(Token(TokenType.DOT, '.', self.line, self.col))
                self.advance()
            else:
                self.error(f"Unexpected character: {current!r}")
        
        self.tokens.append(Token(TokenType.EOF, None, self.line, self.col))
        return self.tokens
