"""Testing dice rolling with math operators."""
from math import ceil
from typing import Union

import pytest

from roll_cli import roll
from roll_cli.parser.types import EvaluationResults


@pytest.mark.parametrize(
    ("equation", "range_low", "range_high"),
    [
        ("d% + 1000", 1001, 1100),
        ("d6 + d8", 2, 14),
        ("1d8 + 3d6", 4, 27),
    ],
)
def test_dice_with_addition(equation: str, range_low: int, range_high: int) -> None:
    """Testing to ensure that dice rolls work with the addition operator."""
    assert roll(equation) in range(range_low, range_high)


@pytest.mark.parametrize(
    ("equation", "range_low", "range_high"),
    [
        ("4 * 1d4", 4, 17),
        ("d6 * 4", 4, 25),
    ],
)
def test_dice_with_multiplication(
    equation: str, range_low: int, range_high: int
) -> None:
    """Testing to ensure that dice rolls work with the multiplication operator."""
    assert roll(equation) in range(range_low, range_high)


@pytest.mark.parametrize(
    ("equation", "range_low", "range_high"),
    [
        ("1d4 + 16 / 4", 5, 9),
        ("(2d8 + 8) * 4", 40, 97),
    ],
)
def test_dice_with_multiple_operators(
    equation: str, range_low: int, range_high: int
) -> None:
    """Testing to ensure dice rolling works with multiple operators at once."""
    assert roll(equation) in range(range_low, range_high)


@pytest.mark.parametrize(
    ("equation", "result"),
    [
        ("5**2d1", 25),
        ("5d1**5", 5),
    ],
)
def test_dice_expo(equation: str, result: Union[int, float]) -> None:
    """Ensure that the exponential op works with dice rolls.

    One of the major things that could be wrong with this is
    the desired order of operations may not be followed.

    Based on what feels right, I believe exponentiation should
    take place before dice rolling. So '5**2d1' should be
    evaluated as '(5**2)d1'.
    """
    assert roll(equation) == result


@pytest.mark.parametrize(
    ("equation", "range_low", "range_high"),
    [
        # Number of dice is being square rooted
        ("sqrt 25 d 6", 5, 30),
        # Sides are being square rooted
        ("1d sqrt 36", 1, 6),
        # Square root an EvaluationResults object after a dice roll
        ("sqrt(1d16)", 1, 4),
    ],
)
def test_dice_sqrt(equation: str, range_low: int, range_high: int) -> None:
    """Test rolling dice before and after taking a squareroot."""
    result = roll(equation, verbose=True)

    if isinstance(result, EvaluationResults):
        total: Union[int, float] = result.total
    else:
        total = result

    # It's important to ceil the value because some of the long
    # decimal places will throw this off.
    # Python states 1.390823490823 not in range(1, 5) otherwise
    assert ceil(total) in range(range_low, range_high + 1)


@pytest.mark.parametrize(
    ("equation", "range_low", "range_high"),
    [
        # Sides is being factorial'd
        ("1d6!", 1, 720),
        # Number is factorial
        ("6!d1", 720, 720),
        # Factorial an EvaluationResults object with a dice roll
        # TODO: Ensure that we have the rolls still present.
        ("(1d6)!", 1, 720),
    ],
)
def test_dice_factorial(equation: str, range_low: int, range_high: int) -> None:
    """Ensure that dice rolling works with the factorial operation."""
    assert roll(equation) in range(range_low, range_high + 1)
