

from roll import roll
from roll.parser.types import RollOption


def test_verbose_dice() -> None:
    output = roll("1d6", verbose=True)
    raise Exception(output)
