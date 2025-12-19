# Turn off pylint warnings unavoidable with pytest
# pylint: disable=redefined-outer-name, line-too-long, redefined-builtin, missing-module-docstring

from jsonschema import validate


def test_generic_120_3_with_extra_parameters(schema, generic_120_3_with_extra_parameters):
    """Validation should pass on the entire example document"""
    validate(instance=generic_120_3_with_extra_parameters, schema=schema)


def test_generic_120_3(schema, generic_120_3):
    """Validation should pass on the entire example document"""
    validate(instance=generic_120_3, schema=schema)


def test_generic_274_20(schema, generic_274_20):
    """Validation should pass on the entire example document"""
    validate(instance=generic_274_20, schema=schema)
