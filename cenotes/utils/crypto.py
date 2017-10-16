import base64
from flask import current_app
from nacl import utils as nacl_utils, secret, exceptions, pwhash

import cenotes.exceptions
from cenotes.models import create_new_note
from cenotes.utils.other import enforce_bytes

kdf = pwhash.kdf_scryptsalsa208sha256
salt = nacl_utils.random(pwhash.SCRYPT_SALTBYTES)
ops = pwhash.SCRYPT_OPSLIMIT_SENSITIVE
mem = pwhash.SCRYPT_MEMLIMIT_SENSITIVE


def generate_random_chars(size=32):
    return nacl_utils.random(size)


def generate_url_safe_pass(size=32):
    return base64.urlsafe_b64encode(generate_random_chars(size)).decode()


def craft_key_from_password(password):
    try:
        password = password.encode()
    except AttributeError:
        pass
    return kdf(secret.SecretBox.KEY_SIZE, password, salt,
               opslimit=ops, memlimit=mem)


def craft_secret_box(key):
    return secret.SecretBox(key)


@enforce_bytes(kwargs_names="what")
def url_safe_sym_encrypt(what, secret_box):
    return base64.urlsafe_b64encode(secret_box.encrypt(what)).decode()


@enforce_bytes(kwargs_names="what")
def url_safe_sym_decrypt(what, secret_box):
    try:
        return secret_box.decrypt(base64.urlsafe_b64decode(what)).decode()
    except exceptions.CryptoError as err:
        raise cenotes.exceptions.InvalidKeyORNoteError(err)


@enforce_bytes(kwargs_names="what")
def server_key_sym_encrypt(what):
    return url_safe_sym_encrypt(what, current_app.server_box)


@enforce_bytes(kwargs_names="what")
def server_key_sym_decrypt(what):
    return url_safe_sym_decrypt(what, current_app.server_box)


@enforce_bytes(kwargs_names="what")
def user_key_sym_encrypt(what, password):
    return craft_secret_box(craft_key_from_password(password)).encrypt(what)


@enforce_bytes(kwargs_names="what")
def user_key_sym_decrypt(what, password):
    return craft_secret_box(
        craft_key_from_password(password)).decrypt(what)


def encrypt_note(cen_parameters, key=None):
    if not cen_parameters.note:
        raise cenotes.exceptions.InvalidUsage("Note payload cannot be empty")

    key = ((key or cen_parameters.note_key or "").encode()
           or generate_random_chars())

    # needs to be url safe so we can share it around
    url_safe_key = base64.urlsafe_b64encode(key)

    if cen_parameters.no_store:
        return url_safe_sym_encrypt(
            cen_parameters.note,
            craft_secret_box(craft_key_from_password(key))
        ), url_safe_key.decode()

    new_note = create_new_note(
        cen_parameters, user_key_sym_encrypt(cen_parameters.note, key))
    return new_note, url_safe_key.decode()
