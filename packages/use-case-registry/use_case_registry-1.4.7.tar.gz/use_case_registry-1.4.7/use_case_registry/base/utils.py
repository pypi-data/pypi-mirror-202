"""Utilities for base process."""

from typing import Any

import fastjsonschema
from fastjsonschema import JsonSchemaDefinitionException, JsonSchemaValueException
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
        validator = fastjsonschema.compile(definition=schema)
        validator(inputs)
    except JsonSchemaDefinitionException:
        return Err(CommandInputValidationError(msg="Invalid schema."))
    except JsonSchemaValueException as e:
        return Err(CommandInputValidationError(msg=e.message))
    return Ok()
