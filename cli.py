#!/usr/bin/env python

import click

from parser import functions as functions_parser


@click.group()
def parser():
    pass


@parser.group()
def functions():
    pass


@functions.command()
@click.argument('function', click.STRING)
def parse_function(function):
    click.echo(functions_parser.lex(function))


if __name__ == '__main__':
    parser()
