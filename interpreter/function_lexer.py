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
        return ('ERROR', exc)


# if __name__ == '__main__':
#    print(lex(input()))
