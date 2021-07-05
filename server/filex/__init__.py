from pathlib import Path
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_migrate import Migrate
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from werkzeug.wrappers import Response


db = SQLAlchemy()


def create_app(config):
    app = Flask('filex')
    app.logger.setLevel(20)
    app.logger.info('Starting Filex...')
    app.config.from_pyfile('base_config.py')
    config_path = Path(__file__).parent.parent.joinpath(config)
    app.logger.info('Loading configuration from %s', config_path)
    app.config.from_pyfile(config_path)

    app.logger.info('Initializing SQLAlchemy...')
    db.init_app(app)

    app.logger.info('Initializing Flask-Migrate...')
    Migrate(app, db)

    app.logger.info('Initializing Flask-CORS...')
    CORS(app)

    app.logger.info('Mounting app onto /api...')
    def default(environ, start_response):
        res = Response('Page not found', status=404, mimetype='text/plain')
        return res(environ, start_response)
    app.wsgi_app = DispatcherMiddleware(default, {'/api': app.wsgi_app})

    app.logger.info('Loading auth module...')
    from .auth.views import bp as auth_bp
    app.register_blueprint(auth_bp)

    app.logger.info('Loading storage module...')
    from .storage.views import bp as storage_bp
    app.register_blueprint(storage_bp)

    @app.route('/ping', methods=['GET'])
    def ping():
        return 'pong'
    
    
    return app
