"""Parsers for jinja templates."""

import os
import pathlib
from typing import Optional

from jinja2 import Environment, FileSystemLoader

from use_case_registry.errors import EnvVarMissingError


def env_var(var: str, default: Optional[str] = None) -> str:
    """
    Return the environment variable named `var`.

    If there is no such environment variable set, return the `default` value.

    If the `default` value is `None`, raise an exception
    """
    if var in os.environ:
        return os.environ[var]

    if default:
        return default
    raise EnvVarMissingError(env_var=var)


class TemplateParser:
    """Interface for template parsers."""

    def __init__(self, path_to_folder: pathlib.Path) -> None:
        """Template parser."""
        if not (path_to_folder.exists() or path_to_folder.is_dir()):
            err_msg = f"{path_to_folder} must be a directory and exists."
            raise RuntimeError(err_msg)
        self.env = Environment(
            loader=FileSystemLoader(
                searchpath=path_to_folder,
                encoding="utf-8",
                followlinks=False,
            ),
            autoescape=True,
        )

    def parse(self, template: str) -> str:
        """Parse a template file."""
        jinja_template = self.env.get_template(
            name=template,
            globals={
                "env_var": env_var,
            },
        )
        return jinja_template.render()
