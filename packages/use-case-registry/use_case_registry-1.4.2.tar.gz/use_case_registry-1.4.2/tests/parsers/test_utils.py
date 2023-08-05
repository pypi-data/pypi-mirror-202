"""Test parsers utils."""
import os
import pathlib
from unittest import mock

import pytest
import yaml

from use_case_registry.errors import ConfigFileError
from use_case_registry.parsers import utils


@mock.patch.dict(
    os.environ,
    {
        "NAME": "name",
        "LAST_NAME": "last-name",
    },
)
@pytest.mark.parametrize(
    argnames=[
        "tag",
        "yaml_to_read",
    ],
    argvalues=[
        (
            "!ENV",
            "yaml-1.yml",
        ),
    ],
)
def test_env_construct_tag(tag: str, yaml_to_read: str) -> None:
    """Test env construct tag works."""
    yml_path = pathlib.Path().cwd().joinpath(f"tests/assets/env_yamls/{yaml_to_read}")
    yaml.Loader.add_constructor(tag=tag, constructor=utils.env_tag_constructor)
    yaml.load(
        stream=yml_path.read_text(),
        Loader=yaml.Loader,  # noqa: S506
    )
    assert {
        "name": "name",
        "last-name": "last-name",
    }


@mock.patch.dict(os.environ, {"LAST_NAME": "last-name"})
@pytest.mark.parametrize(
    argnames=[
        "tag",
        "yaml_to_read",
    ],
    argvalues=[
        ("!ENV", "yaml-1.yml"),
    ],
)
def test_env_construct_tag_fails(
    tag: str,
    yaml_to_read: str,
) -> None:
    """Test env construct tag works."""
    os.environ["LAST_NAME"] = "LAST_NAME"
    yml_path = pathlib.Path().cwd().joinpath(f"tests/assets/env_yamls/{yaml_to_read}")
    yaml.Loader.add_constructor(tag=tag, constructor=utils.env_tag_constructor)
    with pytest.raises(ConfigFileError):
        yaml.load(
            stream=yml_path.read_text(),
            Loader=yaml.Loader,  # noqa: S506
        )
