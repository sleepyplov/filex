from pathlib import Path
import shutil

from flask import Blueprint, jsonify, g, current_app, make_response, abort
import jwt

from ..middleware import jwt_required   
from .validators import get_requested_path, validate_folder_request


bp = Blueprint('storage', __name__, url_prefix='/storage')


@bp.route('/dir', methods=['GET'])
@jwt_required()
def list_dir():
    path = validate_folder_request(get_requested_path())
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


@bp.route('/dir', methods=['POST'])
@jwt_required()
def make_dir():
    path = validate_folder_request(get_requested_path(), must_exist=False)
    try:
        path.mkdir()
        return jsonify({
            'dir': path.stat() # TODO: return only needed fields
        }), 201
    except OSError as e:
        current_app.logger.error('Failed to create directory %(path)s for user %(user)s', path, g.user)
        return jsonify({
            'error': 'Failed to create folder.',
        }), 500


@bp.route('/dir', methods=['DELETE'])
@jwt_required()
def delete_dir():
    path = validate_folder_request(get_requested_path())
    if path == g.user.get_home_path():
        abort(make_response(jsonify({
            'error': 'Cannot delete home path.'
        }), 400))
    try:
        shutil.rmtree(path)
        return '', 204
    except OSError as e:
        current_app.logger.error('Failed to delete directory %(path)s for user %(user)s', path, g.user.name)
        return jsonify({
            'error': 'Failed to delete folder.',
        }), 500

