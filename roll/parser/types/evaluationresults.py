from __future__ import annotations

from enum import Enum
from typing import List, Union

from .rollresults import RollResults


class Operators(Enum):
    add = "+"
    sub = "-"
    mul = "*"
    truediv = "/"
    floordiv = "//"
    mod = "%"
    expo = "^"
    die = "d"


class EvaluationResults():
    """Hold the current state of all rolls and the total from other ops."""

    def __init__(self, total: Union[int, float] = 0,
                 rolls: List[RollResults] = [],
                 last_operation: Operators = None):
        self.total: Union[int, float] = total
        self.rolls: List[RollResults] = rolls
        self.last_operation: Union[Operators, None] = last_operation

    def add_roll(self, roll: RollResults) -> None:
        self.total += roll['total']
        self.rolls.append(roll)

    def _collect_rolls(self, er: EvaluationResults) -> None:
        '''
        Adds all rolls together if both objects are EvaluationResults.

        The way that we do this is by extending the other object's rolls
        in place for efficiency's sake and then we set our object to that
        one instead of the other way around so that we hopefully are going
        to have the most recently roll as our last.
        '''
        er.rolls.extend(self.rolls)
        self.rolls = er.rolls

    def __int__(self) -> int:
        return int(self.total)

    def __float__(self) -> float:
        return float(self.total)

    def __len__(self) -> int:
        return len(self.rolls)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, (int, float, EvaluationResults)):
            return NotImplemented

        if isinstance(other, (int, float)):
            return other == self.total

        return self.total == other.total

    def __neg__(self):
        self.total = -self.total
        return self

    def __add__(self,
                x: Union[int, float, EvaluationResults]) -> EvaluationResults:
        self.last_operation = Operators.add

        if isinstance(x, (int, float)):
            self.total += x
        elif isinstance(x, EvaluationResults):
            self._collect_rolls(x)
            self.total += x.total
        else:
            raise TypeError("The supplied type is not valid: " + type(x))

        return self

    def __iadd__(self,
                 x: Union[int, float, EvaluationResults]) -> EvaluationResults:
        return self.__add__(x)

    def __radd__(self,
                 x: Union[int, float, EvaluationResults]) -> EvaluationResults:
        return self.__add__(x)

    def __sub__(self,
                x: Union[int, float, EvaluationResults]) -> EvaluationResults:
        self.last_operation = Operators.sub

        if isinstance(x, (int, float)):
            self.total -= x
        elif isinstance(x, EvaluationResults):
            self._collect_rolls(x)
            self.total -= x.total
        else:
            raise TypeError("The supplied type is not valid: " + type(x))

        return self

    def __isub__(self,
                 x: Union[int, float, EvaluationResults]) -> EvaluationResults:
        return self.__sub__(x)

    def __rsub__(self, x: Union[int, float]) -> EvaluationResults:
        self.last_operation = Operators.sub

        if isinstance(x, (int, float)):
            self.total = x - self.total
        elif isinstance(x, EvaluationResults):
            self._collect_rolls(x)
            self.total = x.total - self.total
        else:
            raise TypeError("The supplied type is not valid: " + type(x))

        return self

    def __mul__(self,
                x: Union[int, float, EvaluationResults]) -> EvaluationResults:
        self.last_operation = Operators.mul

        if isinstance(x, (int, float)):
            self.total *= x
        elif isinstance(x, EvaluationResults):
            self._collect_rolls(x)
            self.total *= x.total
        else:
            raise TypeError("The supplied type is not valid: " + type(x))

        return self

    def __imul__(self,
                 x: Union[int, float, EvaluationResults]) -> EvaluationResults:
        return self.__mul__(x)

    def __rmul__(self,
                 x: Union[int, float, EvaluationResults]) -> EvaluationResults:
        return self.__mul__(x)

    def __truediv__(self,
                    x: Union[int, float, EvaluationResults]
                    ) -> EvaluationResults:
        self.last_operation = Operators.truediv

        if isinstance(x, (int, float)):
            self.total /= x
        elif isinstance(x, EvaluationResults):
            self._collect_rolls(x)
            self.total /= x.total
        else:
            raise TypeError("The supplied type is not valid: " + type(x))

        return self

    def __itruediv__(self,
                     x: Union[int, float, EvaluationResults]
                     ) -> EvaluationResults:
        return self.__truediv__(x)

    def __rtruediv__(self,
                     x: Union[int, float, EvaluationResults]
                     ) -> EvaluationResults:
        self.last_operation = Operators.truediv

        if isinstance(x, (int, float)):
            self.total = x / self.total
        elif isinstance(x, EvaluationResults):
            self._collect_rolls(x)
            self.total = x.total / self.total
        else:
            raise TypeError("The supplied type is not valid: " + type(x))

        return self

    def __floordiv__(self,
                     x: Union[int, float, EvaluationResults]
                     ) -> EvaluationResults:
        self.last_operation = Operators.floordiv

        if isinstance(x, (int, float)):
            self.total //= x
        elif isinstance(x, EvaluationResults):
            self._collect_rolls(x)
            self.total //= x.total
        else:
            raise TypeError("The supplied type is not valid: " + type(x))

        return self

    def __ifloordiv__(self,
                      x: Union[int, float, EvaluationResults]
                      ) -> EvaluationResults:
        return self.__floordiv__(x)

    def __rfloordiv__(self,
                      x: Union[int, float, EvaluationResults]
                      ) -> EvaluationResults:
        self.last_operation = Operators.floordiv

        if isinstance(x, (int, float)):
            self.total = x // self.total
        elif isinstance(x, EvaluationResults):
            self._collect_rolls(x)
            self.total = x.total // self.total
        else:
            raise TypeError("The supplied type is not valid: " + type(x))

        return self

    def __mod__(self,
                x: Union[int, float, EvaluationResults]) -> EvaluationResults:
        self.last_operation = Operators.mod

        if isinstance(x, (int, float)):
            self.total %= x
        elif isinstance(x, EvaluationResults):
            self._collect_rolls(x)
            self.total %= x.total
        else:
            raise TypeError("The supplied type is not valid: " + type(x))

        return self

    def __imod__(self,
                 x: Union[int, float, EvaluationResults]) -> EvaluationResults:
        return self.__mod__(x)

    def __rmod__(self,
                 x: Union[int, float, EvaluationResults]) -> EvaluationResults:
        self.last_operation = Operators.mod

        if isinstance(x, (int, float)):
            self.total = x % self.total
        elif isinstance(x, EvaluationResults):
            self._collect_rolls(x)
            self.total = x.total % self.total
        else:
            raise TypeError("The supplied type is not valid: " + type(x))

        return self

    def __pow__(self,
                x: Union[int, float, EvaluationResults]) -> EvaluationResults:
        self.last_operation = Operators.expo

        if isinstance(x, (int, float)):
            self.total **= x
        elif isinstance(x, EvaluationResults):
            self._collect_rolls(x)
            self.total **= x.total
        else:
            raise TypeError("The supplied type is not valid: " + type(x))

        return self

    def __ipow__(self,
                 x: Union[int, float, EvaluationResults]) -> EvaluationResults:
        return self.__pow__(x)

    def __rpow__(self,
                 x: Union[int, float, EvaluationResults]) -> EvaluationResults:
        self.last_operation = Operators.expo

        if isinstance(x, (int, float)):
            self.total = x ** self.total
        elif isinstance(x, EvaluationResults):
            self._collect_rolls(x)
            self.total = x.total ** self.total
        else:
            raise TypeError("The supplied type is not valid: " + type(x))

        return self
