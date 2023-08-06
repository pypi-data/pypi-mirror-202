# Subjugate

Write your Django templates with Python!

* All built-in Django loaders work.
* All built-in filters work.
* Caching and autoreloading works.

The missing companion library for Django to use
[dominate](https://pypi.org/project/dominate/) to write templates.

## Installation

```bash
pip install subjugate

# Subjugate doesn't actually depend on Domainate but it's highly highly recommended.
pip install domainate
```

```python
INSTALLED_APPS = [
    ...,
    "subjugate",
    ...
]

TEMPLATES = [
  ...,
  {
    "BACKEND": "subjugate.template.backends.subjugate.SubjugateTemplates",
    "DIRS": [],
    "APP_DIRS": True,
    "OPTIONS": {"debug": False},
  }
]
```

## Usage

Assuming you're using `APP_DIRS` create a file `yourapp/subjugate/yourapp/page.py`.

```python
from subjugate import SubjugateTemplate
from dominate import tags as t

class PageTemplate(SubjugateTemplate):
  def render(self, title="Page", description="Cool stuff here", **kwargs):
        document = dominate.document(title=title)
        abs_url = self.request.build_absolute_uri()

        with document.head:
            t.meta(name="charset", content="UTF-8")
            t.meta(name="viewport", content="width=device-width, initial-scale=1")
            t.title(title)
            t.script(
                """
                document.documentElement.classList.remove('no-js');\
                document.documentElement.classList.add('js');
                """,
                type="module",
            )
            t.base(href=f"{abs_url}")
            t.link(rel="canonical", href=f"{abs_url}")
            t.link(rel="author", href=f"{self.static('humans.txt')}")
            t.link(rel="license", href=f"{self.url('copyright')}")
            t.meta(name="description", cotent=description)
            t.meta(property="og:title", content=title)
            t.meta(property="og:locale", content="en_US")
            t.meta(property="og:type", content="website")
            t.meta(property="og:url", content=f"{abs_url}")

        with document:
          t.p("Hello World!")

        return document
```

Then in `urls.py`

```python
urlpatterns = [
  ...,
  path("page/", TemplateView.as_view(template_name="yourapp/page.py")),
]
```

## Template Reuse

```python
class BaseTemplate(SubjugateTemplate):
  def render(self, title="Blah", **kwargs):
    document = dominate.document(title=title)

    with document.head:
      t.title(title)

    return document

class DerivedTemplate(SubjugateTemplate):
  def render(self, **kwargs):
    base = self.extend("yourapp/base.py", title="Title Works")

    with base:
      t.p("Hello from the derived template!")

    return base
```

## Other Features

```python
class TemplateVars(SubjugateTemplate):
  def render(self, **kwargs):
    base = self.extend("yourapp/base.py", title="Title Works")

    with base:
      # Context Vars
      t.p(self.vars.message)

      # Page URLs
      t.p(self.url('yourapp/copyright.py'))

      # Static URLs
      t.p(self.static('yourapp/humans.txt'))

      # CSRF Tokens
      t.p(self.csrf_token())

      # Filters
      t.p(self.filter("upper", "yes"))

      # Lorem Ipsum
      t.p(self.lorem_words(count=15))
      t.p(self.lorem_paragraphs(count=3))

    return base
```

## But I don't want to use Domainate

Cool cool, like I said this library doesn't actually require Domainate. Just
make sure that the thing your `render` function returns has a `__str__` method
that actually outputs the renderd HTML.

## Authors

* Estelle Poulin ([dev@inspiredby.es](mailto:dev@inspiredby.es))
