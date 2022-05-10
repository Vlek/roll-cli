"""Helper class that stores all available operations within the dice roller.

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
from math import floor
from random import randint

from .types import EvaluationResults
from .types import RollOption
from .types import RollResults


def _to_eval_results(x: int | float | EvaluationResults) -> EvaluationResults:
    """Change given object to an EvaluationResults object."""
    if not isinstance(x, EvaluationResults):
        x = EvaluationResults(x)

    return x


def add(
    x: int | float | EvaluationResults, y: int | float | EvaluationResults
) -> EvaluationResults:
    """Add x and y together with extended types."""
    return _to_eval_results(x) + y


def sub(
    x: int | float | EvaluationResults, y: int | float | EvaluationResults
) -> EvaluationResults:
    """Subtract x and y together with extended types."""
    return _to_eval_results(x) - y


def mult(
    x: int | float | EvaluationResults, y: int | float | EvaluationResults
) -> EvaluationResults:
    """Multiply x and y together with extended types."""
    return _to_eval_results(x) * y


def true_div(
    x: int | float | EvaluationResults, y: int | float | EvaluationResults
) -> EvaluationResults:
    """Divide (true) x and y with extended types."""
    return _to_eval_results(x) / y


def floor_div(
    x: int | float | EvaluationResults, y: int | float | EvaluationResults
) -> EvaluationResults:
    """Divide (floor) x and y with extended types."""
    return _to_eval_results(x) // y


def mod(
    x: int | float | EvaluationResults, y: int | float | EvaluationResults
) -> EvaluationResults:
    """Divide (modulus) x and y with extended types."""
    return _to_eval_results(x) % y


def expo(
    x: int | float | EvaluationResults, y: int | float | EvaluationResults
) -> EvaluationResults:
    """Exponentiate x by y with extended types."""
    return _to_eval_results(x) ** y


def factorial(x: int | float | EvaluationResults) -> EvaluationResults:
    """Handle the factorial operation for int, float, and EvaluationResults.

    Depending on the passed datatype, we do different things:
        int: No change required, it is able to use the built-in function
            and then change the resulting value into an EvaluationResults.
        float: The value is ceil'd and then passed as an int.
        EvaluationResults: The total is ceil'd and passed.
    """
    if not isinstance(x, EvaluationResults):
        x = _to_eval_results(x)

    x.factorial()

    return x


def sqrt(x: int | float | EvaluationResults) -> EvaluationResults:
    """Perform sqrt on x with extended types."""
    if not isinstance(x, EvaluationResults):
        x = _to_eval_results(x)

    x.sqrt()

    return x


def roll_dice(  # noqa: max-complexity: 13
    num_dice: int | float | EvaluationResults,
    sides: int | float | EvaluationResults,
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
        result += num_dice
        num_dice = num_dice.total

    if isinstance(sides, EvaluationResults):
        result += sides
        sides = sides.total

    result.total = 0

    starting_num_dice: int | float = num_dice
    starting_sides: int | float = sides

    # If it's the case that we were given a dice with negative sides,
    # then that doesn't mean anything in the real world. I cannot
    # for the life of me figure out a possible scenario where that
    # would make sense. We will just error out.
    if sides < 0:
        raise ValueError("The sides of a die must be positive or zero.")

    result_is_negative: bool = num_dice < 0

    if result_is_negative:
        num_dice = abs(num_dice)

    sides = ceil(sides)

    rolls: list[int | float] = []

    if roll_option == RollOption.Minimum:
        rolls = [1] * ceil(num_dice)
    elif roll_option == RollOption.Maximum:
        rolls = [floor(sides)] * floor(num_dice)

        if isinstance(num_dice, float) and (num_dice % 1) != 0:
            rolls.append(sides * (num_dice % 1))
    elif sides != 0:
        # Because this is not cryptographically secure, we have to noqa it
        # otherwise we get an S311 warning.
        rolls = [randint(1, floor(sides)) for _ in range(floor(num_dice))]  # noqa

        # If it's the case that the number of dice is a float, then
        # we take that to mean that it is a dice where the sides should
        # be lowered to reflect the float amount.
        #
        # We do not want this to effect all dice rolls however, only the
        # last one (or the only one if there's only a decimal portion).
        if isinstance(num_dice, float) and num_dice % 1 != 0:
            sides = ceil(sides * (num_dice % 1))
            # Not cryptographically secure
            rolls.append(randint(1, sides))  # noqa

    if result_is_negative:
        for roll_num in range(len(rolls)):
            rolls[roll_num] = -rolls[roll_num]

    result.add_roll(RollResults(f"{starting_num_dice}d{starting_sides}", rolls))

    return result
