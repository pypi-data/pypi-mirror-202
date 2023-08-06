"""Test target-based parser."""
import dataclasses
import os
import pathlib
from typing import Any
from unittest import mock

import pytest
from jsonschema.exceptions import ValidationError

from use_case_registry.base import ICommandInput
from use_case_registry.errors import EnvVarMissingError
from use_case_registry.pasers.target_based import TargetBasedConfigParser


@dataclasses.dataclass(frozen=True, repr=False, eq=False)
class _ValidationInput(ICommandInput):
    name: str
    last_name: str


class TestTargetBasedConfigParser:  # noqa: D101
    @mock.patch.dict(
        os.environ,
        {
            "EXECUTION_ENV_MOCKED": "mock",
        },
        clear=True,
    )
    @pytest.mark.parametrize(
        argnames=["template", "expected_result"],
        argvalues=[
            (
                "config-1.yml",
                {
                    "name": "t",
                    "last_name": "p",
                },
            ),
            (
                "config-4.yml",
                {
                    "name": "t",
                    "last_name": "p",
                },
            ),
        ],
    )
    def test_parse_works(self, template: str, expected_result: dict[str, Any]) -> None:
        """Test parse works as expected."""
        folder = pathlib.Path().cwd().joinpath("tests/assets/templates/target-based/")
        parser = TargetBasedConfigParser(path_to_folder=folder)
        result = parser.parse(template=template, expected_schema=_ValidationInput)
        assert result == expected_result

    @pytest.mark.parametrize(
        argnames="template",
        argvalues=[
            "config-2.yml",
        ],
    )
    def test_parse_fails_validation(self, template: str) -> None:
        """Test parse works as expected."""
        folder = pathlib.Path().cwd().joinpath("tests/assets/templates/target-based/")
        parser = TargetBasedConfigParser(path_to_folder=folder)
        with pytest.raises(ValidationError):
            parser.parse(template=template, expected_schema=_ValidationInput)

    @pytest.mark.parametrize(
        argnames="template",
        argvalues=[
            "config-3.yml",
        ],
    )
    def test_parse_fails_missing_env_var(self, template: str) -> None:
        """Test parse works as expected."""
        folder = pathlib.Path().cwd().joinpath("tests/assets/templates/target-based/")
        parser = TargetBasedConfigParser(path_to_folder=folder)
        with pytest.raises(EnvVarMissingError):
            parser.parse(template=template, expected_schema=_ValidationInput)
