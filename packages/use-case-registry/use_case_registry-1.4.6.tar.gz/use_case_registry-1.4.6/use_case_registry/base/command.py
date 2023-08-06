"""Interface for concrete commands."""
import abc
from dataclasses import dataclass
from typing import Any

import jsonschema
from jsonschema.exceptions import ValidationError
from mashumaro.jsonschema import DRAFT_2020_12, JSONSchemaBuilder
from mashumaro.mixins.orjson import DataClassORJSONMixin
from result import Err, Ok, Result

from use_case_registry import UseCaseRegistry
from use_case_registry.errors import CommandInputValidationError, UseCaseExecutionError


@dataclass(
    frozen=True,
)
class ICommandInput(DataClassORJSONMixin):
    """ICommandInput."""


def validate_inputs(inputs: ICommandInput) -> Result[None, CommandInputValidationError]:
    """Validate inputs."""
    input_schema = (
        JSONSchemaBuilder(dialect=DRAFT_2020_12, all_refs=False)
        .build(
            instance_type=inputs.__class__,
        )
        .to_dict()
    )
    try:
        jsonschema.validate(instance=inputs.to_dict(), schema=input_schema)
    except ValidationError as e:
        return Err(CommandInputValidationError(msg=e.message))
    except ValueError as e:
        return Err(CommandInputValidationError(msg=e.args[0]))
    return Ok()


class BaseCommand(abc.ABC):
    """Command abstract class."""

    @abc.abstractmethod
    def execute(
        self,
        write_ops_registry: UseCaseRegistry[Any],
    ) -> Result[Any, UseCaseExecutionError]:
        """Workflow execution command to complete the use case."""
