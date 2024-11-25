import hashlib
import os

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.padding import PKCS7


class Encryptor:

    _sep = b"//"

    def __init__(self, hashed_key: bytes):
        self.hashed_key = hashed_key
        self.aes = algorithms.AES(self.hashed_key)
        self.block_size = algorithms.AES.block_size
        self.backend = default_backend()

    @classmethod
    def from_plaintext_key(cls, plaintext_key: str) -> "Encryptor":
        hashed_key = hashlib.sha256(plaintext_key.encode()).digest()  # (32 bytes) key
        return cls(hashed_key)

    @classmethod
    def from_encryption_key(cls, encryption_key: bytes) -> tuple["Encryptor", bytes]:
        hashed_key, iv = encryption_key.split(cls._sep)
        return cls(hashed_key), iv

    def encrypt(self, plaintext: str) -> tuple[bytes, bytes]:
        iv = os.urandom(16)  # Generate a random 16-byte IV

        cipher = Cipher(self.aes, modes.CBC(iv), backend=self.backend)
        encryptor = cipher.encryptor()

        padded_data = self._pad(plaintext.encode())
        ciphertext = encryptor.update(padded_data) + encryptor.finalize()

        return iv, ciphertext

    def decrypt(self, ciphertext: bytes, iv: bytes) -> str:
        cipher = Cipher(self.aes, modes.CBC(iv), backend=self.backend)
        decryptor = cipher.decryptor()

        decrypted_data = decryptor.update(ciphertext) + decryptor.finalize()
        plaintext = self._unpad(decrypted_data).decode()

        return plaintext

    def get_encryption_key(self, iv: bytes) -> bytes:
        return self.hashed_key + self._sep + iv

    def _pad(self, data: bytes) -> bytes:
        padder = PKCS7(self.block_size).padder()
        return padder.update(data) + padder.finalize()

    def _unpad(self, data: bytes) -> bytes:
        unpadder = PKCS7(self.block_size).unpadder()
        return unpadder.update(data) + unpadder.finalize()
