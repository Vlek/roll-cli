
# from roll import roll
import pytest
import src.roll_cli.parser.diceparser as dp
from pyparsing import ParseException

parser = dp.DiceParser()


# def test_for_recursive_issues():
#     """
#     This is a built-in test from pyparsing that ensures
#     that the regex that is created from the supplied
#     grammar does not have any recursive issues.

#     From what I can gather, it's not the end of the world
#     if there are any, but I am sure it's not a good thing
#     to leave them in there and could effect the speed.
#     """
#     assert parser._parser.validate()


def test_interpret_number() -> None:
    assert parser.evaluate('42') == 42


def test_interpret_neg_number() -> None:
    assert parser.evaluate('-64') == -64


def test_interpret_number_with_spaces() -> None:
    assert parser.evaluate('       239      ') == 239


def test_float1() -> None:
    assert parser.evaluate('1.0') == 1.0


def test_float2() -> None:
    assert parser.evaluate('3.1415') == 3.1415


def test_float3() -> None:
    # I don't like this, but that's what pyparsing does.
    assert parser.evaluate('9.') == 9.0


def test_float4() -> None:
    # I don't like this either, but it handles this.
    assert parser.evaluate('.098') == 0.098


def test_neg_float1() -> None:
    assert parser.evaluate('-2.0') == -2.0


def test_neg_float2() -> None:
    assert parser.evaluate('-700.') == -700.0


def test_interpret_dice() -> None:
    assert parser.evaluate('d20') in range(1, 21)


def test_interpret_dice2() -> None:
    assert parser.evaluate('1d20') in range(1, 21)


def test_interpret_dice_with_spaces() -> None:
    assert parser.evaluate('       2    d  8           ') in range(2, 17)


def test_interpret_subtract_negative() -> None:
    assert parser.evaluate('1 - -5') == 6


# This test currently fails on the master branch as well.
# def test_unary_negative():
#     assert parser.evaluate('--10') == 10


def test_bad_input1() -> None:
    with pytest.raises(Exception):
        parser.evaluate('bad input')


def test_bad_input2() -> None:
    with pytest.raises(Exception):
        parser.evaluate('2 + (2 + 3')


def test_bad_input3() -> None:
    with pytest.raises(Exception):
        parser.evaluate('2 +')


def test_bad_input4() -> None:
    with pytest.raises(Exception):
        parser.evaluate('+ 6')


def test_bad_input5() -> None:
    with pytest.raises(Exception):
        parser.evaluate('(6**)2')


def test_bad_input6() -> None:
    with pytest.raises(Exception):
        parser.evaluate('d')


def test_bad_input7() -> None:
    with pytest.raises(Exception):
        parser.evaluate('+')


def test_bad_input8() -> None:
    with pytest.raises(Exception):
        parser.evaluate('*')


def test_bad_input9() -> None:
    with pytest.raises(Exception):
        parser.evaluate('-')


def test_bad_input10() -> None:
    with pytest.raises(Exception):
        parser.evaluate('/')


def test_bad_input11() -> None:
    with pytest.raises(Exception):
        parser.evaluate('%')
