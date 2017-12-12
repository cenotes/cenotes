from cenotes_lib import crypto
from flask import Blueprint, request, current_app
from functools import partial

from cenotes import api, models
from cenotes.helpers import generate_decrypt_response

notes_bp = Blueprint('notes', __name__, url_prefix='/notes')


@notes_bp.route("/", methods=["POST"])
def decrypt_json_note():
    request_params = request.get_json(silent=True) or {}
    cen_parameters = api.get_request_params(request_params)
    enote_id_or_payload = cen_parameters.payload
    key = cen_parameters.key

    return generate_decrypt_response(enote_id_or_payload, key)


@notes_bp.route("/<enote_id_or_payload>/<key>", methods=["GET"])
def decrypt_note(enote_id_or_payload, key):
    return generate_decrypt_response(enote_id_or_payload, key)


@notes_bp.route("/<enote_id>/<key>", methods=["PATCH"])
@notes_bp.route("/<enote_id>", methods=["PATCH"])
def modify_note(enote_id, key):
    pass


@notes_bp.route("/encrypt/", methods=["POST"])
@notes_bp.route("/encrypt/<key>/", methods=["POST"])
def encrypt_note(key=None):
    cen_parameters = api.get_request_params(
        request.get_json(silent=True) or {})

    payload, final_key = crypto.encrypt_note(
        cen_parameters.plaintext, key or cen_parameters.key)

    if cen_parameters.no_store:
        return api.craft_json_response(payload=payload, key=final_key), 200

    else:
        new_note = models.create_new_note(cen_parameters, payload)
        encrypted_id, duress_key = map(
            crypto.url_safe_encode,
            map(partial(crypto.encrypt_with_box,
                        secret_box=current_app.server_box),
                (str(new_note.id), crypto.generate_random_chars()))
        )

        return api.craft_json_response(payload=encrypted_id, enote=new_note,
                                       key=final_key, dkey=duress_key), 200
