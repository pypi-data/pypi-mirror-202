"""Parser utils."""
import os
from typing import Any

import yaml

from use_case_registry.parsers.errors import ConfigFileError


def construct_env_tag(loader: yaml.Loader, node: yaml.Node) -> Any:  # noqa: ANN401
    """Assign value of ENV variable referenced at node."""
    if isinstance(node, yaml.nodes.ScalarNode):
        env_variables = [loader.construct_scalar(node)]
    elif isinstance(node, yaml.nodes.SequenceNode):
        child_nodes = node.value
        if len(child_nodes) > 1:
            # default is resolved using YAML's (implicit) types.
            loader.construct_object(child_nodes[-1])  # type: ignore[no-untyped-call]
            child_nodes = child_nodes[:-1]
        # Env env_variables are resolved as string values, ignoring (implicit) types.
        env_variables = [loader.construct_scalar(child) for child in child_nodes]
    else:
        raise yaml.constructor.ConstructorError(
            None,
            None,
            f"expected a scalar or sequence node, but found {node.id}",  # type: ignore[attr-defined]  # noqa: E501
            node.start_mark,
        )

    for var in env_variables:
        if var in os.environ:
            value = os.environ[var]  # type: ignore[index]
            # Resolve value to Python type using YAML's implicit resolvers
            tag = loader.resolve(  # type: ignore[no-untyped-call]
                yaml.nodes.ScalarNode,
                value,
                (
                    True,
                    False,
                ),
            )
            return loader.construct_object(  # type: ignore[no-untyped-call]
                yaml.nodes.ScalarNode(
                    tag,
                    value,
                ),
            )

    raise ConfigFileError(f"No environment variable for {var}")  # noqa: EM102, TRY003
