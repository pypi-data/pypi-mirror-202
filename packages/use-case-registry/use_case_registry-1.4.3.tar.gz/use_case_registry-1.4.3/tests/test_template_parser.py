"""Test template parser."""
import os
import pathlib
from typing import Any
from unittest import mock

import pytest
import yaml

from use_case_registry.errors import EnvVarMissingError
from use_case_registry.template_parsers import TemplateParser


class TestTemplateParser:
    """Test template parser."""

    @pytest.mark.parametrize(
        argnames="template_folder",
        argvalues=[
            pathlib.Path()
            .cwd()
            .joinpath(
                "tests/assets/not-existing",
            ),
        ],
    )
    def test_constructor_fails(self, template_folder: pathlib.Path) -> None:
        """Test constructor fails."""
        with pytest.raises(RuntimeError):
            TemplateParser(path_to_folder=template_folder)

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
        template_folder = pathlib.Path().cwd().joinpath("tests/assets/templates")
        parser = TemplateParser(path_to_folder=template_folder)
        result = parser.parse(template_name)
        assert yaml.safe_load(result) == expected_result

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
        template_folder = pathlib.Path().cwd().joinpath("tests/assets/templates")
        parser = TemplateParser(path_to_folder=template_folder)
        with pytest.raises(EnvVarMissingError):
            parser.parse(template_name)
