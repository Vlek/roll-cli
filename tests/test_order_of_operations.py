
from roll import roll


def test_inception_dice():
    assert roll('1d7d4d6') in range(7, 169)


def test_inception_dice_with_parens():
    assert roll('(1d4)d6') in range(1, 25)
