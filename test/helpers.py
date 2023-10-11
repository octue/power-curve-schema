def get_subschema(schema, section):
    """Get a schema with only one of the top-level sections in it, allowing anything in other sections to pass unvalidated.
    This is useful for testing because it allows us to reuse fixtures more flexibly and focus on only modifying data under test.
    """

    schema["required"] = [section] if section in schema["required"] else []
    for key in [*schema["properties"].keys()]:
        if key not in [section]:
            schema["properties"].pop(key, None)

    return schema
