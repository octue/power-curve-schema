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


def alpha_3_to_alpha_4(doc):
    """Convert documents compliant with alpha-3 to documents compliant with alpha-4"""

    lenses = [_add_power_reference_location]
    for lens in lenses:
        doc = lens(doc)
    return doc
