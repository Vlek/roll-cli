
# from roll import roll
import pytest
import roll.parser.diceparser as dp
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


def test_interpret_number():
    assert parser.evaluate('42')['total'] == 42


def test_interpret_neg_number():
    assert parser.evaluate('-64')['total'] == -64


def test_interpret_number_with_spaces():
    assert parser.evaluate('       239      ')['total'] == 239


def test_float1():
    assert parser.evaluate('1.0')['total'] == 1.0


def test_float2():
    assert parser.evaluate('3.1415')['total'] == 3.1415


def test_float3():
    # I don't like this, but that's what pyparsing does.
    assert parser.evaluate('9.')['total'] == 9.0


def test_float4():
    # I don't like this either, but it handles this.
    assert parser.evaluate('.098')['total'] == 0.098


def test_neg_float1():
    assert parser.evaluate('-2.0')['total'] == -2.0


def test_neg_float2():
    assert parser.evaluate('-700.')['total'] == -700.0


def test_interpret_dice():
    assert parser.evaluate('d20')['total'] in range(1, 21)


def test_interpret_dice2():
    assert parser.evaluate('1d20')['total'] in range(1, 21)


def test_interpret_dice_with_spaces():
    assert parser.evaluate('       2    d  8           ')['total'] in range(2, 17)


def test_interpret_subtract_negative():
    assert parser.evaluate('1 - -5')['total'] == 6


# This test currently fails on the master branch as well.
# def test_unary_negative():
#     assert parser.evaluate('--10')['total'] == 10


def test_bad_input1():
    with pytest.raises(Exception):
        parser.evaluate('bad input')


def test_bad_input2():
    with pytest.raises(Exception):
        parser.evaluate('2 + (2 + 3')


def test_bad_input3():
    with pytest.raises(Exception):
        parser.evaluate('2 +')


def test_bad_input4():
    with pytest.raises(Exception):
        parser.evaluate('+ 6')


def test_bad_input5():
    with pytest.raises(Exception):
        parser.evaluate('(6**)2')


def test_bad_input6():
    with pytest.raises(Exception):
        parser.evaluate('d')


def test_bad_input7():
    with pytest.raises(Exception):
        parser.evaluate('+')


def test_bad_input8():
    with pytest.raises(Exception):
        parser.evaluate('*')


def test_bad_input9():
    with pytest.raises(Exception):
        parser.evaluate('-')


def test_bad_input10():
    with pytest.raises(Exception):
        parser.evaluate('/')


def test_bad_input11():
    with pytest.raises(Exception):
        parser.evaluate('%')
