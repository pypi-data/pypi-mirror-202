"""Test base parser abstract class."""

import pathlib

import pytest

from use_case_registry.pasers.raw import RawParser


class TestBaseParser:
    """Test BaseParser."""

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
            RawParser(path_to_folder=template_folder)
