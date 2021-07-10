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

from __future__ import annotations

from math import e, factorial, pi
from typing import Callable, Dict, List, Union

from pyparsing import (CaselessKeyword, CaselessLiteral, Forward, Literal,
                       ParseException, ParserElement, infixNotation, oneOf,
                       opAssoc, pyparsing_common)
from roll.parser.operations import (add, expo, floor_div, mod, mult, roll_dice,
                                    sqrt, sub, true_div)
from roll.parser.types import EvaluationResults, RollOption

ParserElement.enablePackrat()


class DiceParser:
    """Parser for evaluating dice strings."""

    OPERATIONS: Dict[str, Callable] = {
        "+": add,
        "-": sub,
        "*": mult,
        "/": true_div,
        "//": floor_div,
        "%": mod,
        "^": expo,
        "d": roll_dice,
    }

    def __init__(self: "DiceParser") -> None:
        """Initialize a parser to handle dice strings."""
        self._parser = self._create_parser()

    @staticmethod
    def _create_parser() -> Forward:
        """Create an instance of a dice roll string parser."""
        atom = (
            CaselessLiteral("d%").setParseAction(lambda: roll_dice(1, 100)) |
            pyparsing_common.number |
            CaselessKeyword("pi").setParseAction(lambda: pi) |
            CaselessKeyword("e").setParseAction(lambda: e)
        )

        expression = infixNotation(atom, [
            # Unary minus
            (Literal('-'), 1, opAssoc.RIGHT, DiceParser._handle_unary_minus),
            # Square root
            (CaselessLiteral('sqrt'), 1, opAssoc.RIGHT,
             DiceParser._handle_sqrt),
            # Exponents
            (oneOf('^ **'), 2, opAssoc.RIGHT, DiceParser._handle_expo),

            # Unary minus (#2)
            (Literal('-'), 1, opAssoc.RIGHT, DiceParser._handle_unary_minus),
            # Factorial
            (Literal('!'), 1, opAssoc.LEFT, DiceParser._handle_factorial),

            # Dice notations
            (CaselessLiteral('d%'), 1, opAssoc.LEFT,
             lambda toks: roll_dice(toks[0][0], 100)),
            (CaselessLiteral('d'), 2, opAssoc.RIGHT,
             lambda toks: roll_dice(toks[0][0], toks[0][2])),
            (CaselessLiteral('k'), 2, opAssoc.LEFT,
             DiceParser._handle_keep_lowest),
            (CaselessLiteral('k'), 1, opAssoc.LEFT,
             DiceParser._handle_keep_highest),

            # This line causes the recursion debug to go off.
            # Will have to find a way to have an optional left
            # operand in this case.
            (CaselessLiteral('d'), 1, opAssoc.RIGHT,
             lambda toks: roll_dice(1, toks[0][1])),

            # Multiplication and division
            (oneOf('* / % //'), 2, opAssoc.LEFT,
             DiceParser._handle_standard_operation),

            # Addition and subtraction
            (oneOf('+ -'), 2, opAssoc.LEFT,
             DiceParser._handle_standard_operation),
        ])

        return expression

    @staticmethod
    def _handle_unary_minus(
            toks: list[list[Union[int, float, EvaluationResults
                                  ]]]) -> Union[int, float, EvaluationResults]:
        return -toks[0][1]

    @staticmethod
    def _handle_sqrt(
            toks: list[list[Union[str, int, float, EvaluationResults
                                  ]]]) -> EvaluationResults:
        value: Union[int, float, EvaluationResults] = float(toks[0][1])
        return sqrt(value)

    @staticmethod
    def _handle_expo(
            toks: list[list[Union[int, float, EvaluationResults
                                  ]]]) -> Union[int, float, EvaluationResults]:
        return toks[0][0] ** toks[0][2]

    @staticmethod
    def _handle_factorial(
            toks: list[list[Union[int, float, EvaluationResults
                                  ]]]) -> Union[int, float, EvaluationResults]:
        return factorial(toks[0][0])

    @staticmethod
    def _handle_keep_highest(
            toks: list[list[Union[int, float, EvaluationResults
                                  ]]]) -> Union[int, float, EvaluationResults]:
        if not isinstance(toks[0][0], EvaluationResults):
            raise Exception("Cannot use keep highest notation on a number.")

        left: EvaluationResults = toks[0][0]
        right: Union[int, float, EvaluationResults] = toks[0][2]

        if isinstance(right, EvaluationResults):
            left += right
            left.total -= right.total
            right = right.total

        left.total -= left.rolls[-1].keep_highest(right)

        return left

    @staticmethod
    def _handle_keep_lowest(
            toks: list[list[Union[int, float, EvaluationResults
                                  ]]]) -> Union[int, float, EvaluationResults]:
        if not isinstance(toks[0][0], EvaluationResults):
            raise Exception("Cannot use keep highest notation on a number.")

        left: EvaluationResults = toks[0][0]
        right: Union[int, float, EvaluationResults] = toks[0][2]

        if isinstance(right, EvaluationResults):
            left += right
            left.total -= right.total
            right = right.total

        left.total -= left.rolls[-1].keep_lowest(right)

        return left

    @staticmethod
    def _handle_standard_operation(
            toks: list[list[Union[str, int, float, EvaluationResults
                                  ]]]) -> Union[int, float, EvaluationResults]:

        if isinstance(toks[0][0], str):
            raise Exception("left value cannot be a string")
        elif isinstance(toks[0][2], str):
            raise Exception("right value cannot be a string")

        operation_string: str = str(toks[0][1])

        if operation_string not in DiceParser.OPERATIONS:
            raise Exception("Operator was not in valid operations")

        op: Callable[
            [
                Union[int, float, EvaluationResults],
                Union[int, float, EvaluationResults]
            ],
            EvaluationResults
        ] = DiceParser.OPERATIONS[operation_string]

        return op(toks[0][0], toks[0][2])

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

        return parsed_values[0]
        """
        result: EvaluationResults = EvaluationResults()
        operator = None
        dice_rolls = []

        val: Union[str, int, float]
        for val in parsed_values:

            # In addition to dealing with values, we are also going to
            # handle constants and nested lists here because, after they
            # are evaluated, they are then used as values in the current
            # evaluation context.
            if (isinstance(val, (int, float,
                                 ParseResults, EvaluationResults))):
                if isinstance(val, ParseResults):
                    evaluation: EvaluationResults = self.evaluate(val,
                                                                  roll_option)
                    result += evaluation

                if operator is not None:
                    # There are currently only two cases that could
                    # cause result to be none, either we're dealing
                    # with a dice roll that doesn't have a left-hand
                    # number or a unary minus. In either case, we have
                    # to initialize the result accordingly.
                    if result is None:
                        if operator is roll_dice:
                            result = 1
                        else:
                            result = 0

                    if operator is roll_dice:
                        current_rolls = roll_dice(result, val, roll_option)

                        result = current_rolls.total
                        dice_rolls.append(current_rolls)
                    elif operator in [_keep_highest_dice, _keep_lowest_dice]:
                        if len(dice_rolls) == 0:
                            raise ValueError(
                                "Unable to use keep without a dice roll.")

                        previous_total: Union[int,
                                              float] = dice_rolls[-1].total()

                        current_rolls = operator(dice_rolls[-1], val)

                        result += current_rolls['total'] - previous_total
                        dice_rolls[-1] = current_rolls

                    else:
                        result = operator(result, val)
                else:
                    result = val

            elif val in self.operations:
                operator = self.operations[val]

        total_results: EvaluationResults = EvaluationResults(
            result if result is not None else 0,
            dice_rolls
        )

        return total_results
        """


if __name__ == "__main__":
    parser = DiceParser()

    print("Recursive issues:", parser._parser.validate())
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
            print(rs)

            parsed_string = parser.parse(rs)

            print(parsed_string)
            print(parser.evaluate(parsed_string))
        except Exception as ex:
            print(f"Exception '{ex}' occured parsing: " + rs)
