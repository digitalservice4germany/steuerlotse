from typing import Optional

from Cryptodome.Cipher import PKCS1_OAEP
from Cryptodome.PublicKey import RSA
from cryptography.fernet import Fernet

from app.config import Config

# For hybrid encryption version 1 we're using:
# Symmetric encryption of data using Fernet (AES-128, 128bit key, CBC mode, PKCS7 padding, HMAC with SHA256)
# Asymmetric encryption of encryption key using pycryptodome (RSA with PKCS#1 OAEP and key length 4096)
HYBRID_ENCRYPTION_VERSION = b'1'


def encrypt(plaintext: bytes):
    cipher = Fernet(Config.ENCRYPTION_KEY)
    return cipher.encrypt(plaintext)


def decrypt(cipher_text: bytes, ttl: Optional[int] = None):
    cipher = Fernet(Config.ENCRYPTION_KEY)
    return cipher.decrypt(cipher_text, ttl)


def hybrid_encrypt(plaintext: bytes):
    """
        The resulting cipher constists of the following parts:
            1 byte: Version Number
            x byte: asymmetrically encrypted symmetric key
            x byte: symmetrically encrypted plaintext

        :param plaintext the text to encrypt
    """
    symm_key = Fernet.generate_key()
    symm_encrypted_data = Fernet(symm_key).encrypt(plaintext)

    asymm_public_key = RSA.import_key(Config.RSA_ENCRYPT_PUBLIC_KEY)
    asymm_encrypted_symm_key = PKCS1_OAEP.new(asymm_public_key).encrypt(symm_key)

    return HYBRID_ENCRYPTION_VERSION + asymm_encrypted_symm_key + symm_encrypted_data


def hybrid_decrypt(encrypted_text: bytes, asymm_private_key):
    """
        The cipher to input should consist of the following parts:
            1 byte: Version Number
            x byte: asymmetrically encrypted symmetric key
            x byte: symmetrically encrypted plaintext

        :param encrypted_text cipher to decrypt in the above format
        :param asymm_private_key the private key to decrypt the encrypted text
    """
    version_number = encrypted_text[0]
    asymm_private_key = RSA.import_key(asymm_private_key)
    asymm_encrypted_symm_key = encrypted_text[1:asymm_private_key.size_in_bytes() + 1]
    symm_encrypted_message = encrypted_text[asymm_private_key.size_in_bytes() + 1:]

    symm_key = PKCS1_OAEP.new(asymm_private_key).decrypt(asymm_encrypted_symm_key)
    message = Fernet(symm_key).decrypt(symm_encrypted_message)

    return message
