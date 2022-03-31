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

from math import e, pi
from typing import Callable, Dict, List, Union

from pyparsing import (CaselessKeyword, CaselessLiteral, Forward, Literal,
                       ParseException, ParserElement, infixNotation, oneOf,
                       opAssoc, pyparsing_common)
from roll.parser.operations import (ROLL_TYPE, add, factorial, floor_div, mod,
                                    mult, roll_dice, sqrt, sub, true_div, expo)
from roll.parser.types import EvaluationResults, RollOption, RollResults

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
        "d": roll_dice,
    }

    def __init__(self: "DiceParser") -> None:
        """Initialize a parser to handle dice strings."""
        self._parser = self._create_parser()

    @staticmethod
    def _create_parser() -> Forward:
        """Create an instance of a dice roll string parser."""
        atom = (
            CaselessLiteral("d%").setParseAction(
                lambda: DiceParser._handle_roll(1, 100)) |
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
             lambda toks: DiceParser._handle_roll(toks[0][0], 100)),
            (CaselessLiteral('d'), 2, opAssoc.RIGHT,
             lambda toks: DiceParser._handle_roll(toks[0][0], toks[0][2])),

            # This line causes the recursion debug to go off.
            # Will have to find a way to have an optional left
            # operand in this case.
            (CaselessLiteral('d'), 1, opAssoc.RIGHT,
             lambda toks: DiceParser._handle_roll(1, toks[0][1])),

            # Keep notation
            (oneOf('k K'), 2, opAssoc.LEFT,
             DiceParser._handle_keep),
            (oneOf('k K'), 1, opAssoc.LEFT,
             DiceParser._handle_keep),

            # Multiplication and division
            (oneOf('* / % //'), 2, opAssoc.LEFT,
             DiceParser._handle_standard_operation),

            # Addition and subtraction
            (oneOf('+ -'), 2, opAssoc.LEFT,
             DiceParser._handle_standard_operation),

            # TODO: Use this to make a pretty exception message
            # where we point out and explain the issue.
        ]).setFailAction(lambda s, loc, expr, err: print(err))

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

        value: Union[int, float, EvaluationResults, str] = toks[0][1]

        if not isinstance(value, (int, float, EvaluationResults)):
            raise TypeError(
                "The given value must be int, float, or EvaluationResults")
        return sqrt(value)

    @staticmethod
    def _handle_expo(
            toks: list[list[Union[int, float, EvaluationResults
                                  ]]]) -> Union[int, float, EvaluationResults]:
        return expo(toks[0][0], toks[0][2])

    @staticmethod
    def _handle_factorial(
            toks: List[List[Union[int, float, EvaluationResults
                                  ]]]) -> Union[int, float, EvaluationResults]:
        return factorial(toks[0][0])

    @staticmethod
    def _handle_roll(sides: Union[int, float, EvaluationResults],
                     num: Union[int, float, EvaluationResults]
                     ) -> Union[int, float, EvaluationResults]:
        global ROLL_TYPE
        roll_option = ROLL_TYPE
        return roll_dice(sides, num, roll_option)

    @staticmethod
    def _handle_keep(
            toks: List[List[Union[int, float, EvaluationResults, str
                                  ]]]) -> Union[int, float, EvaluationResults]:
        tokens: List[Union[int, float,
                           EvaluationResults, str]] = toks[0]

        if not isinstance(tokens[0], EvaluationResults):
            raise TypeError("Left value must contain a dice roll.")

        # We initialize our result with the left-most value.
        # As we perform operations, this value will be continuously
        # updated and used as the left-hand side.
        result: EvaluationResults = tokens[0]

        # If it's the case that we have an implied keep amount, we
        # need to manually add it to the end here.
        if len(tokens) % 2 == 0:
            tokens.append(1)

        # Because we get things like [[1, "+", 2, "+", 3]], we have
        # to be able to handle additional operations beyond a single
        # left/right pair.
        for i in range(1, len(tokens), 2):

            op_index = i
            right_index = i + 1

            operation_string: str = str(tokens[op_index])

            right: Union[EvaluationResults, float, int,
                         str] = tokens[right_index]

            if isinstance(right, EvaluationResults):
                result += right
                result.total -= right.total
                right = right.total

            last_roll: RollResults = result.rolls[-1]
            lower_total_by: Union[int, float] = 0

            if operation_string == 'k':
                lower_total_by = last_roll.keep_lowest(float(right))
                result.history.append(f"Keeping lowest: {right}: {last_roll.rolls}")
            else:
                lower_total_by = last_roll.keep_highest(float(right))
                result.history.append(f"Keeping highest: {right}: {last_roll.rolls}")

            result.total -= lower_total_by

        return result

    @staticmethod
    def _handle_standard_operation(
            toks: list[list[Union[str, int, float, EvaluationResults
                                  ]]]) -> Union[str, int, float, EvaluationResults]:
        # We initialize our result with the left-most value.
        # As we perform operations, this value will be continuously
        # updated and used as the left-hand side.
        result: Union[int, float, EvaluationResults, str] = toks[0][0]

        # Because we get things like [[1, "+", 2, "+", 3]], we have
        # to be able to handle additional operations beyond a single
        # left/right pair.
        for pair in range(1, len(toks[0]), 2):

            right: Union[int, float,
                         EvaluationResults, str] = toks[0][pair + 1]

            operation_string: str = str(toks[0][pair])

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
        global ROLL_TYPE
        ROLL_TYPE = roll_option
        try:
            result: List[
                Union[
                    int,
                    float,
                    EvaluationResults]
            ] = self._parser.parseString(dice_string, parseAll=True)
        except ParseException:
            raise SyntaxError("Unable to parse input string: " + dice_string)

        return result

    def evaluate(self: DiceParser,
                 dice_string: str,
                 roll_option: RollOption = RollOption.Normal,
                 ) -> Union[int, float, EvaluationResults]:
        """Parse and evaluate the given dice string."""
        return self.parse(dice_string, roll_option)[0]
