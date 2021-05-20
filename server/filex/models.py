from posixpath import abspath
from sys import path
import jwt
import datetime
import pathlib

import uuid
from flask import current_app
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.dialects.postgresql import UUID

from . import db

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = db.Column(db.String(), unique=True, nullable=False)
    password = db.Column(db.String(), nullable=False)

    def __init__(self, name, password):
        self.name = name
        self.password = generate_password_hash(password)

    def __repr__(self):
        return '<User #{0} {1}>'.format(self.id, self.name)
    
    def init_folder(self):
        if not hasattr(self, 'id'):
            raise AttributeError('This user has no id!') # TODO: log errors
        pathlib.Path(current_app.config['STORAGE_ROOT']).joinpath(str(self.id)).mkdir(exist_ok=False);

    def set_password(self, password):
        self.password = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password, password)
    
    def encode_token(self, refresh=False):
        lifetime = datetime.timedelta(days=7) if refresh else datetime.timedelta(seconds=1800)
        type = 'refresh' if refresh else 'access'
        payload = {
            'exp': datetime.datetime.utcnow() + lifetime,
            'iat': datetime.datetime.utcnow(),
            'sub': str(self.id),
            'type': type,
        }
        try:
            return jwt.encode(payload, current_app.config['SECRET_KEY'], algorithm='HS256')
        except Exception as e:
            raise e # TODO: log errors

    @staticmethod
    def decode_token(token: str, refresh=False):
        allowed_types = ['access', 'refresh']
        try:
            if BlacklistToken.check_blacklist(token):
                return {
                    'error': 'Token is blacklisted.'
                }
            payload = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'], options={
                'require': ['exp', 'iat', 'sub', 'type']
            })
            if payload['type'] not in allowed_types:
                return {
                    'error': 'Invalid token.',
                }
            if payload['type'] != 'refresh' and refresh:
                return {
                    'error': 'Invalid token.',
                }
            return payload
        except jwt.ExpiredSignatureError:
            return {
                'error': 'Token expired.'
            }
        except jwt.InvalidTokenError:
            return {
                'error': 'Invalid token.'
            }
    
    def is_allowed_path(self, path):
        abspath = pathlib.Path(current_app.config['STORAGE_ROOT']).joinpath(str(self.id), path).resolve()
        user_home = pathlib.Path(current_app.config['STORAGE_ROOT']).joinpath(str(self.id)).resolve()
        return (user_home in abspath.parents) or (user_home == abspath)


class BlacklistToken(db.Model):
    __tablename__ = 'blacklist_tokens'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    token = db.Column(db.String, unique=True, nullable=False)
    blacklisted_on = db.Column(db.DateTime, nullable=True)

    def __init__(self, token):
        self.token = token
        self.blacklisted_on = datetime.datetime.now()
    
    def __repr__(self):
        return '<Token {}'.format(self.token)
    
    @staticmethod
    def check_blacklist(token: str):
        token = BlacklistToken.query.filter_by(token=token).first()
        if token:
            return True
        return False
