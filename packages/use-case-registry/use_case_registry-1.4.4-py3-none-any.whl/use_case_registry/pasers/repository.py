"""Repository config parser."""


import pathlib
from typing import Any

import yaml

from use_case_registry.enums import OptionEnums
from use_case_registry.pasers import macros
from use_case_registry.pasers.base import BaseParser


class NoRepoEngineSetError(Exception):
    """Raised when there's already a repo engine."""


class RepoEngineAlreadySetError(Exception):
    """Raised when there's already a repo engine."""


class RepoEngines(OptionEnums):
    """Repository engines."""

    SQLALCHEMY = "SQLALCHEMY"


class RepoConfigParser(BaseParser):
    """Repository config parser."""

    def __init__(self, path_to_folder: pathlib.Path) -> None:
        """Repository confi parser contains logic specific for this usecase."""
        super().__init__(path_to_folder)

    def _parse_sqlalchemy_connection(
        self,
        connection: dict[str, Any],
    ) -> dict[str, Any]:
        from sqlalchemy import URL

        connection_url = connection.get("url")
        if not connection_url:
            conn_eng = connection["engine"]
            msg = f"A `url` is required by the engine {conn_eng}"
            raise RuntimeError(msg)
        conn_url_drivername = connection_url.get("drivername")
        if not conn_url_drivername:
            msg = "A `drivername` is a required field."
            raise RuntimeError(msg)
        formmated_url = URL(
            drivername=conn_url_drivername,
            username=connection_url.get("username"),
            password=connection_url.get("password"),
            host=connection_url.get("host"),
            port=connection_url.get("port"),
            database=connection_url.get("database"),
            query=connection_url.get("query", ""),
        )
        return {
            "url": formmated_url.render_as_string(
                hide_password=True,
            ),
        }

    def parse(self, template: str) -> dict[str, Any]:
        """Parse a repository config file."""
        self.path_to_folder.joinpath(template)

        jinja_template = self.env.get_template(
            name=template,
            globals={
                "env_var": macros.env_var,
            },
        )
        config = yaml.safe_load(jinja_template.render())
        selected_connection: dict[str, Any] = config["connections"].get(
            config["target"],
        )
        if not selected_connection:
            msg = f"No connection for target {selected_connection}"
            raise RuntimeError(msg)
        selected_engine = RepoEngines.from_display(
            enum_choice=selected_connection["engine"],
        )
        if selected_engine is RepoEngines.SQLALCHEMY:
            return self._parse_sqlalchemy_connection(connection=selected_connection)

        supported_engines = RepoEngines.to_display()
        msg = f"The only supported engines are {supported_engines}"
        raise RuntimeError(msg)
