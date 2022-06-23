import typing

from markupsafe import Markup
from wtforms import Field
from wtforms import Form

from .context import RendererContext
from .registry import FormElement
from .registry import register


@register(target_cls=Form)
def render_form(context: RendererContext, element: FormElement) -> Markup:
    form: Form = element
    fields = [context.render(field) for field in form._fields.values()]
    # TODO: add form action, method and other stuff
    return Markup("<form>" + "\n".join(fields) + "</form>")


@register(target_cls=Field)
def render_field(context: RendererContext, element: FormElement) -> Markup:
    field: Field = element
    kwargs: typing.Dict[str, str] = {}
    if context.field_class is not None:
        kwargs["class"] = context.field_class
    content = []
    if field.label is not None:
        content.insert(
            0,
            Markup(
                f'<label for="{field.name}" class="form-label">{field.label}</label>'
            ),
        )
    content.append(field.widget(field, **kwargs))
    # TODO: display help
    # TODO: handle error
    content_str = "".join(content)
    return Markup(f'<div class="mb-3">{content_str}</div>')
