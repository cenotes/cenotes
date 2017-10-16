import json
import base64
from cenotes.models import Note
from cenotes.utils import crypto


def assert_successful_request(response):
    assert response.status_code == 200
    assert response.json["success"] is True


def test_encrypt_simple(db, client):
    plaintext = "test-note"
    assert Note.query.count() == 0
    response = client.post("notes/encrypt/",
                           data=json.dumps(dict(note=plaintext)),
                           content_type='application/json')
    assert_successful_request(response)
    assert Note.query.count() == 1

    note = Note.query.one()
    key = base64.urlsafe_b64decode(
        response.json["key"].encode())
    assert crypto.user_key_sym_decrypt(
        note.payload, key).decode() == plaintext
    assert str(note.id) == crypto.server_key_sym_decrypt(
        response.json["enote"]["enote_id"])


def test_encrypt_no_note(db, client):

    assert Note.query.count() == 0
    response = client.post("notes/encrypt/",
                           data=json.dumps(dict(note_key="test")),
                           content_type='application/json')
    assert response.status_code == 400
    assert response.json["success"] is False
    assert "Note payload cannot be empty" in response.json["error"]


def test_encrypt_no_store(db, client):
    plaintext = "test-note"
    assert Note.query.count() == 0
    response = client.post(
        "notes/encrypt/", data=json.dumps(dict(note=plaintext, no_store=True)),
        content_type='application/json')
    assert_successful_request(response)
    assert Note.query.count() == 0

    note = response.json["payload"]
    key = base64.urlsafe_b64decode(response.json["key"].encode())
    assert crypto.url_safe_sym_decrypt(
        note, crypto.craft_secret_box(
            crypto.craft_key_from_password(key))) == plaintext
