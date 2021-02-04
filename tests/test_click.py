
from click.testing import CliRunner

from roll.click import roll_cli

runner = CliRunner()


# def test_basic_rolls():
#     for _ in range(1000):
#         result = runner.invoke(roll_cli, [])
#         assert result.exit_code == 0
#         assert int(result.output.split()[-1]) in range(1, 21)


# def test_basic_roll_verbose():
#     result = runner.invoke(roll_cli, ["-v"])
#     assert result.exit_code == 0
#     assert '1d20: ' in result.output
#     assert int(result.output.split()[-1]) in range(1, 21)
