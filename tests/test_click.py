
import pytest
from click.testing import CliRunner
from roll.click.click_dice import roll_cli

runner = CliRunner()


def test_basic_roll():
    result = runner.invoke(roll_cli, [""])
    print(result.output)
    assert result.exit_code == 0
    assert int(result.output.split()[-1]) in range(1, 21)


def test_roll_with_input():
    result = runner.invoke(roll_cli, ["2d6 + 4"])
    assert result.exit_code == 0
    assert int(result.output.split()[-1]) in range(6, 17)


def test_verbose_output():
    result = runner.invoke(roll_cli, ["4d6", "-v"])
    assert result.exit_code == 0
    assert "4d6: [" in result.output
    assert int(result.output.split()[-1]) in range(4, 25)


def test_verbose_ouput_mult_dice():
    result = runner.invoke(roll_cli, ["4d6 + 5d10", "-v"])
    assert result.exit_code == 0
    assert "4d6: [" in result.output
    assert "5d10: [" in result.output
    assert int(result.output.split()[-1]) in range(9, 75)


@pytest.mark.parametrize(('equation', 'result'), [
    # Int num dice and sides
    ("1d6", 1),
    ("10d6", 10),
    ("1000d10000", 1000),

    # Float number of dice
    ("0.5d1000", 1),
    ("0.99d9", 1),

    # Float sides
    ("15d5.5", 15),

    # Float num dice and sides
    ("100.5d2.75", 101),
])
def test_min_roll(equation: str, result: int):
    roll_result = runner.invoke(roll_cli, [equation, "-m", "-v"])
    print(roll_result.output)
    assert roll_result.exit_code == 0
    assert int(roll_result.output.split()[-1]) == result


@pytest.mark.parametrize(('equation', 'result'), [
    # Int num dice and sides
    ("1d6", 6),

    # Float number of dice
    ("0.01d100", 1),

    # Float number of sides
    ("1d0.5", 1),
    ("10d99.5", 1000),

    # float num dice and sides
    ("0.5d0.5", 0.5),
    ("0.5d19.5", 10),
    ("1.5d5.5", 9),
])
def test_max_roll(equation: str, result: int):
    roll_result = runner.invoke(roll_cli, [equation, "-M", "-v"])
    print(roll_result.output)
    assert roll_result.exit_code == 0
    assert float(roll_result.output.split()[-1]) == result
