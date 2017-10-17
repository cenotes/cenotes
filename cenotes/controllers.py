from flask import jsonify, Blueprint, request
from cenotes.utils import crypto as cu_crypto, api as capi

notes_bp = Blueprint('notes', __name__, url_prefix='/notes')


@notes_bp.route("/", methods=["GET"])
def index():
    return jsonify(text="Welcome to Cenotes!"), 200


@notes_bp.route("/<note_id>/<key>", methods=["GET"])
@notes_bp.route("/<note_id>", methods=["GET"])
def decrypt_note(note_id, key):
    pass


@notes_bp.route("/<note_id>/<key>", methods=["PATCH"])
@notes_bp.route("/<note_id>", methods=["PATCH"])
def modify_note(note_id, key):
    pass


@notes_bp.route("/<note_id>/<key>", methods=["DELETE"])
@notes_bp.route("/<note_id>", methods=["DELETE"])
def delete_note(note_id, key):
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
        return capi.craft_json_response(enote=new_note, key=final_key), 200
