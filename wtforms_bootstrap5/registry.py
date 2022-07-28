from __future__ import annotations

import dataclasses
import typing

from markupsafe import Markup
from wtforms import Field
from wtforms import Form

from .helpers import traverse_base_classes

# Union type of form element
FormElement = typing.Union[Field, Form]
# Type for form element renderer
FormElementRenderer = typing.Callable[["RenderContext", FormElement], Markup]


@dataclasses.dataclass
class ClassMetadata:
    cls: typing.Type
    renderers: typing.List[FormElementRenderer] = dataclasses.field(
        default_factory=list
    )
    subclasses: typing.Dict[typing.Type, ClassMetadata] = dataclasses.field(
        default_factory=dict
    )


class RendererRegistry:
    def __init__(self):
        self.class_metadata: ClassMetadata = ClassMetadata(cls=object)

    def add(
        self,
        renderer: FormElementRenderer,
        target_cls: typing.Type,
    ):
        base_class_paths: typing.List[typing.Tuple] = traverse_base_classes(
            cls=target_cls
        )
        for path in base_class_paths:
            current_metadata = self.class_metadata
            for cls in reversed(path):
                if cls not in current_metadata.subclasses:
                    new_metadata = ClassMetadata(cls=cls)
                    current_metadata.subclasses[cls] = new_metadata
                    current_metadata = new_metadata
                else:
                    current_metadata = current_metadata.subclasses[cls]
            current_metadata.renderers.append(renderer)


DEFAULT_REGISTRY = RendererRegistry()


def register(
    target_cls: typing.Type,
    registry: RendererRegistry = DEFAULT_REGISTRY,
):
    def decorator(renderer: FormElementRenderer) -> FormElementRenderer:
        registry.add(renderer=renderer, target_cls=target_cls)
        return renderer

    return decorator
