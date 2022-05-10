"""Defines EvaluationResults object to hold parsing state throughout evaluation.

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
from math import ceil
from math import factorial
from math import sqrt

from .rollresults import RollResults


class Operators(Enum):
    """Helper operator names for handling operations.

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


class EvaluationResults:
    """Hold the current state of all rolls and the total from other ops."""

    def __init__(
        self: EvaluationResults,
        value: int | float | EvaluationResults = 0,
        rolls: list[RollResults] | None = None,
    ) -> None:
        """Initialize an EvaluationResults object."""
        if rolls is None:
            rolls = []

        total: int | float | None = None
        history: list[str] = []

        if isinstance(value, EvaluationResults):
            rolls.extend(value.rolls)
            history = value.history
            total = value.total
        else:
            total = value

        self.total: int | float = total
        self.rolls: list[RollResults] = rolls
        self.history: list[str] = history

    def add_roll(self: EvaluationResults, roll: RollResults) -> None:
        """Add the results of a roll to the total evaluation results."""
        self.total += roll.total()
        self.rolls.append(roll)
        self.history.append(f"Rolled: {roll.dice}: {roll.rolls}")

    def sqrt(self: EvaluationResults) -> None:
        """Take the square root of the total value."""
        new_total = sqrt(self.total)
        self.history.append(f"Square Root: {self.total}: {new_total}")

        self.total = new_total

    def factorial(self: EvaluationResults) -> None:
        """Factorial the total value."""
        new_total = factorial(ceil(self.total))
        self.history.append(f"Factorial: {self.total}! = {new_total}")

        self.total = new_total

    def _process_right_hand_value(
        self: EvaluationResults, x: EvaluationResults | int | float
    ) -> int | float:
        """Allows two ER objects to have their dice and history combined.

        This is important so that the history and rolls are preserved
        otherwise we lose key pieces of information that would disallow us
        from being able to make modifications to rolls, i.e., keep notation,
        as well as being able to give a complete verbose output when finished.
        """
        right_hand_value: int | float | EvaluationResults

        if isinstance(x, (int, float)):
            right_hand_value = x
        elif isinstance(x, EvaluationResults):
            self._collect_rolls(x)
            self.history.extend(x.history)
            right_hand_value = x.total
        else:
            raise TypeError("The supplied type is not valid: " + type(x).__name__)

        return right_hand_value

    def _collect_rolls(self: EvaluationResults, er: EvaluationResults) -> None:
        """Add all rolls together if both objects are EvaluationResults.

        The way that we do this is by extending the other object's rolls
        in place for efficiency's sake and then we set our object to that
        one instead of the other way around so that we hopefully are going
        to have the most recently roll as our last.
        """
        er.rolls.extend(self.rolls)
        self.rolls = er.rolls

    def __str__(self: EvaluationResults) -> str:
        """Return a string representation of the eval results.

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
        history_string: str = "\n".join([h for h in self.history]) + "\n"

        total_string: str = f"{self.total}"

        if isinstance(self.total, float) and self.total % 1 == 0:
            total_string = f"{int(self.total)}"

        return f"{history_string}{total_string}"

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

    def __add__(
        self: EvaluationResults, x: int | float | EvaluationResults
    ) -> EvaluationResults:
        """Add a given value to the evaluation result total."""
        right_hand_value: int | float = self._process_right_hand_value(x)
        previous_total = self.total

        self.total += right_hand_value
        self.history.append(
            f"Adding: {previous_total} + {right_hand_value} = {self.total}"
        )

        return self

    def __iadd__(
        self: EvaluationResults, x: int | float | EvaluationResults
    ) -> EvaluationResults:
        """Add a given value to the evaluation result total."""
        return self.__add__(x)

    def __radd__(
        self: EvaluationResults, x: int | float | EvaluationResults
    ) -> EvaluationResults:
        """Add a given value to the evaluation result total."""
        return self.__add__(x)

    def __sub__(
        self: EvaluationResults, x: int | float | EvaluationResults
    ) -> EvaluationResults:
        """Subtract a given value from the evaluation result total."""
        right_hand_value: int | float = self._process_right_hand_value(x)
        previous_total = self.total

        self.total -= right_hand_value
        self.history.append(
            f"Subtracting: {previous_total} - {right_hand_value} = {self.total}"
        )

        return self

    def __isub__(
        self: EvaluationResults, x: int | float | EvaluationResults
    ) -> EvaluationResults:
        """Subtract a given value from the evaluation result total."""
        return self.__sub__(x)

    def __rsub__(self: EvaluationResults, x: int | float) -> EvaluationResults:
        """Subtract a given value from the evaluation result total."""
        right_hand_value: int | float = self._process_right_hand_value(x)
        previous_total = self.total

        self.total = right_hand_value - self.total
        self.history.append(
            f"Adding: {right_hand_value} - {previous_total} = {self.total}"
        )

        return self

    def __mul__(
        self: EvaluationResults, x: int | float | EvaluationResults
    ) -> EvaluationResults:
        """Multiply the evaluation result total by a given value."""
        right_hand_value: int | float = self._process_right_hand_value(x)
        previous_total = self.total

        self.total *= right_hand_value
        self.history.append(
            f"Multiplying: {previous_total} * {right_hand_value} = {self.total}"
        )

        return self

    def __imul__(
        self: EvaluationResults, x: int | float | EvaluationResults
    ) -> EvaluationResults:
        """Multiply the evaluation result total by a given value."""
        return self.__mul__(x)

    def __rmul__(
        self: EvaluationResults, x: int | float | EvaluationResults
    ) -> EvaluationResults:
        """Multiply the evaluation result total by a given value."""
        return self.__mul__(x)

    def __truediv__(
        self: EvaluationResults, x: int | float | EvaluationResults
    ) -> EvaluationResults:
        """Divide the evaluation result total by a given number."""
        right_hand_value: int | float = self._process_right_hand_value(x)
        previous_total = self.total

        self.total /= right_hand_value
        self.history.append(
            f"Dividing: {previous_total} / {right_hand_value} = {self.total}"
        )

        return self

    def __itruediv__(
        self: EvaluationResults, x: int | float | EvaluationResults
    ) -> EvaluationResults:
        """Divide the evaluation result total by a given number."""
        return self.__truediv__(x)

    def __rtruediv__(
        self: EvaluationResults, x: int | float | EvaluationResults
    ) -> EvaluationResults:
        """Divide the evaluation result total by a given number."""
        right_hand_value: int | float = self._process_right_hand_value(x)
        previous_total = self.total

        self.total = right_hand_value / self.total
        self.history.append(
            f"Dividing: {right_hand_value} / {previous_total} = {self.total}"
        )

        return self

    def __floordiv__(
        self: EvaluationResults, x: int | float | EvaluationResults
    ) -> EvaluationResults:
        """Divide the evaluation result total by a given number and floor."""
        right_hand_value: int | float = self._process_right_hand_value(x)
        previous_total = self.total

        self.total //= right_hand_value
        self.history.append(
            f"Floor dividing: {previous_total} // {right_hand_value} = {self.total}"
        )

        return self

    def __ifloordiv__(
        self: EvaluationResults, x: int | float | EvaluationResults
    ) -> EvaluationResults:
        """Divide the evaluation result total by a given number and floor."""
        return self.__floordiv__(x)

    def __rfloordiv__(
        self: EvaluationResults, x: int | float | EvaluationResults
    ) -> EvaluationResults:
        """Divide the evaluation result total by a given number and floor."""
        right_hand_value: int | float = self._process_right_hand_value(x)
        previous_total = self.total

        self.total = right_hand_value // self.total
        self.history.append(
            f"Floor dividing: {right_hand_value} // {previous_total} = {self.total}"
        )

        return self

    def __mod__(
        self: EvaluationResults, x: int | float | EvaluationResults
    ) -> EvaluationResults:
        """Perform modulus divison on the evaluation total with given value."""
        right_hand_value: int | float = self._process_right_hand_value(x)
        previous_total = self.total

        self.total %= right_hand_value
        self.history.append(
            f"Modulus dividing: {previous_total} % {right_hand_value} = {self.total}"
        )

        return self

    def __imod__(
        self: EvaluationResults, x: int | float | EvaluationResults
    ) -> EvaluationResults:
        """Perform modulus divison on the evaluation total with given value."""
        return self.__mod__(x)

    def __rmod__(
        self: EvaluationResults, x: int | float | EvaluationResults
    ) -> EvaluationResults:
        """Perform modulus divison on the evaluation total with given value."""
        right_hand_value: int | float = self._process_right_hand_value(x)
        previous_total = self.total

        self.total = right_hand_value % self.total
        self.history.append(
            f"Modulus dividing: {right_hand_value} % {previous_total} = {self.total}"
        )

        return self

    def __pow__(
        self: EvaluationResults, x: int | float | EvaluationResults
    ) -> EvaluationResults:
        """Exponentiate the evaluation results by the given value."""
        right_hand_value: int | float = self._process_right_hand_value(x)
        previous_total = self.total

        self.total **= right_hand_value
        self.history.append(
            f"Exponentiating: {previous_total} ** {right_hand_value} = {self.total}"
        )

        return self

    def __ipow__(
        self: EvaluationResults, x: int | float | EvaluationResults
    ) -> EvaluationResults:
        """Exponentiate the evaluation results by the given value."""
        return self.__pow__(x)

    def __rpow__(
        self: EvaluationResults, x: int | float | EvaluationResults
    ) -> EvaluationResults:
        """Exponentiate the evaluation results by the given value."""
        right_hand_value: int | float = self._process_right_hand_value(x)
        previous_total = self.total

        self.total = right_hand_value**self.total
        self.history.append(
            f"Exponentiating: {right_hand_value} ** {previous_total} = {self.total}"
        )

        return self

    def __lt__(
        self: EvaluationResults, x: int | float | EvaluationResults
    ) -> EvaluationResults:
        """Add a given value to the evaluation result total."""
        right_hand_value: int | float = self._process_right_hand_value(x)
        previous_total = self.total
        new_total: int | float | EvaluationResults = (
            1 if self.total < right_hand_value else 0
        )

        self.history.append(
            f"Comparing: {previous_total} < {right_hand_value}: {new_total}"
        )
        self.total = new_total

        return self

    def __gt__(
        self: EvaluationResults, x: int | float | EvaluationResults
    ) -> EvaluationResults:
        """Add a given value to the evaluation result total."""
        right_hand_value: int | float = self._process_right_hand_value(x)
        previous_total = self.total
        new_total: int | float | EvaluationResults = (
            1 if self.total > right_hand_value else 0
        )

        self.history.append(
            f"Comparing: {previous_total} > {right_hand_value}: {new_total}"
        )
        self.total = new_total

        return self

    def __le__(
        self: EvaluationResults, x: int | float | EvaluationResults
    ) -> EvaluationResults:
        """Add a given value to the evaluation result total."""
        right_hand_value: int | float = self._process_right_hand_value(x)
        previous_total = self.total
        new_total: int | float | EvaluationResults = (
            1 if self.total <= right_hand_value else 0
        )

        self.history.append(
            f"Comparing: {previous_total} <= {right_hand_value}: {new_total}"
        )
        self.total = new_total

        return self

    def __ge__(
        self: EvaluationResults, x: int | float | EvaluationResults
    ) -> EvaluationResults:
        """Add a given value to the evaluation result total."""
        right_hand_value: int | float = self._process_right_hand_value(x)
        previous_total = self.total
        new_total: int | float | EvaluationResults = (
            1 if self.total >= right_hand_value else 0
        )

        self.history.append(
            f"Comparing: {previous_total} >= {right_hand_value}: {new_total}"
        )
        self.total = new_total

        return self
