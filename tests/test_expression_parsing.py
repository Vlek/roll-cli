"""Test that expressions are being parsed correctly."""
# from roll import roll
from typing import Union

import pytest

import roll_cli.parser.diceparser as dp
from roll_cli.parser.types import EvaluationResults

parser = dp.DiceParser()


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
        ("       2    d  8           ", 2, 16),
    ],
)
def test_interpret_dice(equation: str, range_low: int, range_high: int) -> None:
    """Test that dice parsing is functioning correctly."""
    evaluation_results: Union[int, float, EvaluationResults] = parser.evaluate(equation)
    if isinstance(evaluation_results, EvaluationResults):
        result: Union[int, float] = evaluation_results.total
    else:
        result = evaluation_results

    assert result in range(range_low, range_high + 1)


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
