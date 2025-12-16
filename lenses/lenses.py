"""
Lenses.py

A collection of conversion functions to convert documents between released schema versions
"""


def _add_power_reference_location(doc, value="low-voltage"):
    """Adds a new power_reference_location property using a given value (or by default
    the committee's suggested default 'low-voltage')
    """

    if doc["turbine"].get("power_reference_location", None) is not None:
        raise ValueError("Input doc cannot have a turbine.power_reference_location value, it will be overwritten")

    doc["turbine"]["power_reference_location"] = value

    return doc


def _change_shear_coefficient_to_vertical_shear_exponent(doc):
    """Unify the shear-coefficient parameter to call it vertical-shear-exponent consistent with usage elsewhere"""

    for mode in doc["power_curves"]["operating_modes"]:
        for parameter in mode["parameters"]:
            if parameter["label"] == "shear-coefficient":
                parameter["label"] = "vertical-shear-exponent"

    return doc


def _move_available_hub_heights_to_restricted(doc):
    """Move overrides.available_hub_heights to mode-level restricted_to_hub_heights"""

    for mode in doc["power_curves"]["operating_modes"]:
        overrides = mode.get("overrides", {})
        if "available_hub_heights" in overrides:
            mode["restricted_to_hub_heights"] = overrides.pop("available_hub_heights")

    return doc


def alpha_3_to_alpha_4(doc):
    """Convert documents compliant with alpha-3 to documents compliant with alpha-4"""

    lenses = [
        _add_power_reference_location,
        _change_shear_coefficient_to_vertical_shear_exponent,
        _move_available_hub_heights_to_restricted,
    ]
    for lens in lenses:
        doc = lens(doc)
    return doc
