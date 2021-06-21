from sys import version_info
from typing import List, Union

# TypedDict was added in 3.8.
if version_info >= (3, 8):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict


class RollResults(TypedDict):
    total: Union[int, float]
    dice: str
    rolls: List[Union[int, float]]
