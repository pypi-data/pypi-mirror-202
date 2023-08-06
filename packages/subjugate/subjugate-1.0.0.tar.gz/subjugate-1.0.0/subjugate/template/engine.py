from typing import List, Tuple, Union
from django.core.exceptions import ImproperlyConfigured
from django.utils.module_loading import import_string
from django.template import Template
from django.template.engine import Engine
from django.template.backends.django import DjangoTemplates

from subjugate.template.loaders import GenericLoader


def derive_from_generic(loader_class, template_cls):
    generic_loader = type(
        f"{GenericLoader.__name__}{template_cls.__name__}",
        (GenericLoader,),
        {"template_cls": template_cls},
    )

    return type(f"Generic{loader_class.__name__}", (loader_class, generic_loader), {})


# This might seem weird but the engine class MUST be a subclass of
# of DjangoTemplates to support cache clearing on modification.
#
# See autoreload.py
class GenericEngine(Engine, DjangoTemplates):
    template_cls = Template
    app_dirname = "template"
    dirs_loader = "django.template.loaders.filesystem.Loader"
    appdirs_loader = "subjugate.template.loaders.app_directories.Loader"
    cache_loader = "django.template.loaders.cached.Loader"

    def __init__(
        self,
        dirs=[],
        app_dirs=False,
        builtins=None,
        context_processors=[],
        file_charset="UTF-8",
        debug=False,
        loaders=None,
        libraries=None,
        autoescape=True,
        **_,
    ):
        self.app_dirs = app_dirs
        self.context_processors = context_processors
        self.dirs = dirs
        self.file_charset = file_charset
        self.debug = debug
        self.autoescape = autoescape
        self.engine = self

        if loaders is None:
            self.loaders = self.get_default_loaders()
        else:
            self.loaders = loaders

        if libraries is None:
            libraries = {}
        if builtins is None:
            builtins = []

        self.libraries = libraries
        self.template_libraries = self.get_template_libraries(libraries)
        self.template_builtins = self.get_template_builtins(builtins + self.default_builtins)

        self.filters = {}
        for lib in self.template_builtins:
            self.filters.update(lib.filters)

    def __repr__(self):
        return f"<{self.__class__.__qualname__}>"

    def find_template_loader(self, loader):
        if isinstance(loader, (tuple, list)):
            loader, *args = loader
        else:
            args = []

        if isinstance(loader, str):
            loader_class = import_string(loader)
            derived_clss = derive_from_generic(loader_class, self.template_cls)
            return derived_clss(self, *args)
        else:
            raise ImproperlyConfigured(
                "Invalid value in template loaders configuration: %r" % loader
            )

    def get_default_loaders(self):
        loaders: List[Union[str, List, Tuple]] = [self.dirs_loader]
        if self.app_dirs:
            loaders.append((self.appdirs_loader, self.app_dirname))

        return [(self.cache_loader, loaders)]

    def get_template_loaders(self, template_loaders):
        return [ld for tl in template_loaders if (ld := self.find_template_loader(tl))]

    def from_string(self, template_code):
        self.template_cls(template_code, engine=self)

    def get_template(self, template_name):
        template, origin = self.find_template(template_name)
        if not hasattr(template, "render"):
            template = self.template_cls(template, origin, template_name, engine=self)
        return template
