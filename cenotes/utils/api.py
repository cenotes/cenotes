import json
from flask import current_app
from cenotes.utils import CENParams
from cenotes.utils.crypto import encrypt_with_box, url_safe_encode


def craft_json_response(
        success=True, error="", enote=None, plaintext="", key="", payload=""):

    return json.dumps(
        {"success": success if not error else False,
         "error": error,
         "key": key,
         "plaintext": plaintext,
         "payload": payload,
         "enote":
             {"enote_id": url_safe_encode(encrypt_with_box(
                 str(enote.id), current_app.server_box)),
              "enote_expiration_date": enote.iso_expiration_date,
              "enote_visits_count": enote.visits_count,
              "enote_max_visits": enote.max_visits} if enote else {}
         })


def get_request_params(request_params):
    return CENParams(**request_params)
