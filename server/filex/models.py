import jwt
import datetime
import pathlib

import uuid
from flask import current_app, abort, jsonify, make_response
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.dialects.postgresql import UUID

from . import db

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = db.Column(db.String(), unique=True, nullable=False)
    password = db.Column(db.String(), nullable=False)
    tokens = db.relationship('RefreshToken')

    def __init__(self, name, password):
        self.name = name
        self.password = generate_password_hash(password)

    def __repr__(self):
        return '<User #{0} {1}>'.format(self.id, self.name)
    
    def init_folder(self):
        if not hasattr(self, 'id'):
            raise AttributeError('This user has no id! Save to database to get id.')
        pathlib.Path(current_app.config['STORAGE_ROOT']).joinpath(str(self.id)).mkdir(exist_ok=False);

    def set_password(self, password):
        self.password = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password, password)
    
    def issue_token_pair(self):
        try:
            at_payload = {
            'exp': datetime.datetime.utcnow() + current_app.config['ACCESS_TOKEN_LIFETIME'],
            'iat': datetime.datetime.utcnow(),
            'sub': str(self.id),
            }
            refresh_token = RefreshToken(self.id)
            db.session.add(refresh_token)
            db.session.commit()
            return {
                'access_token': jwt.encode(at_payload, current_app.config['SECRET_KEY'], algorithm='HS256'),
                'refresh_token': str(refresh_token.id)
            }
        except Exception as e:
            current_app.logger.critical('Failed to encode token for user %(user)s, error = %(error)s', self, e)
            abort(make_response(jsonify({
                'error': 'Server error, authentication failed.',
            }), 500))

    @staticmethod
    def decode_token(token: str):
        try:
            return jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'], options={
                'require': ['exp', 'iat', 'sub',]
            })
        except jwt.ExpiredSignatureError:
            return {
                'error': 'Token expired.'
            }
        except jwt.InvalidTokenError:
            return {
                'error': 'Invalid token.'
            }
    
    def get_home_path(self):
        return pathlib.Path(current_app.config['STORAGE_ROOT']).joinpath(str(self.id)).resolve()
    
    def is_allowed_path(self, path):
        user_home = pathlib.Path(current_app.config['STORAGE_ROOT']).joinpath(str(self.id)).resolve()
        return (user_home in path.parents) or (user_home == path)


class RefreshToken(db.Model):
    __tablename__ = 'tokens'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    iat = db.Column(db.DateTime, nullable=False)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('users.id'), nullable=False)

    def __init__(self, user_id):
        self.iat = datetime.datetime.now()
        self.user_id = user_id

    def __repr__(self):
        return '<Token {0}, iat: {1}'.format(self.id, self.iat)
