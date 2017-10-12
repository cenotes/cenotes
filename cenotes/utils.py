import base64
from nacl import pwhash, secret, utils as nacl_utils, exceptions
from flask import current_app
from cenotes import errors

kdf = pwhash.kdf_scryptsalsa208sha256
salt = nacl_utils.random(pwhash.SCRYPT_SALTBYTES)
ops = pwhash.SCRYPT_OPSLIMIT_SENSITIVE
mem = pwhash.SCRYPT_MEMLIMIT_SENSITIVE


def enforce_bytes(func, nof_args=1, nof_kwargs=0):
    def byte_force(what):
        try:
            return what.encode()
        except AttributeError:
            return what

    def enforce(*args, **kwargs):
        new_args = [arg if i >= nof_args else byte_force(arg)
                    for i, arg in enumerate(args)]
        new_kwargs = {key: val if i >= nof_kwargs else byte_force(val)
                      for i, (key, val) in enumerate(kwargs.items())}
        return func(*new_args, **new_kwargs)
    return enforce


def craft_key_from_password(password):
    try:
        password = password.encode()
    except AttributeError:
        pass
    return kdf(secret.SecretBox.KEY_SIZE, password, salt,
               opslimit=ops, memlimit=mem)


def craft_secret_box(key):
    return secret.SecretBox(key)


@enforce_bytes
def url_safe_sym_encrypt(what, secret_box):
    return base64.urlsafe_b64encode(secret_box.encrypt(what)).decode()


@enforce_bytes
def url_safe_sym_decrypt(what, secret_box):
    try:
        return secret_box.decrypt(base64.urlsafe_b64decode(what)).decode()
    except exceptions.CryptoError as err:
        raise errors.InvalidKeyORNoteError(err)


@enforce_bytes
def server_key_sym_encrypt(what):
    return url_safe_sym_encrypt(what, current_app.server_box)


@enforce_bytes
def server_key_sym_decrypt(what):
    return url_safe_sym_decrypt(what, current_app.server_box)


@enforce_bytes
def user_key_sym_encrypt(what, password):
    return url_safe_sym_encrypt(
        what, craft_secret_box(craft_key_from_password(password)))


@enforce_bytes
def user_key_sym_decrypt(what, password):
    return url_safe_sym_decrypt(
        what, craft_secret_box(craft_key_from_password(password)))
