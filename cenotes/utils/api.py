import json

from cenotes.utils import CENParams
from cenotes.utils.crypto import server_key_sym_encrypt


def craft_json_response(
        success=True, error="", enote=None, plaintext="", key="", payload=""):

    return json.dumps(
        {"success": success if not error else False,
         "error": error,
         "key": key,
         "plaintext": plaintext,
         "payload": payload,
         "enote":
             {"enote_id": server_key_sym_encrypt(str(enote.id)),
              "enote_expiration_date": enote.iso_expiration_date,
              "enote_visits_count": enote.visits_count,
              "enote_max_visits": enote.max_visits} if enote else {}
         })


def get_request_params(request_params):
    return CENParams(**request_params)
