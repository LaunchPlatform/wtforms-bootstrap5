import typing

from markupsafe import escape
from markupsafe import Markup
from wtforms import BooleanField
from wtforms import Field
from wtforms import Form
from wtforms import HiddenField
from wtforms import SelectField
from wtforms import SelectMultipleField
from wtforms import SubmitField
from wtforms.widgets import html_params as raw_html_params

from .context import FieldOptions
from .context import RendererContext
from .registry import FormElement
from .registry import register


def _field_option(context: RendererContext, name: str) -> FieldOptions:
    return context.field_options.get(name, context.default_field_options)


def html_params(**kwargs) -> str:
    if not kwargs:
        return ""
    return " " + raw_html_params(**kwargs)


def wrap_with(
    html: str,
    enabled: bool,
    class_name: typing.Optional[str],
    attrs: typing.Dict[str, str],
    tag: str = "div",
) -> Markup:
    """Optionally wrap given html with a div tag with given class and attributes

    :param html: given html to wrap
    :param enabled: wrapper enabled or not
    :param class_name: class value of wrapper
    :param attrs: attributes of wrapper
    :param tag: type of tag, `div` will be used by default
    :return: wrapped html
    """
    if not enabled:
        return Markup(html)
    kwargs = {}
    if class_name is not None:
        kwargs["class"] = class_name
    kwargs.update(attrs)
    return Markup(f"<{tag}{html_params(**kwargs)}>{html}</{tag}>")


@register(target_cls=Form)
def render_form(context: RendererContext, element: FormElement) -> Markup:
    form: Form = element
    form_options = context.form_options
    fields = [context.render(field) for field in form._fields.values()]
    content = "\n".join(fields)
    base_attrs = {}
    if form_options.action is not None:
        base_attrs["action"] = form_options.action
    if form_options.method is not None:
        base_attrs["method"] = form_options.method
    if form_options.enctype is not None:
        base_attrs["enctype"] = form_options.enctype
    return wrap_with(
        content,
        enabled=form_options.form_enabled,
        class_name=form_options.form_class,
        attrs=base_attrs | form_options.form_attrs,
        tag="form",
    )


@register(target_cls=Field)
def render_field(context: RendererContext, element: FormElement) -> Markup:
    field: Field = element
    is_checkbox = isinstance(field, BooleanField)
    is_select = isinstance(field, (SelectField, SelectMultipleField))

    field_kwargs: typing.Dict[str, str] = {}
    field_options: FieldOptions = _field_option(context, name=field.name)
    field_classes = []
    if field_options.field_class is not None:
        if is_checkbox:
            field_classes.append(field_options.checkbox_field_class)
        elif is_select:
            field_classes.append(field_options.select_field_class)
        else:
            field_classes.append(field_options.field_class)
    if field.errors:
        field_classes.append(field_options.field_invalid_class)
    if field_classes:
        field_kwargs["class"] = " ".join(field_classes)
    field_kwargs.update(field_options.field_attrs)

    field_content = [field.widget(field, **field_kwargs)]
    if field.description:
        help_message = escape(field.description)
        field_content.append(
            wrap_with(
                help_message,
                enabled=True,
                class_name=field_options.help_class,
                attrs=field_options.help_attrs,
            )
        )

    if field.errors:
        error_message = escape(field_options.error_separator.join(field.errors))
        field_content.append(
            wrap_with(
                error_message,
                enabled=True,
                class_name=field_options.error_class,
                attrs=field_options.error_attrs,
            )
        )

    field_html = "".join(field_content)
    field_html = wrap_with(
        field_html,
        enabled=field_options.field_wrapper_enabled,
        class_name=field_options.field_wrapper_class,
        attrs=field_options.field_wrapper_attrs,
    )

    content = [field_html]

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

    content_html = "".join(content)
    content_html = wrap_with(
        content_html,
        enabled=is_checkbox and field_options.checkbox_wrapper_enabled,
        class_name=field_options.checkbox_wrapper_class,
        attrs=field_options.checkbox_wrapper_attrs,
    )
    content_html = wrap_with(
        content_html,
        enabled=field_options.wrapper_enabled,
        class_name=field_options.wrapper_class,
        attrs=field_options.wrapper_attrs,
    )
    return wrap_with(
        content_html,
        enabled=field_options.row_enabled,
        class_name=field_options.row_class,
        attrs=field_options.row_attrs,
    )


@register(target_cls=SubmitField)
def render_submit(context: RendererContext, element: FormElement) -> Markup:
    field: SubmitField = element

    field_kwargs: typing.Dict[str, str] = {}
    field_options: FieldOptions = _field_option(context, name=field.name)
    if field_options.submit_field_class is not None:
        field_kwargs["class"] = field_options.submit_field_class
    field_kwargs.update(field_options.field_attrs)

    field_html = field.widget(field, **field_kwargs)
    field_html = wrap_with(
        field_html,
        enabled=field_options.field_wrapper_enabled,
        class_name=field_options.field_wrapper_class,
        attrs=field_options.field_wrapper_attrs,
    )

    content = [field_html]
    content_html = "".join(content)
    content_html = wrap_with(
        content_html,
        enabled=field_options.wrapper_enabled,
        class_name=field_options.wrapper_class,
        attrs=field_options.wrapper_attrs,
    )
    return wrap_with(
        content_html,
        enabled=field_options.row_enabled,
        class_name=field_options.row_class,
        attrs=field_options.row_attrs,
    )


@register(target_cls=HiddenField)
def render_hidden(context: RendererContext, element: FormElement) -> Markup:
    field: HiddenField = element

    field_kwargs: typing.Dict[str, str] = {}
    field_options: FieldOptions = _field_option(context, name=field.name)
    field_kwargs.update(field_options.field_attrs)
    field_html = field.widget(field, **field_kwargs)
    return field_html
