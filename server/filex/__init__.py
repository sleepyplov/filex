import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask('filex')
app.config.from_object(os.environ['APP_SETTINGS'])

db = SQLAlchemy(app)
from .models import User

@app.route('/')
def index():
    return 'Hello World!'
