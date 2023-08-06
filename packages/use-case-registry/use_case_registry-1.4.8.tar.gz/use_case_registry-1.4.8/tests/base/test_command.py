"""Tests for command."""
from dataclasses import dataclass
from typing import Any

import pytest
from result import Ok, Result

from use_case_registry import UseCaseRegistry
from use_case_registry.base.command import BaseCommand, ICommandInput
from use_case_registry.base.utils import validate_inputs
from use_case_registry.errors import CommandInputValidationError, UseCaseExecutionError


@dataclass(
    frozen=True,
    repr=False,
    eq=False,
)
class ExampleCommandInput(ICommandInput):
    """Example command input."""

    name: str
    last_name: str
    age: int


SCHEMA = {
    "type": "object",
    "properties": {
        "name": {
            "type": "string",
            "maxLength": 9,
        },
        "last_name": {
            "type": "string",
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


class ExampleCommand(BaseCommand):
    """Example command."""

    def execute(
        self,
        write_ops_registry: UseCaseRegistry[Any],
    ) -> Result[Any, UseCaseExecutionError]:
        """Null command executuion."""
        _ = write_ops_registry

        return Ok()


def test_validate_command_pass() -> None:
    """Test validate command passes."""
    inputs = ExampleCommandInput(name="tomas", last_name="perez", age=10)
    validate_inputs(inputs=inputs.to_dict(), schema=SCHEMA).unwrap()


@pytest.mark.parametrize(
    argnames="inputs",
    argvalues=[
        ExampleCommandInput(
            name="tomas" * 5,
            last_name="perez",
            age=-10,
        ),
        ExampleCommandInput(
            name="a" * 11,
            last_name="perez",
            age=10,
        ),
    ],
)
def test_validate_command_fails(inputs: ICommandInput) -> None:
    """Test validate command fails."""
    validation_err = validate_inputs(inputs=inputs.to_dict(), schema=SCHEMA).err()

    assert isinstance(validation_err, CommandInputValidationError)
