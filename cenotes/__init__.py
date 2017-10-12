import os
from flask import Flask
from flask_migrate import Migrate
import nacl.secret
from cenotes.models import db
from cenotes import controllers, errors

migrate = Migrate()


def create_app(app_settings=None):
    app = Flask(__name__)
    app.config.from_object(app_settings or os.environ['APP_SETTINGS'])
    db.init_app(app)
    migrate.init_app(app, db)

    app.server_box = nacl.secret.SecretBox(app.config["SERVER_ENCRYPTION_KEY"])

    app.register_blueprint(controllers.notes_bp)
    app.register_blueprint(errors.error_bp)
    return app
