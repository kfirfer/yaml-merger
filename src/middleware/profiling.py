# -*- coding: utf-8 -*-
import time

from flask import g, request

from src.loggings.custom_json_format_log import json_serializer, SKIP_MESSAGE_IN_JSON_LOG
from src.loggings.logger import logger

log = logger(__name__)


def register_profiling(app):
    @app.before_request
    def before_request():
        g.start = int(round(time.time() * 1000))

    @app.after_request
    def after_request(response):
        try:
            if request.path == '/favicon.ico' or request.path.startswith('/static') or request.path == '/health':
                return response

            duration = int(round(time.time() * 1000)) - g.start
            ip = request.headers.get('X-Forwarded-For', request.remote_addr)
            request_rule = None
            if request.url_rule and request.url_rule.rule:
                request_rule = request.url_rule.rule

            props = {
                "method": request.method,
                "request_rule": request_rule,
                "request_path": request.full_path,
                "status": response.status_code,
                "took": duration,
                "ip_address": ip
            }
            if response.status_code >= 500:
                props["response"] = "Response: {}".format(response.data)
                if hasattr(response, "error_id"):
                    props["error_id"] = response.error_id
                log.error(json_serializer(props), extra={"props": props, SKIP_MESSAGE_IN_JSON_LOG: True})
            elif response.status_code >= 400:
                props["response"] = "Response: {}".format(response.data)
                log.warning(json_serializer(props), extra={"props": props, SKIP_MESSAGE_IN_JSON_LOG: True})
            else:
                log.info(json_serializer(props), extra={"props": props, SKIP_MESSAGE_IN_JSON_LOG: True})
        except Exception as e:
            log.exception(e)
        return response
