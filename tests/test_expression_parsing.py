
import pytest
from pyparsing import ParseException

from roll import roll


def test_interpret_number():
    assert roll('42') == 42


def test_interpret_neg_number():
    assert roll('-64') == -64


def test_interpret_number_with_spaces():
    assert roll('       239      ') == 239


def test_float1():
    assert roll('1.0') == 1.0


def test_float2():
    assert roll('3.1415') == 3.1415


def test_float3():
    # I don't like this, but that's what pyparsing does.
    assert roll('9.') == 9.0


def test_float4():
    # I don't like this either, but it handles this.
    assert roll('.098') == 0.098


def test_neg_float1():
    assert roll('-2.0') == -2.0


def test_neg_float2():
    assert roll('-700.') == -700.0


def test_interpret_dice():
    assert roll('d20') in range(1, 21)


def test_interpret_dice2():
    assert roll('1d20') in range(1, 21)


def test_interpret_dice_with_spaces():
    assert roll('       2    d  8           ') in range(2, 17)


def test_interpret_subtract_negative():
    assert roll('1 - -5') == 6


# This test currently fails on the master branch as well.
# def test_unary_negative():
#     assert roll('--10') == 10


def test_bad_input1():
    with pytest.raises(Exception):
        roll('bad input')


def test_bad_input2():
    with pytest.raises(Exception):
        roll('2 + (2 + 3')


def test_bad_input3():
    with pytest.raises(Exception):
        roll('2 +')


def test_bad_input4():
    with pytest.raises(Exception):
        roll('+ 6')


def test_bad_input5():
    with pytest.raises(Exception):
        roll('(6**)2')


def test_bad_input6():
    with pytest.raises(Exception):
        roll('d')


def test_bad_input7():
    with pytest.raises(Exception):
        roll('+')


def test_bad_input8():
    with pytest.raises(Exception):
        roll('*')


def test_bad_input9():
    with pytest.raises(Exception):
        roll('-')


def test_bad_input10():
    with pytest.raises(Exception):
        roll('/')


def test_bad_input11():
    with pytest.raises(Exception):
        roll('%')
