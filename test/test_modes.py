# Turn off pylint warnings unavoidable with pytest
# pylint: disable=redefined-outer-name, line-too-long, redefined-builtin, missing-module-docstring


def test_missing_modes():
    """Validation should fail if there is no modes section"""
    assert 1 == 0


def test_missing_default_mode():
    """Validation should fail if default mode is missing or blank"""
    assert 1 == 0


def test_invalid_modes():
    """Validation should fail if modes is not a list"""
    assert 1 == 0
