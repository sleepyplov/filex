import os

ENV = 'production'
DEBUG = False
TESTING = True
SQLALCHEMY_DATABASE_URI = os.environ['TEST_DATABASE_URI']
