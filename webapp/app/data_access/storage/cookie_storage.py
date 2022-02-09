from typing import Optional
from flask import session

from app.data_access.storage.form_storage import FormStorage


class CookieStorage(FormStorage):
    @staticmethod
    def get_data(data_identifier, ttl: Optional[int] = None, default_data=None):
        serialized_session = session.get(data_identifier, b"")

        if default_data:
            # updates session_data only with non_existent values
            stored_data = default_data | CookieStorage.deserialize_data(serialized_session, ttl)
        else:
            stored_data = CookieStorage.deserialize_data(serialized_session, ttl)

        return stored_data

    @staticmethod
    def override_data(data_to_store, data_identifier='form_data'):
        session[data_identifier] = CookieStorage.serialize_data(data_to_store)