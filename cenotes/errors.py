from flask import jsonify, Blueprint


class InvalidKeyORNoteError(Exception):
    pass


error_bp = Blueprint('error_handlers', __name__)


@error_bp.app_errorhandler(404)
def not_found(error):
    return jsonify(error=404, text="Not found"), 404


@error_bp.app_errorhandler(InvalidKeyORNoteError)
def invalid_key_or_note(error):
    return jsonify(error=400, text="Invalid key or note not found"), 400
