import base64
from nacl import utils as nacl_utils, secret, pwhash
import cenotes.exceptions
from cenotes.models import create_new_note, fetch_note
from cenotes.utils.other import enforce_bytes, safe_decryption


def generate_random_chars(size=32):
    return nacl_utils.random(size)


def generate_url_safe_pass(size=32):
    return base64.urlsafe_b64encode(generate_random_chars(size)).decode()


@enforce_bytes(kwargs_names="password")
def craft_key_from_password(password):
    kdf = pwhash.kdf_scryptsalsa208sha256
    salt = nacl_utils.random(pwhash.SCRYPT_SALTBYTES)
    ops = pwhash.SCRYPT_OPSLIMIT_SENSITIVE
    mem = pwhash.SCRYPT_MEMLIMIT_SENSITIVE
    return kdf(secret.SecretBox.KEY_SIZE, password, salt,
               opslimit=ops, memlimit=mem)


def craft_secret_box(key):
    return secret.SecretBox(key)


@enforce_bytes(kwargs_names="what")
def url_safe_encode(what):
    return base64.urlsafe_b64encode(what).decode()


@safe_decryption
@enforce_bytes(kwargs_names="what")
def url_safe_decode(what):
    return base64.urlsafe_b64decode(what)


@enforce_bytes(kwargs_names="what")
def encrypt_with_box(what, secret_box):
    return secret_box.encrypt(what)


@enforce_bytes(nof_args=2, kwargs_names=["what", "key"])
def encrypt_with_key(what, key):
    return encrypt_with_box(what, craft_secret_box(key))


@enforce_bytes(kwargs_names="what")
def encrypt_with_password(what, password):
    key = craft_key_from_password(password)
    return encrypt_with_key(what, key), key


@safe_decryption
@enforce_bytes(kwargs_names="what")
def decrypt_with_box(what, secret_box):
    return secret_box.decrypt(what)


@enforce_bytes(kwargs_names="what")
def decrypt_with_key(what, key):
    return decrypt_with_box(what, craft_secret_box(key))


def encrypt_note(note, password=None):
    if not note:
        raise cenotes.exceptions.InvalidUsage("Note payload cannot be empty")

    password = (password or "").encode() or generate_random_chars()

    ciphertext, key = encrypt_with_password(note, password)

    # needs to be url safe so we can share it around
    return ciphertext, url_safe_encode(key)


def craft_url_safe_encrypted_payload(cen_parameters, key=None):
    payload, encoded_key = encrypt_note(cen_parameters.plaintext,
                                        key or cen_parameters.key)
    return url_safe_encode(payload), encoded_key


def create_encrypted_note(cen_parameters, key=None):
    payload, encoded_key = encrypt_note(cen_parameters.plaintext,
                                        key or cen_parameters.key)
    return create_new_note(cen_parameters, payload), encoded_key


@safe_decryption
def decrypt_payload(payload, key):
    return decrypt_with_key(payload, url_safe_decode(key))


@safe_decryption
def decrypt_note(note_id, key):
    return decrypt_payload(fetch_note(int(note_id)), key)
