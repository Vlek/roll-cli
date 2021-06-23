"""
Helper class that stores all available operations within the dice roller.

Operations:

    Addition "+"
    Subtraction "-"
    Multiplication "*"
    'True' division "/"
    'Floor' divison "//"
    Modulus "%"
    Exponential "^" OR "**"
    Factorial "!"
    Square root "sqrt"

    Dice roll "d"
    Keep lowest roll "k"
    Keep highest roll "K"
"""
from __future__ import annotations

from math import ceil, factorial, floor, sqrt
from random import randint
from typing import List, Union

from roll.parser.types.evaluationresults import EvaluationResults
from roll.parser.types.rollresults import RollResults
from roll.praser.types.rolloption import RollOption


class Operations:

    @staticmethod
    def _toEvalResults(
            x: Union[int, float, EvaluationResults]) -> EvaluationResults:
        if not isinstance(x, EvaluationResults):
            x = EvaluationResults(x)

        return x

    @staticmethod
    def add(x: Union[int, float, EvaluationResults],
            y: Union[int, float, EvaluationResults]) -> EvaluationResults:
        return Operations._toEvalResults(x + y)

    @staticmethod
    def sub(x: Union[int, float, EvaluationResults],
            y: Union[int, float, EvaluationResults]) -> EvaluationResults:
        return Operations._toEvalResults(x - y)

    @staticmethod
    def mult(x: Union[int, float, EvaluationResults],
             y: Union[int, float, EvaluationResults]) -> EvaluationResults:
        return Operations._toEvalResults(x * y)

    @staticmethod
    def trueDiv(x: Union[int, float, EvaluationResults],
                y: Union[int, float, EvaluationResults]) -> EvaluationResults:
        return Operations._toEvalResults(x / y)

    @staticmethod
    def floorDiv(x: Union[int, float, EvaluationResults],
                 y: Union[int, float, EvaluationResults]) -> EvaluationResults:
        return Operations._toEvalResults(x // y)

    @staticmethod
    def mod(x: Union[int, float, EvaluationResults],
            y: Union[int, float, EvaluationResults]) -> EvaluationResults:
        return Operations._toEvalResults(x % y)

    @staticmethod
    def expo(x: Union[int, float, EvaluationResults],
             y: Union[int, float, EvaluationResults]) -> EvaluationResults:
        return Operations._toEvalResults(x ** y)

    @staticmethod
    def factorial(
            x: Union[int, float, EvaluationResults]) -> EvaluationResults:
        return Operations._toEvalResults(factorial(x))

    @staticmethod
    def sqrt(x: Union[int, float, EvaluationResults]) -> EvaluationResults:
        return Operations._toEvalResults(sqrt(x))

    @staticmethod
    def roll_dice(
            num_dice: Union[int, float],
            sides: Union[int, float],
            roll_option: RollOption = RollOption.Normal,
            ) -> EvaluationResults:
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

        roll_result: RollResults = {
            'total': rolls_total,
            'dice': f'{starting_num_dice}d{starting_sides}',
            'rolls': rolls
        }

        result = EvaluationResults()
        result.add_roll(roll_result)

        return result

    @staticmethod
    def keep_lowest_dice(results: RollResults,
                         k: Union[int, float] = 1) -> EvaluationResults:
        """Remove k number of lowest rolls from given RollResults."""
        if len(results['rolls']) < k:
            results['rolls'] = []
            results['total'] = 0
        else:
            results['rolls'] = sorted(results['rolls'])[:ceil(k)]
            results['total'] = sum(results['rolls'])
        return results

    @staticmethod
    def keep_highest_dice(results: RollResults,
                          k: Union[int, float] = 1) -> EvaluationResults:
        """Trim the results of a roll based on the provided amount to keep."""
        if len(results['rolls']) < k:
            results['rolls'] = []
            results['total'] = 0
        else:
            results['rolls'] = sorted(results['rolls'])[-ceil(k):]
            results['total'] = sum(results['rolls'])
        return results
