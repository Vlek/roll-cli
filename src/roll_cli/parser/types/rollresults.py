"""
Roll result object for saving information for a group of rolls.

The RollResult is an object that keeps information regarding a
roll (either a singular die roll or a group of like dice rolled).
"""

from __future__ import annotations

from math import ceil, fsum
from typing import List, Union


class RollResults:
    """
    Saves results for a single or group of dice.

    dice: The dice string that was rolled
    rolls: A collection of the values of all rolls

    Contains helper methods for handling changes to a given
    roll in order to contain the logic for roll collections.
    """

    def __init__(self: RollResults, dice: str,
                 rolls: List[Union[int, float]]) -> None:
        """Initialize a RollResults object."""
        self.dice: str = dice
        self.rolls: List[Union[int, float]] = rolls

    def total(self: RollResults) -> Union[int, float]:
        """Return the sum of the values of the rolls."""
        return sum(self.rolls)

    def keep_lowest(self: RollResults,
                    num: Union[int, float] = 1) -> Union[int, float]:
        """Keep the lowest num rolls."""
        previous_sum: Union[int, float] = sum(self.rolls)
        self.rolls = sorted(self.rolls)[:ceil(num)]

        return previous_sum - fsum(self.rolls)

    def keep_highest(self: RollResults,
                     num: Union[int, float] = 1) -> Union[int, float]:
        """Keep the highest num rolls."""
        previous_sum: Union[int, float] = sum(self.rolls)
        self.rolls = sorted(self.rolls)[-ceil(num):]

        return previous_sum - fsum(self.rolls)
