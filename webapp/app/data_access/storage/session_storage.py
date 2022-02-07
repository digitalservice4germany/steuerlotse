from typing import Optional

from pydantic import MissingError
from flask_login import current_user

from app.data_access.form_data_controller import FormDataController
from app.data_access.storage.form_storage import FormStorage


class SessionStorage(FormStorage):
    
    def get_data(self, data_identifier, ttl: Optional[int] = None, default_data=None):
        key = self.create_key_identifier_with_user_id(data_identifier)
        if not key:
            return None
        try:
            form_data = FormDataController().get_from_redis(key)
        except MissingError:
            form_data = {}

        if default_data:
            # updates session_data only with non_existent values
            stored_data = default_data | self.deserialize_data(form_data, ttl)
        else:
            stored_data = self.deserialize_data(form_data, ttl)

        return stored_data


    def override_data(self, stored_data, data_identifier='form_data'):
        key = self.create_key_identifier_with_user_id(data_identifier)
        if not key:
            return
        FormDataController().save_to_redis(key, self.serialize_data(stored_data))


    def create_key_identifier_with_user_id(self, identifier):
        default_identifier = 'default'
        if identifier is None:
            identifier = default_identifier

        if not hasattr(current_user, 'idnr_hashed'):
            return None

        return current_user.idnr_hashed + '_' + identifier