# Turn off pylint warnings unavoidable with pytest
# pylint: disable=redefined-outer-name, line-too-long, redefined-builtin, missing-module-docstring

from jsonschema import validate
from jsonschema.exceptions import ValidationError
import pytest
from .helpers import get_subschema


@pytest.fixture
def subschema(schema):
    """Provide a schema that requires only the design_basis part of the whole schema"""
    return get_subschema(schema, "design_bases")


def test_generic_120_3_design_basis_1(subschema, generic_120_3):
    """Validation should pass on the generic turbine design basis"""
    validate(instance=generic_120_3, schema=subschema)


def test_missing_design_basis(subschema):
    """Validation should fail if there is no design basis section"""
    with pytest.raises(ValidationError) as e:
        validate(instance={}, schema=subschema)
    assert "'design_bases' is a required property" in str(e)
