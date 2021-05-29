import os
from pathlib import Path

from flask import request, current_app, g, make_response, abort
from flask.json import jsonify


def get_requested_path(json=False):
    req_data = request.get_json() if json else request.args
    if not req_data:
        abort(make_response(jsonify({
            'error': 'Bad request.'
        }), 400))
    if not (type(req_data.get('path')) is str):
        abort(make_response(jsonify({
            'error': 'Path invalid or not provided.',
        }), 400))
    return req_data['path']


def validate_folder_request(path, must_exist=True):
    path = Path(current_app.config['STORAGE_ROOT']).joinpath(str(g.user.id), path).resolve()
    if not g.user.is_allowed_path(path):
        abort(make_response(jsonify({
            'error': 'Not allowed location.',
        }), 403))
    if must_exist and not (path.exists() and path.is_dir()):
        abort(make_response(jsonify({
            'error': 'Folder not found.',
        }), 404))
    if not must_exist and path.exists():
        abort(make_response(jsonify({
            'error': 'This folder already exists.'
        }), 409))
    return path
