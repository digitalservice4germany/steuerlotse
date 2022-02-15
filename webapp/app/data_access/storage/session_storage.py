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
        if Config.USE_COOKIE_STORAGE:
            logger.debug(f"USE_COOKIE_STORAGE used!")
            return CookieStorage.get_data(data_identifier=data_identifier, ttl=ttl, default_data=default_data)
        
        
        key = SessionStorage.create_key_identifier_with_user_id(data_identifier)
        logger.debug(f"Session Key generated for get: {key}")
        if not key:
            return None
        try:
            form_data = RedisConnectorService().get_from_redis(key)
        except MissingError:
            logger.debug(f"MissingError from redis for key {key}")
            form_data = {}

        if default_data:
            # updates session_data only with non_existent values
            stored_data = default_data | SessionStorage.deserialize_data(form_data, ttl)
        else:
            stored_data = SessionStorage.deserialize_data(form_data, ttl)

        return stored_data

    @staticmethod
    def override_data(stored_data, data_identifier='form_data'):
        if Config.USE_COOKIE_STORAGE:
            logger.debug(f"USE_COOKIE_STORAGE used!")
            CookieStorage.override_data(data_to_store=stored_data, data_identifier=data_identifier)
            return
        
        key = SessionStorage.create_key_identifier_with_user_id(data_identifier)
        logger.debug(f"Session Key generated for set: {key}")
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