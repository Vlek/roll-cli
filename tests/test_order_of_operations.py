
from roll import roll


def mul_b4_add1():
    assert roll('2+6*4') == 26


def mul_b4_add2():
    assert roll('5+4*2+9') == 22


def mul_b4_add3():
    assert roll('1+2*3+4*5+6') == 33


def mul_b4_add4():
    assert roll('7 * 4+ 2 + 8') == 38


def mul_b4_add5():
    assert roll('9 + 4 + 42 + 7 * 4') == 83


def div_b4_sub1():
    assert roll('100 - 21 / 7') == 97


def test_inception_dice1():
    assert roll('1d7d4d6') in range(1, 169)


def test_inception_dice2():
    assert roll('7d4d20') in range(7, 561)


def test_inception_dice3():
    assert roll('10d2d4') in range(10, 81)


def test_inception_dice4():
    assert roll('2d4d6d8') in range(2, 385)


def test_inception_dice_with_parens1():
    assert roll('(1d4)d6') in range(1, 25)


def test_inception_dice_with_parens2():
    assert roll('1d(1d20)') in range(1, 21)


def test_inception_dice_with_parens3():
    assert roll('4d(10d7d8)') in range(10, 2241)

