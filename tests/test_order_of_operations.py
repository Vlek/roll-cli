
from typing import Union

import pytest
from src.roll_cli import roll


def test_mul_b4_add1():
    assert roll('2+6*4') == 26


def test_mul_b4_add2():
    assert roll('5+4*2+9') == 22


def test_mul_b4_add3():
    assert roll('1+2*3+4*5+6') == 33


def test_mul_b4_add4():
    assert roll('7 * 4+ 2 + 8') == 38


def test_mul_b4_add5():
    assert roll('9 + 4 + 42 + 7 * 4') == 83


def test_div_b4_sub1():
    assert roll('100 - 21 / 7') == 97


def test_parens():
    assert roll('(1 + 4) / 5') == 1


def test_inception_dice1():
    assert roll('1d7d4d6') in range(1, 169)


def test_inception_dice2():
    assert roll('7d4d20') in range(7, 561)


def test_inception_dice3():
    assert roll('10d2d4') in range(10, 81)


def test_inception_dice4():
    assert roll('2d4d6d8') in range(2, 385)


def test_inception_dice_with_parens1():
    assert roll('(1d4)d6') in range(1, 25)


def test_inception_dice_with_parens2():
    assert roll('1d(1d20)') in range(1, 21)


def test_inception_dice_with_parens3():
    assert roll('4d(10d7d8)') in range(10, 2241)

@pytest.mark.parametrize("equation,answer", [
    ('7 - 24 / 8 * 4 + 6', 1),
    ('18 / 3 - 7 + 2 * 5', 9),
    ('6 * 4 / 12 + 72 / 8 - 9', 2),
    ('(17 - 6 / 2) + 4 * 3', 26),
    ('-2 * (1 * 4 - 2 / 2) + (6 + 2 - 3)', -1),
    ('-1 * ((3 - 4 * 7) / 5) - 2 * 24 / 6', -3),
    ('(3*5^2/15)-(5-2^2)', 4),
    ('(1^4*2^2+3^3)-2**5/4', 23),
    ('(22/2-2*5)^2 + (4-6/6)**2', 10),
    ('8 + 2 - (11/4) * 6 + 3', -3.5),
    ('2 * 2 + 11 * 4 - (10 + 6)', 32),
    ('3 + (2 / 5 * 5 - 6 / 3)', 3),
    ('7 - 10 * 2 - 4 * (6-9)', -1),
    ('5 - (8 * 6 / 6 * 7) / 7', -3),
    ('7 * 3 / 8 - 5 + (5 * 9)', 42.625),
    ('2-(2 / 8 - 7 / 2 * 4)', 15.75),
    ('(11 - (2^3 - 11)) * (2 - (-2))', 56),
    ('(((-3)^2 + (-3)) * (-3)) - (-2) + (-3)', -19),
    ('4 - (-11) * (5 - (5^2 + (-11)))', -95),
    ('(((-2)^2 + (-2)) * (-2)) - (-7) + (-2)', 1),
])
def test_oop_worksheet_problems(
        equation: str,
        answer: Union[int, float]):
    """
    These are all ones I've pulled from order of operations math
    worksheets. These are ones with verified answers and should
    be able to thoroughly test our order of operations even for
    pretty crazy problems!
    """
    assert roll(equation) == answer
