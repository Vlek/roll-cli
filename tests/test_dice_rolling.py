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
    ('2.5d300', 3, 750),
    ('0.25d100', 1, 25),
    ('0.01d1000', 1, 10),
    ('100.5d6', 101, 603),
    ('1.0d6.5', 1, 7),
    ('1d0', 0, 0),
    ('1d1', 1, 1),
    ('1d2', 1, 2),
])
def test_roll(equation: str, range_low: int, range_high: int):
    assert roll(equation) in range(range_low, range_high + 1)


@pytest.mark.parametrize(('equation', 'range_low', 'range_high'), [
    ('0.5d100', 1, 50),
    ('0.1d10', 1, 1),
    ('0.9d100', 1, 90),
])
def test_float_roll(equation: str, range_low: int, range_high: int) -> None:
    """
    Test the case where we give a non-int value for num dice.

    The logic that we have chosen for this is that any floating point
    value that contains a decimal value means that another dice should
    be rolled but we should only allow for a portion of the amount for
    the sides to be returned.

    e.g. 0.5d100 == 1d50
    """
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


@pytest.mark.parametrize(('equation', 'range_low', 'range_high'), [
    ('2d6d100', 2, 1200),
    ('1d2d3d4', 1, 24),
])
def test_inception_dice(equation: str, range_low: int,
                        range_high: int) -> None:
    """
    Test cases like '1d2d3d4' to ensure proper evaluation.

    The worry here is that the parser may only interpret the
    left-most dice roll without continuing to parse the right
    ones. It may also not parse them in order from
    left-to-right
    """
    assert roll(equation) in range(range_low, range_high + 1)


@pytest.mark.parametrize(('equation', 'range_low', 'range_high'), [
    # Implied number of dice, implied number to keep
    ('d6K', 1, 6),
    ('d10k', 1, 10),
    ('d%k', 1, 100),

    # Verbose dice, implied number to keep
    ('10d6K', 1, 6),
    ('10d9k', 1, 9),

    # Implied number of dice, verbose number to keep
    ('d100K1', 1, 100),
    ('d1k5', 1, 1),

    # Verbose dice, verbose keep
    ('10d6k1', 1, 6),
    ('4d6K3', 3, 18),

    # Multiple keeps
    ('10d5k4k3k2k1', 1, 5),
    ('10d6K5k4', 4, 24),

    # Multiple dice rolls
    ('4d6K1d2', 2, 12),

    # With parens
    ('(4+1)d100k5', 5, 500),
    ('(4d100k2)K1', 1, 100),
    ('(4)d(3)k((2))', 2, 6),
])
def test_keep(equation: str, range_low: int, range_high: int) -> None:
    assert roll(equation) in range(range_low, range_high + 1)


@pytest.mark.parametrize(('equation', 'exception_msg'), [
    # No dice given
    # 'Left value must contain a dice roll.'
    ('((1+2))k', 'Unable to parse input string'),
    ('sqrt10k', 'Unable to parse input string'),
])
def test_keep_exceptions(equation: str, exception_msg: str) -> None:
    """Test the exception paths for the keep notation."""
    with pytest.raises(Exception, match=exception_msg):
        roll(equation)
