# WTForms-Bootstrap5
Simple library for rendering WTForms in HTML as Bootstrap 5 form controls

**Notice: this project is still in very early stage, the API may change a lots rapidly**

## Features

- **MIT licensed** - it doesn't infect your code
- **Light weight** - not much code and little dependencies
- **Latest Bootstrap 5** - generates forms in latest Bootstrap 5 style 
- **Highly customizable** - you can generate different kind of Bootstrap 5 form controls and layouts
- **Template engine friendly** - chained method calls making it easy to integrate with template engine
- **Covered with automatic tests** - yep, we have test cases

## Why?

Everytime I build a website with [WTForms](https://wtforms.readthedocs.io), I spend way too much time in writing HTML and [Jinja template](https://jinja.palletsprojects.com/) for rendering a form as [Bootstrap 5 form controls](https://getbootstrap.com/docs/5.2/forms/overview/).
Work smart is an important value we have here at [Launch Platform](https://launchplatform.com), so I wonder why not make a library for making rendering Bootstrap 5 style WTForms controls easily?
So here you go, wtforms-bootstrap5 is created, open sourced under MIT license.
It's a simple Python library for rendering WTForms in Bootstrap 5 favor.

## Install

To install the formatter, simply run

```bash
pip install wtforms-bootstrap5
```

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
<form method="POST"><div class="mb-3"><label class="form-label" for="email">Email</label><input class="form-control" id="email" name="email" type="email" value=""></div>
<div class="mb-3"><label class="form-label" for="password">Password</label><input class="form-control" id="password" name="password" type="password" value=""><div class="form-text">Your super secret password</div></div>
<div class="mb-3"><label class="form-label" for="city">City</label><select class="form-select" id="city" name="city"><option value="Los Angle">Los Angle</option><option value="San Francisco">San Francisco</option><option value="New York">New York</option></select></div>
<div class="mb-3"><div class="form-check"><label class="form-check-label" for="agree_terms">I agrees to terms and service</label><input class="form-check-input" id="agree_terms" name="agree_terms" type="checkbox" value="y"></div></div>
<div class="mb-3"><input class="btn btn-primary" id="submit" name="submit" type="submit" value="Submit"></div></form>
```

And it will look like this

<p align="center">
  <img src="assets/default-style-example.png?raw=true" alt="Form rendered in Bootstrap 5 favor" />
</p>

By default, a sensible simple layout style will be used.

## Customize the form

There are many similar open source libraries out there, but most of them are very hard to customize.
Once you adopt it, then you can only render your form in a specific style.
As a result, I found myself writing HTML manually without using the library to save time.

To avoid the same mistake, we want to make wtforms-bootstrap5 very easy to customize without compromising too much of its reusability.
Here's an example how you can turn the example above into a column based form.

```python
html = (
    renderer_context
    .form(action="/sign-up")
    .default_field(
        row_class="row mb-3",
        label_class="form-label col-2",
        field_wrapper_class="col-10",
        field_wrapper_enabled=True,
    )
    .field(
        "agree_terms",
        wrapper_class="offset-2",
        wrapper_enabled=True,
        field_wrapper_enabled=False,
    )
    .field(
        "submit",
        field_wrapper_class="offset-2",
        field_wrapper_enabled=True,
    )
).render(form)
```

And this is how it looks like

<p align="center">
  <img src="assets/column-style-example.png?raw=true" alt="Form rendered in Bootstrap 5 favor" />
</p>

As you can see in the example, we use `default_field` method for overwriting the options of all fields by default.
We also use `field` method for overwriting the options for a specific field.
The `field` method takes multiple input name arguments, so that you can overwrite options for multiple fields at once like this

```python
html = (context
    .field("email", "password", label_class="my-custom-class", ...)
)
```

Please notice that, **the order of `default_field` and `field` method calls matter**.
When `field` is called, the current default field options will be used as the default values.
So if you make the calls in order like this

```python
html = (context
    .field("email", row_class="row")
    .default_field(label_class="my-custom-class")
)
```

The `label_class` for `email` field here will be `form-label` instead of `my-custom-class` since when it's called, the original default value was still `form-label`.

To customize the form element, you can use the `form` method like this

```python
html = (context
    .form(
        method="POST",
        action="/sign-up",
        enctype="application/x-www-form-urlencoded",
        form_class="my-form",
        form_attrs=dict(custom="value")
    )
)
```

### Field HTML structure

In general, the field HTML structure can be controlled by the option values and it looks like this

```html
<!-- enabled by .row_enabled, default: true -->
<div class=".row_class" {.row_attrs}>
  <!-- enabled by .wrapper_enabled, default: false -->
  <div class=".wrapper_class" {.wrapper_attrs}>
    <!-- enabled by .label_enabled, default: true -->
    <label class=".label_class" for="email" {.label_attrs}>Email</label>
    <!-- enabled by .field_wrapper_enabled, default: false -->
    <div class=".field_wrapper" {.field_wrapper_attrs}>
      <input class=".field_class" id="email" name="email" type="email" value="" {.field_attrs}>
      <!-- enabled by .help_enabled, default: true -->
      <div class=".help_class" {.helper_attrs}>Your super secret password</div>
      <!-- enabled by .error_enabled, default: true -->
      <div class=".error_class" {.error_attrs}>Bad password</div>
    </div>
  </div>
</div>
```

## Integrate with template engine

We want to make it as easy as possible to integrate with template engine such as [Jinja](https://jinja.palletsprojects.com/).
That's why we use chained method calls for customizing the form.
You should be able to pass the `form` and `RenderContext` objects and write all your form customization from the template.
This way, you don't get your view relative code pollute your controller code.
For example, after passing `form` and `render_context` object, you can write this in Jinja:

```html
<h1>New user</h1>

{{
    renderer_context
        .default_field(
            row_class="row mb-3",
            label_class="form-label col-2",
            field_wrapper_class="col-10",
            field_wrapper_enabled=True,
        )
        .field(
            "agree_terms",
            wrapper_class="offset-2",
            wrapper_enabled=True,
            field_wrapper_enabled=False,
        )
        .field(
            "submit",
            field_wrapper_class="offset-2",
            field_wrapper_enabled=True,
        )
    ).render(form)
}}
```

## Feedbacks

Feedbacks, bugs reporting or feature requests are welcome 🙌, just please open an issue.
No guarantee we have time to deal with them, but will see what we can do.
