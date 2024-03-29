"""Test the inner workings of the DiceParser object.

In order to perform comprehensive testing, we are testing
both the underlying class methods as well as the CLIs
functionality.

The reason specifically why I am doing this now is because
of the code coverage not being up to admissible levels.
This is due to the fact that our code is overly defensive,
likely taking care of edgecases that may not be possible
due to how the parser works. Still, the type checking is
flagging these as issues when there are not exception
cases being raised if the types do not match what we are
expecting.
"""
import pytest

from roll_cli.parser import DiceParser


def test_handle_keep() -> None:
    """Test whether we properly throw erros for no rolls."""
    dp = DiceParser()

    with pytest.raises(TypeError, match="Left value must contain a dice roll."):
        dp._handle_keep([["hello", "k", 1]])


def test_handle_sqrt() -> None:
    """Test whether we properly throw errors for string values."""
    dp = DiceParser()

    with pytest.raises(
        TypeError, match="The given value must be int, float, or EvaluationResults"
    ):
        dp._handle_sqrt([["sqrt", "banana"]])


@pytest.mark.skip(
    reason="""This currently fails and the fix is part of another
    github issue (#45)"""
)
def test_pyparsing_recursion_issues() -> None:
    """Test to ensure no recursive issues exist in parser.

    This is a built-in test from pyparsing that ensures
    that the regex that is created from the supplied
    grammar does not have any recursive issues.

    From what I can gather, it's not the end of the world
    if there are any, but I am sure it's not a good thing
    to leave them in there and could effect the speed.

    With the latest update, it now throws an error instead
    of giving a boolean.
    """
    dp = DiceParser()
    dp._parser.validate()
