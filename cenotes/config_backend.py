import os
import binascii
from cenotes.utils import crypto


def is_url_base64_encoded(what):
    try:
        crypto.url_safe_decode(what)
    except binascii.Error:
        return False
    else:
        return True


class Config(object):
    DEBUG = DEVELOPMENT = TESTING = False

    # Define the application directory
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))

    # Define the database - we are working with
    # SQLite for this example
    SQLALCHEMY_DATABASE_URI = os.getenv("DB_URI", 'sqlite:///{0}'.format(
        os.path.join(BASE_DIR, 'cenotes.sqlite3')))
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DATABASE_CONNECT_OPTIONS = {}

    # Enable protection against *Cross-site Request Forgery (CSRF)*
    CSRF_ENABLED = True

    # Use a secure, unique and absolutely secret key for
    # signing the data.
    CSRF_SESSION_KEY = os.getenv("CSRF_KEY", crypto.generate_random_chars())

    # Secret key for signing cookies
    SECRET_KEY = os.getenv("SECRET_KEY", crypto.generate_random_chars())

    # Server key must be 32-bytes long
    SERVER_ENCRYPTION_KEY = os.getenv("SERVER_ENCRYPTION_KEY", "").encode()
    if is_url_base64_encoded(SERVER_ENCRYPTION_KEY):
        SERVER_ENCRYPTION_KEY = crypto.url_safe_decode(SERVER_ENCRYPTION_KEY)

    if SERVER_ENCRYPTION_KEY and len(SERVER_ENCRYPTION_KEY) != 32:
        raise RuntimeError("Key must be 32 bytes long\n"
                           "Leave it empty if you want to autogenerate one")


class Production(Config):
    DEBUG = DEVELOPMENT = TESTING = False


class Development(Config):
    DEBUG = True
    DEVELOPMENT = True


class Testing(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.getenv("TEST_DB_URI", 'sqlite:///{0}'.format(
        os.path.join(Config.BASE_DIR, 'cenotes_test.sqlite3')))
