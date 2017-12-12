from flask import current_app
from sqlalchemy.orm.exc import NoResultFound
from cenotes_lib import crypto
from cenotes_lib.exceptions import CenotesError
from cenotes_lib.helpers import safe_decryption

from cenotes import api
from cenotes.models import delete_note, fetch_note


@safe_decryption(extra_exceptions=[NoResultFound])
def decrypt_stored_note(note_id, key):
    return crypto.decrypt_note(fetch_note(int(note_id)), key)


def check_duress_signal(func):
    def duress(enote_id, key):
        try:
            # avoid deletion when issuing the payload as key
            assert (crypto.decrypt_with_box(crypto.url_safe_decode(key),
                                            current_app.server_box)
                    != enote_id)
        except (CenotesError, AssertionError):
            return func(enote_id, key)

        safe_decryption([NoResultFound])(delete_note)(int(enote_id))
        raise CenotesError()
    return duress


def generate_decrypt_response(enote_id_or_payload, key):
    try:
        enote_id_or_payload = crypto.decrypt_with_box(
            crypto.url_safe_decode(enote_id_or_payload),
            current_app.server_box)
        decryptor = check_duress_signal(decrypt_stored_note)
    except CenotesError:
        # if we can't decrypt it, we assume it's a payload instead of id
        decryptor = crypto.decrypt_note

    plaintext = decryptor(enote_id_or_payload, key).decode()

    return api.craft_json_response(plaintext=plaintext), 200
