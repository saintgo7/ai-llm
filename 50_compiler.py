"""
50. Simple Compiler - 간단한 컴파일러 (Lexer, Parser, Interpreter)
"""
import re
from enum import Enum
from typing import List

# Token Types
class TokenType(Enum):
    NUMBER = 'NUMBER'
    PLUS = 'PLUS'
    MINUS = 'MINUS'
    MUL = 'MUL'
    DIV = 'DIV'
    LPAREN = 'LPAREN'
    RPAREN = 'RPAREN'
    IDENT = 'IDENT'
    ASSIGN = 'ASSIGN'
    SEMICOLON = 'SEMICOLON'
    EOF = 'EOF'
    PRINT = 'PRINT'
    IF = 'IF'
    ELSE = 'ELSE'
    LBRACE = 'LBRACE'
    RBRACE = 'RBRACE'
    EQ = 'EQ'
    LT = 'LT'
    GT = 'GT'

class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __repr__(self):
        return f'Token({self.type}, {self.value})'

class Lexer:
    """렉서 (토큰화)"""

    def __init__(self, text):
        self.text = text
        self.pos = 0

    def tokenize(self):
        """텍스트를 토큰 리스트로 변환"""
        tokens = []

        while self.pos < len(self.text):
            # 공백 건너뛰기
            if self.text[self.pos].isspace():
                self.pos += 1
                continue

            # 숫자
            if self.text[self.pos].isdigit():
                num = ''
                while self.pos < len(self.text) and (self.text[self.pos].isdigit() or self.text[self.pos] == '.'):
                    num += self.text[self.pos]
                    self.pos += 1
                tokens.append(Token(TokenType.NUMBER, float(num)))
                continue

            # 식별자 및 키워드
            if self.text[self.pos].isalpha():
                ident = ''
                while self.pos < len(self.text) and (self.text[self.pos].isalnum() or self.text[self.pos] == '_'):
                    ident += self.text[self.pos]
                    self.pos += 1

                # 키워드 체크
                if ident == 'print':
                    tokens.append(Token(TokenType.PRINT, ident))
                elif ident == 'if':
                    tokens.append(Token(TokenType.IF, ident))
                elif ident == 'else':
                    tokens.append(Token(TokenType.ELSE, ident))
                else:
                    tokens.append(Token(TokenType.IDENT, ident))
                continue

            # 연산자 및 구두점
            char = self.text[self.pos]

            if char == '+':
                tokens.append(Token(TokenType.PLUS, '+'))
            elif char == '-':
                tokens.append(Token(TokenType.MINUS, '-'))
            elif char == '*':
                tokens.append(Token(TokenType.MUL, '*'))
            elif char == '/':
                tokens.append(Token(TokenType.DIV, '/'))
            elif char == '(':
                tokens.append(Token(TokenType.LPAREN, '('))
            elif char == ')':
                tokens.append(Token(TokenType.RPAREN, ')'))
            elif char == '{':
                tokens.append(Token(TokenType.LBRACE, '{'))
            elif char == '}':
                tokens.append(Token(TokenType.RBRACE, '}'))
            elif char == ';':
                tokens.append(Token(TokenType.SEMICOLON, ';'))
            elif char == '=' and self.pos + 1 < len(self.text) and self.text[self.pos + 1] == '=':
                tokens.append(Token(TokenType.EQ, '=='))
                self.pos += 1
            elif char == '=':
                tokens.append(Token(TokenType.ASSIGN, '='))
            elif char == '<':
                tokens.append(Token(TokenType.LT, '<'))
            elif char == '>':
                tokens.append(Token(TokenType.GT, '>'))

            self.pos += 1

        tokens.append(Token(TokenType.EOF, None))
        return tokens

