import pytest
import nacl.secret
from cenotes import utils, errors


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
        dummy_func, nof_kwargs=1)("test1", y="test2", z="test3")
    assert isinstance(results[0], bytes)
    assert isinstance(results[1], bytes)
    assert not isinstance(results[2], bytes)


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
    with pytest.raises(errors.InvalidKeyORNoteError):
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
