import pytest
from roll.parser.types import EvaluationResults, RollResults


def test_eq() -> None:
    er = EvaluationResults(200)
    assert er == 200


def test_to_float() -> None:
    er = EvaluationResults(1000)
    assert isinstance(float(er), float)


def test_rtruediv() -> None:
    er = EvaluationResults(2)
    assert 10 / er == 5


def test_rtruediv_bad_type() -> None:
    er = EvaluationResults()
    with pytest.raises(
        TypeError,
        match="The supplied type is not valid: str"
    ):
        'banana' / er


def test_floordiv_er() -> None:
    er = EvaluationResults(6)
    second_er = EvaluationResults(13)

    assert second_er // er == 2


def test_floordiv_bad_type() -> None:
    er = EvaluationResults(100)
    with pytest.raises(
        TypeError,
        match="can only concatenate str"
    ):
        er // 'banana'


def test_rfloordiv_bad_type() -> None:
    er = EvaluationResults(50)
    with pytest.raises(
        TypeError,
        match="The supplied type is not valid: str"
    ):
        'banana' // er


def test_mod_er() -> None:
    er = EvaluationResults(1)
    second_er = EvaluationResults(4)
    assert er % second_er == 1


def test_mod_bad_type() -> None:
    er = EvaluationResults(250)
    with pytest.raises(
        TypeError,
        match="can only concatenate str"
    ):
        er % 'banana'


def test_rmod_bad_type() -> None:
    er = EvaluationResults(5556)
    with pytest.raises(
        TypeError,
        match="The supplied type is not valid"
    ):
        ['Skippy'] % er


def test_pow_er() -> None:
    er = EvaluationResults(2)
    second_er = EvaluationResults(8)
    assert er ** second_er == 256


def test_pow_bad_type() -> None:
    er = EvaluationResults(1298084.12)
    with pytest.raises(
        TypeError,
        match="The supplied type is not valid"
    ):
        er ** 'apple'


def test_rpow_bad_type() -> None:
    er = EvaluationResults(109)
    with pytest.raises(
        TypeError,
        match="The supplied type is not valid: str"
    ):
        'apple' ** er


def test_er_eq_er() -> None:
    er = EvaluationResults(200)
    second_er = EvaluationResults()
    second_er += 200
    assert er == second_er


def test_eq_non_num() -> None:
    er = EvaluationResults(9001)
    assert er != "Banana"


def test_add() -> None:
    er = EvaluationResults()
    er = er + 2
    assert er == 2


def test_add_non_num() -> None:
    er = EvaluationResults()
    with pytest.raises(TypeError, match="can only concatenate str"):
        er + 'Banana'  # noqa


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


def test_sub_non_num() -> None:
    er = EvaluationResults()
    with pytest.raises(TypeError, match="can only concatenate str"):
        er - 'Banana'  # noqa


def test_rsub_non_num() -> None:
    er = EvaluationResults()
    with pytest.raises(TypeError, match="can only concatenate str"):
        'Banana' - er  # noqa


def test_isub() -> None:
    er = EvaluationResults(0)
    er -= -10
    assert er == 10


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


def test_mul_non_num() -> None:
    with pytest.raises(TypeError, match="can only concatenate str"):
        EvaluationResults() * "banana"


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


def test_truediv_er() -> None:
    assert EvaluationResults(10) / EvaluationResults(2) == 5


def test_truediv_non_num() -> None:
    with pytest.raises(TypeError, match="can only concatenate str"):
        EvaluationResults(0) / "Pants"  # noqa


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


def test_make_er_from_er() -> None:
    er = EvaluationResults()
    er += 234
    second_er = EvaluationResults(er)
    assert second_er == 234


def test_to_int() -> None:
    er = EvaluationResults(5.5)
    assert isinstance(int(er), int)
    assert int(er) == 5


def test_len() -> None:
    er = EvaluationResults()
    rr = RollResults("1d6", [6])

    assert len(er) == 0
    er.add_roll(rr)
    assert len(er) == 1
