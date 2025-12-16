# Turn off pylint warnings unavoidable with pytest
# pylint: disable=redefined-outer-name, line-too-long, redefined-builtin, missing-module-docstring

import copy
import json
import os

import pytest

from lenses.lenses import _add_power_reference_location

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
