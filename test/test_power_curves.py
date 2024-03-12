# Turn off pylint warnings unavoidable with pytest
# pylint: disable=redefined-outer-name, line-too-long, redefined-builtin, missing-module-docstring

from copy import deepcopy

import pytest
from jsonschema import validate
from jsonschema.exceptions import ValidationError

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
        validate(
            instance={"power_curves": {"modes": [one_dimensional_mode]}},
            schema=subschema,
        )
    assert "'default_mode' is a required property" in str(e)


def test_blank_default_mode(subschema, one_dimensional_mode):
    """Validation should fail if default_mode is blank"""
    with pytest.raises(ValidationError) as e:
        validate(
            instance={
                "power_curves": {"default_mode": "", "modes": [one_dimensional_mode]}
            },
            schema=subschema,
        )
    assert "does not match" in str(e)


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


def test_one_dimensional_mode(subschema, one_dimensional_mode):
    """Validation should fail if there is no overrides section in a mode"""

    validate(
        instance={
            "power_curves": {
                "default_mode": "one_dimensional",
                "modes": [one_dimensional_mode],
            }
        },
        schema=subschema,
    )


def test_two_dimensional_mode(subschema, two_dimensional_mode):
    """Validation should fail if there is no overrides section in a mode"""

    validate(
        instance={
            "power_curves": {
                "default_mode": "two_dimensional",
                "modes": [two_dimensional_mode],
            }
        },
        schema=subschema,
    )


def test_missing_mode_properties(subschema, one_dimensional_mode):
    """Validation should fail if there is no overrides section in a mode"""

    for required in [
        "overrides",
        "cuts",
        "parameters",
        "cp",
        "ct",
        "cp_is_coefficient",
        "ct_is_coefficient",
    ]:
        partial = deepcopy(one_dimensional_mode)
        partial.pop(required)
        with pytest.raises(ValidationError) as e:
            validate(
                instance={
                    "power_curves": {
                        "default_mode": "one_dimensional",
                        "modes": [partial],
                    }
                },
                schema=subschema,
            )
        assert f"'{required}' is a required property" in str(e)


def test_invalid_cuts(subschema, one_dimensional_mode):
    """Validation should fail if cut kind, speed or period is invalid"""

    invalid = [
        (
            {
                "kind": "not_a_cut",
                "wind_speed": 25,
                "period": 600,
            },
            "is not one of",
        ),
        (
            {
                "kind": "low_cut_in",
                "wind_speed": "not a speed",
                "period": 600,
            },
            "is not of type 'number'",
        ),
        (
            {
                "kind": "low_cut_in",
                "wind_speed": 20,
                "period": "not a period",
            },
            "is not of type 'number'",
        ),
    ]

    for cut, reason in invalid:
        one_dimensional_mode["cuts"][0] = cut

        with pytest.raises(ValidationError) as e:
            validate(
                instance={
                    "power_curves": {
                        "default_mode": "one_dimensional",
                        "modes": [one_dimensional_mode],
                    }
                },
                schema=subschema,
            )

        assert reason in str(e)


def test_invalid_overrides(subschema, one_dimensional_mode):
    """Validation should fail if overrides are invalid"""

    invalid = [
        (
            {"rated_power": -10},
            "is less than",
        ),
        (
            {
                "available_hub_heights": "not an array or hub heights dict",
            },
            "is not valid under any of the given schemas",
        ),
        (
            {
                "rated_rpm": "not an rpm value",
            },
            "is not of type 'number'",
        ),
        (
            {
                "cut_in_rpm": "not an rpm value",
            },
            "is not of type 'number'",
        ),
    ]

    for overrides, reason in invalid:
        one_dimensional_mode["overrides"] = overrides

        with pytest.raises(ValidationError) as e:
            validate(
                instance={
                    "power_curves": {
                        "default_mode": "one_dimensional",
                        "modes": [one_dimensional_mode],
                    }
                },
                schema=subschema,
            )

        assert reason in str(e)
