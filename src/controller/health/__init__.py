# -*- coding: utf-8 -*-

from flask import Blueprint

health_blueprint = Blueprint(__name__, __name__)


@health_blueprint.route('/health', methods=['GET'])
def health_app_controller():
    return "", 200
