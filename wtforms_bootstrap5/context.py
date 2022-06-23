from __future__ import annotations

import dataclasses
import typing

from markupsafe import Markup

from .helpers import traverse_base_classes
from .registry import DEFAULT_REGISTRY
from .registry import FormElement
from .registry import RendererRegistry


@dataclasses.dataclass
class FieldOptions:
    # class for field wrapper div
    wrapper_class: typing.Optional[str] = "mb-3"
    # extra attributes for field wrapper div
    wrapper_attrs: typing.Dict[str, str] = dataclasses.field(default_factory=dict)
    # Enable wrapper div or not
    wrapper_enabled: bool = True
    # class for field input element
    field_class: str = "form-control"
    # extra attributes for field input element
    field_attrs: typing.Dict[str, str] = dataclasses.field(default_factory=dict)
    # class for submit field input element
    submit_field_class: str = "btn btn-primary"
    # class for field label element
    label_class: str = "form-label"
    # extra attributes for field label element
    label_attrs: typing.Dict[str, str] = dataclasses.field(default_factory=dict)


class RendererContext:
    def __init__(
        self,
        registry: RendererRegistry = DEFAULT_REGISTRY,
        default_field_option: FieldOptions = FieldOptions(),
    ):
        self.default_field_option = default_field_option
        self.registry = registry
        self.field_options: typing.Dict[str, FieldOptions] = {}

    def field(self, name: str, **kwargs) -> RendererContext:
        if name in self.field_options:
            self.field_options[name].update(kwargs)
        else:
            self.field_options[name] = FieldOptions(**kwargs)
        return self

    def render(self, element: FormElement) -> Markup:
        base_class_paths: typing.List[typing.Tuple] = traverse_base_classes(
            cls=element.__class__
        )
        for path in base_class_paths:
            current_metadata = self.registry.class_metadata
            metadatas = [current_metadata]
            for cls in reversed(path):
                if cls not in current_metadata.subclasses:
                    break
                current_metadata = current_metadata.subclasses[cls]
                metadatas.append(current_metadata)
            for metadata in reversed(metadatas):
                for renderer in metadata.renderers:
                    return renderer(self, element)
            raise ValueError(f"Cannot find renderer for {element}")
