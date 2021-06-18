from _pytest.config import create_terminal_writer
import pytest

from filex import create_app, db as app_db


@pytest.fixture(scope='session')
def client():
    app = create_app(mode='test')
    return app.test_client()


@pytest.fixture
def db():
    try:
        app_db.create_all()
        yield app_db
    finally:
        db.drop_all()
