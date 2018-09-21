import json
from datetime import date
from cenotes.models import Note
from cenotes_lib import crypto


def assert_successful_request(response):
    assert response.status_code == 200
    assert response.json["success"] is True


def assert_bad_request(response):
    assert response.status_code == 400
    assert response.json["success"] is False
    assert response.json["error"] == "Invalid key or note not found"


def test_encrypt_simple(app, db, client):
    plaintext = "test-note"
    assert Note.query.count() == 0
    response = client.post(
        "notes/encrypt/", data=json.dumps(
            dict(plaintext=plaintext, expiration_date="19-10-2017")),
        content_type='application/json')
    assert_successful_request(response)
    assert Note.query.count() == 1

    note = Note.query.one()
    key = crypto.url_safe_decode(response.json["key"])
    assert crypto.decrypt_with_key(crypto.url_safe_decode(note.payload),
                                   key).decode() == plaintext
    assert str(note.id) == crypto.decrypt_with_box(
        crypto.url_safe_decode(
            response.json["payload"]), app.server_box).decode()
    assert note.expiration_date == date(year=2017, month=10, day=19)


def test_encrypt_no_plaintext(db, client):
    assert Note.query.count() == 0
    response = client.post(
        "notes/encrypt/", data=json.dumps(
            dict(expiration_date="19")),
        content_type='application/json')
    assert response.status_code == 200
    assert Note.query.count() == 1


def test_encrypt_no_note(db, client):

    assert Note.query.count() == 0
    response = client.post("notes/encrypt/",
                           data=json.dumps(dict(key="test")),
                           content_type='application/json')
    assert_successful_request(response)
    note = Note.query.one()
    key = crypto.url_safe_decode(response.json["key"])
    assert crypto.decrypt_with_key(crypto.url_safe_decode(note.payload),
                                   key).decode() == ""


def test_encrypt_no_store(db, client):
    plaintext = "test-note"
    assert Note.query.count() == 0
    response = client.post(
        "notes/encrypt/", data=json.dumps(dict(plaintext=plaintext, no_store=True)),
        content_type='application/json')
    assert_successful_request(response)
    assert Note.query.count() == 0

    note = crypto.url_safe_decode(response.json["payload"])
    key = crypto.url_safe_decode(response.json["key"])
    assert crypto.decrypt_with_key(note, key).decode() == plaintext


def test_decrypt_payload(client):
    plaintext = "test-note"
    enc_response = client.post(
        "notes/encrypt/", data=json.dumps(dict(plaintext=plaintext, no_store=True)),
        content_type='application/json')
    note = enc_response.json["payload"]
    key = enc_response.json["key"]

    dec_response = client.get("/notes/{0}/{1}".format(note, key))
    assert_successful_request(dec_response)
    assert dec_response.json["plaintext"] == plaintext


def test_decrypt_payload_in_json(client):
    plaintext = "test-note"
    enc_response = client.post(
        "notes/encrypt/", data=json.dumps(dict(plaintext=plaintext, no_store=True)),
        content_type='application/json')
    note = enc_response.json["payload"]
    key = enc_response.json["key"]

    dec_response = client.post(
        "/notes/", data=json.dumps(dict(payload=note, key=key)),
        content_type='application/json')
    assert_successful_request(dec_response)
    assert dec_response.json["plaintext"] == plaintext


def test_decrypt_payload_wrong_password(client):
    plaintext = "test-note"
    enc_response = client.post(
        "notes/encrypt/", data=json.dumps(dict(plaintext=plaintext, no_store=True)),
        content_type='application/json')
    note = enc_response.json["payload"]
    key = crypto.url_safe_encode(enc_response.json["key"])

    dec_response = client.get("/notes/{0}/{1}".format(note, key))
    assert_bad_request(dec_response)


def test_decrypt_note(db, client):
    plaintext = "test-note"
    enc_response = client.post(
        "notes/encrypt/", data=json.dumps(dict(plaintext=plaintext)),
        content_type='application/json')
    encr_note_id = enc_response.json["payload"]
    key = enc_response.json["key"]

    dec_response = client.get("/notes/{0}/{1}".format(encr_note_id, key))
    assert_successful_request(dec_response)
    assert dec_response.json["plaintext"] == plaintext


def test_decrypt_note_wrong_password(db, client):
    plaintext = "test-note"
    enc_response = client.post(
        "notes/encrypt/", data=json.dumps(dict(plaintext=plaintext)),
        content_type='application/json')
    encr_note_id = enc_response.json["payload"]
    key = crypto.url_safe_encode(enc_response.json["key"])

    dec_response = client.get("/notes/{0}/{1}".format(encr_note_id, key))
    assert_bad_request(dec_response)


def test_decrypt_note_one_time(db, client):
    plaintext = "test-note"
    enc_response = client.post(
        "notes/encrypt/", data=json.dumps(dict(plaintext=plaintext)),
        content_type='application/json')
    assert Note.query.count() == 1
    encr_note_id = enc_response.json["payload"]
    key = enc_response.json["key"]

    dec_response = client.get("/notes/{0}/{1}".format(encr_note_id, key))
    assert_successful_request(dec_response)
    assert Note.query.count() == 0


