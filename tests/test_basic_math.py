
import math
from typing import Union

import pytest
#from roll_cli.roll import roll
from src.roll_cli.roll import roll


@pytest.mark.parametrize("equation,result", [
    ('2 + 2', 4),
    ('10 + 52', 62),
    ('1 + 10 + 100 + 1000', 1111),
    ('8 + 16', 24),
    ('5 + 17 + 202 + 81', 305),
    ('19 + 57', 76),
    ('-5 + 20', 15),
    ('50 + -25', 25),
    ('1.5 + 0.5', 2),
    ('204.5 + 20', 224.5),
])
def test_addition(equation: str, result: Union[int, float]):
    assert roll(equation) == result


def test_addition_with_uneven_spaces2():
    with pytest.raises(Exception):
        roll('321\t\n  + \t\t\t   \t 18')


@pytest.mark.parametrize("equation,result", [
    ('10 - 5', 5),
    ('100 - 52', 48),
    ('1111 - 100 - 10 - 1', 1000),
    ('73 - 100', -27),
    ('5 - -10', 15),
])
def test_subtraction(equation: str, result: Union[int, float]):
    assert roll(equation) == result


@pytest.mark.parametrize("equation,result", [
    ('2 * 2', 4),
    ('20 * 5', 100),
    ('1 * 10 * 100', 1000),
    ('6 * 8 * 2 * 10', 960),
])
def test_multiplication(equation: str, result: Union[int, float]):
    assert roll(equation) == result


@pytest.mark.parametrize("equation,result", [
    ('5 / 5', 1),
    ('15 / 3', 5),
    ('48 / 6', 8),
    ('54 / 9', 6),
])
def test_division(equation: str, result: Union[int, float]):
    assert roll(equation) == result


@pytest.mark.parametrize(("equation", "result"), [
    ('5 // 5', 1),
    ('5.5 // 5', 1),
])
def test_floor_division(equation: str, result: Union[int, float]):
    """Ensure that the floor division operator works correctly."""
    assert roll(equation) == result


@pytest.mark.parametrize(("equation", "result"), [
    ('5**2', 25),
    ('2 ** 8', 256),
    ('1000 ** 0', 1),
])
def test_exponential(equation: str, result: Union[int, float]):
    """Ensure that the floor division operator works correctly."""
    assert roll(equation) == result


def test_add_mul():
    assert roll('1 + 2 * 3') == 7


def test_mul_add():
    assert roll('3 * 2 + 1') == 7


def test_sub_div():
    assert roll('10 - 5 / 5') == 9


def test_div_sub():
    assert roll('15 / 3 - 2') == 3


def test_sub_mul_add_mul_sub():
    assert roll('40 - 3 * 7 + 2 * 9 - 20') == 17


def test_parens():
    assert roll('(2 + 5) * 3') == 21


def test_parens1():
    assert roll('(4 + 2) * 3') == 18


def test_parens2():
    assert roll('3 * (10 - 5)') == 15


def test_parens3():
    assert roll('(2 + 8 / (9 - 5)) * 3') == 12


def test_modulus1():
    assert roll('5 % 2') == 1


def test_modulus2():
    assert roll('23 % 13') == 10


def test_modulus3():
    assert roll('19 % 12') == 7


def test_modulus4():
    assert roll('1 % 112') == 1


def test_modulus5():
    assert roll('66 % 11') == 0


def test_exponential1():
    assert roll('6 ** 3') == 216


def test_exponential2():
    assert roll('7 ** 5') == 16807


def test_factorial1():
    assert roll('5!') == 120


def test_factorial2():
    assert roll('0!') == 1


def test_bad_factorial1():
    with pytest.raises(ValueError):
        roll('-256!')


def test_bad_parens():
    with pytest.raises(Exception):
        roll('((')


def test_bad_parens2():
    with pytest.raises(Exception):
        roll('(2 +)')


def test_add_explonential():
    assert roll("3 + 7**3") == 346


@pytest.mark.parametrize("equation,result", [
    ('pi', math.pi),
    ('Pi', math.pi),
    ('PI', math.pi),
    ('pI', math.pi),
    ('e', math.e),
    ('E', math.e),
])
def test_constants(equation: str, result: Union[int, float]):
    assert roll(equation) == result


@pytest.mark.parametrize("equation,result", [
    ('sqrt 25', 5),
    ('Sqrt 25', 5),
    ('sqrT 25', 5),
    ('sQRt 25', 5),
    ('sQRT 25', 5),
    ('SQRT 25', 5),
    # Addition
    ('2 + sqrt 9', 5),
    ('sqrt 36 + 7', 13),
    # Subtraction
    ('sqrt 16 - 4', 0),
    ('20 - sqrt 100', 10),
    # Multiplication
    ('sqrt 4 * 12', 24),
    ('10 * sqrt 81', 90),
    # Division
    ('sqrt 25 / 5', 1),
    ('60 / sqrt 36', 10),
    # Unary minus
    ('sqrt --16', 4),
    ('- sqrt 49', -7),
    # Constants
    ('sqrt e', math.sqrt(math.e)),
    ('sqrt pi', math.sqrt(math.pi)),
    # Exponentiation
    ('sqrt 169 ** 2', 169),
    ('5 ** sqrt 9', 125),
    ('sqrt sqrt 10000', 10),
])
def test_sqrt(equation: str, result: Union[int, float]):
    assert roll(equation) == result
