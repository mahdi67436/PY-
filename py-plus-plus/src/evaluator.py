"""Evaluator/runtime for py++."""

from typing import Any, Dict, List
from .ast_nodes import *
from .errors import ReturnValue, BreakException, ContinueException, NameError, TypeError as PyPPTypeError, RuntimeError
from .builtins_advanced import PyPPFunction, BUILTINS

class Evaluator:
    """Evaluates the AST."""
    
    def __init__(self):
        self.globals = BUILTINS.copy()
        self.locals_stack = [{}]
        self.module_loader = None
    
    def eval(self, node: ASTNode) -> Any:
        if isinstance(node, Program):
            result = None
            for stmt in node.statements:
                result = self.eval(stmt)
            return result
        
        elif isinstance(node, ImportStatement):
            if self.module_loader:
                module_exports = self.module_loader.load_module(node.module_name, self)
                for name, value in module_exports.items():
                    if not name.startswith('_'):
                        self.set_variable(name, value)
            return None
        
        elif isinstance(node, LetStatement):
            value = self.eval(node.value)
            if node.type_annotation:
                value = self.check_type(value, node.type_annotation)
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
        
        elif isinstance(node, MemberAccess):
            obj = self.eval(node.obj)
            if isinstance(obj, dict):
                return obj.get(node.member)
            else:
                raise PyPPTypeError(f"Cannot access member {node.member} on {type(obj).__name__}")
        
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
    
    def check_type(self, value: Any, expected_type: str) -> Any:
        """Optional runtime type checking."""
        if expected_type == 'int' and not isinstance(value, int):
            raise PyPPTypeError(f"Expected int, got {type(value).__name__}")
        elif expected_type == 'string' and not isinstance(value, str):
            raise PyPPTypeError(f"Expected string, got {type(value).__name__}")
        elif expected_type == 'float' and not isinstance(value, (int, float)):
            raise PyPPTypeError(f"Expected float, got {type(value).__name__}")
        elif expected_type == 'bool' and not isinstance(value, bool):
            raise PyPPTypeError(f"Expected bool, got {type(value).__name__}")
        return value
    
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
