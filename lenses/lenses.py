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


def _rename_dimension_to_axis(doc):
    """Rename 'dimension' property to 'axis' in all parameters"""

    for mode in doc["power_curves"]["operating_modes"]:
        for parameter in mode["parameters"]:
            if "dimension" in parameter:
                parameter["axis"] = parameter.pop("dimension")

    return doc


def _collapse_singleton_dimensions(doc):
    """Collapse singleton dimensions in power curves.

    If a parameter has a 'values' list with only one element, convert it to a
    non-axis 'value' parameter and remove the corresponding singleton dimension
    from power and thrust_coefficient arrays. Renumber the axes of remaining
    parameters accordingly.
    """

    for mode in doc["power_curves"]["operating_modes"]:
        parameters = mode["parameters"]

        # Find singleton dimensions (sorted by axis descending so we can remove from end first)
        singletons = []
        for param in parameters:
            if "axis" in param and "values" in param and len(param["values"]) == 1:
                singletons.append((param["axis"], param))

        # Sort by axis descending to remove from highest dimension first
        singletons.sort(key=lambda x: x[0], reverse=True)

        for singleton_axis, param in singletons:
            # Convert parameter to non-axis value format
            single_value = param["values"][0]
            del param["axis"]
            del param["values"]
            param["value"] = single_value

            # Remove singleton dimension from power array
            power = mode["power"]
            for _ in range(singleton_axis):
                power = power[0] if isinstance(power, list) and len(power) > 0 else power
            if isinstance(power, list) and len(power) == 1:
                # Navigate to and unwrap the singleton dimension
                mode["power"] = _remove_dimension(mode["power"], singleton_axis)

            # Remove singleton dimension from thrust_coefficient array
            thrust = mode["thrust_coefficient"]
            mode["thrust_coefficient"] = _remove_dimension(thrust, singleton_axis)

            # Renumber axes of remaining parameters
            for other_param in parameters:
                if "axis" in other_param and other_param["axis"] > singleton_axis:
                    other_param["axis"] -= 1

    return doc


def _remove_dimension(arr, dim):
    """Remove a singleton dimension from an n-dimensional array.

    Args:
        arr: The n-dimensional array (nested lists)
        dim: The dimension index to remove (0-based)

    Returns:
        The array with the singleton dimension removed
    """
    if dim == 0:
        # Remove outermost dimension
        if isinstance(arr, list) and len(arr) == 1:
            return arr[0]
        return arr
    else:
        # Recurse into the array
        if isinstance(arr, list):
            return [_remove_dimension(item, dim - 1) for item in arr]
        return arr


def _convert_dcmi_term_to_term_name(doc):
    """Convert document.metadata entries from 'term' (capitalized label) to 'term_name' (lowercase name).

    Old format: {"term": "Identifier", "value": "..."}
    New format: {"term_name": "identifier", "value": "..."}
    """

    if "document" not in doc or "metadata" not in doc["document"]:
        return doc

    for entry in doc["document"]["metadata"]:
        if "term" in entry:
            # Convert capitalized label to lowercase name
            term_value = entry.pop("term")
            entry["term_name"] = term_value.lower()

    return doc


def alpha_3_to_alpha_4(doc):
    """Convert documents compliant with alpha-3 to documents compliant with alpha-4"""

    lenses = [
        _add_power_reference_location,
        _change_shear_coefficient_to_vertical_shear_exponent,
        _move_available_hub_heights_to_restricted,
        _rename_dimension_to_axis,
        _collapse_singleton_dimensions,
        _convert_dcmi_term_to_term_name,
    ]
    for lens in lenses:
        doc = lens(doc)
    return doc
