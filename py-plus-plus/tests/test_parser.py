"""Tests for parser."""

import unittest
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.lexer import Lexer
from src.parser import Parser
from src.ast_nodes import *

class TestParser(unittest.TestCase):
    
    def parse_code(self, code):
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        return parser.parse()
    
    def test_simple_assignment(self):
        ast = self.parse_code("let x = 5;")
        assert isinstance(ast, Program)
        assert len(ast.statements) == 1
        assert isinstance(ast.statements[0], LetStatement)
        assert ast.statements[0].name == 'x'
    
    def test_function_decl(self):
        ast = self.parse_code("fn greet(name) { print(name); }")
        assert len(ast.statements) == 1
        assert isinstance(ast.statements[0], FunctionDecl)
        assert ast.statements[0].name == 'greet'
        assert ast.statements[0].params == ['name']
    
    def test_if_statement(self):
        ast = self.parse_code("if (x > 0) { print(x); }")
        assert isinstance(ast.statements[0], IfStatement)
    
    def test_for_loop(self):
        ast = self.parse_code("for (let i = 0; i < 10; i = i + 1) { print(i); }")
        assert isinstance(ast.statements[0], ForStatement)
    
    def test_while_loop(self):
        ast = self.parse_code("while (true) { break; }")
        assert isinstance(ast.statements[0], WhileStatement)
    
    def test_binary_op(self):
        ast = self.parse_code("let x = a + b;")
        stmt = ast.statements[0]
        assert isinstance(stmt.value, BinaryOp)
        assert stmt.value.op == '+'

if __name__ == '__main__':
    unittest.main()
