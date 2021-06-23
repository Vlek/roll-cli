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

from math import e, factorial, pi, sqrt
from operator import add, floordiv, mod, mul, sub, truediv
from sys import version_info
from typing import Callable, List, Optional, Union

# TypedDict was added in 3.8.
if version_info >= (3, 8):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict

from pyparsing import (CaselessKeyword, CaselessLiteral, Forward, Literal,
                       ParseException, ParserElement, ParseResults,
                       infixNotation, oneOf, opAssoc, pyparsing_common)
from roll.evaluationresults import EvaluationResults

ParserElement.enablePackrat()


class DiceParser:
    """Parser for evaluating dice strings."""

    operations: Callable[[int, float, EvaluationResults], EvaluationResults] = {
        "+": lambda x, y: EvaluationResults(add(x, y)),
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

    def __init__(self: "DiceParser") -> None:
        """Initialize a parser to handle dice strings."""
        self._parser = self._create_parser()

    @staticmethod
    def _create_parser() -> Forward:
        """Create an instance of a dice roll string parser."""
        atom = (
            CaselessLiteral("d%").setParseAction(lambda: _roll_dice(1, 100)) |
            pyparsing_common.number |
            CaselessKeyword("pi").setParseAction(lambda: pi) |
            CaselessKeyword("e").setParseAction(lambda: e)
        )

        expression = infixNotation(atom, [
            (Literal('-'), 1, opAssoc.RIGHT, DiceParser._handle_unary_minus),
            (CaselessLiteral('sqrt'), 1, opAssoc.RIGHT,
             DiceParser._handle_sqrt),
            (oneOf('^ **'), 2, opAssoc.RIGHT, DiceParser._handle_expo),

            (Literal('-'), 1, opAssoc.RIGHT, DiceParser._handle_unary_minus),
            (Literal('!'), 1, opAssoc.LEFT, DiceParser._handle_factorial),

            (CaselessLiteral('d%'), 1, opAssoc.LEFT,
             lambda toks: _roll_dice(toks[0][0], 100)),
            (CaselessLiteral('d'), 2, opAssoc.RIGHT,
             lambda toks: _roll_dice(toks[0][0], toks[0][2])),
            (CaselessLiteral('k'), 2, opAssoc.LEFT, lambda toks: print(toks)),
            (CaselessLiteral('k'), 1, opAssoc.LEFT, lambda toks: print(toks)),

            # This line causes the recursion debug to go off.
            # Will have to find a way to have an optional left
            # operand in this case.
            (CaselessLiteral('d'), 1, opAssoc.RIGHT,
             lambda toks: _roll_dice(1, toks[0][1])),

            (oneOf('* / % //'), 2, opAssoc.LEFT,
             DiceParser._handle_standard_operation),

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
            toks: list[list[Union[int, float, EvaluationResults
                                  ]]]) -> Union[int, float, EvaluationResults]:
        value: Union[int, float, EvaluationResults] = toks[0][1]
        result: Union[int, float] = sqrt(value)

        if isinstance(value, EvaluationResults):
            value.total = result
            return value

        return result

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
    def _handle_standard_operation(
            toks: list[list[Union[str, int, float, EvaluationResults
                                  ]]]) -> Union[int, float, EvaluationResults]:

        operation_string: str = str(toks[0][1])

        if operation_string not in DiceParser.operations:
            raise Exception("Operator was not in valid operations")

        op: Callable[[int, float, EvaluationResults], EvaluationResults] = DiceParser.operations[operation_string]

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

        result: Union[int, float, EvaluationResults] = 0
        operator = None
        dice_rolls = []

        val: Union[str, int, float, Optional[float]]
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
                        if operator is _roll_dice:
                            result = 1
                        else:
                            result = 0

                    if operator is _roll_dice:
                        current_rolls = _roll_dice(result, val, roll_option)

                        result = current_rolls['total']
                        dice_rolls.append(current_rolls)
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
                operator = self.operations[val]

        total_results: EvaluationResults = EvaluationResults(
            result if result is not None else 0,
            dice_rolls
        )

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
