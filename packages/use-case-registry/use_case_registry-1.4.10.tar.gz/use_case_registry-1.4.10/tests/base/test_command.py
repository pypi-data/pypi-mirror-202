"""Tests for command."""
from dataclasses import dataclass
from typing import Any

from result import Ok, Result

from use_case_registry import UseCaseRegistry
from use_case_registry.base.command import BaseCommand, ICommandInput
from use_case_registry.errors import UseCaseExecutionError


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


class ExampleCommand(BaseCommand):
    """Example command."""

    def execute(
        self,
        write_ops_registry: UseCaseRegistry[Any],
    ) -> Result[Any, UseCaseExecutionError]:
        """Null command executuion."""
        _ = write_ops_registry

        return Ok()
