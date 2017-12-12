from flask import Blueprint

from cenotes.api import craft_json_response
from cenotes_lib.exceptions import CenotesError, InvalidUsage

error_bp = Blueprint('error_handlers', __name__)


@error_bp.app_errorhandler(404)
def not_found(error):
    return craft_json_response(error="Not found"), 404


@error_bp.app_errorhandler(400)
def bad_request(error):
    return craft_json_response(error="Bad request"), 404


@error_bp.app_errorhandler(InvalidUsage)
def invalid_usage(error):
    return craft_json_response(error=str(error)), 400


@error_bp.app_errorhandler(InvalidKeyORNoteError)
def invalid_key_or_note(error):
    return craft_json_response(error=str(error)), 400
