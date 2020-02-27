#!/usr/bin/env python3

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
import functools
import math
import parsley
from random import randint
from typing import List

_print_debug_output = False


def calculate(start, pairs):
    result = start
    global _print_debug_output

    # print(f'Start: {start}, pairs: {pairs}')

    for op, value in pairs:

        # This is for the case where it's like "6 +" without a right-hand side:
        if type(value) == bool:
            raise Exception('An operation was missing a right-hand side')

        # This is for the missing left-hand side:
        if type(start) == bool:

            # If it's not a dice, then that's a problem.
            if op != 'd':
                raise Exception("An operation was missing a left-hand side")
            start = 1

        if op == '+':
            result += value
        elif op == '-':
            result -= value
        elif op == '*':
            result *= value
        elif op == '/':
            result /= value
        elif op == '%':
            result %= value
        elif op == '**':
            result **= value
        elif op == 'd':

            # If it's the case that we were given a dice with negative sides,
            # then that doesn't mean anything in the real world. I cannot
            # for the life of me figure out a possible scenario where that
            # would make sense. We will just error out.
            if 0 > value:
                raise Exception('The sides of a die must be positive or zero.')

            result_type = type(result)

            if result_type == float:
                value *= result

            # When we use a dice expression without explicitly expressing
            # how many to roll, we want to specifically state that it's
            # supposed to be a 1. It's for some reason returning a boolean
            # true when it finds the whitespace or nothing character first
            # instead of a value.
            #
            # This is also the case when we have a floating point number
            # as the number of dice that we will roll. 0.5d20 == 1d10, so,
            # after we've changed the value, we need to reset the start.
            if result_type in [bool, float]:
                result = 1

            result_is_negative = 0 > result

            if result_is_negative:
                result = abs(result)

            value = math.ceil(value)

            rolls = [
                randint(1, value) if value != 0 else 0 for _ in range(result)
            ]

            rolls_total = sum(rolls)

            if result_is_negative:
                rolls_total *= -1

            if _print_debug_output:

                debug_message = [
                    f'{"-" if result_is_negative else ""}{start}d{value}:',
                    f'{rolls_total}',
                    (f'{rolls}' if len(rolls) > 1 else '')
                ]

                click.echo(' '.join(debug_message))

            result = rolls_total

    return result


expression_grammar = parsley.makeGrammar(
    """
    number = ws <digit+>:ds ws -> int(ds)
    neg_number = '-' number:n -> n * -1
    float = <number '.' number>:f -> float(f)
    neg_float = <neg_number '.' number>:nf -> float(nf)
    factorial = (number | neg_number):n '!' -> handle_factorial(n)
    parens = '(' ws expr:e ws ')' -> e
    value = neg_float | float | factorial | neg_number | number | parens

    add = '+' ws expr2:n -> ('+', n)
    sub = '-' ws expr2:n -> ('-', n)
    mul = '*' ws expr3:n -> ('*', n)
    div = '/' ws expr3:n -> ('/', n)
    mod = '%' ws expr3:n -> ('%', n)
    exp = '**' ws value:n -> ('**', n)
    percentage_die = 'd' ws '%' -> ('d', 100)
    die = 'd' ws expr4:n -> ('d', n)

    add_sub = ws (add | sub)
    mul_div = ws (mod | mul | div)
    dice = ws (percentage_die | die)

    expr = expr2:left add_sub*:right -> calculate(left, right)
    expr2 = expr3:left mul_div*:right -> calculate(left, right)
    expr3 =  expr4:left dice*:right -> calculate(left, right)
    expr4 = (value|ws):left exp*:right -> calculate(left, right)
    """,
    {"calculate": calculate, 'handle_factorial': math.factorial}
)


def roll(expression='') -> str:

    input_had_bad_chars = len(expression.strip("0123456789d-/*() %+.!")) > 0

    if input_had_bad_chars:
        raise Exception('Input contained invalid characters.')

    if expression.strip() == '':
        expression = "1d20"

    return expression_grammar(expression).expr()


@click.command()
@click.argument('expression', nargs=-1, type=str)
@click.option('-v', '--verbose', 'verbose', is_flag=True,
              help='Print the individual die roll values')
def roll_cli(expression: List[str], verbose: bool) -> None:
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

    # TODO: Make all output be returned

    command_input = ' '.join(expression)

    global _print_debug_output
    _print_debug_output = verbose

    click.echo(roll(command_input))


if __name__ == '__main__':
    roll_cli()
