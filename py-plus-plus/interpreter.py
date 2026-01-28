"""py++ interpreter main module."""

from src.lexer import Lexer
from src.parser import Parser
from src.evaluator import Evaluator
from src.module_loader import ModuleLoader

def interpret(source: str):
    """Complete pipeline: source -> tokens -> AST -> evaluation."""
    lexer = Lexer(source)
    tokens = lexer.tokenize()
    
    parser = Parser(tokens)
    ast = parser.parse()
    
    evaluator = Evaluator()
    evaluator.module_loader = ModuleLoader()
    return evaluator.eval(ast)
