"""py++ interpreter package."""
__version__ = "0.2.0"
__author__ = "py++ Team"
__description__ = "Python-like language with C++ speed, advanced data structures, and professional tooling"

# Core components
from .lexer import Lexer, TokenType
from .parser import Parser
from .evaluator import Evaluator
from .ast_nodes import *
from .errors import *

# Advanced features
from .advanced import (
    PyPPArray,
    PyPPObject,
    PyPPSet,
    AdvancedMath,
    StringUtils,
    DataValidation,
)

# Built-in functions
from .builtins_advanced import BUILTINS, PyPPFunction

__all__ = [
    # Core
    'Lexer', 'TokenType', 'Parser', 'Evaluator',
    # Advanced data structures
    'PyPPArray', 'PyPPObject', 'PyPPSet',
    # Utilities
    'AdvancedMath', 'StringUtils', 'DataValidation',
    # Functions
    'PyPPFunction', 'BUILTINS',
]
