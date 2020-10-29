# -*- coding: utf-8 -*-
import os
import uuid

import flask
from flask import Blueprint, request, abort
from ruamel.yaml import round_trip_dump

from src.loggings.logger import logger
from src.util.yaml_tools import successive_merge

log = logger(__name__)
api = Blueprint(__name__, __name__)


def merge_yaml_files(input_files):
    uid = uuid.uuid4().hex
    file_name = "/tmp/output-{}.yaml".format(uid)
    file_contents = []
    for f in input_files:
        file = open(f, 'r')
        file_contents.append(file.read())
        file.close()
    out_content = successive_merge(file_contents)
    output_file = open(file_name, 'w')
    round_trip_dump(out_content, output_file)
    output_file.close()
    return file_name


def delete_files(files):
    for file in files:
        os.remove(file)


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
