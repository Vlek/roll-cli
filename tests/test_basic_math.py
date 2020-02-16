
import pytest
from roll import roll


def test_addition1():
    assert roll('2 + 2') == 4


def test_addition2():
    assert roll('10 + 52') == 62


def test_addition3():
    assert roll('1 + 10 + 100 + 1000') == 1111


def test_addition_without_spaces1():
    assert roll('8+16') == 24


def test_addition_without_spaces2():
    assert roll('5+17+202+81') == 305


def test_addition_with_uneven_spaces1():
    assert roll('19     +    57') == 76


def test_addition_with_uneven_spaces2():
    with pytest.raises(Exception):
        roll('321\t\n  + \t\t\t   \t 18')


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


def test_add_mul():
    assert roll('1 + 2 * 3') == 7


def test_mul_add():
    assert roll('3 * 2 + 1') == 7


def test_sub_div():
    assert roll('10 - 5 / 5') == 9


def test_div_sub():
    assert roll('15 / 3 - 2') == 3


def test_sub_mul_add_mul_sub():
    assert roll('40 - 3 * 7 + 2 * 9 - 20') == 17


def test_parens1():
    assert roll('(4 + 2) * 3') == 18


def test_parens2():
    assert roll('3 * (10 - 5)') == 15


def test_modulus1():
    assert roll('5 % 2') == 1


def test_modulus2():
    assert roll('23 % 13') == 10


def test_modulus3():
    assert roll('19 % 12') == 7


def test_modulus4():
    assert roll('1 % 112') == 1


def test_modulus5():
    assert roll('66 % 11') == 0


def test_exponential1():
    assert roll('6 ** 3') == 216


def test_exponential2():
    assert roll('7 ** 5') == 16807
