import base64
import nacl.secret
from flask import current_app
from cenotes import errors


def craft_secret_box(key):
    return nacl.secret.SecretBox(key)


def url_safe_sym_encrypt(what, secret_box):
    return base64.urlsafe_b64decode(secret_box.encrypt(what)).decode()


def url_safe_sym_decrypt(what, secret_box):
    try:
        return secret_box.decrypt(base64.urlsafe_b64decode(what))
    except Exception as err:
        raise errors.InvalidKeyORNoteError(err)


def server_key_sym_encrypt(what):
    return url_safe_sym_encrypt(what, current_app.server_box)


def server_key_sym_decrypt(what):
    return url_safe_sym_decrypt(what, current_app.server_box)


def user_key_sym_encrypt(what, key):
    return url_safe_sym_encrypt(what, craft_secret_box(key))


def user_key_sym_decrypt(what, key):
    return url_safe_sym_decrypt(what, craft_secret_box(key))
