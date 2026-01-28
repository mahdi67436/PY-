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
