"""
Test the project's operations to ensure proper functioning.

These tests should include targeted parameters to ensure that
the individual functions are working correctly by themselves
without being used in the greater project.
"""


from typing import Union

import pytest
from roll.parser.operations import roll_dice
from roll.parser.types import EvaluationResults, RollOption


@pytest.mark.parametrize(
    ('num_dice', 'sides', 'range_low', 'range_high'), [
        (0.5, 10, 1, 5),
        (0.01, 1000, 1, 10),
    ])
def test_dice_roll(
    num_dice: Union[int, float, EvaluationResults],
    sides: Union[int, float, EvaluationResults],
    range_low: int, range_high: int
) -> None:
    """Test the dice_roll function."""
    assert roll_dice(
        num_dice, sides, RollOption.Normal) in range(range_low, range_high + 1)
