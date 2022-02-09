
import logging
import zlib

from cryptography.fernet import InvalidToken
from flask import json
from typing import Optional

from app.crypto.encryption import encrypt, decrypt

logger = logging.getLogger(__name__)

class FormStorage:

    @staticmethod
    def get_data(data_identifier, ttl: Optional[int] = None, default_data=None):
        """
        Gets data from a storage that is associated with the currect session. The data is return deserialized.

        :param data_identifier: A string used to identify what data should be taken from the cookie
        :param ttl: The time to live for the cookie
        :param default_data: Default data that will be used to replace missing data points
        """
        pass

    @staticmethod
    def override_data(data_to_store, data_identifier):
        """
        Stores data in a storage that is associated with the currect session. The data is serialized before it is stored.

        :param data_to_store: The data that is overriding the existing data in the cookie
        :param cookie_data_identifier: A string used to identify what data should be taken from the cookie
        """
        pass

    @staticmethod
    def serialize_data(data):
        json_bytes = json.dumps(data).encode()
        compressed = zlib.compress(json_bytes)
        encrypted = encrypt(compressed)

        return encrypted

    @staticmethod
    def deserialize_data(serialized_session, ttl: Optional[int] = None):
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