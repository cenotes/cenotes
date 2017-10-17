import json
from cenotes.models import Note
from cenotes.utils import crypto


def assert_successful_request(response):
    assert response.status_code == 200
    assert response.json["success"] is True


def test_encrypt_simple(app, db, client):
    plaintext = "test-note"
    assert Note.query.count() == 0
    response = client.post("notes/encrypt/",
                           data=json.dumps(dict(note=plaintext)),
                           content_type='application/json')
    assert_successful_request(response)
    assert Note.query.count() == 1

    note = Note.query.one()
    key = crypto.url_safe_decode(response.json["key"])
    assert crypto.decrypt_with_password(
        note.payload, key).decode() == plaintext
    assert str(note.id) == crypto.decrypt_with_box(
        crypto.url_safe_decode(
            response.json["enote"]["enote_id"]), app.server_box).decode()


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

    note = crypto.url_safe_decode(response.json["payload"])
    key = crypto.url_safe_decode(response.json["key"])
    assert crypto.decrypt_with_password(note, key).decode() == plaintext
