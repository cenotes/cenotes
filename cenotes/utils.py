import base64
import json
from nacl import pwhash, secret, utils as nacl_utils, exceptions
from flask import current_app
from cenotes import errors

kdf = pwhash.kdf_scryptsalsa208sha256
salt = nacl_utils.random(pwhash.SCRYPT_SALTBYTES)
ops = pwhash.SCRYPT_OPSLIMIT_SENSITIVE
mem = pwhash.SCRYPT_MEMLIMIT_SENSITIVE


def make_type(mtype, *args):
    t_args = []
    accepted_collections = (list, tuple, set)
    similar_type = tuple if mtype is list else list
    for x in args:
        if not isinstance(x, accepted_collections):
            t_args.extend([x])
        else:
            t_args.extend(similar_type(x))
    return mtype(t_args)


def make_tuple(*args):
    return make_type(tuple, *args)


def enforce_bytes(nof_args=1, kwargs_names=tuple(["test"])):
    def byte_force(what):
        try:
            return what.encode()
        except AttributeError:
            return what

    def enforcer(func):
        if set(make_tuple(kwargs_names)) - set(func.__code__.co_varnames):
            raise SyntaxWarning("Wrong kwarg names in decorator!")

        def enforce(*args, **kwargs):
            new_args = [arg if i >= nof_args else byte_force(arg)
                        for i, arg in enumerate(args)]
            new_kwargs = {
                key: val if key not in kwargs_names else byte_force(val)
                for key, val in kwargs.items()
            }
            return func(*new_args, **new_kwargs)
        return enforce
    return enforcer


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
        raise errors.InvalidKeyORNoteError(err)


@enforce_bytes(kwargs_names="what")
def server_key_sym_encrypt(what):
    return url_safe_sym_encrypt(what, current_app.server_box)


@enforce_bytes(kwargs_names="what")
def server_key_sym_decrypt(what):
    return url_safe_sym_decrypt(what, current_app.server_box)


@enforce_bytes(kwargs_names="what")
def user_key_sym_encrypt(what, password):
    return url_safe_sym_encrypt(
        what, craft_secret_box(craft_key_from_password(password)))


@enforce_bytes(kwargs_names="what")
def user_key_sym_decrypt(what, password):
    return url_safe_sym_decrypt(
        what, craft_secret_box(craft_key_from_password(password)))


def craft_json_response(success=True, enotes=tuple(), **kwargs):
    return json.dumps(
        dict(success=success if not kwargs.get("error") else False,
             error=kwargs.get("error", ""),
             enotes=[
                 {"enote_id": server_key_sym_encrypt(
                     str(getattr(enote, "id", ""))),
                  "enote_key": kwargs.get("enote_key", ""),
                  "enote_expiration_date": getattr(
                      enote, "iso_expiration_date", ""),
                  "enote_visits_count": getattr(enote, "visits_count", ""),
                  "enote_max_visits": getattr(enote, "max_visits", "")}
                 for enote in enotes]
             )
    )
