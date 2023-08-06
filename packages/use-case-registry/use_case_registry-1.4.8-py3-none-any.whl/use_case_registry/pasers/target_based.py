"""Target based configuration parser."""
import pathlib
from typing import Any

import jinja2
import yaml
from result import Ok
from typing_extensions import assert_never

from use_case_registry.base.utils import validate_inputs
from use_case_registry.errors import CommandInputValidationError
from use_case_registry.pasers.macros import env_var


class TargetBasedConfigParser:
    """Target based config parser."""

    def __init__(
        self,
        path_to_folder: pathlib.Path,
    ) -> None:
        """Target based configuration file parser."""
        self.path_to_folder = path_to_folder

    def parse(self, template: str, schema: dict[str, Any]) -> dict[str, Any]:
        """Parse file and return especific target config."""
        jinja_env = jinja2.Environment(
            loader=jinja2.FileSystemLoader(
                searchpath=self.path_to_folder,
                followlinks=False,
                encoding="utf-8",
            ),
            autoescape=True,
        )
        rendered_template = jinja_env.get_template(
            name=template,
            globals={
                "env_var": env_var,
            },
        ).render()
        configuration = yaml.safe_load(stream=rendered_template)
        target_selected = configuration["target"]
        config = configuration["options"].get(target_selected)
        if not config:
            msg = f"No `option` for target {target_selected}"
            raise CommandInputValidationError(msg)

        validation_result = validate_inputs(schema=schema, inputs=config)
        if not isinstance(validation_result, Ok):
            validation_err = validation_result.err()
            if isinstance(validation_err, CommandInputValidationError):
                raise validation_err
            assert_never(validation_err)

        return config
