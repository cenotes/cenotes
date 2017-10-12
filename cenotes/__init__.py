import os
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import nacl.secret
from cenotes import controllers, errors


app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
db = SQLAlchemy(app)
migrate = Migrate(app, db)
server_box = nacl.secret.SecretBox(app.config["SERVER_ENCRYPTION_KEY"])

from cenotes.models import Note


app.register_blueprint(controllers.notes_bp)


@app.errorhandler(404)
def not_found(error):
    return jsonify(error=404, text="Not found"), 404


@app.errorhandler(errors.InvalidKeyORNoteError)
def invalid_key_or_note(error):
    return jsonify(error=400, text="Invalid key or note not found"), 400

