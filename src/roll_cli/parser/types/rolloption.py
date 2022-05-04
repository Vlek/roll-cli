"""Create options that change the outcomes of dice rolls.

In order to have the feature that we allow for minimum and maximum rolls,
we need to be able to flag that that is an option within our dice roller.
This feature is required to play some games, including D&D where critical
hits and misses are sometimes used with these options.
"""
from enum import Enum


class RollOption(Enum):
    """Enum for expressing dice roll behavior.

    Available roll options:
        Minimum: The dice will return the lowest possible roll.
            e.g. 1d6 -> 1

        Normal: The dice are rolled normally, a random number
                is given in range.
            e.g. 1d6 -> (Number between 1 - 6 inclusive)

        Maximum: The dice will return the highest possible roll.
            e.g. 1d6 -> 6
    """

    Minimum = 0
    Normal = 1
    Maximum = 2
