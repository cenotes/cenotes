import pytest
import json
import nacl.secret
from cenotes import utils, exceptions, models


def test_craft_key():
    utils.craft_key_from_password("lalala".encode())
    utils.craft_key_from_password("lalala")


def test_secret_box_crafting(testing_key):
    assert isinstance(utils.craft_secret_box(testing_key),
                      nacl.secret.SecretBox)


def test_encrypt_decrypt():
    password = "test"
    plaintext = "can you see me?"
    box1 = utils.craft_secret_box(utils.craft_key_from_password(password))
    box2 = utils.craft_secret_box(utils.craft_key_from_password(password))
    ciphertext = box1.encrypt(plaintext.encode())
    assert box2.decrypt(ciphertext).decode() == plaintext


def test_enforce_bytes():
    def dummy_func(x, y, z):
        return x, y, z
    results = utils.enforce_bytes(
        kwargs_names=["y"])(dummy_func)("test1", y="test2", z="test3")
    assert isinstance(results[0], bytes), type(results[0])
    assert isinstance(results[1], bytes), type(results[1])
    assert not isinstance(results[2], bytes), type(results[2])


def test_enforce_bytes_wrong_kwarg():
    def dummy_func(x, y, z):
        return x, y, z
    with pytest.raises(SyntaxWarning):
        utils.enforce_bytes(
            kwargs_names=["N"])(dummy_func)("test1", y="test2", z="test3")


def test_maketype():
    assert type(utils.make_type(tuple, "lala")) == tuple
    assert type(utils.make_type(set, "lala")) == set
    assert type(utils.make_type(list, "lala")) == list


def test_maketuple():
    assert utils.make_tuple("lala") == ("lala",)
    assert utils.make_tuple(["lala"]) == ("lala",)
    assert utils.make_tuple(("lala",)) == ("lala",)
    assert utils.make_tuple({"lala"}) == ("lala",)


def test_url_safe_sym_encrypt(testing_box):
    plaintext = "can you see me?"
    assert utils.url_safe_sym_encrypt(plaintext, testing_box) != plaintext


def test_url_safe_sym_decrypt(testing_box):
    plaintext = "can you see me?"
    ciphertext = utils.url_safe_sym_encrypt(plaintext, testing_box)
    assert utils.url_safe_sym_decrypt(ciphertext, testing_box) == plaintext


def test_url_safe_sym_decrypt_wrong_password(testing_box):
    plaintext = "can you see me?"
    ciphertext = utils.url_safe_sym_encrypt(plaintext, testing_box)
    with pytest.raises(exceptions.InvalidKeyORNoteError):
        utils.url_safe_sym_decrypt(ciphertext, utils.craft_secret_box(
            utils.craft_key_from_password("mallory")))


def test_server_key_sym_encrypt(app):
    plaintext = "can you see me?"
    assert utils.server_key_sym_encrypt(plaintext) != plaintext


def test_server_key_sym_decrypt(app):
    plaintext = "can you see me?"
    ciphertext = utils.server_key_sym_encrypt(plaintext)
    assert utils.server_key_sym_decrypt(ciphertext) == plaintext


def test_user_encrypt_decrypt():
    plaintext = "can you see me?"
    assert (utils.user_key_sym_decrypt(
        utils.user_key_sym_encrypt(
            plaintext, "user-key!"), "user-key!") == plaintext)


def test_generate_random_chars():
    random_chars = utils.generate_random_chars(15)
    assert isinstance(random_chars, bytes)
    assert len(random_chars) == 15


def test_craft_json_response_error_aka_no_success():
    assert (json.loads(utils.craft_json_response(error="Oh noes"))["success"]
            is False)


def test_craft_json_response_default_success():
    assert json.loads(utils.craft_json_response())["success"] is True


def test_craft_json_response_multiple_notes(app):
    note1 = models.Note("test1")
    note2 = models.Note("test2")
    models.db.session.add(note1, note2)
    models.db.session.commit()
    response = json.loads(utils.craft_json_response(enotes=[note1, note2]))
    assert (set(map(utils.server_key_sym_decrypt,
                    map(lambda x: x["enote_id"], response["enotes"])))
            == set(map(str, [note1.id, note2.id])))
    for attribute, model_attr in (
            ("enote_expiration_date", "iso_expiration_date"),
            ("enote_visits_count", "visits_count"),
            ("enote_max_visits", "max_visits")):
        assert (set(map(lambda x: x[attribute], response["enotes"]))
                == set(map(lambda x: getattr(x, model_attr), [note1, note2])))

    assert (tuple(map(lambda x: x["enote_key"], response["enotes"]))
            == tuple(["", ""]))
