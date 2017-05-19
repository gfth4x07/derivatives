#!/usr/bin/env python
# -*- coding: utf-8 -*-

import decimal

from flexicon import FlexiconError, Lexer


EXPRESSION_LEXER = Lexer().simple(
    (r'[ \t]+', lambda: None),
    (r'.*\w?\=\w?', lambda: None),  # e.g:'f(x) = '
    (r'\+', lambda: ('ADD',)),
    (r'\/', lambda: ('DIVIDE',)),
    (r'\-', lambda: ('SUBTRACT',)),
    (r'\*', lambda: ('MULTIPLY',)),
    (r'\^', lambda: ('POW',)),
    (r'sqrt', lambda: ('SQRT',)),
    (r'\(', lambda: ('OPAREN',)),
    (r'\)', lambda: ('CPAREN',)),
    (r'sin\w?', lambda: ('SIN',)),
    (r'cos\w?', lambda: ('COS',)),
    (r'tan\w?', lambda: ('TAN',)),
    (r'cotan\w?', lambda: ('COTAN',)),
    (r'sec\w?', lambda: ('SEC',)),
    (r'csc\w?', lambda: ('COSEC',)),
    (r'[\+\-]?([0-9]*\.?[0-9]+)', lambda n: ('NUMBER', decimal.Decimal(n))),
    (r'([a-zA-Z]+)', lambda c: ('VARIABLE', c)),
)


def lex(text):

    try:
        return EXPRESSION_LEXER.lex(text)
    except FlexiconError as exc:
        return ('ERROR', str(exc))


class MetaFunction:

    def __init__(self, body):
        self.body = body

    def __hash__(self):
        return hash(tuple(self.body))

    def __eq__(self, function):
        return hash(self) == hash(function)


class Constant(MetaFunction):

    def __hash__(self):

        if not(len(self.body) == 1 and self.body[0][0] == 'NUMBER'):
            raise ValueError('It is not a constant function')
        return hash('CONSTANT FUNCTION')


class Identity(MetaFunction):

    def __hash__(self):

        if not(len(self.body) == 1 and self.body[0][0] == 'VARIABLE'):
            raise ValueError('It is not an identity function')
        return hash('IDENTITY FUNCTION')
