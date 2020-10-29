#!/usr/bin/env python3

"""
Dice roller CLI Script.

Makes it easy to roll dice via command line and is able handle the basic
math functions, including parens!

Grammar:
Digit ::=  [1234567890]
Number ::= ( '-' )? Digit Digit* ( '.' Digit Digit*)?
AddOrSub ::= Number ('+' | '-') Number
MultOrDiv ::= Number ('*' | '/' | '%') Number
Exponent ::= Number '**' Number
PercentDie ::= Number? 'd%'
Die ::= Number? 'd' Number
Dice ::= Die | PercentDie
Expression ::= (Exponent | Dice | MultOrDiv | AddOrSub)
Parens ::= '(' Expression ')'
Main ::= (Parens | Expression)*

Website used to do railroad diagrams: https://www.bottlecaps.de/rr/ui

Input -> Output
1d20 -> 19
1d8 + 3d6 + 5 -> 15
d% -> 42
<Nothing> -> 14 (Rolls a d20)
etc.
"""

import math
from random import randint
from typing import Union

import pyparsing as pp


def _roll_dice(num_dice: Union[int, float],
               sides: Union[int, float], debug_print: bool = False) -> int:
    """Calculate value of dice roll notation."""
    starting_num_dice = num_dice
    starting_sides = sides

    # If it's the case that we were given a dice with negative sides,
    # then that doesn't mean anything in the real world. I cannot
    # for the life of me figure out a possible scenario where that
    # would make sense. We will just error out.
    if sides < 0:
        raise Exception('The sides of a die must be positive or zero.')

    result_type = type(num_dice)

    if result_type == float:
        sides *= num_dice

        # 0.5d20 == 1d10, so, after we've changed the value,
        # we need to set the left value to 1.
        num_dice = 1

    result_is_negative = num_dice < 0

    if result_is_negative:
        num_dice = abs(num_dice)

    sides = math.ceil(sides)

    rolls = [
        randint(1, sides) if sides != 0 else 0 for _ in range(num_dice)
    ]

    rolls_total = sum(rolls)

    if result_is_negative:
        rolls_total *= -1

    if debug_print:

        debug_message = [
            f'{starting_num_dice}d{starting_sides}:',
            f'{rolls_total}',
            (f'{rolls}' if len(rolls) > 1 else '')
        ]

    return {rolls_total, debug_message}


def _parse_and_calculate(expression: str = '') -> int:
    """Parse and calculate the total of a given expression."""
    result = 0
    return result


def roll(expression: str = '') -> str:
    """Evalute a string for dice and mathematical operations and calculate."""
    input_had_bad_chars: bool = len(
        expression.strip("0123456789d-/*() %+.!")) > 0

    if input_had_bad_chars:
        raise Exception('Input contained invalid characters.')

    if expression.strip() == '':
        expression = "1d20"

    return _parse_and_calculate(expression)


if __name__ == "__main__":
    print(roll("1d20"))
