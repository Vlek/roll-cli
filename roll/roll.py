#!/usr/bin/env python3

"""
Dice roller CLI Script.

Makes it easy to roll dice via command line and is able handle the basic
math functions, including parens!

1d20 -> 19
1d8 + 3d6 + 5 -> 15
d% -> 42
<Nothing> -> 14 (Rolls a d20)
etc.
"""

import math
from random import randint
from typing import List, Union

import click
import parsley

PRINT_DEBUG_OUTPUT = False


def _roll_dice(left: Union[int, float, bool],
               right: Union[int, float], debug_print: bool = False) -> int:
    """Calculate value of dice roll notation."""
    starting_left_value = left if not isinstance(left, bool) else 1

    # If it's the case that we were given a dice with negative sides,
    # then that doesn't mean anything in the real world. I cannot
    # for the life of me figure out a possible scenario where that
    # would make sense. We will just error out.
    if right < 0:
        raise Exception('The sides of a die must be positive or zero.')

    result_type = type(left)

    if result_type == float:
        right *= left

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
        left = 1

    result_is_negative = left < 0

    if result_is_negative:
        left = abs(left)

    right = math.ceil(right)

    rolls = [
        randint(1, right) if right != 0 else 0 for _ in range(left)
    ]

    rolls_total = sum(rolls)

    if result_is_negative:
        rolls_total *= -1

    if debug_print:

        debug_message = [
            f'{starting_left_value}d{right}:',
            f'{rolls_total}',
            (f'{rolls}' if len(rolls) > 1 else '')
        ]

        click.echo(' '.join(debug_message))

    return rolls_total


def calculate(start: int, pairs: List[Union['str', 'int']]) -> int:
    """Calculate the total value based on operation."""
    result = start
    global PRINT_DEBUG_OUTPUT

    print(f'Start: {start}, pairs: {pairs}')

    for opr, value in pairs:

        # This is for the case where it's like "6 +" without a right-hand side:
        if isinstance(value, bool):
            raise Exception('An operation was missing a right-hand side')

        # This is for the missing left-hand side:
        if isinstance(start, bool):
            # If it's not a dice, then that's a problem.
            if opr != 'd':
                raise Exception("An operation was missing a left-hand side")
            start = 1

        if opr == '+':
            result += value
        elif opr == '-':
            result -= value
        elif opr == '*':
            result *= value
        elif opr == '/':
            result /= value
        elif opr == '%':
            result %= value
        elif opr == '**':
            result **= value
        elif opr == 'd':
            result = _roll_dice(result, value, PRINT_DEBUG_OUTPUT)

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
    mul_div = ws (mul | div | mod)
    dice = ws (percentage_die | die)

    expr = expr2:left add_sub*:right -> calculate(left, right)
    expr2 = expr3:left mul_div*:right -> calculate(left, right)
    expr3 =  expr4:left dice*:right -> calculate(left, right)
    expr4 = (value|ws):left exp*:right -> calculate(left, right)
    """,
    {"calculate": calculate, 'handle_factorial': math.factorial}
)


def roll(expression: str = '') -> str:
    """Evalute a string for dice and mathematical operations and calculate."""
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
def roll_cli(expression: List[str] = None, verbose: bool = False) -> None:
    """
    CLI dice roller.

    Usage: roll [EXPRESSION]
    A cli command for rolling dice and adding modifiers in the
    same fashion as the node.js version on npm.

    Examples:
        roll                - Rolls 1d20

        roll <expression>   - Rolls all dice + does math

    Expressions:
        1d20                - Rolls one 20-sided die

        d20                 - Does not require a '1' in front of 'd'

        d%                  - Rolls 1d100

        d8 + 3d6 + 5        - Rolls 1d8, 3d6, and adds everything together

        (1d4)d6             - Rolls 1d4 d6 die
    """
    command_input = ' '.join(expression) if expression is not None else ''

    global PRINT_DEBUG_OUTPUT
    PRINT_DEBUG_OUTPUT = verbose

    click.echo(roll(command_input))


if __name__ == '__main__':
    roll_cli()
