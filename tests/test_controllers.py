import json
from cenotes.models import Note
from cenotes.utils import crypto


def assert_successful_request(response):
    assert response.status_code == 200
    assert response.json["success"] is True


def assert_bad_request(response):
    assert response.status_code == 400
    assert response.json["success"] is False
    assert response.json["error"] != ""


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


def test_decrypt_payload(client):
    plaintext = "test-note"
    enc_response = client.post(
        "notes/encrypt/", data=json.dumps(dict(note=plaintext, no_store=True)),
        content_type='application/json')
    note = enc_response.json["payload"]
    key = enc_response.json["key"]

    dec_response = client.get("/notes/{0}/{1}".format(note, key))
    assert_successful_request(dec_response)
    assert dec_response.json["plaintext"] == plaintext


def test_decrypt_payload_wrong_password(client):
    plaintext = "test-note"
    enc_response = client.post(
        "notes/encrypt/", data=json.dumps(dict(note=plaintext, no_store=True)),
        content_type='application/json')
    note = enc_response.json["payload"]
    key = crypto.url_safe_encode(enc_response.json["key"])

    dec_response = client.get("/notes/{0}/{1}".format(note, key))
    assert_bad_request(dec_response)


def test_decrypt_note(db, client):
    plaintext = "test-note"
    enc_response = client.post(
        "notes/encrypt/", data=json.dumps(dict(note=plaintext)),
        content_type='application/json')
    note = enc_response.json["enote"]["enote_id"]
    key = enc_response.json["key"]

    dec_response = client.get("/notes/{0}/{1}".format(note, key))
    assert_successful_request(dec_response)
    assert dec_response.json["plaintext"] == plaintext


def test_decrypt_note_wrong_password(db, client):
    plaintext = "test-note"
    enc_response = client.post(
        "notes/encrypt/", data=json.dumps(dict(note=plaintext)),
        content_type='application/json')
    note = enc_response.json["enote"]["enote_id"]
    key = crypto.url_safe_encode(enc_response.json["key"])

    dec_response = client.get("/notes/{0}/{1}".format(note, key))
    assert_bad_request(dec_response)


def test_decrypt_note_one_time(db, client):
    plaintext = "test-note"
    enc_response = client.post(
        "notes/encrypt/", data=json.dumps(dict(note=plaintext)),
        content_type='application/json')
    assert Note.query.count() == 1
    note = enc_response.json["enote"]["enote_id"]
    key = enc_response.json["key"]

    dec_response = client.get("/notes/{0}/{1}".format(note, key))
    assert_successful_request(dec_response)
    assert Note.query.count() == 0

