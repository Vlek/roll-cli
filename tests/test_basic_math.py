"""Test basic math operators."""
import math
from typing import Union

import pytest

from roll_cli.roll import roll


@pytest.mark.parametrize(
    "equation,result",
    [
        ("2 + 2", 4),
        ("10 + 52", 62),
        ("1 + 10 + 100 + 1000", 1111),
        ("8 + 16", 24),
        ("5 + 17 + 202 + 81", 305),
        ("19 + 57", 76),
        ("-5 + 20", 15),
        ("50 + -25", 25),
        ("1.5 + 0.5", 2),
        ("204.5 + 20", 224.5),
    ],
)
def test_addition(equation: str, result: Union[int, float]) -> None:
    """Test that the addition operator works."""
    assert roll(equation) == result


def test_addition_with_uneven_spaces2() -> None:
    """Test whitespace does not cause errors."""
    with pytest.raises(Exception):
        roll("321\t\n  + \t\t\t   \t 18")


@pytest.mark.parametrize(
    "equation,result",
    [
        ("10 - 5", 5),
        ("100 - 52", 48),
        ("1111 - 100 - 10 - 1", 1000),
        ("73 - 100", -27),
        ("5 - -10", 15),
    ],
)
def test_subtraction(equation: str, result: Union[int, float]) -> None:
    """Test that the subtraction operator works."""
    assert roll(equation) == result


@pytest.mark.parametrize(
    "equation,result",
    [
        ("2 * 2", 4),
        ("20 * 5", 100),
        ("1 * 10 * 100", 1000),
        ("6 * 8 * 2 * 10", 960),
    ],
)
def test_multiplication(equation: str, result: Union[int, float]) -> None:
    """Test that the multiplcation operator works."""
    assert roll(equation) == result


@pytest.mark.parametrize(
    "equation,result",
    [
        ("5 / 5", 1),
        ("15 / 3", 5),
        ("48 / 6", 8),
        ("54 / 9", 6),
    ],
)
def test_division(equation: str, result: Union[int, float]) -> None:
    """Test that the normal division operator works."""
    assert roll(equation) == result


@pytest.mark.parametrize(
    ("equation", "result"),
    [
        ("5 // 5", 1),
        ("5.5 // 5", 1),
    ],
)
def test_floor_division(equation: str, result: Union[int, float]) -> None:
    """Ensure that the floor division operator works correctly."""
    assert roll(equation) == result


@pytest.mark.parametrize(
    ("equation", "result"),
    [
        ("5**2", 25),
        ("2 ** 8", 256),
        ("1000 ** 0", 1),
        ("6 ** 3", 216),
        ("7 ** 5", 16807),
    ],
)
def test_exponential(equation: str, result: Union[int, float]) -> None:
    """Ensure that the floor division operator works correctly."""
    assert roll(equation) == result


@pytest.mark.parametrize(
    ("equation", "result"),
    [
        ("1 + 2 * 3", 7),
        ("3 * 2 + 1", 7),
        ("10 - 5 / 5", 9),
        ("15 / 3 - 2", 3),
        ("40 - 3 * 7 + 2 * 9 - 20", 17),
    ],
)
def test_multiple_operators(equation: str, result: int) -> None:
    """Test that multiple operators together function expectedly."""
    assert roll(equation) == result


def test_add_explonential() -> None:
    """Test the addition operator with the exponential operator."""
    assert roll("3 + 7**3") == 346


@pytest.mark.parametrize(
    ("equation", "result"),
    [
        ("(2 + 5) * 3", 21),
        ("(4 + 2) * 3", 18),
        ("3 * (10 - 5)", 15),
        ("(2 + 8 / (9 - 5)) * 3", 12),
    ],
)
def test_parens(equation: str, result: Union[int, float]) -> None:
    """Test that parens are working correctly."""
    assert roll(equation) == result


@pytest.mark.parametrize(
    ("equation", "result"),
    [
        ("5 % 2", 1),
        ("23 % 13", 10),
        ("19 % 12", 7),
        ("1 % 112", 1),
        ("66 % 11", 0),
    ],
)
def test_modulus(equation: str, result: Union[int, float]) -> None:
    """Test that the modulus operator works correctly."""
    assert roll(equation) == result


@pytest.mark.parametrize(
    ("equation", "result"),
    [
        ("5!", 120),
        ("0!", 1),
    ],
)
def test_factorial(equation: str, result: int) -> None:
    """Test that the exponential operator works correctly."""
    assert roll(equation) == result


def test_bad_factorial1() -> None:
    """Test that given an incorrect factorial errors out."""
    with pytest.raises(ValueError):
        roll("-256!")


@pytest.mark.parametrize(
    ("equation"),
    [
        ("(2 +)"),
        ("(("),
    ],
)
def test_bad_parens(equation: str) -> None:
    """Test to ensure that incorrectly given parens errors out."""
    with pytest.raises(Exception):
        roll(equation)


@pytest.mark.parametrize(
    "equation,result",
    [
        ("pi", math.pi),
        ("Pi", math.pi),
        ("PI", math.pi),
        ("pI", math.pi),
        ("e", math.e),
        ("E", math.e),
    ],
)
def test_constants(equation: str, result: Union[int, float]) -> None:
    """Test that the constants are being parsed correctly."""
    assert roll(equation) == result


@pytest.mark.parametrize(
    "equation,result",
    [
        ("sqrt 25", 5),
        ("Sqrt 25", 5),
        ("sqrT 25", 5),
        ("sQRt 25", 5),
        ("sQRT 25", 5),
        ("SQRT 25", 5),
        # Addition
        ("2 + sqrt 9", 5),
        ("sqrt 36 + 7", 13),
        # Subtraction
        ("sqrt 16 - 4", 0),
        ("20 - sqrt 100", 10),
        # Multiplication
        ("sqrt 4 * 12", 24),
        ("10 * sqrt 81", 90),
        # Division
        ("sqrt 25 / 5", 1),
        ("60 / sqrt 36", 10),
        # Unary minus
        ("sqrt --16", 4),
        ("- sqrt 49", -7),
        # Constants
        ("sqrt e", math.sqrt(math.e)),
        ("sqrt pi", math.sqrt(math.pi)),
        # Exponentiation
        ("sqrt 169 ** 2", 169),
        ("5 ** sqrt 9", 125),
        ("sqrt sqrt 10000", 10),
    ],
)
def test_sqrt(equation: str, result: Union[int, float]) -> None:
    """Test the squareroot operator."""
    assert roll(equation) == result


@pytest.mark.parametrize(
    "equation,result",
    [
        # Equal to
        ("1=1", 1),
        ("0=0", 1),
        ("5=3.0", 0),
        # Less than
        ("1<5", 1),
        ("4<5", 1),
        ("9.999<10", 1),
        ("100<-100", 0),
        # Greater than
        ("1>10", 0),
        ("10>0", 1),
        # Less than or equal to
        ("1<=1", 1),
        ("2<=99", 1),
        ("100<=50", 0),
        # Greater than or equal to
        ("100000>=23.25", 1),
        ("1>=1", 1),
        ("37>=50", 0),
    ],
)
def test_comparison_ops(equation: str, result: Union[int, float]) -> None:
    """Testing comparison operators."""
    assert roll(equation) == result
