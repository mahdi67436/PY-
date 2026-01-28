"""Module and import system for py++."""

import os
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
        
        # Create module evaluator
        module_eval = Evaluator()
        module_eval.module_loader = self
        module_eval.eval(ast)
        
        # Cache module exports
        exports = {k: v for k, v in module_eval.globals.items() if not k.startswith('_')}
        self.loaded_modules[name] = exports
        return exports
