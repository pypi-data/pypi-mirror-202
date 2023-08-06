from django.template.loaders import filesystem
from django.template.utils import get_app_template_dirs


class Loader(filesystem.Loader):
    def __init__(self, engine, app_dirname, *args):
        self.app_dirname = app_dirname
        super().__init__(engine, *args)

    def get_dirs(self):
        return get_app_template_dirs(self.app_dirname)
