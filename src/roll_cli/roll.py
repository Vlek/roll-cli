#!/usr/bin/env python3
"""Dice roller CLI Script.

Makes it easy to roll dice via command line and is able handle the basic
math functions, including parens!

Input -> Output
1d20 -> 19
1d8 + 3d6 + 5 -> 15
d% -> 42
<Nothing> -> 14 (Rolls a d20)
etc.
"""
from typing import Union

from .parser.diceparser import DiceParser
from .parser.types import EvaluationResults
from .parser.types import RollOption

_DICE_PARSER = DiceParser()

GOOD_CHARS: str = "0123456789d-/*() %+.!^pPiIeEsSqQrRtTkKxX<>="


def roll(
    expression: str = "",
    verbose: bool = False,
    roll_option: RollOption = RollOption.Normal,
) -> Union[int, float, EvaluationResults]:
    """Evalute a string for dice and mathematical operations and calculate."""
    input_had_bad_chars: bool = len(expression.strip(GOOD_CHARS)) > 0

    if input_had_bad_chars:
        raise ValueError("Input contained invalid characters.")

    if expression.strip() == "":
        expression = "1d20"

    result: Union[int, float, EvaluationResults] = _DICE_PARSER.evaluate(
        expression, roll_option
    )

    if verbose:
        return result

    return result.total if isinstance(result, EvaluationResults) else result


if __name__ == "__main__":
    print(roll("1d20"))
