from src.roll_cli import roll
from src.roll_cli.parser.types import RollOption
import pytest


@pytest.mark.parametrize("equation,expected_output", [
    ("1+2", "Adding: 1 + 2 = 3\n3"),
    ("2-1", "Subtracting: 2 - 1 = 1\n1"),
    ("3*7", "Multiplying: 3 * 7 = 21\n21"),
    ("100/5", "Dividing: 100 / 5 = 20.0\n20.0"),
    ("50//7", "Floor dividing: 50 // 7 = 7\n7"),
    ("37%100", "Modulus dividing: 37 % 100 = 37\n37"),
    ("2**8", "Exponentiating: 2 ** 8 = 256\n256"),
    ("2^8", "Exponentiating: 2 ** 8 = 256\n256"),
    ("5!", "Factorial: 5! = 120\n120"),
])
def test_verbose_math(equation: str, expected_output: str) -> None:
    output = roll(equation, verbose=True, roll_option=RollOption.Minimum)

    if str(output) != expected_output:
        raise Exception(f"The string output of the roll was not what we expected.\nRecieved: {output}\n\nExpected: {expected_output}")


@pytest.mark.parametrize("equation,expected_output", [
    ("1d6", "Rolled: 1d6: [1]\n1"),
    ("1d4+1d5+1d6", "\n".join([
        "Rolled: 1d4: [1]",
        "Rolled: 1d5: [1]",
        "Adding: 1 + 1 = 2",
        "Rolled: 1d6: [1]",
        "Adding: 2 + 1 = 3",
        "3",
    ])),
    ("4d6K3", "\n".join([
        "Rolled: 4d6: [1, 1, 1, 1]",
        "Keeping highest: 3: [1, 1, 1]",
        "3"
    ])),
    ("10d50k7", "\n".join([
        "Rolled: 10d50: [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]",
        "Keeping lowest: 7: [1, 1, 1, 1, 1, 1, 1]",
        "7"
    ])),
    ("10d50k7k6K5k4K3k2K1", "\n".join([
        "Rolled: 10d50: [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]",
        "Keeping lowest: 7: [1, 1, 1, 1, 1, 1, 1]",
        "Keeping lowest: 6: [1, 1, 1, 1, 1, 1]",
        "Keeping highest: 5: [1, 1, 1, 1, 1]",
        "Keeping lowest: 4: [1, 1, 1, 1]",
        "Keeping highest: 3: [1, 1, 1]",
        "Keeping lowest: 2: [1, 1]",
        "Keeping highest: 1: [1]",
        "1"
    ])),
])
def test_verbose_dice(equation: str, expected_output: str) -> None:
    output = roll(equation, verbose=True, roll_option=RollOption.Minimum)

    if str(output) != expected_output:
        raise Exception(f"The string output of the roll was not what we expected.\nRecieved: {output}\n\nExpected: {expected_output}")
