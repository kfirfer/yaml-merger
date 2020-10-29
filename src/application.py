# -*- coding: utf-8 -*-
import code
import os
import signal
import traceback

from flask import Flask
from flask_cors import CORS

import src
from src.loggings.custom_json_format_log import CustomJSONLog
from src.util.util import Singleton


class Application(metaclass=Singleton):
    app = None

    def __init__(self):
        self.app = Flask(__name__)
        self.__load()

    def __load(self):
        if "TEST_MODE" not in os.environ or os.environ["TEST_MODE"] == "0":
            from flask import send_from_directory

            @self.app.route('/static/<path:path>')
            def send_js(path):
                return send_from_directory('static', path)
        if 'ENABLE_CORS' in os.environ and os.environ['ENABLE_CORS'] == "1":
            CORS(self.app)
        import logging
        log = logging.getLogger('werkzeug')
        log.setLevel(logging.WARNING)
        with self.app.app_context():
            from src.middleware import register_middleware
            register_middleware(self.app)
            from src.controller import register_blueprint
            register_blueprint(self.app)

    def run(self):
        src.loggings.init(custom_formatter=CustomJSONLog)
        if 'DEV_MODE' in os.environ and os.environ['DEV_MODE'] == "1":
            self.app.run(host="0.0.0.0", debug=False, port=int(os.environ["SERVER_PORT"]))
        else:
            from waitress import serve
            number_of_threads = 4
            if 'NUMBER_OF_THREADS' in os.environ:
                number_of_threads = int(os.environ["NUMBER_OF_THREADS"])
            serve(self.app, host="0.0.0.0", port=int(os.environ["SERVER_PORT"]), threads=number_of_threads, _quiet=True)

    def get_app(self):
        return self.app


def debug_process(sig, frame):
    """Interrupt running process, and provide a python prompt for
    interactive debugging."""
    d = {'_frame': frame}  # Allow access to frame object.
    d.update(frame.f_globals)  # Unless shadowed by global
    d.update(frame.f_locals)

    i = code.InteractiveConsole(d)
    message = "Signal received : entering python shell.\nTraceback:\n"
    message += ''.join(traceback.format_stack(frame))
    i.interact(message)


def listen():
    from sys import platform
    if platform == "win32":
        return
    signal.signal(signal.SIGUSR1, debug_process)  # Register handler
