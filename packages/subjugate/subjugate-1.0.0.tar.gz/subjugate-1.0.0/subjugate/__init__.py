__version__ = "0.0.1"

from abc import ABC, abstractmethod
from django.urls import reverse
from django.apps import apps
from django.utils.encoding import iri_to_uri
from urllib.parse import quote, urljoin
from django.utils.lorem_ipsum import paragraphs, words
from types import SimpleNamespace


class SubjugateTemplate(ABC):
    def __init__(self, engine, context, request):
        self.engine = engine
        self.context = context
        self.request = request
        self.vars = SimpleNamespace(**self.context.flatten())

    def extend(self, template_name, **kwargs):
        return self.engine.get_template(template_name).render(self.context, self.request, **kwargs)

    def csrf_token(self):
        return self.context.get("csrf_token", "") if self.context else ""

    def csrf_input(self):
        return str(self.context.get("csrf_input", "")) if self.context else ""

    def url(self, path):
        return reverse(path)

    def static(self, path):
        # Damn, I thought doing this was janky as hell but it's official!
        if apps.is_installed("django.contrib.staticfiles"):
            from django.contrib.staticfiles.storage import staticfiles_storage

            return staticfiles_storage.url(path)
        else:
            try:
                from django.conf import settings
            except ImportError:
                prefix = ""
            else:
                prefix = iri_to_uri(getattr(settings, "STATIC_URL", ""))
            return urljoin(prefix, quote(path))

    def filter(self, name, value):
        return self.engine.filters[name](value)

    def lorem_words(self, count=1, common=True):
        return words(count, common).split(" ")

    def lorem_paragraphs(self, count=1, common=True):
        return paragraphs(count, common)

    @abstractmethod
    def render(**kwargs):
        pass