class Parser:
    """파서 (AST 생성)"""

    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def current_token(self):
        return self.tokens[self.pos]

    def eat(self, token_type):
        if self.current_token().type == token_type:
            self.pos += 1
        else:
            raise Exception(f"Expected {token_type}, got {self.current_token().type}")

    def parse(self):
        """프로그램 파싱"""
        statements = []
        while self.current_token().type != TokenType.EOF:
            statements.append(self.parse_statement())
        return statements

    def parse_statement(self):
        """문장 파싱"""
        if self.current_token().type == TokenType.PRINT:
            return self.parse_print()
        elif self.current_token().type == TokenType.IF:
            return self.parse_if()
        elif self.current_token().type == TokenType.IDENT:
            return self.parse_assignment()
        else:
            raise Exception(f"Unexpected token: {self.current_token()}")

    def parse_print(self):
        """print 문 파싱"""
        self.eat(TokenType.PRINT)
        self.eat(TokenType.LPAREN)
        expr = self.parse_expression()
        self.eat(TokenType.RPAREN)
        self.eat(TokenType.SEMICOLON)
        return ('print', expr)

    def parse_if(self):
        """if 문 파싱"""
        self.eat(TokenType.IF)
        self.eat(TokenType.LPAREN)
        condition = self.parse_expression()
        self.eat(TokenType.RPAREN)
        self.eat(TokenType.LBRACE)

        then_stmts = []
        while self.current_token().type != TokenType.RBRACE:
            then_stmts.append(self.parse_statement())
        self.eat(TokenType.RBRACE)

        else_stmts = []
        if self.current_token().type == TokenType.ELSE:
            self.eat(TokenType.ELSE)
            self.eat(TokenType.LBRACE)
            while self.current_token().type != TokenType.RBRACE:
                else_stmts.append(self.parse_statement())
            self.eat(TokenType.RBRACE)

        return ('if', condition, then_stmts, else_stmts)

    def parse_assignment(self):
        """대입문 파싱"""
        var_name = self.current_token().value
        self.eat(TokenType.IDENT)
        self.eat(TokenType.ASSIGN)
        expr = self.parse_expression()
        self.eat(TokenType.SEMICOLON)
        return ('assign', var_name, expr)

    def parse_expression(self):
        """표현식 파싱"""
        left = self.parse_term()

        while self.current_token().type in [TokenType.PLUS, TokenType.MINUS, TokenType.EQ, TokenType.LT, TokenType.GT]:
            op = self.current_token().type
            self.eat(op)
            right = self.parse_term()
            left = (op.value, left, right)

        return left

    def parse_term(self):
        """항 파싱"""
        left = self.parse_factor()

        while self.current_token().type in [TokenType.MUL, TokenType.DIV]:
            op = self.current_token().type
            self.eat(op)
            right = self.parse_factor()
            left = (op.value, left, right)

        return left

    def parse_factor(self):
        """인자 파싱"""
        token = self.current_token()

        if token.type == TokenType.NUMBER:
            self.eat(TokenType.NUMBER)
            return ('number', token.value)

        elif token.type == TokenType.IDENT:
            self.eat(TokenType.IDENT)
            return ('var', token.value)

        elif token.type == TokenType.LPAREN:
            self.eat(TokenType.LPAREN)
            expr = self.parse_expression()
            self.eat(TokenType.RPAREN)
            return expr

        raise Exception(f"Unexpected token: {token}")

class Interpreter:
    """인터프리터 (실행)"""

    def __init__(self):
        self.variables = {}

    def execute(self, ast):
        """AST 실행"""
        for statement in ast:
            self.execute_statement(statement)

    def execute_statement(self, stmt):
        """문장 실행"""
        if stmt[0] == 'print':
            value = self.evaluate(stmt[1])
            print(value)

        elif stmt[0] == 'assign':
            var_name = stmt[1]
            value = self.evaluate(stmt[2])
            self.variables[var_name] = value

        elif stmt[0] == 'if':
            condition = self.evaluate(stmt[1])
            if condition:
                for s in stmt[2]:
                    self.execute_statement(s)
            else:
                for s in stmt[3]:
                    self.execute_statement(s)

    def evaluate(self, expr):
        """표현식 평가"""
        if expr[0] == 'number':
            return expr[1]

        elif expr[0] == 'var':
            return self.variables.get(expr[1], 0)

        elif expr[0] == 'PLUS':
            return self.evaluate(expr[1]) + self.evaluate(expr[2])

        elif expr[0] == 'MINUS':
            return self.evaluate(expr[1]) - self.evaluate(expr[2])

        elif expr[0] == 'MUL':
            return self.evaluate(expr[1]) * self.evaluate(expr[2])

        elif expr[0] == 'DIV':
            return self.evaluate(expr[1]) / self.evaluate(expr[2])

        elif expr[0] == 'EQ':
            return self.evaluate(expr[1]) == self.evaluate(expr[2])

        elif expr[0] == 'LT':
            return self.evaluate(expr[1]) < self.evaluate(expr[2])

        elif expr[0] == 'GT':
            return self.evaluate(expr[1]) > self.evaluate(expr[2])

        raise Exception(f"Unknown expression: {expr}")

if __name__ == '__main__':
    print("=== Simple Compiler ===\n")

    # 테스트 프로그램
    program = """
        x = 10;
        y = 20;
        z = x + y * 2;
        print(z);

        if (z > 40) {
            print(100);
        } else {
            print(0);
        }
    """

    print("Source Code:")
    print(program)
    print("\n" + "="*50 + "\n")

    # 1. Lexical Analysis (Lexing)
    print("1. Lexical Analysis (Tokens):")
    lexer = Lexer(program)
    tokens = lexer.tokenize()
    for token in tokens[:20]:  # 처음 20개만 표시
        print(f"  {token}")
    print()

    # 2. Syntax Analysis (Parsing)
    print("2. Syntax Analysis (AST):")
    parser = Parser(tokens)
    ast = parser.parse()
    for i, stmt in enumerate(ast, 1):
        print(f"  Statement {i}: {stmt}")
    print()

    # 3. Execution (Interpretation)
    print("3. Execution Output:")
    interpreter = Interpreter()
    interpreter.execute(ast)

    print(f"\nFinal variables: {interpreter.variables}")

    print("\n=== Compiler Complete ===")
