import jwt
import datetime

from flask import current_app
from werkzeug.security import generate_password_hash, check_password_hash

from . import db

class User(db.Model):
    __tablename__ = 'users'
    pk = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(), unique=True, nullable=False)
    password = db.Column(db.String(), nullable=False)

    def __init__(self, name, password):
        self.name = name
        self.password = generate_password_hash(password)

    def __repr__(self):
        return '<User #{0} {1}>'.format(self.pk, self.name)

    def set_password(self, password):
        self.password = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password, password)
    
    def encode_token(self):
        payload = {
            'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=1800),
            'iat': datetime.datetime.utcnow(),
            'sub': self.pk,
        }
        try:
            return jwt.encode(payload, current_app.config['SECRET_KEY'], algorithm='HS256')
        except Exception as e:
            raise e # TODO: log errors
    
    @staticmethod
    def decode_token(token):
        try:
            if BlacklistToken.check_blacklist(token):
                return {
                    'error': 'Token is blacklisted.'
                }
            payload = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
            return payload
        except jwt.ExpiredSignatureError:
            return {
                'error': 'Token expired.'
            }
        except jwt.InvalidTokenError:
            return {
                'error': 'Invalid token.'
            }


class BlacklistToken(db.Model):
    __tablename__ = 'blacklist_tokens'

    pk = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String, unique=True, nullable=False)
    blacklisted_on = db.Column(db.DateTime, nullable=True)

    def __init__(self, token):
        self.token = token
        self.blacklisted_on = datetime.datetime.now()
    
    def __repr__(self):
        return '<Token {}'.format(self.token)
    
    @staticmethod
    def check_blacklist(token):
        token = BlacklistToken.query.filter_by(token=token).first()
        if token:
            return True
        return False
