"""Parser for string-based dice notation notes.

DiceParser:

    Acts as the interpreter for the incoming dice rolling string.
"""
from typing import Tuple

from .diceparser import DiceParser as DiceParser

__all__: Tuple[str, ...] = ("DiceParser",)
