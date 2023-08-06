from importlib.util import module_from_spec
from django.template.context import make_context
from django.template.exceptions import TemplateSyntaxError
from django.template.backends.utils import csrf_input_lazy, csrf_token_lazy

from subjugate import SubjugateTemplate as SubjugateUserTemplate

import inspect
import re
import importlib.machinery


class SubjugateTemplate:
    def find_template_class(self, module, base_class):
        userclass = next(
            (
                cls
                for _, cls in inspect.getmembers(module, inspect.isclass)
                if cls.__module__ == module.__name__ and issubclass(cls, base_class)
            ),
            None,
        )

        if not userclass:
            raise TemplateSyntaxError("Templates must have a subjugate of SubjugateTemplate")

        return userclass

    def code_to_module(self, code, template_name):
        module_name = self.modulify(template_name)
        spec = importlib.machinery.ModuleSpec(name=module_name, loader=None, origin=self.origin)
        module = module_from_spec(spec)
        exec(code, module.__dict__)

        return module

    def modulify(self, template_name: str):
        # Remove any extensions.
        noext = re.sub(r"\..*$", "", template_name)

        # Split on any non asciibetical characters.
        words = re.split(r"\W+", noext)

        # Capitalize each word and join them back together.
        base = ".".join((w.lower() for w in words))

        # Prefix the class to ensure it doesn't start with a number.
        return f"subjugate.usertemplates.{base}"

    def classify(self, template_name: str):
        # Remove any extensions.
        noext = re.sub(r"\..*$", "", template_name)

        # Split on any non asciibetical characters.
        words = re.split(r"\W+", noext)

        # Capitalize each word and join them back together.
        base = "".join((w.capitalize() for w in words))

        # Prefix the class to ensure it doesn't start with a number.
        return f"SubjugateTemplate{base}"

    def __init__(self, contents, origin, template_name, engine):
        self.contents = contents
        self.origin = origin
        self.template_name = template_name
        self.engine = engine
        self.module = self.code_to_module(self.contents, template_name)
        self.userclass = self.find_template_class(self.module, SubjugateUserTemplate)

    def render(self, context, request, **kwargs):
        if isinstance(context, dict) or context is None:
            context = make_context(context, request, autoescape=self.engine.autoescape)

        if request is not None:
            context["request"] = request
            context["csrf_input"] = csrf_input_lazy(request)
            context["csrf_token"] = csrf_token_lazy(request)

        return self.userclass(self.engine, context, request).render(**kwargs)
