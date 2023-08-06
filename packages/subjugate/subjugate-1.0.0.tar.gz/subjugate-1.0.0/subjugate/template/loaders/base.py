from django.template.loaders import base
from django.template import TemplateDoesNotExist, Template

# Despite deriving from base.Loader this class is actually more generic and can
# be used to leverage the Django template loader ecosystem for any kind of
# template.
class GenericLoader(base.Loader):
    template_cls = Template

    def __init__(self, engine):
        self.engine = engine

    def get_contents(self, _):
        return NotImplemented("Subclasses must implement get_contents")

    def get_template(self, template_name, skip=None):
        tried = []

        for origin in self.get_template_sources(template_name):
            if skip is not None and origin in skip:
                tried.append((origin, "Skipped to avoid recursion"))
                continue

            try:
                contents = self.get_contents(origin)
            except TemplateDoesNotExist:
                tried.append((origin, "Source does not exist"))
                continue
            else:
                return self.template_cls(
                    contents,
                    origin,
                    origin.template_name,
                    self.engine,
                )

        raise TemplateDoesNotExist(template_name, tried=tried)

    def from_string(self, template_code):
        return self.template_cls(template_code, self.engine)
