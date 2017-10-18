from flask import jsonify, Blueprint, request, current_app
from cenotes.utils import crypto as cu_crypto, api as capi
from cenotes.exceptions import InvalidKeyORNoteError

notes_bp = Blueprint('notes', __name__, url_prefix='/notes')


@notes_bp.route("/", methods=["GET"])
def index():
    return jsonify(text="Welcome to Cenotes!"), 200


@notes_bp.route("/<enote_id_or_payload>/<key>", methods=["GET"])
@notes_bp.route("/<enote_id_or_payload>", methods=["GET"])
def decrypt_note(enote_id_or_payload, key):
    enote_id_or_payload = cu_crypto.url_safe_decode(enote_id_or_payload)
    try:
        enote_id = cu_crypto.decrypt_with_box(
            enote_id_or_payload, current_app.server_box)
    except InvalidKeyORNoteError:
        # if we can't decrypt it, we assume it's a payload instead of id
        enote_id = None

    if enote_id:
        plaintext = cu_crypto.decrypt_note(enote_id, key).decode()
    else:
        plaintext = cu_crypto.decrypt_payload(
            enote_id_or_payload, key).decode()

    return capi.craft_json_response(plaintext=plaintext), 200


@notes_bp.route("/<enote_id>/<key>", methods=["PATCH"])
@notes_bp.route("/<enote_id>", methods=["PATCH"])
def modify_note(enote_id, key):
    pass


@notes_bp.route("/<enote_id>/<key>", methods=["DELETE"])
@notes_bp.route("/<enote_id>", methods=["DELETE"])
def delete_note(enote_id, key):
    pass


@notes_bp.route("/encrypt/", methods=["POST"])
@notes_bp.route("/encrypt/<key>/", methods=["POST"])
def encrypt_note(key=None):
    request_params = request.get_json(silent=True) or {}
    cen_parameters = capi.get_request_params(request_params)

    if cen_parameters.no_store:
        new_note, final_key = cu_crypto.craft_url_safe_encrypted_payload(
            cen_parameters, key)
        return capi.craft_json_response(payload=new_note, key=final_key), 200

    else:
        new_note, final_key = cu_crypto.create_encrypted_note(
            cen_parameters, key)
        encrypted_id = cu_crypto.url_safe_encode(
            cu_crypto.encrypt_with_box(str(new_note.id),
                                       current_app.server_box))
        return capi.craft_json_response(
            payload=encrypted_id, enote=new_note, key=final_key), 200
