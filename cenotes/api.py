from flask import jsonify, current_app
from cenotes_lib.exceptions import InvalidUsage


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
    def __init__(self, plaintext="", key=None, expiration_date=None,
                 visits_count=None, max_visits=None, no_store=False,
                 payload=None, algorithm=None, hardness=None,
                 **kwargs):
        self.plaintext = plaintext
        self.key = key
        self.payload = payload
        self.expiration_date = expiration_date
        self.visits_count = visits_count
        self.max_visits = max_visits
        self.no_store = no_store
        self.algorithm, self.hardness = self.enforce_correct_encr_options(
            algorithm, hardness)

    @staticmethod
    def enforce_correct_encr_options(algorithm, hardness):
        supported = current_app.config["SUPPORTED_ALGORITHM_PARAMS"]
        fallback = current_app.config["FALLBACK_ALGORITHM_PARAMS"]

        matched_algorithm = (algorithm if algorithm in supported.keys()
                             else fallback["algorithm"])

        if hardness not in supported[matched_algorithm]["hardness"]:
            return tuple(map(
                lambda x: current_app.config["FALLBACK_ALGORITHM_PARAMS"][x],
                ("algorithm", "hardness")))
        else:
            return matched_algorithm, hardness
