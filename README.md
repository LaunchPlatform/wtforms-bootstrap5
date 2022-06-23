# wtforms-bootstrap5
Simple library for rendering WTForms in HTML as Bootstrap 5 form controls

## Why?

Everytime I build a website with [WTForms](https://wtforms.readthedocs.io), I spend way too much time in writing HTML and [Jinja template](https://jinja.palletsprojects.com/) for rendering a form as [Bootstrap 5 form controls](https://getbootstrap.com/docs/5.2/forms/overview/).
Work smart is an important value we have here at [Launch Platform](https://launchplatform.com), so I wonder why not make a library for making rendering Bootstrap 5 style WTForms controls easily?
So here you go, wtforms-bootstrap5 is created, and it's a simple Python library for rendering WTForms in Bootstrap 5 favor.

## Example

First, you define your form as you would usually do with WTForms:

```python
from wtforms import Form
from wtforms import EmailField
from wtforms import PasswordField
from wtforms import SelectField
from wtforms import BooleanField
from wtforms import SubmitField


class MyForm(Form):
    email = EmailField("Email", render_kw=dict(placeholder="Foobar"))
    password = PasswordField("Password", description="Your super secret password")
    city = SelectField("City", choices=["Los Angle", "San Francisco", "New York"])
    agree_terms = BooleanField("I agrees to terms and service")
    submit = SubmitField()

```

Then you can use `RenderContext` for rendering your form like this

```python
from wtforms_bootstrap5 import RendererContext

form = MyForm()
context = RendererContext()
html = context.render(form)
```

The form will be rendered as HTML like

```html
<form><div class="mb-3"><label class="form-label" for="email">Email</label><input class="form-control" id="email" name="email" type="email" value=""></div>
<div class="mb-3"><label class="form-label" for="password">Password</label><input class="form-control" id="password" name="password" type="password" value=""><div class="form-text">Your super secret password</div></div>
<div class="mb-3"><label class="form-label" for="city">City</label><select class="form-select" id="city" name="city"><option value="Los Angle">Los Angle</option><option value="San Francisco">San Francisco</option><option value="New York">New York</option></select></div>
<div class="mb-3"><div class="form-check"><label class="form-check-label" for="agree_terms">I agrees to terms and service</label><input class="form-check-input" id="agree_terms" name="agree_terms" type="checkbox" value="y"></div></div>
<div class="mb-3"><input class="btn btn-primary" id="submit" name="submit" type="submit" value="Submit"></div></form>
```

