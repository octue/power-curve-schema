# Turn off pylint warnings unavoidable with pytest
# pylint: disable=redefined-outer-name, line-too-long, redefined-builtin, missing-module-docstring

from jsonschema import validate
from jsonschema.exceptions import ValidationError
import pytest
from .helpers import get_subschema


@pytest.fixture
def subschema(schema):
    """Provide a schema that requires only the turbine part of the whole schema"""
    return get_subschema(schema, "power_curves")


def test_missing_power_curves(subschema):
    """Validation should fail if there is no power_curves section"""
    with pytest.raises(ValidationError) as e:
        validate(instance={}, schema=subschema)
    assert "'power_curves' is a required property" in str(e)


def test_missing_default_mode(subschema, one_dimensional_mode):
    """Validation should fail if there is no default_mode value"""
    with pytest.raises(ValidationError) as e:
        validate(instance={"power_curves": {"modes": [one_dimensional_mode]}}, schema=subschema)
    assert "'default_mode' is a required property" in str(e)


def test_blank_default_mode(subschema, one_dimensional_mode):
    """Validation should fail if default_mode is blank"""
    with pytest.raises(ValidationError) as e:
        validate(instance={"power_curves": {"default_mode": "", "modes": [one_dimensional_mode]}}, schema=subschema)
    assert "is too short" in str(e)


def test_missing_modes(subschema):
    """Validation should fail if there is no modes section"""
    with pytest.raises(ValidationError) as e:
        validate(instance={"power_curves": {"default_mode": ""}}, schema=subschema)
    assert "'modes' is a required property" in str(e)


def test_invalid_modes(subschema):
    """Validation should fail if modes is not a list"""
    with pytest.raises(ValidationError) as e:
        validate(
            instance={"power_curves": {"default_mode": "", "modes": {}}},
            schema=subschema,
        )

    assert "is not of type 'array'" in str(e)
