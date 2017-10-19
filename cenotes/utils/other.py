from functools import wraps
from nacl.exceptions import CryptoError
from sqlalchemy.orm.exc import NoResultFound
from cenotes.exceptions import InvalidKeyORNoteError


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

        @wraps(func)
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


def safe_decryption(func):
    @wraps(func)
    def safe_decrypt(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except (CryptoError, UnicodeDecodeError, NoResultFound,
                ValueError, TypeError) as err:
            raise InvalidKeyORNoteError(err)
    return safe_decrypt
