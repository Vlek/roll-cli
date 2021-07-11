from roll.parser.types import EvaluationResults


def test_add() -> None:
    er = EvaluationResults()
    er = er + 2
    assert er == 2


def test_unary_minus() -> None:
    er = EvaluationResults()
    er += 5
    er = -er
    assert er == -5


def test_add_reversed() -> None:
    er = EvaluationResults()
    er = 2 + er
    assert er == 2


def test_sub() -> None:
    er = EvaluationResults()
    er = er - 2
    assert er == -2


def test_sub_reversed() -> None:
    er = EvaluationResults()
    er = 2 - er
    assert er == 2


def test_mul() -> None:
    er = EvaluationResults()
    er += 5
    er *= 2
    er = 7 * er
    assert er == 70


def test_mul_reversed() -> None:
    er = EvaluationResults()
    er += 5
    er = 7 * er
    assert er == 35


def test_truediv() -> None:
    er = EvaluationResults()
    er += 60
    er /= 10
    assert er == 6


def test_truediv_reversed() -> None:
    er = EvaluationResults()
    er += 8
    er = 24 / er
    assert er == 3


def test_floordiv() -> None:
    er = EvaluationResults()
    er += 120
    er //= 10
    assert er == 12


def test_floordiv_reversed() -> None:
    er = EvaluationResults()
    er += 14
    er = 112 // er
    assert er == 8


def test_modulus() -> None:
    er = EvaluationResults()
    er += 240
    er %= 9
    assert er == 6


def test_modulus_reversed() -> None:
    er = EvaluationResults()
    er += 7
    er = 6 % er
    assert er == 6


def test_exponential() -> None:
    er = EvaluationResults()
    er += 2
    er **= 5
    assert er == 32


def test_exponential_reversed() -> None:
    er = EvaluationResults()
    er += 8
    er = 7 ** er
    assert er == 5764801
