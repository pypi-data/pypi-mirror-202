from typing import Any

from phml.embedded import exec_embedded, exec_embedded_blocks
from phml.helpers import build_recursive_context
from phml.nodes import Element, Literal, Parent

from .base import scoped_step


def _process_attributes(node: Element, context: dict[str, Any]):
    context = build_recursive_context(node, context)
    for attribute in list(node.attributes.keys()):
        if attribute.startswith(":"):
            result = exec_embedded(
                str(node[attribute]).strip(),
                f"<{node.tag} {attribute}='{node[attribute]}'>",
                **context,
            )
            if result is not None:
                node.pop(attribute, None)
                node[attribute.lstrip(":")] = result
        else:
            if isinstance(node[attribute], str):
                value = exec_embedded_blocks(
                    str(node.attributes[attribute]).strip(),
                    f"<{node.tag} {attribute}='{node.attributes[attribute]}'>",
                    **context,
                )
                if value is not None:
                    node[attribute] = value


@scoped_step
def step_execute_embedded_python(node: Parent, _, context: dict[str, Any]):
    """Step to process embedded python inside of attributes and text nodes."""
    for child in node:
        if isinstance(child, Element):
            _process_attributes(
                child,
                build_recursive_context(child, context),
            )
        elif (
            Literal.is_text(child)
            and "{{" in child.content
            and child.parent.tag not in ["script", "style", "python"]
        ):
            child.content = exec_embedded_blocks(
                child.content.strip(),
                f"Text in <{node.tag}> at {node.position!r}",
                **build_recursive_context(child, context),
            )
