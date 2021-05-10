from flask import Blueprint, jsonify, make_response, request, abort

from .. import db
from ..models import BlacklistToken, User
from .validators import validate_user_data


bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/login', methods=['POST'])
def login():
    req_data = validate_user_data()
    if 'error' in req_data:
        return jsonify({
            'error': req_data['error']
        })
    username = req_data['username']
    password = req_data['password']
    user = User.query.filter_by(name=username).first()
    if user and user.check_password(password):
        return jsonify({
            'token': user.encode_token()
        }), 200
    return jsonify({
        'error': 'Invalid username or password'
    }), 401


@bp.route('/register', methods=['POST'])
def register():
    req_data = validate_user_data()
    if 'error' in req_data:
        return jsonify({
            'error': req_data['error'],
        }), 400
    username = req_data['username']
    password = req_data['password']
    user = User.query.filter_by(name=username).first()
    if user:
        return jsonify({
            'error': 'Username already taken'
        }), 409
    user = User(username, password)
    db.session.add(user)
    db.session.commit()
    return jsonify({
        'user': {
            'name': user.name,
        }
    }), 201


@bp.route('/refresh', methods=['GET'])
def refresh():
    token = request.headers.get('Authorization')
    if not token:
        return jsonify({
            'error': 'Missing authorization token.'
        }), 401
    parsedToken = User.decode_token(token)
    if 'error' in parsedToken:
        return jsonify({
            'error': parsedToken['error']
        }), 401
    user = User.query.get(parsedToken['sub'])
    token = user.encode_token()
    return jsonify({
        'token': token,
    }), 200


@bp.route('/logout', methods=['GET'])
def logout():
    token = request.headers.get('Authorization')
    if not token:
        return jsonify({
            'error': 'Missing authorization token.'
        }), 401
    parsedToken = User.decode_token(token)
    if 'error' in parsedToken:
        return jsonify({
            'error': parsedToken['error']
        }), 401
    blacklist_token = BlacklistToken(token=token)
    db.session.add(blacklist_token)
    db.session.commit()
    return ('', 204)