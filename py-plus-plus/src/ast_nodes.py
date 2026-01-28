"""AST node definitions for py++."""

class ASTNode:
    """Base class for all AST nodes."""
    pass

# Statements
class Program(ASTNode):
    def __init__(self, statements):
        self.statements = statements

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
        self.return_type = return_type
        self.param_types = param_types or {}

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

class ImportStatement(ASTNode):
    def __init__(self, module_name):
        self.module_name = module_name

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

class MemberAccess(ASTNode):
    def __init__(self, obj, member):
        self.obj = obj
        self.member = member
