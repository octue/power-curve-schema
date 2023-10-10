# Turn off pylint warnings unavoidable with pytest
# pylint: disable=redefined-outer-name, line-too-long, redefined-builtin, missing-module-docstring

from jsonschema import validate


def test_generic_117_3(schema, generic_117_3):
    """Validation should pass on the entire example document"""
    validate(instance=generic_117_3, schema=schema)


def test_generic_274_20(schema, generic_274_20):
    """Validation should pass on the entire example document"""
    validate(instance=generic_274_20, schema=schema)
