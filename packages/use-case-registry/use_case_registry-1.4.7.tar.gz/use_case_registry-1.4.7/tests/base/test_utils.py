"""Test utilities."""

from use_case_registry.base import utils
from use_case_registry.errors import CommandInputValidationError


def test_validate_inputs_invalid_schema() -> None:
    """Test invalid schema."""
    schema = {
        "type": "object",
        "properties": {
            "name": {
                "type": "string",
                "maxLength": 9,
            },
            "last_name": {
                "type": "any",
            },
            "age": {
                "type": "integer",
                "minimum": 1,
            },
        },
        "sdsrequired": [
            "name",
            "last_name",
        ],
    }
    validation_err = utils.validate_inputs(schema=schema, inputs={}).err()
    assert isinstance(validation_err, CommandInputValidationError)
