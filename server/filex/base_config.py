from pathlib import Path
import os, datetime


SQLALCHEMY_TRACK_MODIFICATIONS = False

SECRET_KEY = 'secretkey'
ACCESS_TOKEN_LIFETIME = datetime.timedelta(minutes=15)
REFRESH_TOKEN_LIFETIME = datetime.timedelta(days=7)

STORAGE_ROOT = os.environ['STORAGE_ROOT']
