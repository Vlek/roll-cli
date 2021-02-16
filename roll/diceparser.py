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

from enum import Enum
from math import ceil, e, factorial, floor, pi, sqrt
from operator import add, floordiv, mod, mul, sub, truediv
from random import randint
from sys import version_info
from typing import Callable, Dict, List, Optional, Union

# TypedDict was added in 3.8.
if version_info >= (3, 8):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict

from pyparsing import (CaselessKeyword, CaselessLiteral, Forward, Literal,
                       ParseException, ParserElement, ParseResults, oneOf,
                       opAssoc, operatorPrecedence, pyparsing_common)

ParserElement.enablePackrat()


class RollResults(TypedDict):
    total: Union[int, float]
    dice: str
    rolls: List[Union[int, float]]


class EvaluationResults(TypedDict):
    total: Union[int, float]
    rolls: List[RollResults]


class RollOption(Enum):
    Minimum = 0
    Normal = 1
    Maximum = 2


def _roll_dice(
        num_dice: Union[int, float],
        sides: Union[int, float],
        roll_option: RollOption = RollOption.Normal,
        ) -> RollResults:
    """Calculate value of dice roll notation."""
    starting_num_dice = num_dice
    starting_sides = sides

    # If it's the case that we were given a dice with negative sides,
    # then that doesn't mean anything in the real world. I cannot
    # for the life of me figure out a possible scenario where that
    # would make sense. We will just error out.
    if sides < 0:
        raise ValueError('The sides of a die must be positive or zero.')

    result_is_negative = num_dice < 0

    if result_is_negative:
        num_dice = abs(num_dice)

    sides = ceil(sides)

    rolls: List[Union[int, float]] = []

    if roll_option == RollOption.Minimum:
        rolls = [1] * ceil(num_dice)
    elif roll_option == RollOption.Maximum:
        rolls = [floor(sides)] * floor(num_dice)

        if isinstance(num_dice, float) and (num_dice % 1) != 0:
            rolls.append(sides * (num_dice % 1))
    elif sides != 0:
        rolls = [randint(1, sides) for _ in range(floor(num_dice))]

        # If it's the case that the number of dice is a float, then
        # we take that to mean that it is a dice where the sides should
        # be lowered to reflect the float amount.
        #
        # We do not want this to effect all dice rolls however, only the
        # last one (or the only one if there's only a decimal portion).
        if isinstance(num_dice, float) and (num_dice % 1) != 0:
            sides = ceil(sides * (num_dice % 1))
            rolls.append(randint(1, sides))

    rolls_total = sum(rolls)

    if result_is_negative:
        rolls_total *= -1

    result: RollResults = {
        'total': rolls_total,
        'dice': f'{starting_num_dice}d{starting_sides}',
        'rolls': rolls
    }

    return result


def _keep_lowest_dice(results: RollResults,
                      k: Union[int, float] = 1) -> RollResults:
    """Remove k number of lowest rolls from given RollResults."""
    if len(results['rolls']) < k:
        results['rolls'] = []
        results['total'] = 0
    else:
        results['rolls'] = sorted(results['rolls'])[:ceil(k)]
        results['total'] = sum(results['rolls'])
    return results


def _keep_highest_dice(results: RollResults,
                       k: Union[int, float] = 1) -> RollResults:
    """Trim the results of a roll based on the provided amount to keep."""
    if len(results['rolls']) < k:
        results['rolls'] = []
        results['total'] = 0
    else:
        results['rolls'] = sorted(results['rolls'])[-ceil(k):]
        results['total'] = sum(results['rolls'])
    return results


