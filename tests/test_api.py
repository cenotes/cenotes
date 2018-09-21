from cenotes.api import CENParams


def test_wrong_algorithm_keeps_hardness(app):
    algo, hardness = CENParams.enforce_correct_encr_options(
        algorithm="lalala", hardness="sensitive")
    assert algo == "scrypt"
    assert hardness == "sensitive"


def test_wrong_algorithm_hardness(app):
    algo, hardness = CENParams.enforce_correct_encr_options(
        algorithm="scrypt", hardness="se")
    assert algo == "scrypt"
    assert hardness == "min"


def test_no_algorithm_options_given(app):
    params = CENParams()
    assert params.algorithm == app.config[
        "FALLBACK_ALGORITHM_PARAMS"]["algorithm"]
    assert params.hardness == app.config[
        "FALLBACK_ALGORITHM_PARAMS"]["hardness"]
