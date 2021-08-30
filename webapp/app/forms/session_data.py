import logging
import zlib
from typing import Optional

from cryptography.fernet import InvalidToken
from flask import session, json

from app.crypto.encryption import encrypt, decrypt


logger = logging.getLogger(__name__)


def get_session_data(session_data_identifier, ttl: Optional[int] = None, default_data=None):
    serialized_session = session.get(session_data_identifier, b"")

    if default_data:
        # updates session_data only with non_existent values
        stored_data = default_data | deserialize_session_data(serialized_session, ttl)
    else:
        stored_data = deserialize_session_data(serialized_session, ttl)

    return stored_data


def serialize_session_data(data):
    json_bytes = json.dumps(data).encode()
    compressed = zlib.compress(json_bytes)
    encrypted = encrypt(compressed)

    return encrypted


def deserialize_session_data(serialized_session, ttl: Optional[int] = None):
    session_data = {}
    if serialized_session:
        try:
            decrypted = decrypt(serialized_session, ttl)
            decompressed = zlib.decompress(decrypted)
            session_data = json.loads(decompressed.decode())
        except InvalidToken:
            logger.warning("Session decryption failed", exc_info=True)
            session_data = {}
    return session_data


def override_session_data(stored_data, session_data_identifier='form_data'):
    session[session_data_identifier] = serialize_session_data(stored_data)
