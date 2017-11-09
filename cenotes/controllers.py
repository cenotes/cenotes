from flask import Blueprint, request, current_app
from cenotes.utils import crypto as cu_crypto, api as capi
from cenotes.exceptions import InvalidKeyORNoteError
from cenotes.models import delete_note as del_note

notes_bp = Blueprint('notes', __name__, url_prefix='/notes')


def check_duress_signal(func):
    def duress(enote_id, key):
        try:
            # avoid deletion when issuing the payload as key
            assert (cu_crypto.decrypt_with_box(cu_crypto.url_safe_decode(key),
                                               current_app.server_box)
                    != enote_id)
        except (InvalidKeyORNoteError, AssertionError):
            return func(enote_id, key)

        cu_crypto.safe_decryption(del_note)(int(enote_id))
        raise InvalidKeyORNoteError()
    return duress


def _generate_decrypt_response(enote_id_or_payload, key):
    enote_id_or_payload = cu_crypto.url_safe_decode(enote_id_or_payload)

    try:
        enote_id_or_payload = cu_crypto.decrypt_with_box(
            enote_id_or_payload, current_app.server_box)
        decryptor = check_duress_signal(cu_crypto.decrypt_note)
    except InvalidKeyORNoteError:
        # if we can't decrypt it, we assume it's a payload instead of id
        decryptor = cu_crypto.decrypt_payload

    plaintext = decryptor(enote_id_or_payload, key).decode()

    return capi.craft_json_response(plaintext=plaintext), 200


@notes_bp.route("/", methods=["POST"])
def decrypt_json_note():
    request_params = request.get_json(silent=True) or {}
    cen_parameters = capi.get_request_params(request_params)
    enote_id_or_payload = cen_parameters.payload
    key = cen_parameters.key

    return _generate_decrypt_response(enote_id_or_payload, key)


@notes_bp.route("/<enote_id_or_payload>/<key>", methods=["GET"])
def decrypt_note(enote_id_or_payload, key):
    return _generate_decrypt_response(enote_id_or_payload, key)


@notes_bp.route("/<enote_id>/<key>", methods=["PATCH"])
@notes_bp.route("/<enote_id>", methods=["PATCH"])
def modify_note(enote_id, key):
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
        duress_key = cu_crypto.url_safe_encode(
            cu_crypto.encrypt_with_box(
                cu_crypto.generate_random_chars(), current_app.server_box))

        return capi.craft_json_response(payload=encrypted_id, enote=new_note,
                                        key=final_key, dkey=duress_key), 200
