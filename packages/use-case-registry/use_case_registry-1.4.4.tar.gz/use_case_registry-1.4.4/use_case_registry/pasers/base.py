"""Interface for parsers."""

import abc
import pathlib
from typing import Any

from jinja2 import Environment, FileSystemLoader


class BaseParser(abc.ABC):
    """Interface for template parsers."""

    def __init__(self, path_to_folder: pathlib.Path) -> None:
        """Template parser is a raw jinja template parser. No logic."""
        if not (path_to_folder.exists() or path_to_folder.is_dir()):
            err_msg = f"{path_to_folder} must be a directory and exists."
            raise RuntimeError(err_msg)
        self.path_to_folder = path_to_folder
        self.env = Environment(
            loader=FileSystemLoader(
                searchpath=path_to_folder,
                encoding="utf-8",
                followlinks=False,
            ),
            autoescape=True,
        )

    @abc.abstractmethod
    def parse(self, template: str) -> dict[str, Any]:
        """Parse a tempalte file."""
