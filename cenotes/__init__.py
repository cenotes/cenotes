import os
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from cenotes import controllers, errors


app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from cenotes.models import Note


app.register_blueprint(controllers.notes_bp)

@app.errorhandler(404)
def not_found(error):
    return jsonify(error=404, text="Not found"), 404


@app.errorhandler(errors.InvalidKeyORNoteError)
def invalid_key_or_note(error):
    return jsonify(error=400, text="Invalid key or note note found"), 400

