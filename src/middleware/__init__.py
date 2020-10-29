# -*- coding: utf-8 -*-

from werkzeug.middleware.proxy_fix import ProxyFix

from src.middleware.profiling import register_profiling


def register_middleware(app):
    app.wsgi_app = ProxyFix(app.wsgi_app, x_for=2)
    register_profiling(app)