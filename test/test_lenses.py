# Turn off pylint warnings unavoidable with pytest
# pylint: disable=redefined-outer-name, line-too-long, redefined-builtin, missing-module-docstring

import copy
import json
import os

import pytest

from lenses.lenses import (
    _add_power_reference_location,
    _change_shear_coefficient_to_vertical_shear_exponent,
    _collapse_singleton_dimensions,
    _convert_dcmi_term_to_term_name,
    _move_available_hub_heights_to_restricted,
    _rename_dimension_to_axis,
)

from .conftest import ROOT_DIR


@pytest.fixture(scope="session")
def loaded_generic_120_3_alpha_3():
    """Provides the generic 120m 3.45MW turbine in alpha-3 compliant form"""
    with open(os.path.join(ROOT_DIR, "test", "fixtures", "generic-120-3-alpha-3.json"), "r", encoding="utf-8") as fp:
        instance = json.load(fp)
    return instance


@pytest.fixture()
def generic_120_3_alpha_3(loaded_generic_120_3_alpha_3):
    """A fresh deep copy of the generic 120m 3.45MW turbine in alpha-3 compliant form as a test instance"""
    return copy.deepcopy(loaded_generic_120_3_alpha_3)


@pytest.fixture(scope="session")
def loaded_generic_274_20_alpha_3():
    """Provides the generic 274m 20MW turbine in alpha-3 compliant form"""
    with open(
        os.path.join(ROOT_DIR, "power-curve-schema", "examples", "generic-274-20.json"), "r", encoding="utf-8"
    ) as fp:
        instance = json.load(fp)
    return instance


@pytest.fixture()
def generic_274_20_alpha_3(loaded_generic_274_20_alpha_3):
    """A fresh deep copy of the generic 274m 20MW turbine in alpha-3 compliant form as a test instance"""
    return copy.deepcopy(loaded_generic_274_20_alpha_3)


def test_add_power_reference_location(generic_120_3_alpha_3):
    """Should add property to an existing document which doesn't have it"""
    transformed = _add_power_reference_location(generic_120_3_alpha_3)
    assert transformed["turbine"]["power_reference_location"] == "low-voltage"


def test_add_power_reference_location_fails_with_invalid_input(generic_120_3_alpha_3):
    """Pass a document which already has the field (should fail to overwrite)"""

    generic_120_3_alpha_3["turbine"]["power_reference_location"] = "high-voltage"

    with pytest.raises(ValueError):
        _add_power_reference_location(generic_120_3_alpha_3)


def test_rename_shear_coefficient(generic_120_3_alpha_3):
    """Should rename a parameter label"""
    # We don't have a test fixture with this so add it for the purpose. This is physically meaningless but tests the code.
    generic_120_3_alpha_3["power_curves"]["operating_modes"][0]["parameters"][1]["label"] = "shear-coefficient"

    transformed = _change_shear_coefficient_to_vertical_shear_exponent(generic_120_3_alpha_3)
    assert transformed["power_curves"]["operating_modes"][0]["parameters"][1]["label"] == "vertical-shear-exponent"


def test_move_available_hub_heights_to_restricted(generic_120_3_alpha_3):
    """Should move overrides.available_hub_heights to mode-level restricted_to_hub_heights"""
    # Add available_hub_heights to overrides for the test
    generic_120_3_alpha_3["power_curves"]["operating_modes"][0]["overrides"] = {
        "available_hub_heights": [100, 120, 140]
    }

    transformed = _move_available_hub_heights_to_restricted(generic_120_3_alpha_3)

    # Check the value was moved to mode-level restricted_to_hub_heights
    assert transformed["power_curves"]["operating_modes"][0]["restricted_to_hub_heights"] == [100, 120, 140]
    # Check available_hub_heights was removed from overrides
    assert "available_hub_heights" not in transformed["power_curves"]["operating_modes"][0]["overrides"]


