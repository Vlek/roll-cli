#!/usr/bin/env python3
"""Dice roller CLI Script.

Makes it easy to roll dice via command line and is able handle the basic
math functions, including parens!

1d20 -> 19
1d8 + 3d6 + 5 -> 15
d% -> 42
<Nothing> -> 14 (Rolls a d20)
etc.
"""
from typing import List
from typing import Union

import click

from . import roll
from roll_cli.parser.types import EvaluationResults
from roll_cli.parser.types import RollOption


@click.command()
@click.argument("expression", nargs=-1, type=str)
@click.option(
    "-m",
    "--minimum",
    "roll_option",
    flag_value=RollOption.Minimum,
    help="Set dice to always roll the minimum value",
)
@click.option(
    "-M",
    "--maximum",
    "roll_option",
    flag_value=RollOption.Maximum,
    help="Set dice to always roll the maximum value",
)
@click.option(
    "-v",
    "--verbose",
    "verbose",
    is_flag=True,
    help="Print the individual die roll values",
)
def main(
    expression: List[str],
    roll_option: RollOption = RollOption.Normal,
    verbose: bool = False,
) -> None:
    """CLI dice roller.

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
    command_input = " ".join(expression)

    result: Union[int, float, EvaluationResults] = roll(
        command_input,
        verbose,
        roll_option,
    )

    click.echo(result)
