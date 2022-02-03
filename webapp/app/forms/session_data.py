import logging
import zlib
from typing import Optional

from cryptography.fernet import InvalidToken
from flask import json
from pydantic import MissingError
from flask_login import current_user

from app.crypto.encryption import encrypt, decrypt
from app.data_access.form_data_controller import FormDataController

logger = logging.getLogger(__name__)


def get_session_data(session_data_identifier, ttl: Optional[int] = None, default_data=None):
    key = create_key_identifier_with_user_id(session_data_identifier)
    try:
        form_data = FormDataController().get_from_redis(key)
    except MissingError:
        form_data = {}

    if default_data:
        # updates session_data only with non_existent values
        stored_data = default_data | deserialize_session_data(form_data, ttl)
    else:
        stored_data = deserialize_session_data(form_data, ttl)

    return stored_data


def serialize_session_data(data):
    json_bytes = json.dumps(data).encode()
    compressed = zlib.compress(json_bytes)
    encrypted = encrypt(compressed)

    return encrypted


def deserialize_session_data(serialized_session, ttl: Optional[int] = None):
    session_data = {}
    if serialized_session:
        serialized_session = serialized_session if type(serialized_session) is bytes else str.encode(serialized_session)
        try:
            decrypted = decrypt(serialized_session, ttl)
            decompressed = zlib.decompress(decrypted)
            session_data = json.loads(decompressed.decode())
        except InvalidToken:
            logger.warning("Session decryption failed", exc_info=True)
            session_data = {}
    return session_data


def override_session_data(stored_data, session_data_identifier='form_data'):
    key = create_key_identifier_with_user_id(session_data_identifier)
    FormDataController().save_to_redis(key, serialize_session_data(stored_data))


def create_key_identifier_with_user_id(identifier):
    return current_user.idnr_hashed + '_' + identifier
