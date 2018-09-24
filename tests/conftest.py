from datetime import date, timedelta
import pytest
from cenotes import create_app, db as _db
from cenotes.config_backend import Testing
from cenotes.models import Note
from cenotes_lib import crypto


@pytest.fixture(name="app", scope="session")
def _app():
    return create_app(app_settings=Testing)


@pytest.fixture(scope="function")
def db(app):
    _db.drop_all()
    _db.app = app
    _db.create_all()
    yield _db
    _db.drop_all()


@pytest.fixture(scope="session", name="testing_key")
def _key():
    return crypto.craft_key_from_password("testing")


@pytest.fixture(scope="session", name="testing_box")
def _box(testing_key):
    return crypto.craft_secret_box(testing_key)


@pytest.fixture(scope="function", name="note")
def _note(db):
    note = Note(b"test")
    db.session.add(note)
    db.session.commit()
    return note


@pytest.fixture(scope="function", name="old_note")
def _old_note(db):
    note = Note(b"test", expiration_date=date.today() - timedelta(weeks=36))
    db.session.add(note)
    db.session.commit()
    return note
