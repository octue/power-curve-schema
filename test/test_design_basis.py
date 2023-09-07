from jsonschema import validate
from jsonschema.exceptions import ValidationError
import pytest
from .helpers import get_subschema


@pytest.fixture
def subschema(schema):
    """Provide a schema that requires only the turbine_metadata part of the whole schema"""
    return get_subschema(schema, "design_basis")


def test_generic_turbine_metadata(subschema, generic_design_basis):
    """Validation should pass on the generic turbine metadata"""
    validate(instance=generic_design_basis, schema=subschema)


def test_missing_design_basis(subschema):
    """Validation should fail if there is no turbine metadata section"""
    with pytest.raises(ValidationError) as e:
        validate(instance={}, schema=subschema)
    assert "'design_basis' is a required property" in str(e)
 