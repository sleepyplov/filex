from _pytest.config import create_terminal_writer
import pytest
from dotenv import load_dotenv

from filex import create_app, db as app_db


@pytest.fixture(scope='session')
def client():
    load_dotenv()
    app = create_app('config/test.py')
    return app.test_client()


@pytest.fixture
def db():
    try:
        app_db.create_all()
        yield app_db
    finally:
        db.drop_all()
