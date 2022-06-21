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
def render_field(render: RendererContext, element: FormElement) -> Markup:
    field: Field = element
    return field.widget(field)
