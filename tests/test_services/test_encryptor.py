import os

import pytest

from app.services.encryptor import Encryptor

PLAINTEXT = "This is a secret message."


def test_encrypt_decrypt_cycle():
    key = os.urandom(32)  # Generate a 256-bit AES key

    encryptor = Encryptor(key)

    iv, ciphertext = encryptor.encrypt(PLAINTEXT)
    decrypted_message = encryptor.decrypt(ciphertext, iv)

    assert decrypted_message == PLAINTEXT


def test_from_plaintext_key():
    key = "This is a secret key."
    encryptor = Encryptor.from_plaintext_key(key)

    iv, ciphertext = encryptor.encrypt(PLAINTEXT)
    decrypted_message = encryptor.decrypt(ciphertext, iv)

    assert decrypted_message == PLAINTEXT


def test_from_encryption_key():
    key = "This is a secret key."
    encryptor = Encryptor.from_plaintext_key(key)

    iv, ciphertext = encryptor.encrypt(PLAINTEXT)
    encryption_key = encryptor.get_encryption_key(iv)

    encryptor, iv = Encryptor.from_encryption_key(encryption_key)
    decrypted_message = encryptor.decrypt(ciphertext, iv)

    assert decrypted_message == PLAINTEXT


def test_invalid_key_size():
    key = b"not a valid key"
    with pytest.raises(ValueError):
        Encryptor(key)
