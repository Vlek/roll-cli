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

            # This line causes the recursion debug to go off.
            # Will have to find a way to have an optional left
            # operand in this case.
            (CaselessLiteral('d'), 1, opAssoc.RIGHT,
             lambda toks: roll_dice(1, toks[0][1])),

            # Keep notation
            (Literal('k'), 2, opAssoc.LEFT,
             DiceParser._handle_keep_lowest),
            (Literal('K'), 2, opAssoc.LEFT,
             DiceParser._handle_keep_highest),
            (Literal('k'), 1, opAssoc.LEFT,
             DiceParser._handle_keep_lowest),
            (Literal('K'), 1, opAssoc.LEFT,
             DiceParser._handle_keep_highest),

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

        print(toks)
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
            raise Exception(f"left value cannot be a string: {toks}")

        # We initialize our result with the left-most value.
        # As we perform operations, this value will be continuously
        # updated and used as the left-hand side.
        result: Union[int, float, EvaluationResults] = toks[0][0]

        # Because we get things like [[1, "+", 2, "+", 3]], we have
        # to be able to handle additional operations beyond a single
        # left/right pair.
        for pair in range(1, len(toks[0]), 2):

            if isinstance(toks[0][pair + 1], str):
                raise Exception(f"right value cannot be a string: {toks}")

            right: Union[int, float, EvaluationResults] = toks[0][pair + 1]

            operation_string: str = str(toks[0][pair])

            if operation_string not in DiceParser.OPERATIONS:
                raise Exception(
                    f"Operator was not in valid operations: {toks}")

            op: Callable[
                [
                    Union[int, float, EvaluationResults],
                    Union[int, float, EvaluationResults]
                ],
                EvaluationResults
            ] = DiceParser.OPERATIONS[operation_string]

            result = op(result, right)

        return result

    def parse(self: DiceParser,
              dice_string: str,
              roll_option: RollOption = RollOption.Normal
              ) -> List[Union[int, float, EvaluationResults]]:
        """Parse well-formed dice roll strings."""
        try:
            result: List[
                Union[
                    int,
                    float,
                    EvaluationResults]
            ] = self._parser.parseString(dice_string, parseAll=True)
        except ParseException:
            raise SyntaxError("Unable to parse input string: " + dice_string)

        if len(result) == 0:
            raise Exception("Did not receive any value from evaluation")
        elif len(result) > 1:
            raise Exception(
                f"Received more values than expected: {result}")
        elif not all(isinstance(i, (int, float,
                                EvaluationResults)) for i in result):
            raise Exception(f"Unexpected types in output: {result}")

        return result

    def evaluate(self: DiceParser,
                 dice_string: str,
                 roll_option: RollOption = RollOption.Normal,
                 ) -> Union[int, float, EvaluationResults]:
        return self.parse(dice_string, roll_option)[0]


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
        except Exception as ex:
            print(f"Exception '{ex}' occured parsing: " + rs)
