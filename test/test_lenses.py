# Turn off pylint warnings unavoidable with pytest
# pylint: disable=redefined-outer-name, line-too-long, redefined-builtin, missing-module-docstring

import copy
import json
import os

import pytest

from lenses.lenses import (
    _add_power_reference_location,
    _change_shear_coefficient_to_vertical_shear_exponent,
    _convert_hub_height_overrides_to_allowed_modes,
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
        os.path.join(ROOT_DIR, "test", "fixtures", "generic-274-20-alpha-3.json"), "r", encoding="utf-8"
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


def test_convert_hub_height_overrides_with_mode_override(generic_274_20_alpha_3):
    """Should convert mode-level available_hub_heights overrides to the new format with allowed_modes"""
    # generic-274-20 has:
    # - turbine.available_hub_heights = [140, 145, 150]
    # - mode_1: no override
    # - mode_2: no override
    # - mode_3: overrides.available_hub_heights = [140, 150]

    transformed = _convert_hub_height_overrides_to_allowed_modes(generic_274_20_alpha_3)

    # Should have converted to array format with allowed_modes
    hub_heights = transformed["turbine"]["available_hub_heights"]
    assert isinstance(hub_heights, list)
    assert len(hub_heights) == 2

    # Find entries by their allowed_modes
    modes_to_entry = {tuple(sorted(e["allowed_modes"])): e for e in hub_heights}

    # Modes without overrides should use turbine-level values
    default_entry = modes_to_entry[("mode_1", "mode_2")]
    assert default_entry["values"] == [140, 145, 150]

    # Mode with override should use its override values
    override_entry = modes_to_entry[("mode_3",)]
    assert override_entry["values"] == [140, 150]

    # Override should be removed from mode_3
    mode_3 = next(m for m in transformed["power_curves"]["operating_modes"] if m["label"] == "mode_3")
    assert "available_hub_heights" not in mode_3.get("overrides", {})


def test_convert_hub_height_overrides_no_overrides(generic_120_3_alpha_3):
    """Should leave hub heights as-is when no modes have overrides"""
    # generic-120-3 has no mode overrides for available_hub_heights
    original_hub_heights = generic_120_3_alpha_3["turbine"]["available_hub_heights"]

    transformed = _convert_hub_height_overrides_to_allowed_modes(generic_120_3_alpha_3)

    # Should remain unchanged (simple format)
    assert transformed["turbine"]["available_hub_heights"] == original_hub_heights


def test_convert_hub_height_overrides_no_turbine_hub_heights(generic_120_3_alpha_3):
    """Should handle case where turbine has no available_hub_heights defined"""
    del generic_120_3_alpha_3["turbine"]["available_hub_heights"]

    transformed = _convert_hub_height_overrides_to_allowed_modes(generic_120_3_alpha_3)

    # Should not add available_hub_heights
    assert "available_hub_heights" not in transformed["turbine"]


def test_convert_hub_height_overrides_with_range_format(generic_274_20_alpha_3):
    """Should handle min/max range format for hub heights"""
    # Set up turbine with range format
    generic_274_20_alpha_3["turbine"]["available_hub_heights"] = {"min": 80, "max": 160}

    # Update mode_3's override to use range format
    mode_3 = next(m for m in generic_274_20_alpha_3["power_curves"]["operating_modes"] if m["label"] == "mode_3")
    mode_3["overrides"]["available_hub_heights"] = {"min": 100, "max": 140}

    transformed = _convert_hub_height_overrides_to_allowed_modes(generic_274_20_alpha_3)

    hub_heights = transformed["turbine"]["available_hub_heights"]
    assert isinstance(hub_heights, list)
    assert len(hub_heights) == 2

    # Find the override entry for mode_3 (should have min/max format)
    override_entry = next(e for e in hub_heights if "mode_3" in e["allowed_modes"])
    assert override_entry["min"] == 100
    assert override_entry["max"] == 140
    assert "values" not in override_entry

    # Find the default entry for mode_1 and mode_2 (should also have min/max format from turbine level)
    default_entry = next(e for e in hub_heights if "mode_1" in e["allowed_modes"])
    assert default_entry["min"] == 80
    assert default_entry["max"] == 160
    assert "values" not in default_entry


def test_convert_hub_height_overrides_multiple_modes_same_override(generic_274_20_alpha_3):
    """Should group modes with identical overrides"""
    # Give mode_1 and mode_2 the same override
    modes = generic_274_20_alpha_3["power_curves"]["operating_modes"]
    modes[0]["overrides"] = {"available_hub_heights": [145, 150]}
    modes[1]["overrides"] = {"available_hub_heights": [145, 150]}
    # mode_3 already has [140, 150]

    transformed = _convert_hub_height_overrides_to_allowed_modes(generic_274_20_alpha_3)

    hub_heights = transformed["turbine"]["available_hub_heights"]

    # Should have 2 entries: one for mode_1+mode_2 (same override), one for mode_3
    assert len(hub_heights) == 2

    # Find the entry with mode_1 and mode_2
    grouped_entry = next(e for e in hub_heights if "mode_1" in e["allowed_modes"])
    assert sorted(grouped_entry["allowed_modes"]) == ["mode_1", "mode_2"]
    assert grouped_entry["values"] == [145, 150]
