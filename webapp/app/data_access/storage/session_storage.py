import logging

from typing import Optional

from pydantic import MissingError
from flask_login import current_user

from app.data_access.redis_connector_service import RedisConnectorService
from app.data_access.storage.form_storage import FormStorage

#TODO: Remove this after security & data protection
from app.data_access.storage.cookie_storage import CookieStorage
from app.config import Config


logger = logging.getLogger(__name__)


class SessionStorage(FormStorage):
    @staticmethod
    def get_data(data_identifier, ttl: Optional[int] = None, default_data=None):        
        key = SessionStorage.create_key_identifier_with_user_id(data_identifier)
        
        if not key:
            return None
        try:
            form_data = RedisConnectorService().get_from_redis(key)
        except MissingError:
            form_data = {}

        stored_data = SessionStorage.deserialize_data(form_data, ttl)
        if default_data and not set(default_data).intersection(set(stored_data)):
            # updates session_data only with non_existent values
            stored_data = default_data | stored_data
            
        logger.info(stored_data)

        return stored_data

    @staticmethod
    def override_data(stored_data, data_identifier='form_data'):        
        key = SessionStorage.create_key_identifier_with_user_id(data_identifier)

        if not key:
            return
        RedisConnectorService().save_to_redis(key, SessionStorage.serialize_data(stored_data))

    @staticmethod
    def create_key_identifier_with_user_id(identifier):
        default_identifier = 'default'
        if identifier is None:
            identifier = default_identifier

        if not hasattr(current_user, 'idnr_hashed'):
            return None

        return current_user.idnr_hashed + '_' + identifier