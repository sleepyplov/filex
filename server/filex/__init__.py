import os

from dotenv import load_dotenv
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS


app = Flask('filex')
app.config.from_object(os.environ['APP_SETTINGS'])

db = SQLAlchemy(app)
CORS(app)

from .auth.views import bp as auth_bp
app.register_blueprint(auth_bp)

@app.route('/')
def index():
    return 'Hello, world'
