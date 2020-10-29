# -*- coding: utf-8 -*-
import importlib
import pkgutil

from src import API_VERSION
from src.controller.health import health_blueprint

INSTALLED_MODULES = [
    (__name__, 'api', '/{}'.format(API_VERSION))
]


def register_blueprint(app):
    app.register_blueprint(health_blueprint, url_prefix="/")
    for folder, attr, prefix in INSTALLED_MODULES:
        modules = import_submodules(folder)
        for module_name, module in modules.items():
            if hasattr(module, attr):
                blue_print = getattr(module, attr)
                if prefix.strip() == '/':
                    app.register_blueprint(blue_print)
                else:
                    app.register_blueprint(blue_print, url_prefix=prefix)


def import_submodules(package, recursive=True):
    if isinstance(package, str):
        package = importlib.import_module(package)
    results = {}
    for loader, name, is_pkg in pkgutil.walk_packages(package.__path__):
        full_name = package.__name__ + '.' + name
        results[full_name] = importlib.import_module(full_name)
        if recursive and is_pkg:
            results.update(import_submodules(full_name))
    return results
