import os
import nacl.utils


def generate_random_chars(size=32):
    return nacl.utils.random(size)


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
    CSRF_SESSION_KEY = os.getenv("CSRF_KEY", generate_random_chars())

    # Secret key for signing cookies
    SECRET_KEY = os.getenv("SECRET_KEY", generate_random_chars())
    SERVER_ENCRYPTION_KEY = os.getenv(
        "SERVER_ENCRYPTION_KEY", "").encode() or generate_random_chars()


class Production(Config):
    DEBUG = DEVELOPMENT = TESTING = False


class Development(Config):
    DEBUG = True
    DEVELOPMENT = True


class Testing(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///{0}'.format(
        os.path.join(Config.BASE_DIR, 'cenotes_test.sqlite3'))
    SERVER_ENCRYPTION_KEY = "TESTING_KEY".encode()
