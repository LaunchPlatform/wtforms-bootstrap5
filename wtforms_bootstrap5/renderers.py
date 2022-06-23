import typing

from markupsafe import escape
from markupsafe import Markup
from wtforms import BooleanField
from wtforms import Field
from wtforms import Form
from wtforms import SubmitField
from wtforms.widgets import html_params as raw_html_params

from .context import FieldOptions
from .context import RendererContext
from .registry import FormElement
from .registry import register


def _field_option(context: RendererContext, name: str) -> FieldOptions:
    return context.field_options.get(name, context.default_field_option)


def html_params(**kwargs) -> str:
    if not kwargs:
        return ""
    return " " + raw_html_params(**kwargs)


@register(target_cls=Form)
def render_form(context: RendererContext, element: FormElement) -> Markup:
    form: Form = element
    fields = [context.render(field) for field in form._fields.values()]
    # TODO: add form action, method and other stuff
    return Markup("<form>" + "\n".join(fields) + "</form>")


@register(target_cls=Field)
def render_field(context: RendererContext, element: FormElement) -> Markup:
    field: Field = element
    is_checkbox = isinstance(field, BooleanField)

    field_kwargs: typing.Dict[str, str] = {}
    field_options: FieldOptions = _field_option(context, name=field.name)
    field_classes = []
    if field_options.field_class is not None:
        if is_checkbox:
            field_classes.append(field_options.checkbox_field_class)
        else:
            field_classes.append(field_options.field_class)
    if field.errors:
        field_classes.append(field_options.field_invalid_class)
    if field_classes:
        field_kwargs["class"] = " ".join(field_classes)
    field_kwargs.update(field_options.field_attrs)

    content = [field.widget(field, **field_kwargs)]

    if field.label is not None and field_options.label_enabled:
        label_kwargs = {"for": field.name}
        if field_options.label_class is not None:
            if is_checkbox:
                label_kwargs["class"] = field_options.checkbox_label_class
            else:
                label_kwargs["class"] = field_options.label_class
        label_kwargs.update(field_options.label_attrs)
        label_html = field.label(**label_kwargs)
        if is_checkbox or field_options.label_first:
            content.insert(0, label_html)
        else:
            content.append(label_html)

    if field.description:
        help_kwargs = {}
        if field_options.help_class is not None:
            help_kwargs["class"] = field_options.help_class
        help_kwargs.update(field_options.help_attrs)
        help_message = escape(field.description)
        content.append(f"<div{html_params(**help_kwargs)}>{help_message}</div>")

    if field.errors:
        error_kwargs = {}
        if field_options.error_class is not None:
            error_kwargs["class"] = field_options.error_class
        error_kwargs.update(field_options.error_attrs)
        error_message = escape(field_options.error_separator.join(field.errors))
        content.append(f"<div{html_params(**error_kwargs)}>{error_message}</div>")

    content_str = "".join(content)

    if is_checkbox and field_options.checkbox_wrapper_enabled:
        checkbox_wrapper_kwargs = {}
        if field_options.checkbox_wrapper_class is not None:
            checkbox_wrapper_kwargs["class"] = field_options.checkbox_wrapper_class
            checkbox_wrapper_kwargs.update(field_options.checkbox_wrapper_attrs)
        content_str = (
            f"<div{html_params(**checkbox_wrapper_kwargs)}>{content_str}</div>"
        )

    if not field_options.wrapper_enabled:
        return Markup(content_str)

    wrapper_kwargs = {}
    if field_options.wrapper_class is not None:
        wrapper_kwargs["class"] = field_options.wrapper_class
    wrapper_kwargs.update(field_options.wrapper_attrs)
    return Markup(f"<div{html_params(**wrapper_kwargs)}>{content_str}</div>")


@register(target_cls=SubmitField)
def render_submit(context: RendererContext, element: FormElement) -> Markup:
    field: SubmitField = element

    field_kwargs: typing.Dict[str, str] = {}
    field_options: FieldOptions = _field_option(context, name=field.name)
    if field_options.submit_field_class is not None:
        field_kwargs["class"] = field_options.submit_field_class
    field_kwargs.update(field_options.field_attrs)

    content = []
    content.append(field.widget(field, **field_kwargs))
    content_str = "".join(content)
    if not field_options.wrapper_enabled:
        return Markup(content_str)

    wrapper_kwargs = {}
    if field_options.wrapper_class is not None:
        wrapper_kwargs["class"] = field_options.wrapper_class
    wrapper_kwargs.update(field_options.wrapper_attrs)
    return Markup(f"<div{html_params(**wrapper_kwargs)}>{content_str}</div>")
