from click.testing import CliRunner

import cli
from parser import functions as functions_parser


def test_function_parser_with_valid_input():

    runner = CliRunner()
    result = runner.invoke(cli.parse_function, ['f(x) = x ^ 2 + 1'])

    assert result.exit_code == 0
    assert result.output == '{}\n'.format(functions_parser.lex('f(x) = x ^ 2 + 1'))  # noqa


def test_function_parser_when_input_is_invalid():

    runner = CliRunner()
    result = runner.invoke(cli.parse_function, [','])

    assert result.exit_code == 0
    assert 'ERROR' in result.output
    assert 'unexpected character' in result.output
