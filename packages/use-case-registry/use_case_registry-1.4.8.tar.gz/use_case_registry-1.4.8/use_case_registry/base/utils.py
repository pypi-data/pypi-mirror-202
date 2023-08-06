"""Utilities for base process."""

from typing import Any

import jsonschema
from jsonschema.exceptions import SchemaError, ValidationError
from result import Err, Ok, Result

from use_case_registry.errors import CommandInputValidationError


def validate_inputs(
    schema: dict[str, Any],
    inputs: dict[str, Any],
) -> Result[None, CommandInputValidationError]:
    """Validate inputs."""
    draft = "$draft"
    try:
        if draft in schema:
            schema.pop(draft)

        schema[draft] = "draft-07"

        jsonschema.validate(instance=inputs, schema=schema)

    except ValidationError as e:
        return Err(CommandInputValidationError(msg=e.message))
    except SchemaError as e:
        return Err(CommandInputValidationError(msg=e.message))

    return Ok()
