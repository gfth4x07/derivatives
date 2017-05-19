import decimal

import pytest

from parser import functions


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
    assert functions.lex(test_input)[0][0] == expected_tag


def test_empty():
    assert functions.lex('') == []


def test_spaces():
    assert functions.lex('    ') == []


def test_optional_function_name():
    assert functions.lex('f(x) = ') == []
    assert functions.lex('g(x)=') == []


def test_number_is_handle_as_decimal():

    result = functions.lex('f(x) = 1')

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
    assert functions.lex(function) == expected


def test_meta_function_object_dunder_hash():

    function_x_plus_2 = functions.MetaFunction(functions.lex('f(x)=x + 2'))

    assert hash(function_x_plus_2) == hash(tuple(functions.lex('f(x)=x + 2')))


def test_meta_function_dunder_equals():

    function_x_plus_2 = functions.MetaFunction(functions.lex('f(x)=x + 2'))

    assert function_x_plus_2.body == functions.lex('f(x)=x + 2')


def test_meta_function_as_dict_key():

    function_x_plus_2 = functions.MetaFunction(functions.lex('f(x)=x + 2'))

    function_map = {function_x_plus_2: 'function_x_plus_2'}

    assert function_map[functions.MetaFunction(functions.lex('f(x)=x + 2'))]


@pytest.mark.parametrize('metafunction,test_input,expected', [
    (functions.Constant, 'f(x) = 1', 'CONSTANT FUNCTION'),
    (functions.Identity, 'f(x) = x', 'IDENTITY FUNCTION')
])
def test_function_when_input_does_represent_expected_one(metafunction, test_input, expected):  # noqa

    function_x = metafunction(functions.lex(test_input))

    assert hash(function_x) == hash(expected)


@pytest.mark.parametrize('metafunction,test_input,expected', [
    (functions.Constant, 'f(x) = x', 'a constant function'),
    (functions.Identity, 'f(x) = 1', 'an identity function')
])
def test_function_when_input_does_not_represent_expected_one(metafunction, test_input, expected):  # noqa

    function_x = metafunction(functions.lex(test_input))
    with pytest.raises(ValueError) as e_info:
        hash(function_x)

    assert str(e_info.value) == 'It is not {}'.format(expected)
