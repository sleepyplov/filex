import datetime
from functools import wraps
from flask import request, jsonify, g
from flask.globals import current_app

from ..models import User, RefreshToken


def jwt_required(view):
    @wraps(view)
    def wrapper(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({
                'error': 'Missing auth token.'
            }), 401
        parsedToken = User.decode_token(token)
        if 'error' in parsedToken:
            return jsonify({
                'error': parsedToken['error']
            }), 401
        g.user = User.query.get(parsedToken['sub'])
        return view(*args, **kwargs)
    return wrapper


def refresh_required(view):
    @wraps(view)
    def wrapper(*args, **kwargs):
        req_data = request.get_json()
        if not req_data:
            return jsonify({
                'error': 'Bad request.',
            }), 400
        req_token = req_data.get('refresh_token')
        if not (type(req_token) is str):
            return jsonify({
                'error': 'Refresh token missing or invalid.',
            }), 400
        db_token = RefreshToken.query.get(req_token)
        if not db_token:
            return jsonify({
                'error': 'Refresh token not found.',
            }), 404
        if datetime.datetime.now() > db_token.iat + current_app.config['REFRESH_TOKEN_LIFETIME']:
            return jsonify({
                'error': 'Token expired.'
            }), 401
        g.refresh_token = db_token
        g.user = User.query.get(db_token.user_id)
        return view(*args, **kwargs)
    return wrapper
