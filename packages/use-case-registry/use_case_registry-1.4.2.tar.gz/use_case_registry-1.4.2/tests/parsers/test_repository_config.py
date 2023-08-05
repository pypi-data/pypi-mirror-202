"""Test repository config parser."""
import pathlib

import pytest
from sqlalchemy import create_engine

from use_case_registry.errors import ConfigFileError
from use_case_registry.parsers.repository_config import RepoConfigParser, RepoEngines


class TestRepoConfigParser:
    """Test Repository Config Parser."""

    @pytest.mark.parametrize(
        argnames="file_name",
        argvalues=[
            "conf-1.yml",
        ],
    )
    def test_parse_works(
        self,
        file_name: str,
        # expected_output: dict[str, Any],
    ) -> None:
        """Test parse."""
        config_path = (
            pathlib.Path().cwd().joinpath(f"tests/assets/repo_configs/{file_name}")
        )
        parser = RepoConfigParser()
        result = parser.parse(config_path)

        if result["engine"] is RepoEngines.SQLALCHEMY:
            engine = create_engine(url=result["url"])
            assert engine
        else:
            raise AssertionError

    @pytest.mark.parametrize(
        argnames="file_name",
        argvalues=[
            "non-existing.yml",
            "conf-2.yml",
            "conf-3.yml",
            "conf-4.yml",
            "conf-5.yml",
            "conf-6.yml",
            "conf-7.yml",
            "conf-8.yml",
        ],
    )
    def test_parse_fails(
        self,
        file_name: str,
        # expected_output: dict[str, Any],
    ) -> None:
        """Test parse."""
        config_path = (
            pathlib.Path().cwd().joinpath(f"tests/assets/repo_configs/{file_name}")
        )
        parser = RepoConfigParser()
        with pytest.raises(ConfigFileError):
            parser.parse(config_path)
