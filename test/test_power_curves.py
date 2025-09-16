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
            instance={"power_curves": {"operating_modes": [one_dimensional_mode]}},
            schema=subschema,
        )
    assert "'default_operating_mode' is a required property" in str(e)


def test_blank_default_mode(subschema, one_dimensional_mode):
    """Validation should fail if default_operating_mode is blank"""
    with pytest.raises(ValidationError) as e:
        validate(
            instance={"power_curves": {"default_operating_mode": "", "operating_modes": [one_dimensional_mode]}},
            schema=subschema,
        )
    assert "does not match" in str(e)


def test_missing_modes(subschema):
    """Validation should fail if there is no modes section"""
    with pytest.raises(ValidationError) as e:
        validate(instance={"power_curves": {"default_operating_mode": ""}}, schema=subschema)
    assert "'operating_modes' is a required property" in str(e)


def test_invalid_modes(subschema):
    """Validation should fail if modes is not a list"""
    with pytest.raises(ValidationError) as e:
        validate(
            instance={"power_curves": {"default_operating_mode": "", "operating_modes": {}}},
            schema=subschema,
        )

    assert "is not of type 'array'" in str(e)


def test_one_dimensional_mode(subschema, one_dimensional_mode):
    """Validation should fail if there is no overrides section in a mode"""

    validate(
        instance={
            "power_curves": {
                "default_operating_mode": "one_dimensional",
                "operating_modes": [one_dimensional_mode],
            }
        },
        schema=subschema,
    )


def test_two_dimensional_mode(subschema, two_dimensional_mode):
    """Validation should fail if there is no overrides section in a mode"""

    validate(
        instance={
            "power_curves": {
                "default_operating_mode": "two_dimensional",
                "operating_modes": [two_dimensional_mode],
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
        "power",
        "thrust",
        "power_is_coefficient",
        "thrust_is_coefficient",
    ]:
        partial = deepcopy(one_dimensional_mode)
        partial.pop(required)
        with pytest.raises(ValidationError) as e:
            validate(
                instance={
                    "power_curves": {
                        "default_operating_mode": "one_dimensional",
                        "operating_modes": [partial],
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
                "kind": "not-a-cut",
                "wind_speed": 25,
                "period": 600,
            },
            "is not one of",
        ),
        (
            {
                "kind": "low-cut-in",
                "wind_speed": "not a speed",
                "period": 600,
            },
            "is not of type 'number'",
        ),
        (
            {
                "kind": "low-cut-in",
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
                        "default_operating_mode": "one_dimensional",
                        "operating_modes": [one_dimensional_mode],
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
                        "default_operating_mode": "one_dimensional",
                        "operating_modes": [one_dimensional_mode],
                    }
                },
                schema=subschema,
            )

        assert reason in str(e)


def test_acoustic_emissions(subschema, one_dimensional_mode):
    """"""
    # fmt: off
    third_octave_noise = {
        "margin": 2,
        "weighting": "A",
        "wind_speed": [5, 6, 7, 8, 9, 10],
        "frequency": [25, 31, 40, 50, 63, 80, 100, 125, 160, 200, 250, 315, 400, 500, 630, 800, 1000, 1250, 1600, 2000, 2500, 3150, 4000, 6300, 8000, 10000, 12500, 16000, 20000],
        "sound_pressure_level": [
            [8.3, 13.6, 18.4, 45.6, 53.4, 62.2, 71.4, 71.2, 75.1, 80, 84.5, 88.3, 90.7, 92.5, 93.1, 93.8, 93.2, 92.2, 90.6, 88.1, 85.8, 83.5, 80.3, 77.6, 52.9, 51.9, 50.5, 48.7, 46.4, 43.7],
            [8.3, 13.6, 18.4, 48.3, 55.8, 62.9, 75.2, 76, 79.3, 84.4, 88.7, 92.2, 94.1, 96, 96.1, 96.3, 95.7, 94.7, 93.3, 91.1, 89, 87.2, 84.3, 80.5, 52.9, 51.9, 50.5, 48.7, 46.4, 43.7],
            [8.3,13.6,18.4,49.2,57.2,64.6,76.6,77.9,81.4,85.9,90,93.3,95,96.9,96.8,96.9,96.4,95.6,94.3,91.8,89.8,88,85.3,82,52.9,51.9,50.5,48.7,46.4,43.7],
            [8.3,13.6,18.4,49,57.2,64.6,76.6,77.4,81,85.6,89.5,92.8,94.4,96.7,96.6,96.8,96.8,96,94.7,91.9,89.7,87.6,84.7,53.5,52.9,51.9,50.5,48.7,46.4,43.7],
            [8.3,13.6,18.4,49.4,56.8,63.4,73.9,75.2,78.6,82.3,86,89.9,91.3,94.4,95.5,96.5,97.7,97.3,95.9,93.1,90.5,87.8,85.1,84.4,52.9,51.9,50.5,48.7,46.4,43.7],
            [8.3,13.6,18.4,48.5,56,62.8,72.5,74,77.1,80.3,83.1,87.4,89,92.7,94.3,95.7,97.2,96.7,95.3,92.5,89.9,54.2,54,53.5,52.9,51.9,50.5,48.7,46.4,43.7]
        ]
    }

    octave_noise = {
        "margin": 2,
        "weighting": "A",
        "frequency": [16, 31.5, 63, 125, 250, 500, 1000, 2000, 4000, 8000, 16000],
        "wind_speed": [5, 6, 7, 8, 9, 10],
        "sound_pressure_level": [
            [5.2, 19.7, 62.8, 77.7, 90.2, 97.0, 97.9, 93.4, 85.9, 56.6, 51.5],
            [5.3, 19.8, 63.8, 82.0, 94.3, 100.3, 100.4, 96.3, 89.6, 56.6, 51.3],
            [5.4, 19.8, 65.4, 83.9, 95.5, 101.1, 101.1, 97.1, 90.5, 56.6, 51.5],
            [5.3, 19.9, 65.4, 83.6, 95.0, 100.8, 101.3, 97.4, 89.4, 56.6, 51.4],
            [5.2, 19.8, 64.4, 81.1, 91.9, 98.8, 102.0, 98.5, 90.8, 56.6, 51.5],
            [5.1, 19.6, 63.8, 79.7, 89.3, 97.3, 101.3, 97.9, 58.7, 56.6, 51.6]
        ]
    }

    total_noise = {
        "margin": 2,
        "weighting": "A",
        "wind_speed": [5, 6, 7, 8, 9, 10],
        "sound_pressure_level": [101.7, 104.7, 105.5, 105.5, 105.2, 104.2]
    }
    # fmt: on

    for acoustic_emissions in [third_octave_noise, octave_noise, total_noise]:
        one_dimensional_mode["acoustic_emissions"] = acoustic_emissions
        validate(
            instance={
                "power_curves": {
                    "default_operating_mode": "one_dimensional",
                    "operating_modes": [one_dimensional_mode],
                }
            },
            schema=subschema,
        )
