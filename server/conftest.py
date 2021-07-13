from _pytest.config import create_terminal_writer
import pytest
from dotenv import load_dotenv

from filex import create_app, db


@pytest.fixture()
def client():
    load_dotenv()
    app = create_app('config/test.py')
    with app.app_context():
        db.create_all()
        yield app.test_client()
        db.session.close()
        db.drop_all()
