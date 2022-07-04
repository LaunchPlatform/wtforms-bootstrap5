from __future__ import annotations

import dataclasses
import typing

from markupsafe import Markup

from .helpers import traverse_base_classes
from .registry import DEFAULT_REGISTRY
from .registry import FormElement
from .registry import RendererRegistry


@dataclasses.dataclass(frozen=True)
class FormOptions:
    # Form method to use
    method: typing.Optional[str] = "POST"
    # Form action (target URL)
    action: typing.Optional[str] = None
    # Form encoding type
    enctype: typing.Optional[str] = None
    # class for form
    form_class: typing.Optional[str] = None
    # extra attributes for form
    form_attrs: typing.Dict[str, str] = dataclasses.field(default_factory=dict)
    # Enable form or not
    form_enabled: bool = True


@dataclasses.dataclass(frozen=True)
class FieldOptions:
    # class for row div
    row_class: typing.Optional[str] = "mb-3"
    # extra attributes for row div
    row_attrs: typing.Dict[str, str] = dataclasses.field(default_factory=dict)
    # Enable wrapper row or not
    row_enabled: bool = True

    # class for the inner wrapper div (inside row div)
    wrapper_class: typing.Optional[str] = "mb-3"
    # extra attributes for the inner wrapper div (inside row div)
    wrapper_attrs: typing.Dict[str, str] = dataclasses.field(default_factory=dict)
    # enable inner wrapper div (inside row div)
    wrapper_enabled: bool = False

    # class for field input wrapper div
    field_wrapper_class: typing.Optional[str] = None
    # extra attributes for field input wrapper div
    field_wrapper_attrs: typing.Dict[str, str] = dataclasses.field(default_factory=dict)
    # enable field input wrapper div or not
    field_wrapper_enabled: bool = False

    # class for field input element
    field_class: typing.Optional[str] = "form-control"
    # extra attributes for field input element
    field_attrs: typing.Dict[str, str] = dataclasses.field(default_factory=dict)
    # invalid class for validation
    field_invalid_class: typing.Optional[str] = "is-invalid"

    # class for submit field input element
    submit_field_class: typing.Optional[str] = "btn btn-primary"

    # class for checkbox input element
    checkbox_field_class: typing.Optional[str] = "form-check-input"
    # class for checkbox label element
    checkbox_label_class: typing.Optional[str] = "form-check-label"

    # class for checkbox wrapper class div
    checkbox_wrapper_class: typing.Optional[str] = "form-check"
    # extra attributes for checkbox wrapper class div
    checkbox_wrapper_attrs: typing.Dict[str, str] = dataclasses.field(
        default_factory=dict
    )
    # enable checkbox wrapper
    checkbox_wrapper_enabled: bool = True

    # class for select input element
    select_field_class: typing.Optional[str] = "form-select"

    # class for field label element
    label_class: typing.Optional[str] = "form-label"
    # extra attributes for field label element
    label_attrs: typing.Dict[str, str] = dataclasses.field(default_factory=dict)

    # render label first before input element
    label_first: bool = True
    # enable label
    label_enabled: bool = True

    # class for error message div
    error_class: typing.Optional[str] = "invalid-feedback"
    # extra attributes error message div
    error_attrs: typing.Dict[str, str] = dataclasses.field(default_factory=dict)
    # Separator of error messages
    error_separator: str = " "

    # class for help message div
    help_class: typing.Optional[str] = "form-text"
    # extra attributes help message div
    help_attrs: typing.Dict[str, str] = dataclasses.field(default_factory=dict)
    # enable help message
    help_enabled: bool = True


class RendererContext:
    def __init__(
        self,
        registry: RendererRegistry = DEFAULT_REGISTRY,
        default_form_options: FormOptions = FormOptions(),
        default_field_options: FieldOptions = FieldOptions(),
    ):
        self.form_options = default_form_options
        self.default_field_options = default_field_options
        self.registry = registry
        self.field_options: typing.Dict[str, FieldOptions] = {}

    def form(self, **kwargs) -> RendererContext:
        old_options = dataclasses.asdict(self.form_options)
        self.form_options = FormOptions(**(old_options | kwargs))
        return self

    def field(self, *names: str, **kwargs: str) -> RendererContext:
        for name in names:
            old_options = dataclasses.asdict(
                self.field_options.get(name, self.default_field_options)
            )
            self.field_options[name] = FieldOptions(**(old_options | kwargs))
        return self

    def default_field(self, **kwargs: str) -> RendererContext:
        self.default_field_options = FieldOptions(
            **(dataclasses.asdict(self.default_field_options) | kwargs)
        )
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
