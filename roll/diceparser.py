#!/user/bin/env python3

"""
Dice rolling PyParser grammar.

Grammar:
Digit ::= [1234567890]
Number ::= ( '-' )? Digit Digit* ( '.' Digit Digit*)?
Add ::= Number '+' Number
Sub ::= Number '-' Number
AddOrSub ::= Add | Sub
Mult ::= Number '*' Number
Div ::= Number '/' Number
Mod ::= Number '%' Number
IntDiv ::= Number '//' Number
MultOrDiv ::= Mult | Div | Mod | IntDiv
Exponent ::= Number '**' Number
PercentDie ::= Number? 'd%'
Die ::= Number? 'd' Number
Dice ::= Die | PercentDie
Parens ::= Number? '(' Expression ')'
Expression ::= (Parens | Exponent | Dice | MultOrDiv | AddOrSub | Number)+
Main ::= Expression

Website used to do railroad diagrams: https://www.bottlecaps.de/rr/ui
"""

from math import ceil, e, factorial, floor, pi
from operator import add, floordiv, mod, mul, sub, truediv
from random import randint
from typing import List, Union

from pyparsing import (CaselessKeyword, Forward, ParserElement, ParseResults,
                       Regex, oneOf, opAssoc, operatorPrecedence,
                       pyparsing_common)

ParserElement.enablePackrat()


def _roll_dice(
        num_dice: Union[int, float],
        sides: Union[int, float],
        debug_print: bool = False) -> Union[int, float]:
    """Calculate value of dice roll notation."""
    starting_num_dice = num_dice
    starting_sides = sides

    # If it's the case that we were given a dice with negative sides,
    # then that doesn't mean anything in the real world. I cannot
    # for the life of me figure out a possible scenario where that
    # would make sense. We will just error out.
    if sides < 0:
        raise ValueError('The sides of a die must be positive or zero.')

    if isinstance(num_dice, float):
        sides *= num_dice

        # 0.5d20 == 1d10, so, after we've changed the value,
        # we need to set the left value to 1.
        num_dice = 1

    result_is_negative = num_dice < 0

    if result_is_negative:
        num_dice = abs(num_dice)

    sides = ceil(sides)

    rolls = [
        randint(1, sides) for _ in range(num_dice)
    ] if sides != 0 else []

    rolls_total = sum(rolls)

    if result_is_negative:
        rolls_total *= -1

    if debug_print:
        debug_message = [
            f'{starting_num_dice}d{starting_sides}:',
            f'{rolls_total}',
            (f'{rolls}' if len(rolls) > 1 else '')
        ]

    return rolls_total


class DiceParser:
    """Parser for evaluating dice strings."""

    operations = {
        "+": add,
        "-": sub,
        "*": mul,
        "/": truediv,
        "//": floordiv,
        "%": mod,
        "^": pow,
        "**": pow,
        "d": _roll_dice,
        "!": factorial
    }

    constants = {
        "pi": pi,
        "e": e
    }

    def __init__(self: "DiceParser") -> None:
        """Initialize a parser to handle dice strings."""
        self._parser = self._create_parser()

    @staticmethod
    def _create_parser() -> Forward:
        """Create an instance of a dice roll string parser."""
        atom = (
            pyparsing_common.number |
            oneOf("d% D%") |
            CaselessKeyword("pi") |
            CaselessKeyword("e")
        )

        expression = operatorPrecedence(atom, [
            (oneOf('^ **'), 2, opAssoc.RIGHT),

            (oneOf('! d% D%'), 1, opAssoc.LEFT),
            (oneOf('d D'), 2, opAssoc.LEFT),
            (oneOf('d D'), 1, opAssoc.RIGHT),

            (oneOf('* / % //'), 2, opAssoc.LEFT),

            (oneOf('+ -'), 2, opAssoc.LEFT),
        ])

        return expression

    def parse(self: "DiceParser", dice_string: str) -> List[Union[str, int]]:
        """Parse well-formed dice roll strings."""
        return self._parser.parseString(dice_string, parseAll=True)

    def evaluate(
            self: "DiceParser",
            parsed_values: Union[List[Union[str, int]], str]
    ) -> Union[int, float]:
        """Evaluate the output parsed values from roll strings."""
        if isinstance(parsed_values, str):
            parsed_values = self.parse(parsed_values)

        result = None
        operator = None

        for val in parsed_values:
            if (
                    isinstance(val, (int, float, ParseResults)) or
                    val in self.constants
            ):
                if val in self.constants:
                    val = self.constants[val]
                elif isinstance(val, ParseResults):
                    val = self.evaluate(val)

                if operator is not None:
                    result = operator(result if result is not None else 1, val)
                else:
                    if result is None:
                        result = val
                    else:
                        result += val

            elif val in self.operations:
                if val == "!":
                    result = factorial(result)
                    continue

                operator = self.operations[val]

            elif val in ["D%", "d%"]:
                result = _roll_dice(result if result is not None else 1, 100)

            else:
                raise Exception("Unable to evaluate input.")

        return result


if __name__ == "__main__":
    parser = DiceParser()

    # print(parser._parser.validate())
    roll_strings = [
        "3",
        "-3",
        "--3",
        "100.",
        "1 2",
        # "--7", # Currently have an issue with this.
        "9.0",
        "-12.05",
        "1 + 2",
        "2 - 1",
        "100 - 3",
        "12 // 4",
        "3+2*4",
        "2^4",
        "3 + 2 * 2^1",
        "9-1+27+(3-5)+9",
        "1d%",
        "d%",
        "D%",
        "1d20",
        "d20",
        "d20 + 5",
        "2d6 + 1d8 + 4",
        "5!",
        "pi",
        "pi + 2",
        "pi * e",
        "(2 + 8 / (9 - 5)) * 3",
        "100 - 21 / 7",
        # "((((((3))))))",
    ]

    for rs in roll_strings:
        try:
            parsed_string = parser.parse(rs)

            # print(rs)
            # print(parsed_string)
            print(parser.evaluate(parsed_string))
        except Exception:
            print("Exception occured parsing: " + rs)
