import typing

import pytest
from lxml import etree
from wtforms.fields import BooleanField
from wtforms.fields import EmailField
from wtforms.fields import HiddenField
from wtforms.fields import PasswordField
from wtforms.fields import SelectField
from wtforms.fields import SubmitField
from wtforms.form import Form

from wtforms_bootstrap5.context import RendererContext


class MockForm(Form):
    email = EmailField("Email", render_kw=dict(placeholder="Foobar"))
    password = PasswordField("Password", description="Your super secret password")
    city = SelectField("City", choices=["Los Angle", "San Francisco", "New York"])
    agree_terms = BooleanField("I agrees to terms and service")
    submit = SubmitField()
    csrf_token = HiddenField()


@pytest.fixture
def renderer_context() -> RendererContext:
    return RendererContext()


@pytest.fixture
def form_cls() -> typing.Type:
    return MockForm


@pytest.fixture
def form(form_cls: typing.Type) -> Form:
    return form_cls()


def test_render(
    renderer_context: RendererContext,
    form: MockForm,
    parse_html: typing.Callable[[str], etree._ElementTree],
):
    form.password.errors = ["Bad password"]
    html = renderer_context.render(form)
    tree = parse_html(html)
    # Notice: lxml parser will add html and body automatically in the tree
    assert tree.xpath("/html/body/form")
    assert tree.xpath('/html/body/form/div[@class="mb-3"]/input[@name="email"]')
    assert tree.xpath(
        '/html/body/form/div[@class="mb-3"]/input[@name="email"]/@placeholder'
    ) == ["Foobar"]
    assert tree.xpath('/html/body/form/div[@class="mb-3"]/input[@name="password"]')
    assert tree.xpath('/html/body/form/div[@class="mb-3"]/select[@name="city"]')
    assert tree.xpath(
        '/html/body/form/div[@class="mb-3"]/div[@class="form-check"]/'
        'input[@name="agree_terms"]'
    )
    assert tree.xpath('/html/body/form/div[@class="mb-3"]/input[@name="submit"]')
    assert tree.xpath('/html/body/form/input[@name="csrf_token"]')
    assert [
        element.tag
        for element in tree.xpath('/html/body/form/div/div[@class="form-check"]/*')
    ] == ["input", "label"]


def test_default_field_options(
    renderer_context: RendererContext,
    form: MockForm,
    parse_html: typing.Callable[[str], etree._ElementTree],
):
    form.password.errors = ["Bad password"]
    html = renderer_context.default_field(row_class="row").render(form)
    tree = parse_html(html)
    # Notice: lxml parser will add html and body automatically in the tree
    assert tree.xpath("/html/body/form")
    assert tree.xpath('/html/body/form/div[@class="row"]/input[@name="email"]')
    assert tree.xpath('/html/body/form/div[@class="row"]/input[@name="password"]')
    assert tree.xpath('/html/body/form/div[@class="row"]/select[@name="city"]')
    assert tree.xpath(
        '/html/body/form/div[@class="row"]/div[@class="form-check"]/'
        'input[@name="agree_terms"]'
    )
    assert tree.xpath('/html/body/form/div[@class="row"]/input[@name="submit"]')


def test_row_options(
    renderer_context: RendererContext,
    form: MockForm,
    parse_html: typing.Callable[[str], etree._ElementTree],
):
    html = renderer_context.field(
        "email", row_class="row", row_attrs={"attr": "MOCK_ATTR"}
    ).render(form.email)
    tree = parse_html(html)
    # Notice: lxml parser will add html and body automatically in the tree
    assert tree.xpath(
        '/html/body/div[@class="row" and @attr="MOCK_ATTR"]/input[@name="email"]'
    )


def test_row_disabled(
    renderer_context: RendererContext,
    form: MockForm,
    parse_html: typing.Callable[[str], etree._ElementTree],
):
    html = renderer_context.field("email", row_enabled=False).render(form.email)
    tree = parse_html(html)
    # Notice: lxml parser will add html and body automatically in the tree
    assert tree.xpath('/html/body/input[@name="email"]')


def test_wrapper_options(
    renderer_context: RendererContext,
    form: MockForm,
    parse_html: typing.Callable[[str], etree._ElementTree],
):
    html = renderer_context.field(
        "submit",
        wrapper_class="offset-3",
        wrapper_attrs={"attr": "MOCK_ATTR"},
        wrapper_enabled=True,
    ).render(form.submit)
    tree = parse_html(html)
    # Notice: lxml parser will add html and body automatically in the tree
    assert tree.xpath(
        '/html/body/div[@class="mb-3"]/div[@class="offset-3" and @attr="MOCK_ATTR"]/'
        'input[@name="submit"]'
    )


def test_form_options(
    renderer_context: RendererContext,
    form: MockForm,
    parse_html: typing.Callable[[str], etree._ElementTree],
):
    html = renderer_context.form(
        method="MOCK_METHOD",
        action="MOCK_ACTION",
        enctype="MOCK_ENCTYPE",
        form_class="MOCK_CLASS",
        form_attrs=dict(mock_attr="MOCK_VALUE"),
    ).render(form)
    tree = parse_html(html)
    # Notice: lxml parser will add html and body automatically in the tree
    form = tree.xpath("/html/body/form")[0]
    assert form.attrib["method"] == "MOCK_METHOD"
    assert form.attrib["action"] == "MOCK_ACTION"
    assert form.attrib["enctype"] == "MOCK_ENCTYPE"
    assert form.attrib["class"] == "MOCK_CLASS"
    assert form.attrib["mock_attr"] == "MOCK_VALUE"


def test_form_options_disable(
    renderer_context: RendererContext,
    form: MockForm,
    parse_html: typing.Callable[[str], etree._ElementTree],
):
    html = renderer_context.form(form_enabled=False).render(form)
    tree = parse_html(html)
    # Notice: lxml parser will add html and body automatically in the tree
    assert not tree.xpath("/html/body/form")
    assert tree.xpath('/html/body/div/input[@name="email"]')


def test_add_field(
    renderer_context: RendererContext,
    parse_html: typing.Callable[[str], etree._ElementTree],
):
    form = Form()
    html = renderer_context.add_field(name="submit", field=SubmitField()).render(form)
    tree = parse_html(html)
    # Notice: lxml parser will add html and body automatically in the tree
    assert tree.xpath('/html/body/form/div/input[@name="submit"]')


def test_add_submit(
    renderer_context: RendererContext,
    parse_html: typing.Callable[[str], etree._ElementTree],
):
    form = Form()
    html = renderer_context.add_submit(name="submit").render(form)
    tree = parse_html(html)
    # Notice: lxml parser will add html and body automatically in the tree
    assert tree.xpath('/html/body/form/div/input[@name="submit"]')


def test_add_field_with_options(
    renderer_context: RendererContext,
    parse_html: typing.Callable[[str], etree._ElementTree],
):
    form = Form()
    html = (
        renderer_context.add_field(name="submit", field=SubmitField())
        .field("submit", row_class="mb-5")
        .render(form)
    )
    tree = parse_html(html)
    # Notice: lxml parser will add html and body automatically in the tree
    assert tree.xpath('/html/body/form/div[@class="mb-5"]/input[@name="submit"]')
