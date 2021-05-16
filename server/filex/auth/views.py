from flask import Blueprint, jsonify, make_response, request, abort, g

from .. import db
from ..models import BlacklistToken, User
from ..middleware import jwt_required
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
            'access_token': user.encode_token(),
            'refresh_token': user.encode_token(refresh=True)
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


@bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    user = User.query.get(g.user_id)
    token = user.encode_token()
    return jsonify({
        'token': token,
    }), 200


@bp.route('/logout', methods=['POST'])
@jwt_required(refresh=True)
@jwt_required()
def logout():
    access_token = request.headers['Authorization']
    blacklist_token = request.get_json()['refresh_token']
    blacklist_access_token = BlacklistToken(token=access_token)
    blacklist_refresh_token = BlacklistToken(token=blacklist_token)
    db.session.add(blacklist_access_token)
    db.session.add(blacklist_refresh_token)
    db.session.commit()
    return ('', 204)


@bp.route('/me', methods=['GET'])
@jwt_required()
def me():
    user = User.query.get(g.user_id)
    return jsonify({
        'id': user.id,
        'name': user.name
    }), 200
