"""
Defines EvaluationResults object to hold parsing state throughout evaluation.

The EvaluationResults object is meant to solve an issue that was encountered
when attempting to add in dice roll modifiers. Instead of having the
heavy-lifting happening within our expression parser (which also caused
issues with recursive expressions and verbose expressions), we are going to
have an object that acts like an onion and coalesce all of the history
together into a comprehensible bundle.

What this will allow us to do is have things like `4d6K3` be two separate
expressions to be parsed by our parser without having to state that there
is a dice expression and another for the keep (K) notation. The real
beauty of this comes from our ability to them chain these statements
together, allowing for things like 10d4K5k2K1 without having to write
our expression parser to handle this case.

This method should also help with dealing with testing. By having the
ability to capture our history for math and dice rolls, we can see
whether it is the case that it is acting normally throughout the
process and not just relying on the end result being within a certain
acceptable range. Better, more informative tests can be made this way.
"""
from __future__ import annotations

from enum import Enum
from typing import List, Optional, Union

import roll.parser.types


class Operators(Enum):
    """
    Helper operator names for handling operations.

    This makes it so that we don't have magic strings
    everywhere. Instead, we can do things like:
        Operators.add
    """

    add = "+"
    sub = "-"
    mul = "*"
    truediv = "/"
    floordiv = "//"
    mod = "%"
    expo = "^"
    expo2 = "**"
    die = "d"


