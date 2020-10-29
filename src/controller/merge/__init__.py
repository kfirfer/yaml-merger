# -*- coding: utf-8 -*-
from flask import Blueprint, request, jsonify, abort
import uuid
from src.loggings.logger import logger

log = logger(__name__)
api = Blueprint(__name__, __name__)


def merge_yaml_files(input_files):
    pass


def delete_files(input_files):
    pass


@api.route('/merge', methods=['POST'])
def merge():
    yamls = request.json
    input_files = []
    if yamls is None or isinstance(yamls, list) is False:
        abort(400, "Input error")
    for yaml in yamls:
        uid = uuid.uuid4().hex
        file_name = "{}.yaml".format(uid)
        input_files.append(file_name)
        text_file = open(file_name, "w")
        text_file.write(yaml)
        text_file.close()

    merge_yaml_files(input_files)
    delete_files(input_files)
    return str(yamls), 200
