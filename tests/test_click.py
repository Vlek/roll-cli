
from click.testing import CliRunner
import pytest
from roll.roll import roll_cli

runner = CliRunner()


def test_basic_roll():
    result = runner.invoke(roll_cli, [])
    assert result.exit_code == 0
    assert int(result.output[-2]) in range(1, 21)


def test_basic_roll_verbose():
    result = runner.invoke(roll_cli, ["-v"])
    assert result.exit_code == 0
    assert '1d20: ' in result.output
    assert int(result.output.split()[-1]) in range(1, 21)
