
from roll import roll


def test_basic_roll():
    assert roll() in range(1, 20)


def test_d20():
    assert roll('d20') in range(1, 20)


def test_1d20():
    assert roll('1d20') in range(1, 20)


def test_3d6():
    assert roll('3d6') in range(3, 18)


def test_d100():
    assert roll('d100') in range(1, 100)


def test_d_percentage():
    assert roll('d%') in range(1, 100)
