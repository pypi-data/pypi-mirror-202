"""Parsing errors."""


class ConfigFileError(Exception):
    """Raised when config file is wrong."""

    def __init__(self, msg: str) -> None:  # noqa: D107
        super().__init__(msg)
