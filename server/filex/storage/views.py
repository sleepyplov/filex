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
        }), req_data['status']
    path = req_data['path']
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
    