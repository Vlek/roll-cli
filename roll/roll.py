#!/usr/bin/env python3

"""
Dice roller CLI Script.

Makes it easy to roll dice via command line and is able handle the basic
math functions, including parens!

Input -> Output
1d20 -> 19
1d8 + 3d6 + 5 -> 15
d% -> 42
<Nothing> -> 14 (Rolls a d20)
etc.
"""

import roll.diceparser as diceparser

_DICE_PARSER = diceparser.DiceParser()


def _parse_and_calculate(expression: str = '1d20', debug: bool = False) -> int:
    """Parse and calculate the total of a given expression."""
    if debug:
        print(f"Parsing expression: {expression}")

    result = _DICE_PARSER.evaluate(expression)

    return result


def roll(expression: str = '', debug: bool = False) -> str:
    """Evalute a string for dice and mathematical operations and calculate."""
    input_had_bad_chars: bool = len(
        expression.strip("0123456789d-/*() %+.!")) > 0

    if input_had_bad_chars:
        raise Exception('Input contained invalid characters.')

    if expression.strip() == '':
        expression = "1d20"

    return _parse_and_calculate(expression, debug)


if __name__ == "__main__":
    print(roll("1d20"))
