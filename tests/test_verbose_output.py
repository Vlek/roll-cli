from roll import roll
from roll.parser.types import RollOption


def test_verbose_dice() -> None:
    output = roll("1d4+1d5+1d6", verbose=True, roll_option=RollOption.Minimum)
    expected_output: str = "\n".join([
        "Rolled: 1d4: [1]",
        "Rolled: 1d5: [1]",
        "Adding: 1 + 1 = 2",
        "Rolled: 1d6: [1]",
        "Adding: 2 + 1 = 3",
        "3",
        ])

    if str(output) != expected_output:
        raise Exception(f"The string output of the roll was not what we expected.\nRecieved: {output}\n\nExpected: {expected_output}")


def test_verbose_math() -> None:
    output = roll("2+3-4*5/2", verbose=True, roll_option=RollOption.Minimum)
    expected_output: str = "\n".join([
        "",
        ])

    if str(output) != expected_output:
        raise Exception(f"The string output of the roll was not what we expected. Recieved: {output}")
