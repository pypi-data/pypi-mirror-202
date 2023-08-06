"""Test raw parser."""

import os
import pathlib
from typing import Any
from unittest import mock

import pytest

from use_case_registry.errors import EnvVarMissingError
from use_case_registry.pasers.raw import RawParser


class TestRawParser:
    """Test template parser."""

    @mock.patch.dict(
        os.environ,
        {
            "NAME": "name",
        },
        clear=True,
    )
    @pytest.mark.parametrize(
        argnames=[
            "template_name",
            "expected_result",
        ],
        argvalues=[
            (
                "config-2.yml",
                {
                    "version": 1,
                    "name": "tomas",
                    "last_name": "perez",
                },
            ),
            (
                "config-3.yml",
                {
                    "version": 1,
                    "name": "name",
                    "last_name": "perez",
                },
            ),
        ],
    )
    def test_parse_works(
        self,
        template_name: str,
        expected_result: dict[str, Any],
    ) -> None:
        """Test parse() works as expected."""
        template_folder = (
            pathlib.Path()
            .cwd()
            .joinpath(
                "tests/assets/templates/raw",
            )
        )
        parser = RawParser(path_to_folder=template_folder)
        result = parser.parse(template_name)
        assert result == expected_result

    @pytest.mark.parametrize(
        argnames="template_name",
        argvalues=[
            "config-1.yml",
        ],
    )
    def test_parse_fails_env_variable_not_set(
        self,
        template_name: str,
    ) -> None:
        """Test parse() fails when env variable is not setted."""
        template_folder = (
            pathlib.Path()
            .cwd()
            .joinpath(
                "tests/assets/templates/raw",
            )
        )
        parser = RawParser(path_to_folder=template_folder)
        with pytest.raises(EnvVarMissingError):
            parser.parse(template_name)
