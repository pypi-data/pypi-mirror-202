"""Custom defined errors."""

import pathlib
from typing import TYPE_CHECKING, Any, Union

from use_case_registry import UseCaseRegistry

if TYPE_CHECKING:
    from pydantic.error_wrappers import ErrorDict


class CommandInputValidationError(Exception):
    """Raised when command input values does pass validation check."""

    def __init__(self, msg: Union[str, list["ErrorDict"]]) -> None:
        """Construct class."""
        super().__init__(msg)


class UseCaseExecutionError(Exception):
    """Raised when there's an error executing a workflow."""

    def __init__(self, error: Exception) -> None:
        """Construct class."""
        super().__init__(f"Error executing a use case {error}")


class CommitTransactionsError(Exception):
    """Raised when there's an error committing a set of transactions."""

    def __init__(self, transactions: UseCaseRegistry[Any]) -> None:
        """Construct class."""
        super().__init__(f"Error commiting transactions {transactions}")


class EnvVarMissingError(Exception):
    """Raised when a required enviroment variable is not set."""

    def __init__(self, env_var: str) -> None:
        """Construct class."""
        super().__init__(f"Env var required but not provided {env_var}")


class SchemaNotFoundError(Exception):
    """Raised when schema not found."""

    def __init__(self, path: pathlib.Path) -> None:
        """Construct class."""
        super().__init__(f"Schema not found {path}")
