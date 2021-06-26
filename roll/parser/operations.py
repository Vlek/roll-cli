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

from math import ceil
from math import factorial as fact
from math import floor
from math import sqrt as squareroot
from random import randint
from typing import List, Union

from roll.parser.types.evaluationresults import EvaluationResults
from roll.parser.types.rollresults import RollResults
from roll.praser.types.rolloption import RollOption


def _toEvalResults(
        x: Union[int, float, EvaluationResults]) -> EvaluationResults:
    if not isinstance(x, EvaluationResults):
        x = EvaluationResults(x)

    return x


def add(x: Union[int, float, EvaluationResults],
        y: Union[int, float, EvaluationResults]) -> EvaluationResults:
    return _toEvalResults(x + y)


def sub(x: Union[int, float, EvaluationResults],
        y: Union[int, float, EvaluationResults]) -> EvaluationResults:
    return _toEvalResults(x - y)


def mult(x: Union[int, float, EvaluationResults],
         y: Union[int, float, EvaluationResults]) -> EvaluationResults:
    return _toEvalResults(x * y)


def trueDiv(x: Union[int, float, EvaluationResults],
            y: Union[int, float, EvaluationResults]) -> EvaluationResults:
    return _toEvalResults(x / y)


def floorDiv(x: Union[int, float, EvaluationResults],
             y: Union[int, float, EvaluationResults]) -> EvaluationResults:
    return _toEvalResults(x // y)


def mod(x: Union[int, float, EvaluationResults],
        y: Union[int, float, EvaluationResults]) -> EvaluationResults:
    return _toEvalResults(x % y)


def expo(x: Union[int, float, EvaluationResults],
         y: Union[int, float, EvaluationResults]) -> EvaluationResults:
    return _toEvalResults(x ** y)


def factorial(
        x: Union[int, float, EvaluationResults]) -> EvaluationResults:
    """
    Handle the factorial operation for int, float, and EvaluationResults.

    Depending on the passed datatype, we do different things:
        int: No change required, it is able to use the built-in function
            and then change the resulting value into an EvaluationResults.
        float: The value is ceil'd and then passed as an int.
        EvaluationResults: The total is ceil'd and passed.
    """

    result: Union[int, EvaluationResults]

    if isinstance(x, EvaluationResults):
        x.total = fact(ceil(x.total))
        result = x
    else:
        result = fact(ceil(x))

    return _toEvalResults(result)


def sqrt(x: Union[int, float, EvaluationResults]) -> EvaluationResults:
    """
    Get the squareroot of the given number and return an EvaluationResults.
    """
    result: Union[int, float, EvaluationResults]

    if isinstance(x, EvaluationResults):
        x.total = squareroot(x.total)
        result = x
    else:
        result = squareroot(x)

    return _toEvalResults(result)


def roll_dice(
        num_dice: Union[int, float, EvaluationResults],
        sides: Union[int, float, EvaluationResults],
        roll_option: RollOption = RollOption.Normal,
        ) -> EvaluationResults:
    """Calculate value of dice roll notation."""
    result: EvaluationResults = EvaluationResults()

    # In order to ensure our types later on, we are going to first
    # take out all of the EvaluationResults objects and take their
    # totals to be used down the line. Their history will be used
    # as the basis for our returned value going forward.
    #
    # Since the totals for either are being used for our count
    # and sides values, we do not include the totals in the final
    # value.
    if isinstance(num_dice, EvaluationResults):
        result = num_dice
        num_dice = num_dice.total
        if isinstance(sides, EvaluationResults):
            result += sides
            sides = sides.total
        result.total = 0
    elif isinstance(sides, EvaluationResults):
        result = sides
        sides = sides.total
        result.total = 0

    starting_num_dice: Union[int, float] = num_dice
    starting_sides: Union[int, float] = sides

    # If it's the case that we were given a dice with negative sides,
    # then that doesn't mean anything in the real world. I cannot
    # for the life of me figure out a possible scenario where that
    # would make sense. We will just error out.
    if sides < 0:
        raise ValueError('The sides of a die must be positive or zero.')

    result_is_negative: bool = num_dice < 0

    if result_is_negative:
        num_dice = abs(num_dice)

    sides = ceil(sides)

    rolls: List[Union[int, float]] = []

    if roll_option == RollOption.Minimum:
        rolls = [1] * ceil(num_dice)
    elif roll_option == RollOption.Maximum:
        # TODO: Ensure that this logic is correct. I am not sure that
        # we want to floor either of these numbers.
        # Example: 1.5d5.5 maxed should be the max of 1.5d6, or 9.
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

    rolls_total: Union[int, float] = sum(rolls)

    # TODO: Shouldn't this instead make the individual rolls negative?
    if result_is_negative:
        rolls_total *= -1

    result.add_roll({
        # TODO: Do we really need a total? This can get out of sync.
        'total': rolls_total,
        'dice': f'{starting_num_dice}d{starting_sides}',
        'rolls': rolls
    })

    return result


def keep_lowest_dice(results: EvaluationResults,
                     k: Union[int, float] = 1) -> EvaluationResults:
    """Remove k number of lowest rolls from last roll."""
    if len(EvaluationResults.rolls) == 0:
        return results

    last_roll = EvaluationResults.rolls[-1]

    if len(last_roll['rolls']) > k:
        last_roll['rolls'] = sorted(last_roll['rolls'])[:ceil(k)]
        last_roll['total'] = sum(last_roll['rolls'])

    return results


def keep_highest_dice(results: EvaluationResults,
                      k: Union[int, float] = 1) -> EvaluationResults:
    """Trim the results of a roll based on the provided amount to keep."""
    if len(EvaluationResults.rolls) == 0:
        return results

    last_roll = EvaluationResults.rolls[-1]

    if len(last_roll['rolls']) > k:
        last_roll['rolls'] = sorted(last_roll['rolls'])[-ceil(k):]
        last_roll['total'] = sum(last_roll['rolls'])

    return results
