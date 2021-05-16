from functools import wraps
from flask import request, jsonify, g

from ..models import User


def _get_token(refresh=False):
    if refresh:
        data = request.get_json()
        if not data:
            return None
        return data.get('refresh_token')
    return request.headers.get('Authorization')


def jwt_required(refresh=False):
    def _jwt_required(view):
        @wraps(view)
        def wrapper(*args, **kwargs):
            token = _get_token(refresh)
            if not token:
                return jsonify({
                    'error': 'Missing auth token.'
                }), 401
            parsedToken = User.decode_token(token, refresh=refresh)
            if 'error' in parsedToken:
                return jsonify({
                    'error': parsedToken['error']
                }), 401
            g.user_id = parsedToken['sub']
            return view(*args, **kwargs)
        return wrapper
    return _jwt_required
