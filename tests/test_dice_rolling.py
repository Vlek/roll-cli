
import pytest
from roll import roll


def test_basic_roll():
    result = roll()
    assert type(result) == int
    assert result in range(1, 21)


@pytest.mark.parametrize('equation,range_low,range_high', [
    ('', 1, 20),
    ('d20', 1, 20),
    ('1d20', 1, 20),
    ('-1d20', -20, 0),
    ('100.0d6', 100, 600),
    ('100d6.0', 100, 600),
    ('2.0d100.0', 2, 200),
    ('100.5d6', 101, 603),
    ('1.0d6.5', 1, 7),
])
def test_roll(equation: str, range_low: int, range_high: int):
    assert roll(equation) in range(range_low, range_high + 1)


def test_zero_dice_roll():
    assert roll('0d20') == 0


def test_zero_sided_dice_roll():
    assert roll('1d0') == 0


def test_1d_neg20():
    with pytest.raises(Exception):
        roll('1d-20')


def test_neg1d_neg20():
    with pytest.raises(Exception):
        roll('-1d-20')


def test_float_roll1():
    assert roll('0.5d20') in range(1, 11)


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


def test_no_sides_given_with_parens():
    with pytest.raises(Exception):
        roll('2d()')


def test_float_num_dice():
    assert roll('0.5d20') in range(1, 11)


def test_float_num_dice2():
    assert roll('0.25d100') in range(1, 26)


def test_float_sides1():
    assert roll('d2.5') in range(1, 4)


def test_float_sides2():
    assert roll('2d19.99') in range(2, 41)
