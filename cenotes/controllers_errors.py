from flask import Blueprint

from cenotes.api import craft_json_response
from cenotes_lib.exceptions import CenotesError, InvalidUsage

error_bp = Blueprint('error_handlers', __name__)


@error_bp.app_errorhandler(404)
def not_found(error):
    return craft_json_response(error="Not found"), 404


@error_bp.app_errorhandler(InvalidUsage)
@error_bp.app_errorhandler(400)
@error_bp.app_errorhandler(405)
def invalid_usage(error):
    return craft_json_response(error=str(error)), 400


@error_bp.app_errorhandler(CenotesError)
def invalid_key_or_note(error):
    return craft_json_response(error="Invalid key or note not found"), 400


@error_bp.app_errorhandler(500)
def internal_error(error):
    return craft_json_response(error="Something bad server-side happened"), 500