def test_decrypt_note_two_times(db, client):
    plaintext = "test-note"
    enc_response = client.post(
        "notes/encrypt/",
        data=json.dumps(dict(plaintext=plaintext, max_visits=2)),
        content_type='application/json')
    assert Note.query.count() == 1
    encr_note_id = enc_response.json["payload"]
    key = enc_response.json["key"]

    dec_response = client.get("/notes/{0}/{1}".format(encr_note_id, key))
    assert_successful_request(dec_response)
    assert Note.query.count() == 1

    dec_response = client.get("/notes/{0}/{1}".format(encr_note_id, key))
    assert_successful_request(dec_response)
    assert Note.query.count() == 0


def test_decrypt_note_more_than_allowed(db, client):
    plaintext = "test-note"
    enc_response = client.post(
        "notes/encrypt/",
        data=json.dumps(dict(plaintext=plaintext, max_visits=1)),
        content_type='application/json')
    assert Note.query.count() == 1
    encr_note_id = enc_response.json["payload"]
    key = enc_response.json["key"]

    dec_response = client.get("/notes/{0}/{1}".format(encr_note_id, key))
    assert_successful_request(dec_response)
    assert Note.query.count() == 0

    dec_response = client.get("/notes/{0}/{1}".format(encr_note_id, key))
    assert_bad_request(dec_response)


def test_delete_note_in_json(db, client):
    plaintext = "test-note"
    enc_response = client.post(
        "notes/encrypt/",
        data=json.dumps(dict(plaintext=plaintext, max_visits=10)),
        content_type='application/json')
    note = enc_response.json["payload"]
    duress_key = enc_response.json["duress_key"]

    assert Note.query.count() == 1

    dec_response = client.post(
        "/notes/", data=json.dumps(dict(payload=note, key=duress_key)),
        content_type='application/json')
    assert_bad_request(dec_response)
    assert Note.query.count() == 0


def test_delete_note(db, client):
    plaintext = "test-note"
    enc_response = client.post(
        "notes/encrypt/",
        data=json.dumps(dict(plaintext=plaintext, max_visits=10)),
        content_type='application/json')
    note = enc_response.json["payload"]
    duress_key = enc_response.json["duress_key"]

    assert Note.query.count() == 1

    assert_bad_request(client.get("/notes/{0}/{1}".format(note, duress_key)))
    assert Note.query.count() == 0


def test_delete_note_multiple_times(db, client):
    plaintext = "test-note"
    enc_response = client.post(
        "notes/encrypt/",
        data=json.dumps(dict(plaintext=plaintext, max_visits=10)),
        content_type='application/json')
    note = enc_response.json["payload"]
    duress_key = enc_response.json["duress_key"]

    assert_bad_request(client.get("/notes/{0}/{1}".format(note, duress_key)))
    assert_bad_request(client.get("/notes/{0}/{1}".format(note, duress_key)))


def test_avoid_note_deletion_issuing_payload_as_key(db, client):
    plaintext = "test-note"
    enc_response = client.post(
        "notes/encrypt/",
        data=json.dumps(dict(plaintext=plaintext, max_visits=10)),
        content_type='application/json')
    note = enc_response.json["payload"]

    assert Note.query.count() == 1

    dec_response = client.get("/notes/{0}/{1}".format(note, note))

    assert_bad_request(dec_response)
    assert Note.query.count() == 1


def test_get_config(client):
    response = client.get("config/algorithms/")

    assert response.status_code == 200
    # scrypt is the default fallback option, so it should always exist
    assert response.json["scrypt"] is not None


def test_get_default_algorithm_options(client):
    response = client.get("config/algorithms/default/")

    assert response.status_code == 200
    assert response.json["algorithm"] == "scrypt"
    assert response.json["hardness"] == "min"


def test_encrypt_with_options(app, client):
    algo, hardness = "scrypt", "moderate"
    assert hardness != app.config["FALLBACK_ALGORITHM_PARAMS"]["hardness"]

    plaintext = "test-note"
    enc_response = client.post(
        "notes/encrypt/", data=json.dumps(
            dict(plaintext=plaintext, no_store=True,
                 algorithm=algo, hardness=hardness)),
        content_type='application/json')
    note = enc_response.json["payload"]
    key = enc_response.json["key"]

    dec_response = client.get("/notes/{0}/{1}".format(note, key))
    assert_successful_request(dec_response)
    assert dec_response.json["plaintext"] == plaintext


def test_encrypt_with_wrong_options(app, client):
    algo, hardness = "wrong", "wrong"
    assert hardness != app.config["FALLBACK_ALGORITHM_PARAMS"]["hardness"]

    plaintext = "test-note"
    enc_response = client.post(
        "notes/encrypt/", data=json.dumps(
            dict(plaintext=plaintext, no_store=True,
                 algorithm=algo, hardness=hardness)),
        content_type='application/json')
    note = enc_response.json["payload"]
    key = enc_response.json["key"]

    dec_response = client.get("/notes/{0}/{1}".format(note, key))
    assert_successful_request(dec_response)
    assert dec_response.json["plaintext"] == plaintext
