
from roll import roll


def test_d6_plus_d8():
    assert roll('d6 + d8') in range(1, 14)


def test_1d8_plus_3d6():
    assert roll('1d8 + 3d6') in range(4, 26)
