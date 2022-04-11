"""Test that expressions are being parsed correctly."""
# from roll import roll
from typing import Union

import pytest

import roll_cli.parser.diceparser as dp

parser = dp.DiceParser()


@pytest.mark.skip()
def test_for_recursive_issues() -> None:
    """Test to ensure no recursive issues exist in parser.

    This is a built-in test from pyparsing that ensures
    that the regex that is created from the supplied
    grammar does not have any recursive issues.

    From what I can gather, it's not the end of the world
    if there are any, but I am sure it's not a good thing
    to leave them in there and could effect the speed.
    """
    assert parser._parser.validate()


@pytest.mark.parametrize(
    "equation,result",
    [
        ("42", 42),
        ("-64", -64),
        ("           239       ", 239),
        ("1.0", 1.0),
        ("3.1415", 3.1415),
        # I don't like this, but Pyparser allows it.
        ("9.", 9.0),
        (".098", 0.098),
        ("-2.0", -2.0),
        ("-700.", -700.0),
    ],
)
def test_interpret_number(equation: str, result: Union[int, float]) -> None:
    """Test that the parser parses numbers correctly."""
    assert parser.evaluate(equation) == result


@pytest.mark.parametrize(
    ("equation", "range_low", "range_high"),
    [
        ("d20", 1, 20),
        ("1d20", 1, 20),
        ("       2    d  8           ", 2, 17),
    ],
)
def test_interpret_dice(equation: str, range_low: int, range_high: int) -> None:
    """Test that dice parsing is functioning correctly."""
    assert parser.evaluate(equation) in range(range_low, range_high)


def test_interpret_subtract_negative() -> None:
    """Test subtracting a negative number."""
    assert parser.evaluate("1 - -5") == 6


def test_unary_negative() -> None:
    """Test that the unary minus works on a negative number."""
    assert parser.evaluate("--10") == 10


@pytest.mark.parametrize(
    "equation",
    [
        ("bad input"),
        ("2 + (2 + 3"),
        ("2 +"),
        ("+ 6"),
        ("(6**)2"),
        ("d"),
        ("+"),
        ("*"),
        ("-"),
        ("/"),
        ("%"),
    ],
)
def test_bad_input(equation: str) -> None:
    """Test that things that should not work do not work."""
    with pytest.raises(Exception):
        parser.evaluate(equation)
