import json
import base64
import pytest
import nacl.secret
import nacl.exceptions
from cenotes import exceptions, models
from cenotes.utils import crypto, api, other, CENParams


def assert_decrypt(payload, key, plaintext):
    assert (crypto.decrypt_with_key(
        payload, crypto.url_safe_decode(key)).decode() == plaintext)


def test_craft_key():
    crypto.craft_key_from_password("lalala".encode())
    crypto.craft_key_from_password("lalala")


def test_secret_box_crafting(testing_key):
    assert isinstance(crypto.craft_secret_box(testing_key),
                      nacl.secret.SecretBox)


def test_encrypt_decrypt():
    password = "test"
    plaintext = "can you see me?"
    key = crypto.craft_key_from_password(password)
    box1 = crypto.craft_secret_box(key)
    box2 = crypto.craft_secret_box(key)
    ciphertext = box1.encrypt(plaintext.encode())
    assert box2.decrypt(ciphertext).decode() == plaintext


def test_enforce_bytes():
    def dummy_func(x, y, z):
        return x, y, z
    results = other.enforce_bytes(
        kwargs_names=["y"])(dummy_func)("test1", y="test2", z="test3")
    assert isinstance(results[0], bytes), type(results[0])
    assert isinstance(results[1], bytes), type(results[1])
    assert not isinstance(results[2], bytes), type(results[2])


def test_enforce_bytes_wrong_kwarg():
    def dummy_func(x, y, z):
        return x, y, z
    with pytest.raises(SyntaxWarning):
        other.enforce_bytes(
            kwargs_names=["N"])(dummy_func)("test1", y="test2", z="test3")


def test_maketype():
    assert type(other.make_type(tuple, "lala")) == tuple
    assert type(other.make_type(set, "lala")) == set
    assert type(other.make_type(list, "lala")) == list


def test_maketuple():
    assert other.make_tuple("lala") == ("lala",)
    assert other.make_tuple(["lala"]) == ("lala",)
    assert other.make_tuple(("lala",)) == ("lala",)
    assert other.make_tuple({"lala"}) == ("lala",)


def test_encrypt_with_box(testing_box):
    plaintext = "can you see me?"
    assert crypto.encrypt_with_box(plaintext, testing_box) != plaintext


def test_decrypt_with_box(testing_box):
    plaintext = "can you see me?"
    ciphertext = crypto.encrypt_with_box(plaintext, testing_box)
    assert (crypto.decrypt_with_box(ciphertext, testing_box).decode()
            == plaintext)


def test_decrypt_with_box_wrong_password(testing_box):
    plaintext = "can you see me?"
    ciphertext = crypto.encrypt_with_box(plaintext, testing_box)
    with pytest.raises(exceptions.InvalidKeyORNoteError):
        crypto.decrypt_with_box(ciphertext, crypto.craft_secret_box(
            crypto.craft_key_from_password("mallory")))


def test_encrypt_with_password():
    plaintext = "can you see me?"
    password = "test"
    assert crypto.encrypt_with_password(plaintext, password) != plaintext


def test_decrypt_with_key():
    plaintext = "can you see me?"
    password = "test"
    assert crypto.decrypt_with_key(*crypto.encrypt_with_password(
        plaintext, password)).decode() == plaintext


def test_key_encrypt_decrypt():
    plaintext = "can you see me?"
    key = crypto.craft_key_from_password("test")
    assert (crypto.decrypt_with_key(
        crypto.encrypt_with_key(
            plaintext, key), key).decode() == plaintext)


def test_generate_random_chars():
    random_chars = crypto.generate_random_chars(15)
    assert isinstance(random_chars, bytes)
    assert len(random_chars) == 15


def test_craft_json_response_error_aka_no_success():
    assert (json.loads(api.craft_json_response(error="Oh noes"))["success"]
            is False)


def test_craft_json_response_default_success():
    assert json.loads(api.craft_json_response())["success"] is True


def test_get_request_params():
    params = api.get_request_params(
        dict(expiration_date="never", visits_count="maximum",
             max_visits="zero", other_option="what?"))
    assert params.expiration_date == "never"
    assert params.visits_count == "maximum"
    assert params.max_visits == "zero"
    assert params.no_store is False


def test_generate_url_safe_pass():
    assert isinstance(crypto.generate_url_safe_pass(), str)


def test_encrypt_note_simple_no_key(db):
    plaintext = "test-note"
    assert models.Note.query.count() == 0
    note, ekey = crypto.create_encrypted_note(CENParams(plaintext=plaintext))
    assert models.Note.query.count() == 1
    assert note.payload != plaintext.encode()
    assert_decrypt(note.payload, ekey, plaintext)


def test_encrypt_note_simple_param_key(db):
    plaintext = "test-note"
    test_key = "testalalla"
    assert models.Note.query.count() == 0
    note, ekey = crypto.create_encrypted_note(
        CENParams(plaintext=plaintext, key=test_key))
    assert models.Note.query.count() == 1
    assert_decrypt(note.payload, ekey, plaintext)


def test_encrypt_note_special_char_key(db):
    plaintext = "test-note"
    test_key = "test|WQPOI@(*!"
    assert models.Note.query.count() == 0
    note, ekey = crypto.create_encrypted_note(
        CENParams(plaintext=plaintext, key=test_key))
    assert models.Note.query.count() == 1
    assert ekey != test_key
    assert_decrypt(note.payload, ekey, plaintext)


def test_encrypt_note_no_note(db):
    assert models.Note.query.count() == 0
    with pytest.raises(exceptions.InvalidUsage):
        crypto.encrypt_note(note="")
    assert models.Note.query.count() == 0


def test_encrypt_no_store(db):
    plaintext = "test-note"
    test_key = "test|WQPOI@(*!"
    assert models.Note.query.count() == 0
    note, ekey = crypto.craft_url_safe_encrypted_payload(
        CENParams(plaintext=plaintext, key=test_key, no_store=True))
    assert models.Note.query.count() == 0
    assert ekey != test_key
    assert_decrypt(crypto.url_safe_decode(note), ekey, plaintext)


def test_url_safe_encode():
    text = "test me|"
    assert crypto.url_safe_encode(text) != text.encode()


def test_url_safe_decode():
    text1 = "test me"
    text2 = "test me|||"

    assert (crypto.url_safe_encode(text1)
            == base64.b64encode(text1.encode()).decode())
    assert (crypto.url_safe_decode(crypto.url_safe_encode(text2)).decode()
            == text2)


def test_safe_decryption():
    @other.safe_decryption
    def raise_a_crypto_error():
        raise nacl.exceptions.CryptoError("catch!")

    with pytest.raises(exceptions.InvalidKeyORNoteError):
        raise_a_crypto_error()
