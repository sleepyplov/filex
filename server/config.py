import os

class Config(object):
    BASEDIR = os.path.abspath(os.path.dirname(__file__))
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = 'secretkey'
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URI']
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    STORAGE_ROOT = os.environ['STORAGE_ROOT']


class ProductionConfig(Config):
    ENV = 'production'
    DEBUG = False
    SECRET_KEY = os.environ.get('SECRET_KEY')


class DevelopmentConfig(Config):
    ENV = 'development'
    DEVELOPMENT = True
    DEBUG = True
