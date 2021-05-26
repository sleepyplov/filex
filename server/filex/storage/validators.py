import os
from pathlib import Path

from flask import request, current_app, g


def validate_folder_request(check_exists=False):
    req_data = request.args
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
    path = req_data['path']
    if not g.user.is_allowed_path(path):
        return {
            'error': 'Not allowed location.',
            'status': 403,
        }
    path = Path(current_app.config['STORAGE_ROOT']).joinpath(str(g.user.id), path).resolve()
    if check_exists:
        if not (path.exists() and path.is_dir()):
            return {
                'error': 'No such folder.',
                'status': 404,
            }
    return req_data + {'path': path}
