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
        elif self.match(TokenType.IMPORT):
            return self.parse_import_statement()
        else:
            return self.parse_expression_statement()
    
    def parse_import_statement(self) -> ImportStatement:
        self.expect(TokenType.IMPORT)
        module_name = self.expect(TokenType.IDENTIFIER).value
        self.consume(TokenType.SEMICOLON)
        return ImportStatement(module_name)
    
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
    
    def parse_function_decl(self) -> FunctionDecl:
        self.expect(TokenType.FN)
        name = self.expect(TokenType.IDENTIFIER).value
        self.expect(TokenType.LPAREN)
        params = []
        param_types = {}
        if not self.match(TokenType.RPAREN):
            param_name = self.expect(TokenType.IDENTIFIER).value
            param_type = None
            if self.consume(TokenType.COLON):
                param_type = self.parse_type()
                param_types[param_name] = param_type
            params.append(param_name)
            while self.consume(TokenType.COMMA):
                param_name = self.expect(TokenType.IDENTIFIER).value
                param_type = None
                if self.consume(TokenType.COLON):
                    param_type = self.parse_type()
                    param_types[param_name] = param_type
                params.append(param_name)
        self.expect(TokenType.RPAREN)
        return_type = None
        if self.consume(TokenType.ARROW):
            return_type = self.parse_type()
        body = self.parse_block_statement()
        return FunctionDecl(name, params, body, return_type, param_types)
    
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
        elif not self.match(TokenType.SEMICOLON):
            init = self.parse_expression()
            self.consume(TokenType.SEMICOLON)
        else:
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
            elif self.consume(TokenType.DOT):
                member = self.expect(TokenType.IDENTIFIER).value
                expr = MemberAccess(expr, member)
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