class EvaluationResults():
    """Hold the current state of all rolls and the total from other ops."""

    def __init__(self: EvaluationResults,
                 value: Union[int, float, EvaluationResults] = None,
                 rolls: List[roll.parser.types.RollResults] = None,
                 last_operation: Operators = None) -> None:
        """Initialize an EvaluationResults object."""
        if rolls is None:
            rolls = []

        total: Optional[Union[int, float]] = None

        if isinstance(value, EvaluationResults):
            rolls.extend(value.rolls)
            total = value.total
        else:
            total = value

        self.total: Union[int, float] = total or 0
        self.rolls: List[roll.parser.types.RollResults] = rolls
        self.last_operation: Union[Operators, None] = last_operation

    def add_roll(self: EvaluationResults,
                 roll: roll.parser.types.RollResults) -> None:
        """Add the results of a roll to the total evaluation results."""
        self.total += roll.total()
        self.rolls.append(roll)

    def _collect_rolls(self: EvaluationResults, er: EvaluationResults) -> None:
        """
        Add all rolls together if both objects are EvaluationResults.

        The way that we do this is by extending the other object's rolls
        in place for efficiency's sake and then we set our object to that
        one instead of the other way around so that we hopefully are going
        to have the most recently roll as our last.
        """
        er.rolls.extend(self.rolls)
        self.rolls = er.rolls

    def __str__(self: EvaluationResults) -> str:
        """
        Return a string representation of the eval results.

        This will output all of the history of the dice roll
        along with the total sum.

        e.g.
        Roll: 4d6 + 2

        4d6: [3, 1, 1, 2]
        7 + 2: 9
        9

        Roll: 10d10K5 + 4

        10d10: [10, 6, 2, 1, 3, 3, 4, 8, 6, 4]
        K5: [4, 6, 6, 8, 10]
        34 + 4: 38
        38
        """
        return f"{self.total}"

    def __int__(self: EvaluationResults) -> int:
        """Change the evaluation result total to an integer."""
        return int(self.total)

    def __float__(self: EvaluationResults) -> float:
        """Change the evaluation result total to a float."""
        return float(self.total)

    def __len__(self: EvaluationResults) -> int:
        """Return the number of rolls that have been rolled."""
        return len(self.rolls)

    def __eq__(self: EvaluationResults, other: object) -> bool:
        """Return whether or not a given value is numerically equal."""
        if not isinstance(other, (int, float, EvaluationResults)):
            return False

        if isinstance(other, (int, float)):
            return other == self.total

        return self.total == other.total

    def __neg__(self: EvaluationResults) -> EvaluationResults:
        """Negate the total value."""
        self.total = -self.total
        return self

    def __add__(self: EvaluationResults,
                x: Union[int, float, EvaluationResults]) -> EvaluationResults:
        """Add a given value to the evaluation result total."""
        self.last_operation = Operators.add

        if isinstance(x, (int, float)):
            self.total += x
        elif isinstance(x, EvaluationResults):
            self._collect_rolls(x)
            self.total += x.total
        else:
            raise TypeError("The supplied type is not valid: " + type(x))

        return self

    def __iadd__(self: EvaluationResults,
                 x: Union[int, float, EvaluationResults]) -> EvaluationResults:
        """Add a given value to the evaluation result total."""
        return self.__add__(x)

    def __radd__(self: EvaluationResults,
                 x: Union[int, float, EvaluationResults]) -> EvaluationResults:
        """Add a given value to the evaluation result total."""
        return self.__add__(x)

    def __sub__(self: EvaluationResults,
                x: Union[int, float, EvaluationResults]) -> EvaluationResults:
        """Subtract a given value from the evaluation result total."""
        self.last_operation = Operators.sub

        if isinstance(x, (int, float)):
            self.total -= x
        elif isinstance(x, EvaluationResults):
            self._collect_rolls(x)
            self.total -= x.total
        else:
            raise TypeError("The supplied type is not valid: " + type(x))

        return self

    def __isub__(self: EvaluationResults,
                 x: Union[int, float, EvaluationResults]) -> EvaluationResults:
        """Subtract a given value from the evaluation result total."""
        return self.__sub__(x)

    def __rsub__(self: EvaluationResults,
                 x: Union[int, float]) -> EvaluationResults:
        """Subtract a given value from the evaluation result total."""
        self.last_operation = Operators.sub

        # We don't have to compare for EvaluationResults because that will
        # use __sub__ instead!
        if isinstance(x, (int, float)):
            self.total = x - self.total
        else:
            raise TypeError("The supplied type is not valid: " + type(x))

        return self

    def __mul__(self: EvaluationResults,
                x: Union[int, float, EvaluationResults]) -> EvaluationResults:
        """Multiply the evaluation result total by a given value."""
        self.last_operation = Operators.mul

        if isinstance(x, (int, float)):
            self.total *= x
        elif isinstance(x, EvaluationResults):
            self._collect_rolls(x)
            self.total *= x.total
        else:
            raise TypeError("The supplied type is not valid: " + type(x))

        return self

    def __imul__(self: EvaluationResults,
                 x: Union[int, float, EvaluationResults]) -> EvaluationResults:
        """Multiply the evaluation result total by a given value."""
        return self.__mul__(x)

    def __rmul__(self: EvaluationResults,
                 x: Union[int, float, EvaluationResults]) -> EvaluationResults:
        """Multiply the evaluation result total by a given value."""
        return self.__mul__(x)

    def __truediv__(self: EvaluationResults,
                    x: Union[int, float, EvaluationResults]
                    ) -> EvaluationResults:
        """Divide the evaluation result total by a given number."""
        self.last_operation = Operators.truediv

        if isinstance(x, (int, float)):
            self.total /= x
        elif isinstance(x, EvaluationResults):
            self._collect_rolls(x)
            self.total /= x.total
        else:
            raise TypeError("The supplied type is not valid: " + type(x))

        return self

    def __itruediv__(self: EvaluationResults,
                     x: Union[int, float, EvaluationResults]
                     ) -> EvaluationResults:
        """Divide the evaluation result total by a given number."""
        return self.__truediv__(x)

    def __rtruediv__(self: EvaluationResults,
                     x: Union[int, float, EvaluationResults]
                     ) -> EvaluationResults:
        """Divide the evaluation result total by a given number."""
        self.last_operation = Operators.truediv

        # We do not have to check for EvaluationResults, those will
        # be handled by __truediv__!
        if isinstance(x, (int, float)):
            self.total = x / self.total
        else:
            raise TypeError("The supplied type is not valid: " + type(x))

        return self

    def __floordiv__(self: EvaluationResults,
                     x: Union[int, float, EvaluationResults]
                     ) -> EvaluationResults:
        """Divide the evaluation result total by a given number and floor."""
        self.last_operation = Operators.floordiv

        if isinstance(x, (int, float)):
            self.total //= x
        elif isinstance(x, EvaluationResults):
            self._collect_rolls(x)
            self.total //= x.total
        else:
            raise TypeError("The supplied type is not valid: " + type(x))

        return self

    def __ifloordiv__(self: EvaluationResults,
                      x: Union[int, float, EvaluationResults]
                      ) -> EvaluationResults:
        """Divide the evaluation result total by a given number and floor."""
        return self.__floordiv__(x)

    def __rfloordiv__(self: EvaluationResults,
                      x: Union[int, float, EvaluationResults]
                      ) -> EvaluationResults:
        """Divide the evaluation result total by a given number and floor."""
        self.last_operation = Operators.floordiv

        # We do not have to check for EvaluationResults, those will be
        # handled by __floordiv__!
        if isinstance(x, (int, float)):
            self.total = x // self.total
        else:
            raise TypeError("The supplied type is not valid: " + type(x))

        return self

    def __mod__(self: EvaluationResults,
                x: Union[int, float, EvaluationResults]) -> EvaluationResults:
        """Perform modulus divison on the evaluation total with given value."""
        self.last_operation = Operators.mod

        if isinstance(x, (int, float)):
            self.total %= x
        elif isinstance(x, EvaluationResults):
            self._collect_rolls(x)
            self.total %= x.total
        else:
            raise TypeError("The supplied type is not valid: " + type(x))

        return self

    def __imod__(self: EvaluationResults,
                 x: Union[int, float, EvaluationResults]) -> EvaluationResults:
        """Perform modulus divison on the evaluation total with given value."""
        return self.__mod__(x)

    def __rmod__(self: EvaluationResults,
                 x: Union[int, float, EvaluationResults]) -> EvaluationResults:
        """Perform modulus divison on the evaluation total with given value."""
        self.last_operation = Operators.mod

        # We do not have to check for EvaluationResults, those will be
        # handled by __mod__!
        if isinstance(x, (int, float)):
            self.total = float(x) % self.total
        else:
            raise TypeError(
                "The supplied type is not valid: " + str(type(x)))

        return self

    def __pow__(self: EvaluationResults,
                x: Union[int, float, EvaluationResults]) -> EvaluationResults:
        """Exponentiate the evaluation results by the given value."""
        self.last_operation = Operators.expo

        if isinstance(x, (int, float)):
            self.total **= x
        elif isinstance(x, EvaluationResults):
            self._collect_rolls(x)
            self.total **= x.total
        else:
            raise TypeError(
                "The supplied type is not valid: " + str(type(x)))

        return self

    def __ipow__(self: EvaluationResults,
                 x: Union[int, float, EvaluationResults]) -> EvaluationResults:
        """Exponentiate the evaluation results by the given value."""
        return self.__pow__(x)

    def __rpow__(self: EvaluationResults,
                 x: Union[int, float, EvaluationResults]) -> EvaluationResults:
        """Exponentiate the evaluation results by the given value."""
        self.last_operation = Operators.expo

        # We do not have to check for EvaluationResults, those will be
        # handled by __pow__!
        if isinstance(x, (int, float)):
            self.total = x ** self.total
        else:
            raise TypeError("The supplied type is not valid: " + type(x))

        return self
