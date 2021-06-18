import os
import datetime
from dotenv.main import load_dotenv

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS


load_dotenv()


class BaseConfig(object):
    BASEDIR = os.path.abspath(os.path.abspath(os.path.dirname(__file__)))
    DEBUG = False
    TESTING = False

    CSRF_ENABLED = True
    SECRET_KEY = 'secretkey'
    ACCESS_TOKEN_LIFETIME = datetime.timedelta(minutes=15)
    REFRESH_TOKEN_LIFETIME = datetime.timedelta(days=7)

    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URI']
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    STORAGE_ROOT = os.environ['STORAGE_ROOT']


db = SQLAlchemy()


def create_app(mode='prod'):
    app = Flask('filex')
    app.config.from_object(BaseConfig)
    app.config.from_pyfile(f'../config/{mode}.py')

    db.init_app(app)
    CORS(app)

    from .auth.views import bp as auth_bp
    from .storage.views import bp as storage_bp
    app.register_blueprint(auth_bp)
    app.register_blueprint(storage_bp)

    @app.route('/ping')
    def index():
        return 'pong'
    return app
