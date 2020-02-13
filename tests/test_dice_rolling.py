
import pytest
from roll import roll


def test_basic_roll():
    assert roll() in range(1, 21)


def test_zero_dice_roll():
    assert roll('0d20') == 0


def test_zero_sided_dice_roll():
    assert roll('1d0') == 0


def test_d20():
    assert roll('d20') in range(1, 21)


def test_1d20():
    assert roll('1d20') in range(1, 21)


def test_neg1d20():
    assert roll('-1d20') in range(-20, 0)


def test_1d_neg20():
    with pytest.raises(Exception):
        roll('1d-20')


def test_neg1d_neg20():
    with pytest.raises(Exception):
        roll('-1d-20')


def test_3d6():
    assert roll('3d6') in range(3, 19)


def test_100d1():
    assert roll('100d1') == 100


def test_d100():
    assert roll('d100') in range(1, 101)


def test_d_percentage():
    assert roll('d%') in range(1, 101)


def test_no_sides_given():
    with pytest.raises(Exception):
        roll('1d')
