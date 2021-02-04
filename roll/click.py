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

from typing import List

import click
from roll import roll


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

    click.echo(roll(command_input, verbose))


if __name__ == '__main__':
    roll_cli()
