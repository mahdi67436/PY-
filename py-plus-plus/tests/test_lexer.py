"""Tests for lexer."""

import unittest
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.lexer import Lexer, TokenType

class TestLexer(unittest.TestCase):
    
    def test_numbers(self):
        lexer = Lexer("let x = 42;")
        tokens = lexer.tokenize()
        assert tokens[3].type == TokenType.NUMBER
        assert tokens[3].value == 42
    
    def test_floats(self):
        lexer = Lexer("let x = 3.14;")
        tokens = lexer.tokenize()
        assert tokens[3].type == TokenType.NUMBER
        assert tokens[3].value == 3.14
    
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
    
    def test_comparison_operators(self):
        lexer = Lexer("a == b && c != d")
        tokens = lexer.tokenize()
        assert tokens[1].type == TokenType.EQ
        assert tokens[3].type == TokenType.AND
        assert tokens[5].type == TokenType.NE
    
    def test_comments(self):
        lexer = Lexer("let x = 5; // comment\nlet y = 10;")
        tokens = lexer.tokenize()
        # Comments should be stripped, only find the variables
        var_names = [t.value for t in tokens if t.type == TokenType.IDENTIFIER]
        assert 'x' in var_names
        assert 'y' in var_names

if __name__ == '__main__':
    unittest.main()
