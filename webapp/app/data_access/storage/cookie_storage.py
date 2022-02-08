from typing import Optional
from flask import session

from app.data_access.storage.form_storage import FormStorage


class CookieStorage(FormStorage):
    def get_data(self, data_identifier, ttl: Optional[int] = None, default_data=None):
        serialized_session = session.get(data_identifier, b"")

        if default_data:
            # updates session_data only with non_existent values
            stored_data = default_data | self.deserialize_data(serialized_session, ttl)
        else:
            stored_data = self.deserialize_data(serialized_session, ttl)

        return stored_data


    def override_data(self, data_to_store, data_identifier='form_data'):
        session[data_identifier] = self.serialize_data(data_to_store)