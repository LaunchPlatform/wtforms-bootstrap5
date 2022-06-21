import typing

from markupsafe import Markup

from .helpers import traverse_base_classes
from .registry import DEFAULT_REGISTRY
from .registry import FormElement
from .registry import RendererRegistry


class RendererContext:
    def __init__(
        self,
        field_class: typing.Optional[str] = "form-control",
        registry: RendererRegistry = DEFAULT_REGISTRY,
    ):
        self.field_class = field_class
        self.registry = registry

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
                # TODO: match name first
                for renderer in metadata.renderers:
                    return renderer(self, element)
            raise ValueError(f"Cannot find renderer for {element}")
