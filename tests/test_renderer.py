import typing

import pytest
from lxml import etree
from wtforms.fields import BooleanField
from wtforms.fields import EmailField
from wtforms.fields import PasswordField
from wtforms.fields import SelectField
from wtforms.fields import SubmitField
from wtforms.form import Form

from wtforms_bootstrap5 import renderers
from wtforms_bootstrap5.context import RendererContext


class MockForm(Form):
    email = EmailField("Email", render_kw=dict(placeholder="Foobar"))
    password = PasswordField("Password", description="Your super secret password")
    city = SelectField("City", choices=["Los Angle", "San Francisco", "New York"])
    agree_terms = BooleanField("I agrees to terms and service")
    submit = SubmitField()


@pytest.fixture
def renderer_context() -> RendererContext:
    return RendererContext()


@pytest.fixture
def form_cls() -> typing.Type:
    return MockForm


def test_renderer(
    renderer_context: RendererContext,
    form_cls: typing.Type,
    parse_html: typing.Callable[[str], etree._ElementTree],
):
    form = form_cls()
    form.password.errors = ["Bad password"]
    html = renderer_context.render(form)
    tree = parse_html(html)
    # Notice: lxml parser will add html and body automatically in the tree
    assert tree.xpath("/html/body/form")
    assert tree.xpath('/html/body/form/div[@class="mb-3"]/input[@name="email"]')
    assert tree.xpath('/html/body/form/div[@class="mb-3"]/input[@name="password"]')
    assert tree.xpath('/html/body/form/div[@class="mb-3"]/select[@name="city"]')
    assert tree.xpath(
        '/html/body/form/div[@class="mb-3"]/div[@class="form-check"]/input[@name="agree_terms"]'
    )
    assert tree.xpath('/html/body/form/div[@class="mb-3"]/input[@name="submit"]')
