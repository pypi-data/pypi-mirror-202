"""Test target-based parser."""
import os
import pathlib
from typing import Any
from unittest import mock

import pytest

from use_case_registry.base.schema_validator import SchemaValidator
from use_case_registry.errors import CommandInputValidationError, EnvVarMissingError
from use_case_registry.pasers.target_based import TargetBasedConfigParser


class _Schema(SchemaValidator):
    name: str
    last_name: str


class _OtherSchema(SchemaValidator):
    other: str


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
        result = parser.parse(template=template, schema=_Schema)
        assert result == expected_result

    @pytest.mark.parametrize(
        argnames=["template", "schema"],
        argvalues=[
            (
                "config-2.yml",
                _Schema,
            ),
            (
                "config-5.yml",
                _Schema,
            ),
            (
                "config-1.yml",
                _OtherSchema,
            ),
        ],
    )
    def test_parse_fails_validation(
        self,
        template: str,
        schema: type[SchemaValidator],
    ) -> None:
        """Test parse works as expected."""
        folder = pathlib.Path().cwd().joinpath("tests/assets/templates/target-based/")
        parser = TargetBasedConfigParser(path_to_folder=folder)
        with pytest.raises(CommandInputValidationError):
            parser.parse(template=template, schema=schema)

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
            parser.parse(template=template, schema=_Schema)
