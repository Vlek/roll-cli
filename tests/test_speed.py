"""
Perform speed tests on the project to ensure performant parsing.

One of the main things that I set out to do with this project is
create a performant, feature-rich dice roller. To ensure that I
have reached that goal, we will include several tests to measure
this.

One issue though is that measuring this is not as straight
forward as simply measuring how quickly something is done timewise.
This is due to differing computer speeds. While this may run quickly
on my desktop, it may not run as well on Termux on an older phone.

Further reading:
- https://therenegadecoder.com/code/how-to-performance-test-python-code/
"""

import timeit

import pytest


# The acceptable speed is set to 1/10th of a second.
ACCEPTABLE_SPEED_AVERAGE = 0.1


def test_basic_roll_time() -> None:
    """Test how long it takes on average to do a simple roll."""
    iterations: int = 1000

    result = timeit.timeit(
        "roll()",
        "gc.enable();from src.roll_cli import roll",
        number=iterations
    )
    current_speed: float = result / iterations

    print(f"The current speed is: {current_speed}")
    assert current_speed < ACCEPTABLE_SPEED_AVERAGE


@pytest.mark.skip(
    reason="""This is failing because of recursion depth, not speed.
    This issue likely will be addressed once the recursion check
    issues are addressed.""")
def test_inception_parens() -> None:
    """
    Test where we are performant even with multiple parens.

    This is something that has been a real performance killer
    for us in the past. What happens is it causes repeated,
    recursive parsing of the inner parens which pyparsing does
    not seem to do well?

    e.g. ((((((((((((((((1 + 1))))))))))))))))
    """
    iterations: int = 1000

    result = timeit.timeit(
        "roll('((((((((((((((((1 + 1))))))))))))))))')",
        "gc.enable();from roll import roll",
        number=iterations
    )
    current_speed: float = result / iterations

    print(f"The current speed is: {current_speed}")
    assert current_speed < ACCEPTABLE_SPEED_AVERAGE