def test_move_available_hub_heights_to_restricted_with_range(generic_120_3_alpha_3):
    """Should handle range format for available_hub_heights"""
    generic_120_3_alpha_3["power_curves"]["operating_modes"][0]["overrides"] = {
        "available_hub_heights": {"min": 100, "max": 140}
    }

    transformed = _move_available_hub_heights_to_restricted(generic_120_3_alpha_3)

    assert transformed["power_curves"]["operating_modes"][0]["restricted_to_hub_heights"] == {"min": 100, "max": 140}
    assert "available_hub_heights" not in transformed["power_curves"]["operating_modes"][0]["overrides"]


def test_move_available_hub_heights_no_op_when_not_present(generic_120_3_alpha_3):
    """Should not modify anything if available_hub_heights is not in overrides"""
    # Ensure no overrides or empty overrides
    generic_120_3_alpha_3["power_curves"]["operating_modes"][0]["overrides"] = {}

    transformed = _move_available_hub_heights_to_restricted(generic_120_3_alpha_3)

    assert "restricted_to_hub_heights" not in transformed["power_curves"]["operating_modes"][0]


def test_rename_dimension_to_axis(generic_120_3_alpha_3):
    """Should rename 'dimension' property to 'axis' in all parameters"""
    # The fixture has dimension: 0 for air-density and dimension: 1 for wind-speed
    params = generic_120_3_alpha_3["power_curves"]["operating_modes"][0]["parameters"]
    assert "dimension" in params[0]
    assert "dimension" in params[1]

    transformed = _rename_dimension_to_axis(generic_120_3_alpha_3)

    params = transformed["power_curves"]["operating_modes"][0]["parameters"]
    assert "dimension" not in params[0]
    assert "dimension" not in params[1]
    assert params[0]["axis"] == 0
    assert params[1]["axis"] == 1


def test_rename_dimension_to_axis_no_op_when_no_dimension(generic_120_3_alpha_3):
    """Should not modify parameters that don't have 'dimension' property"""
    # Convert fixture to use 'value' format instead of 'dimension'
    generic_120_3_alpha_3["power_curves"]["operating_modes"][0]["parameters"][0] = {
        "label": "air-density",
        "value": 1.225,
    }

    transformed = _rename_dimension_to_axis(generic_120_3_alpha_3)

    params = transformed["power_curves"]["operating_modes"][0]["parameters"]
    assert "axis" not in params[0]
    assert params[0]["value"] == 1.225


def test_collapse_singleton_dimensions(generic_120_3_alpha_3):
    """Should collapse singleton dimensions, converting to value format and flattening arrays.

    The fixture has:
    - air-density with axis: 0 and values: [1.225] (singleton)
    - wind-speed with axis: 1 and values: [3.0, 3.5, ...]
    - power as 2D array [[...]]
    - thrust_coefficient as 2D array [[...]]

    After collapsing:
    - air-density should have value: 1.225 (no axis)
    - wind-speed should have axis: 0 (renumbered from 1)
    - power should be 1D array
    - thrust_coefficient should be 1D array
    """
    # First rename dimension to axis (prerequisite)
    generic_120_3_alpha_3 = _rename_dimension_to_axis(generic_120_3_alpha_3)

    # Verify initial state
    mode = generic_120_3_alpha_3["power_curves"]["operating_modes"][0]
    assert mode["parameters"][0]["axis"] == 0
    assert mode["parameters"][0]["values"] == [1.225]
    assert mode["parameters"][1]["axis"] == 1
    assert isinstance(mode["power"][0], list)  # 2D array
    assert isinstance(mode["thrust_coefficient"][0], list)  # 2D array

    transformed = _collapse_singleton_dimensions(generic_120_3_alpha_3)

    mode = transformed["power_curves"]["operating_modes"][0]
    air_density = mode["parameters"][0]
    wind_speed = mode["parameters"][1]

    # air-density should now be a value parameter
    assert "axis" not in air_density
    assert "values" not in air_density
    assert air_density["value"] == 1.225

    # wind-speed should have renumbered axis
    assert wind_speed["axis"] == 0
    assert len(wind_speed["values"]) == 45

    # power should be 1D array
    assert isinstance(mode["power"], list)
    assert not isinstance(mode["power"][0], list)
    assert len(mode["power"]) == 45

    # thrust_coefficient should be 1D array
    assert isinstance(mode["thrust_coefficient"], list)
    assert not isinstance(mode["thrust_coefficient"][0], list)
    assert len(mode["thrust_coefficient"]) == 45


