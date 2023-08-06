"""Target based configuration parser."""
import pathlib
from typing import Any

import jinja2
import jsonschema
import yaml
from mashumaro.jsonschema import DRAFT_2020_12, JSONSchemaBuilder

from use_case_registry.base.command import ICommandInput
from use_case_registry.pasers.macros import env_var


class TargetBasedConfigParser:
    """Target based config parser."""

    def __init__(
        self,
        path_to_folder: pathlib.Path,
    ) -> None:
        """Target based configuration file parser."""
        self.path_to_folder = path_to_folder

    def parse(
        self,
        template: str,
        expected_schema: type[ICommandInput],
    ) -> dict[str, Any]:
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
        input_schema = (
            JSONSchemaBuilder(dialect=DRAFT_2020_12, all_refs=False)
            .build(
                instance_type=expected_schema,
            )
            .to_dict()
        )
        try:
            jsonschema.validate(
                instance=configuration["options"][target_selected],
                schema=input_schema,
            )
        except Exception as e:
            raise e from None

        return configuration["options"][target_selected]
