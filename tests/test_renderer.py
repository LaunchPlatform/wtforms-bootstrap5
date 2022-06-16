import pytest
from wtforms.form import Form

from wtforms_bootstrap5.renderer import Renderer


@pytest.fixture
def renderer() -> Renderer:
    return Renderer()


def test_renderer(renderer: Renderer):
    form = Form()
    html = renderer.render(form)
    assert html == ""
