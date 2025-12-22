# Turn off pylint warnings unavoidable with pytest
# pylint: disable=redefined-outer-name, line-too-long, redefined-builtin, missing-module-docstring


import pytest
from jsonschema import validate
from jsonschema.exceptions import ValidationError

from .helpers import get_subschema


@pytest.fixture
def subschema(schema):
    """Provide a schema that requires only the turbine part of the whole schema"""
    return get_subschema(schema, "turbine")


def test_generic_turbine(subschema, generic_turbine):
    """Validation should pass on the generic turbine"""
    validate(instance=generic_turbine, schema=subschema)


def test_missing_turbine(subschema):
    """Validation should fail if there is no turbine section"""
    with pytest.raises(ValidationError) as e:
        validate(instance={}, schema=subschema)
    assert "'turbine' is a required property" in str(e)


@pytest.mark.parametrize(
    "property",
    [
        "model_name",
        "manufacturer_name",
        "rated_power",
        "rotor_diameter",
        "model_description",
        "drive_type",
        "regulation_type",
        "number_of_blades",
    ],
)
def test_missing_properties(subschema, generic_turbine, property):
    """Validation should fail if any required property is missing from turbine metadata"""
    generic_turbine["turbine"].pop(property, None)
    with pytest.raises(ValidationError) as e:
        validate(instance=generic_turbine, schema=subschema)
    assert f"'{property}' is a required property" in str(e)


@pytest.mark.parametrize(
    "property",
    ["model_name", "manufacturer_name", "manufacturer_display_name"],
)
def test_non_blankable_properties(subschema, generic_turbine, property):
    """Validation should fail if any required string property (other than model_description) contains a blank string"""
    generic_turbine["turbine"][property] = ""
    with pytest.raises(ValidationError) as e:
        validate(instance=generic_turbine, schema=subschema)
    assert "is too short" in str(e)


@pytest.mark.parametrize(
    "property",
    ["model_description", "platform_name", "platform_description"],
)
def test_blankable_properties(subschema, generic_turbine, property):
    """Validation should pass if these string properties contain a blank string"""
    generic_turbine["turbine"][property] = ""
    validate(instance=generic_turbine, schema=subschema)


@pytest.mark.parametrize(
    "property",
    ["model_name", "platform_name", "manufacturer_display_name"],
)
def test_name_length_limits(subschema, generic_turbine, property):
    """Validation should fail if name properties exceed a character limit"""
    generic_turbine["turbine"][property] = "01234567890123456789012345678901234567890-"
    with pytest.raises(ValidationError) as e:
        validate(instance=generic_turbine, schema=subschema)
    assert "is too long" in str(e)


@pytest.mark.parametrize(
    "value",
    ["", "wrong", None],
)
def test_invalid_power_reference_location(subschema, generic_turbine, value):
    """Validation should fail if any required string property (other than model_description) contains a blank string"""
    generic_turbine["turbine"]["power_reference_location"] = value
    with pytest.raises(ValidationError) as e:
        validate(instance=generic_turbine, schema=subschema)
    assert "is not one of" in str(e)


@pytest.mark.parametrize("available_hub_heights", [{"max": 168, "min": 84}, [100, 110, 112.3]])
def test_available_hub_heights(subschema, generic_turbine, available_hub_heights):
    """Hub heights should be definable as a continuous range of values or as a list of numbers"""
    generic_turbine["turbine"]["available_hub_heights"] = available_hub_heights
    validate(instance=generic_turbine, schema=subschema)


@pytest.mark.parametrize(
    "manufacturer_display_name",
    [
        (10, "is not of type 'string'"),
        (True, "is not of type 'string'"),
        (
            "12345678901234567890123456789012345678901",
            "is too long",
        ),  # 41 characters
    ],
)
def test_invalid_manufacturer_display_names(subschema, generic_turbine, manufacturer_display_name):
    """Ensure manufacturer_display_name is validated as a string of maximum length"""
    generic_turbine["turbine"]["manufacturer_display_name"] = manufacturer_display_name[0]
    with pytest.raises(ValidationError) as e:
        validate(instance=generic_turbine, schema=subschema)
    assert manufacturer_display_name[1] in str(e)


