import os

from dotenv import load_dotenv
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

load_dotenv()

app = Flask('filex')
app.config.from_object(os.environ['APP_SETTINGS'])

db = SQLAlchemy(app)

@app.route('/')
def index():
    return 'Hello World!'
