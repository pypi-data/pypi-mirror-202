"""Raw template parser."""


import pathlib
from typing import Any

import yaml

from use_case_registry.pasers import macros
from use_case_registry.pasers.base import BaseParser


class RawParser(BaseParser):
    """Raw template parser."""

    def __init__(self, path_to_folder: pathlib.Path) -> None:
        """Raw parser does not contain any logic."""
        super().__init__(path_to_folder)

    def parse(self, template: str) -> dict[str, Any]:
        """Parse a template file."""
        jinja_template = self.env.get_template(
            name=template,
            globals={
                "env_var": macros.env_var,
            },
        )
        return yaml.safe_load(stream=jinja_template.render())
