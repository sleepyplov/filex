import os
from pathlib import Path

from flask import request, current_app, g


def validate_folder_request(query=False, must_exist=True):
    req_data = request.args if query else request.get_json()
    if not req_data:
        return {
            'error': 'Bad request.',
            'status': 400,
        }
    if not (type(req_data.get('path')) is str):
        return {
            'error': 'Path invalid or not provided.',
            'status': 400,
        }

    path = Path(current_app.config['STORAGE_ROOT']).joinpath(str(g.user.id), req_data['path']).resolve()
    if not g.user.is_allowed_path(path):
        return {
            'error': 'Not allowed location.',
            'status': 403,
        }
    if must_exist and not (path.exists() and path.is_dir()):
        return {
            'error': 'No such folder.',
            'status': 404,
        }
    if not must_exist and path.exists():
        return {
            'error': 'This folder already exists',
            'status': 409,
        }
    return {**req_data, 'path': path}
