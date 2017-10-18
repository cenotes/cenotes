from datetime import date, timedelta
import pytest
from sqlalchemy.orm.exc import NoResultFound
from cenotes import models


def test_note_has_expired(old_note):
    assert old_note.has_expired


def test_note_too_many_visits(db, note):
    note.max_visits = 0
    db.session.add(note)
    db.session.commit()
    assert note.has_expired is False
    assert note.should_not_exist


def test_fetch_note(note):
    assert models.fetch_note(note.id) is not None


def test_fetch_expired_note(db, note):
    note.expiration_date = date.today() - timedelta(weeks=1)
    db.session.add(note)
    db.session.commit()
    with pytest.raises(NoResultFound):
        models.fetch_note(note.id)


def test_update_note(db, note):
    note.max_visits = 2
    db.session.add(note)
    db.session.commit()
    assert note.visits_count == 0
    models.update_note(note)
    assert note.visits_count == 1


def test_update_note_delete(note):
    assert models.Note.query.count() == 1
    models.update_note(note)
    assert models.Note.query.count() == 0


def test_fetch_note_paranoid(note):
    assert models.Note.query.count() == 1
    models.fetch_note(note.id)
    assert models.Note.query.count() == 0