def test_collapse_singleton_dimensions_no_singletons(generic_120_3_alpha_3):
    """Should not modify anything if there are no singleton dimensions"""
    # Convert fixture to have no singleton dimensions
    generic_120_3_alpha_3["power_curves"]["operating_modes"][0]["parameters"][0] = {
        "label": "air-density",
        "value": 1.225,
    }
    generic_120_3_alpha_3["power_curves"]["operating_modes"][0]["parameters"][1]["axis"] = 0
    del generic_120_3_alpha_3["power_curves"]["operating_modes"][0]["parameters"][1]["dimension"]
    # Flatten arrays to 1D
    generic_120_3_alpha_3["power_curves"]["operating_modes"][0]["power"] = (
        generic_120_3_alpha_3["power_curves"]["operating_modes"][0]["power"][0]
    )
    generic_120_3_alpha_3["power_curves"]["operating_modes"][0]["thrust_coefficient"] = (
        generic_120_3_alpha_3["power_curves"]["operating_modes"][0]["thrust_coefficient"][0]
    )

    mode_before = copy.deepcopy(generic_120_3_alpha_3["power_curves"]["operating_modes"][0])
    transformed = _collapse_singleton_dimensions(generic_120_3_alpha_3)
    mode_after = transformed["power_curves"]["operating_modes"][0]

    # Should be unchanged
    assert mode_after["parameters"][0] == mode_before["parameters"][0]
    assert mode_after["parameters"][1] == mode_before["parameters"][1]
    assert mode_after["power"] == mode_before["power"]
    assert mode_after["thrust_coefficient"] == mode_before["thrust_coefficient"]


def test_convert_dcmi_term_to_term_name(generic_120_3_alpha_3):
    """Should convert 'term' property to 'term_name' and lowercase the value"""
    # Verify initial state - fixture has old format
    metadata = generic_120_3_alpha_3["document"]["metadata"]
    assert metadata[0]["term"] == "Identifier"
    assert metadata[1]["term"] == "Format"
    assert metadata[2]["term"] == "Source"

    transformed = _convert_dcmi_term_to_term_name(generic_120_3_alpha_3)

    metadata = transformed["document"]["metadata"]
    # Check term was renamed to term_name and lowercased
    assert "term" not in metadata[0]
    assert metadata[0]["term_name"] == "identifier"
    assert metadata[0]["value"] == "126b9e41-722f-49ab-9586-b55188adf420"

    assert "term" not in metadata[1]
    assert metadata[1]["term_name"] == "format"
    assert metadata[1]["value"] == "IEC61400-16-1"

    assert "term" not in metadata[2]
    assert metadata[2]["term_name"] == "source"
    assert metadata[2]["value"] == "Doc 12345 - Rev 01"


def test_convert_dcmi_term_to_term_name_no_op_when_already_converted(generic_120_3_alpha_3):
    """Should not modify documents that already use term_name"""
    # Convert to new format first
    generic_120_3_alpha_3["document"]["metadata"] = [
        {"term_name": "identifier", "value": "test-id"},
        {"term_name": "format", "value": "IEC61400-16-1"},
    ]

    metadata_before = copy.deepcopy(generic_120_3_alpha_3["document"]["metadata"])
    transformed = _convert_dcmi_term_to_term_name(generic_120_3_alpha_3)
    metadata_after = transformed["document"]["metadata"]

    # Should be unchanged
    assert metadata_after == metadata_before


def test_convert_dcmi_term_to_term_name_handles_missing_document(generic_120_3_alpha_3):
    """Should handle documents without a document section gracefully"""
    del generic_120_3_alpha_3["document"]

    # Should not raise an error
    transformed = _convert_dcmi_term_to_term_name(generic_120_3_alpha_3)
    assert "document" not in transformed


def test_convert_dcmi_term_to_term_name_handles_missing_metadata(generic_120_3_alpha_3):
    """Should handle documents without metadata section gracefully"""
    del generic_120_3_alpha_3["document"]["metadata"]

    # Should not raise an error
    transformed = _convert_dcmi_term_to_term_name(generic_120_3_alpha_3)
    assert "metadata" not in transformed["document"]
