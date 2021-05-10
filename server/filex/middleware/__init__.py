from functools import wraps
from flask import request, jsonify, g

from ..models import User


def jwt_required(view):
    @wraps(view)
    def wrapper(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({
                'error': 'Missing authorization header.'
            }), 401
        parsedToken = User.decode_token(token)
        if 'error' in parsedToken:
            return jsonify({
                'error': parsedToken['error']
            }), 401
        g.user_id = parsedToken['sub']
        return view(*args, **kwargs)
    return wrapper
