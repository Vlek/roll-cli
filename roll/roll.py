#!/usr/bin/env python

"""
Dice roller CLI Script

Makes it easy to roll dice via command line and is able handle the basic
math functions, including parens!

1d20 -> 19
1d8 + 3d6 + 5 -> 15
d% -> 42
<Nothing> -> 14 (Rolls a d20)
etc.
"""

import click
import parsley
from random import randint

_print_debug_output = False


def calculate(start, pairs):
    result = start
    global _print_debug_output

    for op, value in pairs:
        if op == '+':
            result += value
        elif op == '-':
            result -= value
        elif op == '*':
            result *= value
        elif op == '/':
            result /= value
        elif op == 'd':

            # In the the case that we're rolling dice, the starting
            # number indicates the number of dice that we're rolling, not
            # the initial value that we're starting with.
            result = 0

            # When we use a dice expression without explicitly expressing
            # how many to roll, we want to specifically state that it's
            # supposed to be a 1. It's for some reason returning a boolean
            # true when it finds the whitespace or nothing character first
            # instead of a value.
            start = start if type(start) == int else 1

            rolls = [randint(1, value) for _ in range(start)]
            rolls_total = sum(rolls)

            if _print_debug_output:
                click.echo(
                    f"{start}d{value}: {rolls_total} " +
                    (f"{rolls}" if len(rolls) > 1 else '')
                )

            result += rolls_total

    return result


expression_grammar = parsley.makeGrammar("""
    number = <digit+>:ds -> int(ds)
    parens = '(' ws expr:e ws ')' -> e
    value = number | parens

    add = '+' ws expr2:n -> ('+', n)
    sub = '-' ws expr2:n -> ('-', n)
    mul = '*' ws expr3:n -> ('*', n)
    div = '/' ws expr3:n -> ('/', n)
    percentage_die = 'd' ws '%' -> ('d', 100)
    die = 'd' ws value:n -> ('d', n)

    add_sub = ws (add | sub)
    mul_div = ws (mul | div)
    dice = ws (die | percentage_die)

    expr = expr2:left add_sub*:right -> calculate(left, right)
    expr2 = expr3:left mul_div*:right -> calculate(left, right)
    expr3 = (value|ws):left dice*:right -> calculate(left, right)
""", {"calculate": calculate})


@click.command()
@click.argument('expression', nargs=-1, type=str)
@click.option('-v', '--verbose', 'verbose', is_flag=True,
              help='Print the individual die roll values')
def roll(expression: [str], verbose: bool) -> None:
    """
    A cli command for rolling dice and adding modifiers in the
    same fashion as the node.js version on npm.

    Usage:

        roll <nothing>      - Rolls 1d20

        roll <expression>   - Rolls all dice + does math

    Expressions:

        1d20                - Rolls one 20-sided die

        d20                 - Does not require a '1' in front of 'd'

        d%                  - Rolls 1d100

        d8 + 3d6 + 5        - Rolls 1d8, 3d6, and adds everything together

        (1d4)d6             - Rolls 1d4 d6 die
    """

    # TODO: Handle negative numbers

    command_input = ' '.join(expression)

    input_had_bad_chars = len(command_input.strip("0123456789d\-/*() %+")) > 0

    if input_had_bad_chars:
        raise Exception('Input contained invalid characters.')

    if command_input == '':
        command_input = "1d20"

    global _print_debug_output
    _print_debug_output = verbose

    click.echo(expression_grammar(command_input).expr())


if __name__ == '__main__':
    roll()
