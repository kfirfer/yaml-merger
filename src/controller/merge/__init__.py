# -*- coding: utf-8 -*-

from flask import Blueprint, request, jsonify, abort

from src.loggings.logger import logger

log = logger(__name__)
api = Blueprint(__name__, __name__)


@api.route('/merge', methods=['POST'])
def merge():
    yamls = request.json
    if not yamls:
        abort(500, "Area not created")
    return str(yamls), 200
