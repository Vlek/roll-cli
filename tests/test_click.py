
from click.testing import CliRunner
from roll.click_dice import roll_cli

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


def test_min_roll():
    result = runner.invoke(roll_cli, ["5d6", "-m", "-v"])
    print(result.output)
    assert result.exit_code == 0
    assert int(result.output.split()[-1]) == 5
