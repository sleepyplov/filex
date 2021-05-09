import jwt
import datetime

from flask import current_app
from werkzeug.security import generate_password_hash, check_password_hash

from . import db

class User(db.Model):
    __tablename__ = 'users'
    pk = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    password = db.Column(db.String())

    def __init__(self, name, password):
        self.name = name
        self.password = generate_password_hash(password)

    def __repr__(self):
        return '<User #{0} {1}>'.format(self.id, self.name)

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
            payload = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
            return payload['sub']
        except jwt.ExpiredSignatureError as e:
            raise e
        except jwt.InvalidTokenError as e:
            raise e
