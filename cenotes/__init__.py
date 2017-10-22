import os
import sys
from flask import Flask
from flask_migrate import Migrate
import nacl.secret
from cenotes.models import db
from cenotes import controllers, errors
from cenotes.utils.crypto import generate_random_chars, url_safe_encode

migrate = Migrate()

if sys.version_info[0] < 3:
    raise RuntimeError("Must be using Python 3!")


def create_app(app_settings=None):
    app = Flask(__name__)
    app.config.from_object(app_settings or os.environ.get('APP_SETTINGS')
                           or "cenotes.config_backend.Production")
    db.init_app(app)
    migrate.init_app(app, db)

    def gen_server_key():
        print("No encryption key set\nGenerating one...")
        auto_key = generate_random_chars(32)
        print("Your key is: \n{0}\n".format(url_safe_encode(auto_key)))
        return auto_key

    key = app.config["SERVER_ENCRYPTION_KEY"] or gen_server_key()
    app.server_box = nacl.secret.SecretBox(key)

    app.register_blueprint(controllers.notes_bp)
    app.register_blueprint(errors.error_bp)
    return app
