from pathlib import Path

from flask import Blueprint, jsonify, g
from flask.globals import current_app

from ..middleware import jwt_required   
from .validators import validate_folder_request


bp = Blueprint('storage', __name__, url_prefix='/storage')


@bp.route('/dir', methods=['GET'])
@jwt_required()
def get_folder():
    req_data = validate_folder_request()
    if 'error' in req_data:
        return jsonify({
            'error': req_data['error']
        }), 400
    path = req_data['path']
    if not g.user.is_allowed_path(path):
        return jsonify({
            'error': 'Not allowed location.'
        }), 403
    path = Path(current_app.config['STORAGE_ROOT']).joinpath(str(g.user.id), path).resolve()
    if not (path.exists() and path.is_dir()):
        return jsonify({
            'error': 'Folder not found.'
        }), 404
    files = []
    folders = []
    for item in path.iterdir(): # TODO: refactor config usage and paths formation
        if item.is_file():
            files.append(str(item.relative_to(Path(current_app.config['STORAGE_ROOT']) / str(g.user.id))))
        else:
            folders.append(str(item.relative_to(Path(current_app.config['STORAGE_ROOT']) / str(g.user.id))))
    return jsonify({
        'files': files,
        'folders': folders
    }), 200
    