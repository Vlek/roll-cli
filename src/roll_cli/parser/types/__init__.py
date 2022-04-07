"""Contains types used for the dice roller.

Types:
    - EvaluationResult:

    - RollOption:

    - RollResults:
"""
from typing import Tuple

from .evaluationresults import EvaluationResults as EvaluationResults
from .rolloption import RollOption as RollOption
from .rollresults import RollResults as RollResults


__all__: Tuple[str, ...] = (
    "EvaluationResults",
    "RollOption",
    "RollResults",
)
