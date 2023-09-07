from jsonschema import validate
from .helpers import get_subschema
from .conftest import ROOT_DIR
import os
import json


def test_generic_117_3(schema, generic_117_3):
    """Validation should fail if there is no turbine metadata section"""
    validate(instance=generic_117_3, schema=schema)


def test_generic_274_20(schema, generic_274_20):
    """Validation should fail if there is no turbine metadata section"""
    validate(instance=generic_274_20, schema=schema)

