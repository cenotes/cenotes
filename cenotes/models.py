from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Note(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    max_visits = db.Column(db.Integer, default=1)
    visits_count = db.Column(db.Integer, default=0)
    payload = db.Column(db.Binary, nullable=False)
    expiration_date = db.Column(db.Date)

    def __init__(self, payload):
        self.payload = payload
