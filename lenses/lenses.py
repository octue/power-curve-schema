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


def _convert_hub_height_overrides_to_allowed_modes(doc):
    """Convert mode-level available_hub_heights overrides to the new format with allowed_modes.

    Old format:
        turbine.available_hub_heights = [140, 145, 150]
        power_curves.operating_modes[2].overrides.available_hub_heights = [140, 150]

    New format:
        turbine.available_hub_heights = [
            {"values": [140, 145, 150], "allowed_modes": ["mode_1", "mode_2"]},
            {"values": [140, 150], "allowed_modes": ["mode_3"]}
        ]
    """
    turbine_hub_heights = doc["turbine"].get("available_hub_heights")
    if turbine_hub_heights is None:
        # TODO should still check for presence of overrides
        return doc

    modes = doc["power_curves"]["operating_modes"]

    # Collect mode overrides
    modes_with_overrides = {}  # hub_heights_key -> [mode_labels]
    modes_without_overrides = []

    for mode in modes:
        mode_label = mode["label"]
        overrides = mode.get("overrides", {})
        mode_hub_heights = overrides.get("available_hub_heights", None)

        if mode_hub_heights is not None:
            # Convert to a hashable key for grouping
            key = _hub_heights_to_key(mode_hub_heights)
            if key not in modes_with_overrides:
                modes_with_overrides[key] = {"hub_heights": mode_hub_heights, "modes": []}
            modes_with_overrides[key]["modes"].append(mode_label)

            # Remove the override from the mode
            del overrides["available_hub_heights"]
        else:
            modes_without_overrides.append(mode_label)

    # If no modes have overrides, leave the turbine-level hub heights as-is (simple format)
    if not modes_with_overrides:
        return doc

    # Build the new hub heights array
    new_hub_heights = []

    # Add entry for modes without overrides (using turbine-level value)
    if modes_without_overrides:
        new_hub_heights.append(_create_hub_height_entry(turbine_hub_heights, modes_without_overrides))

    # Add entries for modes with overrides
    for override_data in modes_with_overrides.values():
        new_hub_heights.append(_create_hub_height_entry(override_data["hub_heights"], override_data["modes"]))

    doc["turbine"]["available_hub_heights"] = new_hub_heights

    return doc


def _hub_heights_to_key(hub_heights):
    """Convert hub heights to a hashable key for grouping identical values."""
    if isinstance(hub_heights, list):
        return ("list", tuple(hub_heights))
    elif isinstance(hub_heights, dict):
        if "values" in hub_heights:
            return ("values", tuple(hub_heights["values"]))
        else:
            return ("range", hub_heights.get("min"), hub_heights.get("max"))
    return None


def _create_hub_height_entry(hub_heights, allowed_modes):
    """Create a hub height entry with allowed_modes.

    Handles both simple formats (array of numbers, min/max object) and
    converts them to the structured format with allowed_modes.
    """
    if isinstance(hub_heights, list):
        # Simple array of numbers -> values format
        return {"values": hub_heights, "allowed_modes": allowed_modes}
    elif isinstance(hub_heights, dict):
        if "values" in hub_heights:
            # Already in values format
            return {"values": hub_heights["values"], "allowed_modes": allowed_modes}
        else:
            # Min/max format
            entry = {"allowed_modes": allowed_modes}
            if "min" in hub_heights:
                entry["min"] = hub_heights["min"]
            if "max" in hub_heights:
                entry["max"] = hub_heights["max"]
            return entry
    return None


def alpha_3_to_alpha_4(doc):
    """Convert documents compliant with alpha-3 to documents compliant with alpha-4"""

    lenses = [_add_power_reference_location, _change_shear_coefficient_to_vertical_shear_exponent]
    for lens in lenses:
        doc = lens(doc)
    return doc


def alpha_4_to_alpha_5(doc):
    """Convert documents compliant with alpha-4 to documents compliant with alpha-5"""

    lenses = [_convert_hub_height_overrides_to_allowed_modes]
    for lens in lenses:
        doc = lens(doc)
    return doc
