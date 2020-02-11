
from roll import roll


def test_interpret_number():
    assert roll('42') == 42


def test_addition1():
    assert roll('2 + 2') == 4


def test_addition2():
    assert roll('10 + 52') == 62


def test_addition3():
    assert roll('1 + 10 + 100 + 1000') == 1111


def test_subtraction1():
    assert roll('10 - 5') == 5


def test_subtraction2():
    assert roll('100 - 52') == 48


def test_subtraction3():
    assert roll('1111 - 100 - 10 - 1') == 1000


def test_subtraction4():
    assert roll('73 - 100') == -27


def test_multiplication1():
    assert roll('2 * 2') == 4


def test_multiplication2():
    assert roll('20 * 5') == 100


def test_multiplication3():
    assert roll('1 * 10 * 100') == 1000


def test_multiplication4():
    assert roll('6 * 8 * 2 * 10') == 960


def test_division1():
    assert roll('5 / 5') == 1


def test_division2():
    assert roll('15 / 3') == 5


def test_division3():
    assert roll('48 / 6') == 8


def test_division4():
    assert roll('54 / 9') == 6
