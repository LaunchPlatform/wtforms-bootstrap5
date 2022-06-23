import io
import pathlib
import typing
import webbrowser

import pytest
from lxml import etree


@pytest.fixture
def view_in_browser(tmp_path: pathlib.Path) -> typing.Callable[[str], None]:
    def _view_in_browser(html: str, include_bootstrap: bool = True):
        filepath = tmp_path / "sample.html"
        with open(filepath, "wt") as fo:
            if include_bootstrap:
                fo.write(
                    """
                <!doctype html>
                <html lang="en">
                  <head>
                    <meta charset="utf-8">
                    <meta name="viewport" content="width=device-width, initial-scale=1">
                    <title>Bootstrap demo</title>
                    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.2.0-beta1/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-0evHe/X+R7YkIZDRvuzKMRqM+OrBnVFBL6DOitfPri4tjfHxaWutUpFmBp4vmVor" crossorigin="anonymous">
                  </head>
                  <body>
                    <div class="container mt-3">
                """
                )
            fo.write(html)
            if include_bootstrap:
                fo.write(
                    """
                    </div>
                    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.2.0-beta1/dist/js/bootstrap.bundle.min.js" integrity="sha384-pprn3073KE6tl6bjs2QrFaJGz5/SUsLqktiwsUTF55Jfv3qYSDhgCecCxMW52nD2" crossorigin="anonymous"></script>
                  </body>
                </html>
                """
                )
        webbrowser.open(filepath)

    return _view_in_browser


@pytest.fixture
def parse_html() -> typing.Callable[[str], etree._ElementTree]:
    def _parse_html(html: str) -> etree._ElementTree:
        parser = etree.HTMLParser(recover=False)
        return etree.parse(io.StringIO(html), parser)

    return _parse_html
