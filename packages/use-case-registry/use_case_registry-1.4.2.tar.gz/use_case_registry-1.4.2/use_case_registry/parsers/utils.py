"""Parser utils."""
import os

import yaml

from use_case_registry.errors import ConfigFileError


def env_tag_constructor(loader: yaml.Loader, node: yaml.Node) -> str:
    """Assing value to !ENV variable referenced at node."""
    if not isinstance(node, yaml.nodes.ScalarNode):
        raise yaml.constructor.ConstructorError(
            context=None,
            context_mark=None,
            problem=f"Expected a scalar node but found {node}",
        )

    env_variable = loader.construct_scalar(node=node)

    if env_variable not in os.environ:
        raise ConfigFileError(msg=f"No environment variable for `{env_variable}`")

    value = os.environ[env_variable]  # type: ignore[index]
    tag = loader.resolve(  # type: ignore[no-untyped-call]
        yaml.nodes.ScalarNode,
        value,
        (
            True,
            False,
        ),
    )
    return loader.construct_object(  # type: ignore[no-untyped-call]
        node=yaml.nodes.ScalarNode(
            tag=tag,
            value=value,
        ),
        deep=False,
    )