@pytest.mark.parametrize(
    "rotor_diameter",
    [
        (0, "is less than or equal to the minimum of 0"),
        (
            1000,
            "is greater than or equal to the maximum of 1000",
        ),
    ],
)
def test_invalid_rotor_diameters(subschema, generic_turbine, rotor_diameter):
    """Ensure rotor diameter cannot be outside acceptable bounds"""
    generic_turbine["turbine"]["rotor_diameter"] = rotor_diameter[0]
    with pytest.raises(ValidationError) as e:
        validate(instance=generic_turbine, schema=subschema)
    assert rotor_diameter[1] in str(e)


@pytest.mark.parametrize("drive_type", ["direct", "geared", "other"])
def test_valid_drive_types(subschema, generic_turbine, drive_type):
    """There is a fixed set of available drive types"""
    generic_turbine["turbine"]["drive_type"] = drive_type
    validate(instance=generic_turbine, schema=subschema)


def test_invalid_drive_type(subschema, generic_turbine):
    """Validation should fail if drive type is anything but one of a set of values"""
    generic_turbine["turbine"]["drive_type"] = "gizmo"
    with pytest.raises(ValidationError) as e:
        validate(instance=generic_turbine, schema=subschema)
    assert "'gizmo' is not one of ['geared', 'direct', 'other']" in str(e)


@pytest.mark.parametrize("drive_type", ["pitch", "stall", "other"])
def test_valid_regulation_types(subschema, generic_turbine, drive_type):
    """There is a fixed set of available regulation types"""
    generic_turbine["turbine"]["regulation_type"] = drive_type
    validate(instance=generic_turbine, schema=subschema)


def test_invalid_regulation_type(subschema, generic_turbine):
    """Validation should fail if regulation type is anything but one of a set of values"""
    generic_turbine["turbine"]["regulation_type"] = "aeroflap"
    with pytest.raises(ValidationError) as e:
        validate(instance=generic_turbine, schema=subschema)
    assert "'aeroflap' is not one of ['pitch', 'stall', 'other']" in str(e)


def test_reactive_power_derating(subschema, generic_turbine):
    """Validation should pass for reactive power based thermal derating"""
    generic_turbine["turbine"]["thermal_regulation"] = {
        "derating": [
            {
                "legend": "High temperature derating, reactive power 0 VAr",
                "reactive_power": 0,
                "temperature": [35, 36, 37, 38, 39, 40],
                "power_limit": [20e6, 18.8e6, 17.5e6, 16.5e6, 15.3e6, 14e6],
            }
        ]
    }
    validate(instance=generic_turbine, schema=subschema)


def test_reactive_power_derating_with_multiple_curves(subschema, generic_turbine):
    """Validation should pass for multiple reactive power based thermal derating curves"""
    generic_turbine["turbine"]["thermal_regulation"] = {
        "derating": [
            {
                "legend": "High temperature derating, reactive power 0 VAr",
                "reactive_power": 0,
                "temperature": [35, 40],
                "power_limit": [20e6, 14e6],
            },
            {
                "legend": "High temperature derating, reactive power 6.5 MVAr",
                "reactive_power": 6.5e6,
                "temperature": [30, 40],
                "power_limit": [20e6, 12.3e6],
            },
            {
                "legend": "High temperature derating, reactive power 9.5 MVAr",
                "reactive_power": 9.5e6,
                "temperature": [30, 40, 41],
                "power_limit": [20e6, 10.2e6, 0],
            },
        ]
    }
    validate(instance=generic_turbine, schema=subschema)


def test_reactive_power_derating_negative_value_invalid(subschema, generic_turbine):
    """Validation should fail for negative reactive power values"""
    generic_turbine["turbine"]["thermal_regulation"] = {
        "derating": [
            {
                "reactive_power": -1000,
                "temperature": [35, 40],
                "power_limit": [20e6, 14e6],
            }
        ]
    }
    with pytest.raises(ValidationError) as e:
        validate(instance=generic_turbine, schema=subschema)
    assert "minimum" in str(e)


def test_reactive_power_derating_missing_required_field(subschema, generic_turbine):
    """Validation should fail if reactive_power derating is missing temperature or power_limit"""
    generic_turbine["turbine"]["thermal_regulation"] = {
        "derating": [
            {
                "reactive_power": 0,
                "temperature": [35, 40],
                # missing power_limit
            }
        ]
    }
    with pytest.raises(ValidationError) as e:
        validate(instance=generic_turbine, schema=subschema)
    # Since derating uses anyOf, the error message indicates it doesn't match any schema
    assert "is not valid under any of the given schemas" in str(e)
