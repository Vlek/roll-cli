"""Testing the functionality of our EvaluationResults object."""
import pytest

from roll_cli.parser.types import EvaluationResults
from roll_cli.parser.types import RollResults


def test_addition() -> None:
    """Test the normal addition operation."""
    er = EvaluationResults(200)
    assert er + 5 == 205


def test_subtraction() -> None:
    """Test the normal subtraction operation."""
    er = EvaluationResults(200)
    assert er - 5 == 195


def test_eq() -> None:
    """Test that the comparison operator works as expected."""
    er = EvaluationResults(200)
    assert er == 200


def test_to_float() -> None:
    """Test that the value of an ER object is correctly changed to float."""
    er = EvaluationResults(1000)
    assert isinstance(float(er), float)


def test_rtruediv() -> None:
    """Test the normal division operator works."""
    er = EvaluationResults(2)
    assert 10 / er == 5


def test_rtruediv_bad_type() -> None:
    """Test that we are supplying the correct error message on bad type for div."""
    er = EvaluationResults()
    with pytest.raises(TypeError, match="The supplied type is not valid: str"):
        "banana" / er  # type: ignore


def test_floordiv_er() -> None:
    """Test that floor division works."""
    er = EvaluationResults(6)
    second_er = EvaluationResults(13)

    assert second_er // er == 2


def test_floordiv_bad_type() -> None:
    """Ensure that the correct error message is supplied for bad type on floor div."""
    er = EvaluationResults(100)
    with pytest.raises(TypeError, match="The supplied type is not valid: str"):
        er // "banana"  # type: ignore


def test_rfloordiv_bad_type() -> None:
    """Ensure that the correct error message is supplied for bad type on floor div."""
    er = EvaluationResults(50)
    with pytest.raises(TypeError, match="The supplied type is not valid: str"):
        "banana" // er  # type: ignore


def test_mod_er() -> None:
    """Test that the modulus operator works."""
    er = EvaluationResults(1)
    second_er = EvaluationResults(4)
    assert er % second_er == 1


def test_mod_bad_type() -> None:
    """Test that the correct error message is supplied for bad types with modulus."""
    er = EvaluationResults(250)
    with pytest.raises(TypeError, match="The supplied type is not valid: str"):
        er % "banana"  # type: ignore


def test_rmod_bad_type() -> None:
    """Test that the correct error message is supplied for bad types with modulus."""
    er = EvaluationResults(5556)
    with pytest.raises(TypeError, match="The supplied type is not valid"):
        ["Skippy"] % er  # type: ignore


def test_pow_er() -> None:
    """Test that exponential works."""
    er = EvaluationResults(2)
    second_er = EvaluationResults(8)
    assert er**second_er == 256


def test_pow_bad_type() -> None:
    """Test that the correct error message is supposed for bad types."""
    er = EvaluationResults(1298084.12)
    with pytest.raises(TypeError, match="The supplied type is not valid"):
        er ** "apple"  # type: ignore


def test_rpow_bad_type() -> None:
    """Test that the correct error message is supposed for bad types."""
    er = EvaluationResults(109)
    with pytest.raises(TypeError, match="The supplied type is not valid: str"):
        "apple" ** er  # type: ignore


def test_er_eq_er() -> None:
    """Test that the comparison operator works with two ER objects."""
    er = EvaluationResults(200)
    second_er = EvaluationResults()
    second_er += 200
    assert er == second_er


def test_eq_non_num() -> None:
    """Test the comparison operator against the wrong type."""
    er = EvaluationResults(9001)
    assert er != "Banana"


def test_add() -> None:
    """Test doing addition with an ER object."""
    er = EvaluationResults()
    er = er + 2
    assert er == 2


def test_add_non_num() -> None:
    """Test that the correct error message is supposed for bad types."""
    er = EvaluationResults()
    with pytest.raises(TypeError, match="The supplied type is not valid: str"):
        er + "Banana"  # type: ignore


def test_unary_minus() -> None:
    """Test the unary minus on an ER object."""
    er = EvaluationResults()
    er += 5
    er = -er
    assert er == -5


