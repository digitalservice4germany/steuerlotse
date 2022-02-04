import os
import sys
from unittest.mock import MagicMock

import fakeredis

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
os.environ["FLASK_ENV"] = 'testing'

from contextlib import contextmanager
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


CURRENT_USER_IDNR = "0123456789"


@pytest.fixture(autouse=True)
def testing_current_user(monkeypatch):
    monkeypatch.setattr("app.forms.session_data.current_user", MagicMock(idnr_hashed=CURRENT_USER_IDNR))


@pytest.fixture(autouse=True)
def testing_database(monkeypatch):
    fakeredis_connection = fakeredis.FakeStrictRedis()
    monkeypatch.setattr("app.data_access.form_data_controller.FormDataController._redis_connection",
                        fakeredis_connection)
    yield
    fakeredis_connection.flushall()


@pytest.fixture
def new_test_request_context(app):
    @contextmanager
    def _new_test_request_context(method='GET', form_data=None, stored_data=None, session_identifier='form_data'):
        from app.forms.session_data import serialize_session_data
        from app.data_access.form_data_controller import FormDataController
        with app.test_request_context() as req:
            req.request.method = method
            if stored_data:
                FormDataController().save_to_redis(CURRENT_USER_IDNR + '_' + session_identifier,
                                                   serialize_session_data(stored_data))
            else:
                FormDataController().save_to_redis(CURRENT_USER_IDNR + '_' + session_identifier,
                                                   serialize_session_data(form_data))
            yield req

    return _new_test_request_context


@pytest.fixture
def test_request_context_with_person_b_disability(app):
    from app.forms.session_data import serialize_session_data
    from app.data_access.form_data_controller import FormDataController
    with app.test_request_context(method="POST") as req:
        FormDataController().save_to_redis(CURRENT_USER_IDNR + '_form_data',
                                            serialize_session_data({'person_b_has_disability': 'yes'}))
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