class DiceParser:
    """Parser for evaluating dice strings."""

    operations: Dict[
        str,
        Union[
            Callable[
                [
                    Union[int, float],
                    Union[int, float]
                ], Union[int, float, RollResults]],
            # This is needed for factorial and sqrt
            Callable[
                [Union[int, float]],
                Union[int, float]
            ]
        ]] = {
        "+": add,
        "-": sub,
        "*": mul,
        "/": truediv,
        "//": floordiv,
        "%": mod,
        "^": pow,
        "**": pow,
        "d": _roll_dice,
        "k": _keep_lowest_dice,
        "K": _keep_highest_dice,
        "!": factorial,
        "sqrt": sqrt
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
            CaselessLiteral("d%") |
            pyparsing_common.number |
            CaselessKeyword("pi") |
            CaselessKeyword("e")
        )

        expression = operatorPrecedence(atom, [
            (Literal('-'), 1, opAssoc.RIGHT),
            (CaselessLiteral('sqrt'), 1, opAssoc.RIGHT),
            (oneOf('^ **'), 2, opAssoc.RIGHT),

            (Literal('-'), 1, opAssoc.RIGHT),
            (Literal('!'), 1, opAssoc.LEFT),

            (CaselessLiteral('d%'), 1, opAssoc.LEFT),
            (CaselessLiteral('d'), 2, opAssoc.RIGHT),
            (CaselessLiteral('k'), 2, opAssoc.LEFT),
            (CaselessLiteral('k'), 1, opAssoc.LEFT),

            # This line causes the recursion debug to go off.
            # Will have to find a way to have an optional left
            # operand in this case.
            (CaselessLiteral('d'), 1, opAssoc.RIGHT),

            (oneOf('* / % //'), 2, opAssoc.LEFT),

            (oneOf('+ -'), 2, opAssoc.LEFT),
        ])

        return expression

    def parse(self: "DiceParser", dice_string: str) -> List[Union[str, int]]:
        """Parse well-formed dice roll strings."""
        try:
            return self._parser.parseString(dice_string, parseAll=True)
        except ParseException:
            raise SyntaxError("Unable to parse input string: " + dice_string)

    def evaluate(
            self: "DiceParser",
            parsed_values: Union[List[Union[str, int]], str],
            roll_option: RollOption = RollOption.Normal,
    ) -> EvaluationResults:
        """Evaluate the output parsed values from roll strings."""
        if isinstance(parsed_values, str):
            parsed_values = self.parse(parsed_values)

        result: Union[int, float, None] = None
        operator = None
        dice_rolls = []

        val: Union[str, int, float, Optional[float]]
        for val in parsed_values:

            # In addition to dealing with values, we are also going to
            # handle constants and nested lists here because, after they
            # are evaluated, they are then used as values in the current
            # evaluation context.
            if (
                    isinstance(val, (int, float, ParseResults)) or
                    val in self.constants
            ):
                if val in self.constants:
                    val = self.constants[str(val)]
                elif isinstance(val, ParseResults):
                    evaluation: EvaluationResults = self.evaluate(val,
                                                                  roll_option)
                    val = evaluation['total']
                    dice_rolls.extend(evaluation['rolls'])

                if operator is not None:
                    # There are currently only two cases that could
                    # cause result to be none, either we're dealing
                    # with a dice roll that doesn't have a left-hand
                    # number or a unary minus. In either case, we have
                    # to initialize the result accordingly.
                    if result is None:
                        if operator is _roll_dice:
                            result = 1
                        else:
                            result = 0

                    if operator is _roll_dice:
                        current_rolls = _roll_dice(result, val, roll_option)

                        result = current_rolls['total']
                        dice_rolls.append(current_rolls)
                    elif operator is sqrt:
                        result = operator(val)
                    elif operator in [_keep_highest_dice, _keep_lowest_dice]:
                        if len(dice_rolls) == 0:
                            raise ValueError(
                                "Unable to use keep without a dice roll.")

                        previous_total: Union[int,
                                              float] = dice_rolls[-1]['total']

                        current_rolls = operator(dice_rolls[-1], val)

                        result += current_rolls['total'] - previous_total
                        dice_rolls[-1] = current_rolls

                    else:
                        result = operator(result, val)
                else:
                    result = val

            elif val in self.operations:

                # Since factorials are unary and the value is to the left-
                # hand side, we will execute the factorial function here
                # as we do not have to wait for any further input.
                if val == "!":
                    result = factorial(result if result is not None else 0)
                    continue

                operator = self.operations[val]

            elif val in ["D%", "d%"]:
                current_rolls = _roll_dice(
                    result if result is not None else 1, 100, roll_option)

                result = current_rolls['total']
                dice_rolls.append(current_rolls)

        total_results: EvaluationResults = {
            'total': result if result is not None else 0,
            'rolls': dice_rolls
        }

        return total_results


if __name__ == "__main__":
    parser = DiceParser()

    # print("Recursive issues:", parser._parser.validate())
    roll_strings = [
        "5-3",
        "3-5",
        "3--5",
        "1d2d3",
        "5^2d1",
        "0!d20",
        "5 + 2!",
        "5**(2)",
        "5**2 * 7",
        "2 + 5 d   6",
        "(2)d6",
        "2d(6)",
        "3",
        "-3",
        "--3",
        "100.",
        "1 2",
        "--7",
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
        "((((((3))))))",
    ]

    for rs in roll_strings:
        try:
            parsed_string = parser.parse(rs)

            # print(rs)
            # print(parsed_string)
            print(parser.evaluate(parsed_string))
        except Exception as e:
            print(f"Exception '{e}' occured parsing: " + rs)