def test_add_reversed() -> None:
    """Test doing addition with an ER object."""
    er = EvaluationResults()
    er = 2 + er
    assert er == 2


def test_sub() -> None:
    """Test doing subtraction on an ER object."""
    er = EvaluationResults()
    er = er - 2
    assert er == -2


def test_sub_non_num() -> None:
    """Test that the correct error message is supposed for bad types."""
    er = EvaluationResults()
    with pytest.raises(TypeError, match="The supplied type is not valid: str"):
        er - "Banana"  # type: ignore


def test_rsub_non_num() -> None:
    """Test that the correct error message is supposed for bad types."""
    er = EvaluationResults()
    with pytest.raises(TypeError, match="The supplied type is not valid: str"):
        "Banana" - er  # type: ignore


def test_isub() -> None:
    """Test doing subtraction with an ER object."""
    er = EvaluationResults(0)
    er -= -10
    assert er == 10


def test_sub_reversed() -> None:
    """Test doing subtraction with an ER object."""
    er = EvaluationResults()
    er = 2 - er
    assert er == 2


def test_mul() -> None:
    """Test that we can do multiplication and addition on an ER object."""
    er = EvaluationResults()
    er += 5
    er *= 2
    er = 7 * er
    assert er == 70


def test_mul_non_num() -> None:
    """Test that the correct error message is supposed for bad types."""
    with pytest.raises(TypeError, match="The supplied type is not valid: str"):
        EvaluationResults() * "banana"  # type: ignore


def test_mul_reversed() -> None:
    """Test whether we can do multiplication with an ER object."""
    er = EvaluationResults()
    er += 5
    er = 7 * er
    assert er == 35


def test_truediv() -> None:
    """Test that we can do vision on an ER object."""
    er = EvaluationResults()
    er += 60
    er /= 10
    assert er == 6


def test_truediv_reversed() -> None:
    """Test that we can do division with an ER object."""
    er = EvaluationResults()
    er += 8
    er = 24 / er
    assert er == 3


def test_truediv_er() -> None:
    """Test doing division on two ER objects."""
    assert EvaluationResults(10) / EvaluationResults(2) == 5


def test_truediv_non_num() -> None:
    """Test that the correct error message is supposed for bad types."""
    with pytest.raises(TypeError, match="The supplied type is not valid: str"):
        EvaluationResults(0) / "Pants"  # type: ignore


def test_floordiv() -> None:
    """Test that we can do floor div on an ER object."""
    er = EvaluationResults()
    er += 120
    er //= 10
    assert er == 12


def test_floordiv_reversed() -> None:
    """Test that we can do floor div with an ER object."""
    er = EvaluationResults()
    er += 14
    er = 112 // er
    assert er == 8


def test_modulus() -> None:
    """Test that we can do mod division on an ER object."""
    er = EvaluationResults()
    er += 240
    er %= 9
    assert er == 6


def test_modulus_reversed() -> None:
    """Test that we can do mod division on an ER object."""
    er = EvaluationResults()
    er += 7
    er = 6 % er
    assert er == 6


def test_exponential() -> None:
    """Test using expo on an er object."""
    er = EvaluationResults()
    er += 2
    er **= 5
    assert er == 32


def test_exponential_reversed() -> None:
    """Testing that we can use an ER object to expo a number."""
    er = EvaluationResults()
    er += 8
    er = 7**er
    assert er == 5764801


def test_make_er_from_er() -> None:
    """Test when combining ER objects that the value is saved between the two."""
    er = EvaluationResults()
    er += 234
    second_er = EvaluationResults(er)
    assert second_er == 234


def test_to_int() -> None:
    """Test that we get the correct result went changing the value to an int."""
    er = EvaluationResults(5.5)
    assert isinstance(int(er), int)
    assert int(er) == 5


def test_len() -> None:
    """Ensure that the length works after adding to it."""
    er = EvaluationResults()
    rr = RollResults("1d6", [6])

    assert len(er) == 0
    er.add_roll(rr)
    assert len(er) == 1
