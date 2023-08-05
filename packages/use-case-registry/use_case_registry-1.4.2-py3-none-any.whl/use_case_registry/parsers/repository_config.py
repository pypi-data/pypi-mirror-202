"""Repository config yaml parser."""
import pathlib
from typing import Any

import yaml
from typing_extensions import assert_never

from use_case_registry.enums import OptionEnums
from use_case_registry.errors import ConfigFileError
from use_case_registry.parsers.utils import env_tag_constructor

yaml.Loader.add_constructor(tag="!ENV", constructor=env_tag_constructor)


class RepoEngines(OptionEnums):
    """Support Repository Engines."""

    SQLALCHEMY = "SQLALCHEMY"


def to_display(enum_class: type[OptionEnums]) -> list[str]:
    """Format options enums for pretty display in CLI."""

    def _formatter(x: str) -> str:
        return x.lower().replace("_", "-")

    return list(map(_formatter, enum_class._member_names_))  # noqa: SLF001


class RepoConfigParser:
    """Parse a `config.yml` repository file."""

    def _get_connection(self, yml_parsed: dict[str, Any]) -> dict[str, Any]:
        available_connections = yml_parsed.get("connections")

        if not available_connections:
            raise ConfigFileError("No `connections` in file.")  # noqa: EM101, TRY003

        target_conn = yml_parsed["connections"].get(yml_parsed["target"])

        if not target_conn:
            raise ConfigFileError(  # noqa: TRY003
                "No connection for target selected",  # noqa: EM101
            )

        return target_conn

    def _format_sqlalchemy_connection(
        self,
        connection: dict[str, Any],
    ) -> dict[str, Any]:
        import sqlalchemy

        url_components = connection.get("url")
        if not url_components:
            raise ConfigFileError("No `url` section found.")  # noqa: EM101, TRY003

        drivername = url_components.pop("drivername", None)
        if not drivername:
            raise ConfigFileError("`drivername` is required ")  # noqa: EM101, TRY003

        url = sqlalchemy.URL(
            drivername=drivername,
            username=url_components.pop("username", None),
            password=url_components.pop("password", None),
            host=url_components.pop("host", None),
            port=url_components.pop("port", None),
            database=url_components.pop("database", None),
            query=url_components.pop("query", {}),
        )
        url_components["url"] = url.render_as_string(hide_password=True)

        url_components["engine"] = RepoEngines.SQLALCHEMY
        return url_components

    def _format_connection(self, connection: dict[str, Any]) -> dict[str, Any]:
        selected_engine = connection.get("engine")

        if not selected_engine:
            raise ConfigFileError("`engine` field missing.")  # noqa: EM101, TRY003
        try:
            engine = RepoEngines[selected_engine.upper()]
        except KeyError:
            formatted_supported_engines = to_display(enum_class=RepoEngines)
            raise ConfigFileError(  # noqa: B904, TRY003, TRY200
                f"`engine` {selected_engine} is not supported. "  # noqa: EM102
                f"Only {formatted_supported_engines}",
            )

        if engine is RepoEngines.SQLALCHEMY:
            formatted_connection = self._format_sqlalchemy_connection(
                connection=connection,
            )
        else:
            assert_never(engine)
        return formatted_connection

    def parse(self, path_to_config: pathlib.Path) -> dict[str, Any]:
        """Parse file."""
        if not (path_to_config.exists() or path_to_config.is_file()):
            raise ConfigFileError(  # noqa: TRY003
                f"Config file not found in location {path_to_config}",  # noqa: EM102
            )

        yml_parsed: dict[str, Any] = yaml.load(
            stream=path_to_config.read_text(encoding="utf-8"),
            Loader=yaml.Loader,  # noqa: S506
        )
        target_defined = yml_parsed.get("target")

        if not target_defined:
            raise ConfigFileError(  # noqa: TRY003
                "No `target` defined in repo configuration.",  # noqa: EM101
            )

        connection = self._get_connection(yml_parsed=yml_parsed)

        return self._format_connection(connection=connection)
