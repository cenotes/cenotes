import json
from cenotes.utils import CENParams


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

    return json.dumps(
        craft_response(enote, error, key, dkey, payload, plaintext, success))


def get_request_params(request_params):
    return CENParams(**request_params)
