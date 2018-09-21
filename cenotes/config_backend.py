import os
import binascii
import json
from collections import namedtuple
from cenotes_lib import crypto, exceptions

AlgoParam = namedtuple("AlgoParam", ['algorithm', 'hardness'])


def validate_algorithm_params(params):
    supported = crypto.SUPPORTED_ALGORITHM_PARAMS

    def verify_options(algo):
        return (algo.algorithm,
                tuple(filter(lambda x: supported.get(algo.algorithm, {}).get(
                    'hardness', {}).get(x) is None,
                             algo.hardness)))

    return tuple(filter(lambda x: x[-1] != (), map(verify_options, params)))


def is_url_base64_encoded(what):
    try:
        crypto.url_safe_decode(what)
    except (binascii.Error, exceptions.CenotesError):
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

    SUPPORTED_ALGORITHM_PARAMS = (
            json.loads(os.getenv("SUPPORTED_ALGORITHM_PARAMS", '{}'))
            or
            {algo: {"hardness": hardness}
             for algo, hardness in tuple(
                crypto.get_supported_algorithm_options())}
    )

    FALLBACK_ALGORITHM_PARAMS = {
        "algorithm": os.getenv("FALLBACK_ALGORITHM") or "scrypt",
        "hardness": os.getenv("FALLBACK_ALGORITHM_HARDNESS") or "interactive"
    }


class Production(Config):
    DEBUG = DEVELOPMENT = TESTING = False


class Development(Config):
    DEBUG = True
    DEVELOPMENT = True


class Testing(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.getenv("TEST_DB_URI", 'sqlite:///{0}'.format(
        os.path.join(Config.BASE_DIR, 'cenotes_test.sqlite3')))

    FALLBACK_ALGORITHM_PARAMS = {
        "algorithm": os.getenv("FALLBACK_ALGORITHM") or "scrypt",
        "hardness": os.getenv("FALLBACK_ALGORITHM_HARDNESS") or "min"
    }


def validate_crypto_configuration(config):
    algorithm_params = config["SUPPORTED_ALGORITHM_PARAMS"]
    if not isinstance(algorithm_params, dict):
        raise RuntimeError("Algorithm params must be of dict type."
                           "See the docs for more info")

    unsupported = validate_algorithm_params(
        map(lambda x: AlgoParam(x[0], x[1]['hardness']),
            algorithm_params.items()))
    if unsupported:
        raise RuntimeError(
            "The following algorithms/algorithm-options are not supported "
            "in your system.\n {0}\n"
            "Please verify your configuration and try again"
            .format(unsupported))

    fbalgo = config["FALLBACK_ALGORITHM_PARAMS"]["algorithm"]
    fbhard = config["FALLBACK_ALGORITHM_PARAMS"]["hardness"]

    if not (algorithm_params.get(fbalgo)
            and fbhard in algorithm_params.get(fbalgo, {}).get("hardness")):
        raise RuntimeError("Fallback algorithm parameters must exist in the "
                           "defined supported algorithm params")


def validate_config(config):
    try:
        validate_crypto_configuration(config)
    except RuntimeError as e:
        print("Error: {}".format(e))
        exit(1)
