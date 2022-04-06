"""
Test the project's operations to ensure proper functioning.

These tests should include targeted parameters to ensure that
the individual functions are working correctly by themselves
without being used in the greater project.
"""


from typing import Union

import pytest
from roll_cli.parser.operations import roll_dice
from roll_cli.parser.types import RollOption


@pytest.mark.parametrize(
    ('num_dice', 'sides', 'range_low', 'range_high'), [
        (0.5, 10, 1, 5),
        (0.01, 1000, 1, 10),
    ])
def test_dice_roll(
        num_dice: Union[int, float],
        sides: Union[int, float],
        range_low: int, range_high: int
    ) -> None:
    """Test the dice_roll function."""
    assert roll_dice(
        num_dice, sides, RollOption.Normal).total in range(range_low, range_high + 1)
