from typing import Optional

from pydantic import MissingError
from flask_login import current_user

from app.data_access.redis_connector_service import RedisConnectorService
from app.data_access.storage.form_storage import FormStorage


class SessionStorage(FormStorage):
    @staticmethod
    def get_data(data_identifier, ttl: Optional[int] = None, default_data=None, key_identifier=None):
        key = SessionStorage.create_key_identifier_with_user_id(data_identifier, key_identifier)

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

        return stored_data

    @staticmethod
    def override_data(stored_data, data_identifier='form_data', key_identifier=None):
        key = SessionStorage.create_key_identifier_with_user_id(data_identifier, key_identifier)

        if not key:
            return
        RedisConnectorService().save_to_redis(key, SessionStorage.serialize_data(stored_data))

    @staticmethod
    def delete_data(data_identifier='form-data', key_identifier=None):
        key = SessionStorage.create_key_identifier_with_user_id(data_identifier, key_identifier)
        if not key:
            return
        RedisConnectorService().remove_from_redis(key)

    @staticmethod
    def create_key_identifier_with_user_id(identifier, key_identifier=None):
        default_identifier = 'default'
        if identifier is None:
            identifier = default_identifier

        if hasattr(current_user, 'idnr_hashed'):
            return current_user.idnr_hashed + '_' + identifier
        elif not hasattr(current_user, 'idnr_hashed') and key_identifier is not None:
            return key_identifier + '_' + identifier
        return None
