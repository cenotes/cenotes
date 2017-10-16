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


@notes_bp.route("/n/<key>/", methods=["POST"])
@notes_bp.route("/n/<key>/<note>", methods=["POST"])
def encrypt_note(key, note=None):
    if not note:
        note = request.get_json(silent=True)
    pass
