"""Testing order of operations."""
from typing import Union

import pytest

from roll_cli import roll
from roll_cli.parser.types import RollOption


@pytest.mark.parametrize(
    "equation,result",
    [
        ("2+6*4", 26),
        ("5+4*2+9", 22),
        ("1+2*3+4*5+6", 33),
        ("7 * 4+ 2 + 8", 38),
        ("9 + 4 + 42 + 7 * 4", 83),
        ("100 - 21 / 7", 97),
        ("(1 + 4) / 5", 1),
    ],
)
def test_order_of_operations(equation: str, result: int) -> None:
    """Test the order of operations with different operator combinations."""
    assert roll(equation) == result


@pytest.mark.parametrize(
    ("equation", "range_low", "range_high"),
    [
        ("1d7d4d6", 1, 169),
        ("7d4d20", 7, 561),
        ("10d2d4", 10, 81),
        ("2d4d6d8", 2, 385),
        ("(1d4)d6", 1, 25),
        ("1d(1d20)", 1, 21),
        ("4d(10d7d8)", 10, 2241),
    ],
)
def test_inception_dice(equation: str, range_low: int, range_high: int) -> None:
    """Test putting dice rolls together one after another."""
    assert roll(equation) in range(range_low, range_high)


@pytest.mark.parametrize(
    ("equation", "result"),
    [
        ("1d4d5", 20),
    ],
)
def test_inception_dice_max(equation: str, result: int) -> None:
    """Test that, when we are rolling maxes, that we get the intended values."""
    assert roll(equation, roll_option=RollOption.Maximum) == result


@pytest.mark.parametrize(
    "equation,answer",
    [
        ("7 - 24 / 8 * 4 + 6", 1),
        ("18 / 3 - 7 + 2 * 5", 9),
        ("6 * 4 / 12 + 72 / 8 - 9", 2),
        ("(17 - 6 / 2) + 4 * 3", 26),
        ("-2 * (1 * 4 - 2 / 2) + (6 + 2 - 3)", -1),
        ("-1 * ((3 - 4 * 7) / 5) - 2 * 24 / 6", -3),
        ("(3*5^2/15)-(5-2^2)", 4),
        ("(1^4*2^2+3^3)-2**5/4", 23),
        ("(22/2-2*5)^2 + (4-6/6)**2", 10),
        ("8 + 2 - (11/4) * 6 + 3", -3.5),
        ("2 * 2 + 11 * 4 - (10 + 6)", 32),
        ("3 + (2 / 5 * 5 - 6 / 3)", 3),
        ("7 - 10 * 2 - 4 * (6-9)", -1),
        ("5 - (8 * 6 / 6 * 7) / 7", -3),
        ("7 * 3 / 8 - 5 + (5 * 9)", 42.625),
        ("2-(2 / 8 - 7 / 2 * 4)", 15.75),
        ("(11 - (2^3 - 11)) * (2 - (-2))", 56),
        ("(((-3)^2 + (-3)) * (-3)) - (-2) + (-3)", -19),
        ("4 - (-11) * (5 - (5^2 + (-11)))", -95),
        ("(((-2)^2 + (-2)) * (-2)) - (-7) + (-2)", 1),
    ],
)
def test_oop_worksheet_problems(equation: str, answer: Union[int, float]) -> None:
    """Test against order of operation worksheets.

    These are all ones I've pulled from order of operations math
    worksheets. These are ones with verified answers and should
    be able to thoroughly test our order of operations even for
    pretty crazy problems!
    """
    assert roll(equation) == answer
