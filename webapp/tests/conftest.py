import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
os.environ["FLASK_ENV"] = 'testing'

import pytest

from app.app import create_app
from app.extensions import db as _db


@pytest.fixture(scope="session")
def app():
    _app = create_app()

    with _app.app_context():
        yield _app


@pytest.fixture
def client(app):
    yield app.test_client()


@pytest.fixture
def test_request_context(app):
    with app.test_request_context() as req:
        yield req


@pytest.fixture(scope="session")
def db(app):
    """Ensure tables are created and dropped at the start and end of test runs."""
    with app.app_context():
        _db.create_all()

    yield _db

    # Explicitly close DB connection
    _db.session.close()
    _db.drop_all()


def _truncate_all_tables(db):
    tables = db.metadata.sorted_tables
    connection = db.engine.connect()
    transaction = connection.begin()
    connection.execute('PRAGMA foreign_keys = OFF;')  # SQLite specific
    for table in tables:
        connection.execute(table.delete())
    connection.execute('PRAGMA foreign_keys = ON;')  # SQLite specific
    transaction.commit()

@pytest.fixture
def transactional_session(db):
    """Reset DB to empty state after each test, allowing faster isolated tests."""
    yield db.session
    db.session.expunge_all()
    _truncate_all_tables(db)
