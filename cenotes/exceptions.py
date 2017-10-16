import traceback
from flask import current_app


class CenotesError(Exception):
    base_text = "Cenotes Error"

    @staticmethod
    def should_traceback():
        return any(map(current_app.config.get,
                       ("DEBUG", "DEVELOPMENT", "TESTING")))

    def __str__(self, *args, **kwargs):
        if self.should_traceback():
            return "{0}: {1}".format(
                self.base_text,
                traceback.extract_tb(super(Exception, self).__traceback__))
        else:
            return self.base_text


class InvalidUsage(CenotesError):
    base_text = "Invalid usage"

    def __init__(self, *args, **kwargs):
        self.base_text = ",".join(args or kwargs.values())


class InvalidKeyORNoteError(CenotesError):
    base_text = "Invalid key or note not found"
