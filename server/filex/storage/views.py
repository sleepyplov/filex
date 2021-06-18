from logging import error
from pathlib import Path
import shutil

from flask import Blueprint, jsonify, g, current_app, make_response, abort, request

from ..middleware import jwt_required   
from .validators import get_requested_path, validate_folder_request
from .. import logger


bp = Blueprint('storage', __name__, url_prefix='/storage')


@bp.route('/dir', methods=['GET'])
@jwt_required
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
@jwt_required
def make_dir():
    path = validate_folder_request(get_requested_path(), must_exist=False)
    try:
        path.mkdir()
        return jsonify({
            'dir': path.stat() # TODO: return only needed fields
        }), 201
    except OSError as e:
        logger.error('Failed to create directory', path=path, userID=g.userid, error=e)
        return jsonify({
            'error': 'Failed to create folder.',
        }), 500


@bp.route('/dir', methods=['DELETE'])
@jwt_required
def delete_dir():
    path = validate_folder_request(get_requested_path())
    if path == g.user.get_home_path():
        abort(make_response(jsonify({
            'error': 'Cannot delete home path.'
        }), 403))
    try:
        shutil.rmtree(path)
        return '', 204
    except OSError as e:
        logger.error('Failed to delete directory', path=path, userID=g.user.id, error=e)
        return jsonify({
            'error': 'Failed to delete folder.',
        }), 500


@bp.route('/dir', methods=['PUT'])
@jwt_required
def move_dir():
    src_path = validate_folder_request(get_requested_path())
    dst_path = validate_folder_request(get_requested_path(json=True), must_exist=False)
    if src_path in dst_path.parents:
        return jsonify({
            'error': 'Cannot move directory into itself.'
        }), 400
    copy = 'copy' in request.args
    if src_path == g.user.get_home_path():
        return jsonify({
            'error': 'Cannot move home directory.',
        }), 403
    try:
        if copy:
            shutil.copytree(src_path, dst_path)
        else:
            shutil.move(src_path, dst_path)
        return '', 204
    except OSError as e:
        logger.error('Failed to move directory',
            src_path=src_path, dst_path=dst_path, userID=g.user.id, error=e)
        return jsonify({
            'error': 'Failed to move directory.',
        }), 500
