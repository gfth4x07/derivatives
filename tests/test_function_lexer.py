import decimal

import pytest

from interpreter import function_lexer


@pytest.mark.parametrize('test_input, expected_tag', [
    ('1', 'NUMBER'),
    ('1.5', 'NUMBER'),
    ('0.2', 'NUMBER'),
    ('+', 'ADD'),
    ('/', 'DIVIDE'),
    ('-', 'SUBTRACT'),
    ('*', 'MULTIPLY'),
    ('^', 'POW'),
    ('sqrt', 'SQRT'),
    ('(', 'OPAREN'),
    (')', 'CPAREN'),
    ('sin', 'SIN'),
    ('cos', 'COS'),
    ('tan', 'TAN'),
    ('cotan', 'COTAN'),
    ('sec', 'SEC'),
    ('csc', 'COSEC'),
    ('foo', 'VARIABLE'),
])
def test_all_tags(test_input, expected_tag):
    assert function_lexer.lex(test_input)[0][0] == expected_tag


def test_empty():
    assert function_lexer.lex('') == []


def test_spaces():
    assert function_lexer.lex('    ') == []


def test_optional_function_name():
    assert function_lexer.lex('f(x) = ') == []
    assert function_lexer.lex('g(x)=') == []


def test_number_is_handle_as_decimal():

    result = function_lexer.lex('f(x) = 1')

    assert len(result) == 1
    assert isinstance(result[0], tuple)

    result = result[0]
    tag, value = result

    assert isinstance(value, decimal.Decimal)
    assert value == 1


@pytest.mark.parametrize('function,expected', [
    ('f(x) = 1', [('NUMBER', decimal.Decimal('1'))]),
    ('f(x) = x', [('VARIABLE', 'x')]),
    ('f(x) = x + 1',
     [('VARIABLE', 'x'), ('ADD',), ('NUMBER', decimal.Decimal(1))]),
    ('f(x) = x^2',
     [('VARIABLE', 'x'), ('POW',), ('NUMBER', decimal.Decimal(2))]),
    ('f(x) = sin(x)',
     [('SIN',), ('OPAREN',), ('VARIABLE', 'x'), ('CPAREN',)]),
    ('f(x) = sqrt(x)',
     [('SQRT',), ('OPAREN',), ('VARIABLE', 'x'), ('CPAREN',)]),
])
def test_simple_functions(function, expected):
    assert function_lexer.lex(function) == expected
