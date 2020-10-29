# -*- coding: utf-8 -*-
import uuid

import flask
from flask import Blueprint, request, abort

from src.loggings.logger import logger
from src.util.util import delete_files
from src.util.yaml_tools import merge_yaml_files

log = logger(__name__)
api = Blueprint(__name__, __name__)


@api.route('/merge', methods=['POST'])
def merge():
    yamls = request.json
    input_files = []
    if yamls is None or isinstance(yamls, list) is False:
        abort(400, "Input error")
    for yaml in yamls:
        uid = uuid.uuid4().hex
        file_name = "/tmp/input-{}.yaml".format(uid)
        input_files.append(file_name)
        text_file = open(file_name, "w")
        text_file.write(yaml)
        text_file.close()

    merged_yaml_file = merge_yaml_files(input_files)
    file = open(merged_yaml_file, 'r')
    merged_yaml_str = file.read()
    file.close()
    input_files.append(merged_yaml_file)
    delete_files(input_files)
    resp = flask.Response(merged_yaml_str)
    resp.headers['Content-Type'] = 'text/plain'
    return resp, 200
