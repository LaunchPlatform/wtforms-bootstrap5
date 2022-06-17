import pytest
from wtforms.form import Form
from wtforms.fields import EmailField
from wtforms.fields import PasswordField

from wtforms_bootstrap5.renderer import Renderer


@pytest.fixture
def renderer() -> Renderer:
    return Renderer()


def test_renderer(renderer: Renderer):
    class MockForm(Form):
        email = EmailField("Email")
        password = PasswordField("Password")

    form = MockForm()
    html = renderer.render(form)
    assert html == ""
