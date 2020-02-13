
import pytest
from roll import roll


def test_interpret_number():
    assert roll('42') == 42


def test_interpret_number_with_spaces():
    assert roll('       239      ') == 239


def test_interpret_dice():
    assert roll('d20') in range(1, 21)


def test_interpret_dice2():
    assert roll('1d20') in range(1, 21)


def test_bad_input1():
    with pytest.raises(Exception):
        roll('bad input')


def test_bad_input2():
    with pytest.raises(Exception):
        roll('2 + (2 + 3')
