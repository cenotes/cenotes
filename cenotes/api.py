from cenotes_lib.exceptions import InvalidUsage
from flask import jsonify


def craft_response(enote, error, key, dkey, payload, plaintext, success):
    return {"success": success if not error else False,
            "error": error,
            "key": key,
            "duress_key": dkey,
            "plaintext": plaintext,
            "payload": payload,
            "expiration_date": enote.iso_expiration_date if enote else "",
            "max_visits": enote.max_visits if enote else ""}


def craft_json_response(success=True, error="", enote=None,
                        plaintext="", key="", payload="", dkey=""):

    return jsonify(
        craft_response(enote, error, key, dkey, payload, plaintext, success))


def get_request_params(request_params):
    try:
        return CENParams(**request_params)
    except TypeError:
        raise InvalidUsage("Wrong format of parameters given. Could not parse")


class CENParams(object):
    def __init__(self, plaintext=None, key=None, expiration_date=None,
                 visits_count=None, max_visits=None, no_store=False,
                 payload=None, **kwargs):
        self.plaintext = plaintext
        self.key = key
        self.payload = payload
        self.expiration_date = expiration_date
        self.visits_count = visits_count
        self.max_visits = max_visits
        self.no_store = no_store
