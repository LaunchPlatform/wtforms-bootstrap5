import pytest
from wtforms.fields import EmailField
from wtforms.fields import PasswordField
from wtforms.form import Form

from wtforms_bootstrap5 import renderers
from wtforms_bootstrap5.context import RendererContext


@pytest.fixture
def renderer_context() -> RendererContext:
    return RendererContext()


def test_renderer(renderer_context: RendererContext):
    class MockForm(Form):
        email = EmailField("Email")
        password = PasswordField("Password")

    form = MockForm()
    html = renderer_context.render(form)
    assert html == ""
