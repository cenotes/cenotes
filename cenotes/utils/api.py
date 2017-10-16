import json
from cenotes.utils import cen_params
from cenotes.utils.crypto import server_key_sym_encrypt


def craft_json_response(success=True, enotes=tuple(), **kwargs):
    return json.dumps(
        {"success": success if not kwargs.get("error") else False,
         "error": kwargs.get("error", ""),
         "enotes": [
             {"enote_id": server_key_sym_encrypt(str(enote.id)),
              "enote_key": kwargs.get("enote_key", ""),
              "enote_expiration_date": enote.iso_expiration_date,
              "enote_visits_count": enote.visits_count,
              "enote_max_visits": enote.max_visits,
              "plaintext": kwargs.get("plaintext", "")} for enote in enotes]
         })


def get_request_params(request_params):
    return cen_params(**{
        key: request_params.get(key) for key in cen_params._fields})
