from flask import Blueprint, jsonify, make_response, request, abort, g

from .. import db
from ..models import User
from ..middleware import jwt_required, refresh_required
from .validators import validate_user_data


bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/login', methods=['POST'])
def login():
    req_data = validate_user_data()
    if 'error' in req_data:
        return jsonify({
            'error': req_data['error']
        }), 400
    username = req_data['username']
    password = req_data['password']
    user = User.query.filter_by(name=username).first()
    if user and user.check_password(password):
        return jsonify(user.issue_token_pair()), 200
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
    user.init_folder()
    return jsonify({
        'user': {
            'id': user.id,
            'name': user.name,
        }
    }), 201


@bp.route('/refresh', methods=['POST'])
@refresh_required
def refresh():
    g.user.tokens.remove(g.refresh_token)
    db.session.add(g.user)
    db.session.commit()
    return jsonify(g.user.issue_token_pair()), 200


@bp.route('/logout', methods=['POST'])
@jwt_required
def logout():
    g.user.tokens.clear()
    db.session.add(g.user)
    db.session.commit(g.user)
    return ('', 204)


@bp.route('/me', methods=['GET'])
@jwt_required
def me():
    return jsonify({
        'id': g.user.id,
        'name': g.user.name
    }), 200
