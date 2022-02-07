
import logging
import zlib

from cryptography.fernet import InvalidToken
from flask import json
from typing import Optional
from abc import ABC, abstractmethod

from app.crypto.encryption import encrypt, decrypt

logger = logging.getLogger(__name__)

class FormStorage(ABC):

    @abstractmethod
    def get_data(self, data_identifier, ttl: Optional[int] = None, default_data=None):
        pass


    @abstractmethod
    def override_data(self, data_to_store, data_identifier):
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