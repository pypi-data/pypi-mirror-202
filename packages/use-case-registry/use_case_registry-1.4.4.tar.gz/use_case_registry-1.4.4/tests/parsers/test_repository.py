"""Test repository parser."""
import os
import pathlib
from typing import Any
from unittest import mock

import pytest

from use_case_registry.pasers.repository import RepoConfigParser


class TestRepoConfigParser:
    """Test repo config parser."""

    @mock.patch.dict(
        os.environ,
        {
            "EXECUTION_ENV": "dev",
            "DB_PASSWORD": "abc",
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
                "config-1.yml",
                {
                    "url": "sqlite:///dev-database.db",
                },
            ),
            (
                "config-2.yml",
                {
                    "url": "sqlite:///dev-database.db",
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
                "tests/assets/templates/repository",
            )
        )
        parser = RepoConfigParser(path_to_folder=template_folder)
        result = parser.parse(template=template_name)
        assert result == expected_result

    @mock.patch.dict(
        os.environ,
        {
            "EXECUTION_ENV": "dev",
            "DB_PASSWORD": "abc",
        },
        clear=True,
    )
    @pytest.mark.parametrize(
        argnames="template_name",
        argvalues=[
            "config-no-url.yml",
            "config-no-drivername.yml",
            "config-no-connection.yml",
        ],
    )
    def test_parse_fails(
        self,
        template_name: str,
    ) -> None:
        """Test parse() works as expected."""
        template_folder = (
            pathlib.Path()
            .cwd()
            .joinpath(
                "tests/assets/templates/repository",
            )
        )
        parser = RepoConfigParser(path_to_folder=template_folder)
        with pytest.raises(RuntimeError):
            parser.parse(template=template_name)
