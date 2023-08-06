"""Utilities for base process."""

from typing import Any

from pydantic import BaseModel, ValidationError
from result import Err, Ok, Result

from use_case_registry.errors import CommandInputValidationError


def validate_inputs(
    schema: type[BaseModel],
    inputs: dict[str, Any],
) -> Result[None, CommandInputValidationError]:
    """Validate inputs."""
    try:
        schema(**inputs)

    except ValidationError as e:
        return Err(CommandInputValidationError(msg=e.errors()))

    return Ok()
