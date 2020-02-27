
from roll import roll


def test_d6_plus_d8():
    assert roll('d6 + d8') in range(1, 14)


def test_1d8_plus_3d6():
    assert roll('1d8 + 3d6') in range(4, 26)


def test_mul_1d4():
    assert roll('4 * 1d4') in range(4, 17)


def test_1d4_add_div():
    assert roll('1d4 + 16 / 4') in range(5, 9)


def test_2d8_parens_add_mult():
    assert roll('(2d8 + 8) * 4') in range(40, 97)


def test_d6_mul_4():
    assert roll('d6 * 4') in range(4, 25)


def test_dice_expo():
    assert roll('5**2d1') == 25


def test_dice_expo1():
    assert roll('5d1**5') == 5
