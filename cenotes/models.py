from datetime import date
from dateutil import parser
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm.exc import NoResultFound

db = SQLAlchemy()


class Note(db.Model):
    DEFAULT_MAX_VISITS = 1
    DEFAULT_VISITS_COUNT = 0

    id = db.Column(db.Integer, primary_key=True)
    max_visits = db.Column(db.Integer, default=DEFAULT_MAX_VISITS)
    visits_count = db.Column(db.Integer, default=DEFAULT_VISITS_COUNT)
    payload = db.Column(db.Binary, nullable=False)
    expiration_date = db.Column(db.Date)

    def __init__(self, payload, max_visits=DEFAULT_MAX_VISITS,
                 visits_count=DEFAULT_VISITS_COUNT, expiration_date=None):
        try:
            self.payload = payload.encode()
        except AttributeError:
            self.payload = payload
        self.expiration_date = expiration_date or date.today()
        self.max_visits = max_visits
        self.visits_count = visits_count

    @property
    def iso_expiration_date(self):
        return (self.expiration_date.isoformat()
                if self.expiration_date else None)

    @property
    def has_expired(self):
        return self.expiration_date and self.expiration_date < date.today()

    @property
    def should_not_exist(self):
        return self.has_expired or self.visits_count >= self.max_visits


def create_new_note(cen_parameters, payload):
    new_note = Note(payload)
    try:
        new_note.expiration_date = parser.parse(cen_parameters.expiration_date)
    except (OverflowError, ValueError, TypeError):
        new_note.expiration_date = None
    new_note.visits_count = cen_parameters.visits_count
    new_note.max_visits = cen_parameters.max_visits
    db.session.add(new_note)
    db.session.commit()
    return new_note


def update_note(note):
    note.visits_count += 1

    if note.should_not_exist:
        db.session.delete(note)

    db.session.commit()


def fetch_note(note_id):
    note = Note.query.filter_by(id=note_id).one()

    if note.should_not_exist:
        db.session.delete(note)
        db.session.commit()
        raise NoResultFound()

    note_payload = note.payload
    update_note(note)

    return note_payload


def delete_note(note_id):
    db.session.delete(Note.query.filter_by(id=note_id).one())
    db.session.commit()


def get_expired_notes():
    return Note.query.filter(Note.expiration_date < date.today())
