from typing import Optional
from flask import session

from app.data_access.storage.form_storage import FormStorage


class CookieStorage(FormStorage):
    def get_data(self, data_identifier, ttl: Optional[int] = None, default_data=None):
        """
        Gets data from the cookie that is associated with the currect session. The data is return deserialized.

        :param data_identifier: A string used to identify what data should be taken from the cookie
        :param ttl: The time to live for the cookie
        :param default_data: Default data that will be used to replace missing data points
        """
        serialized_session = session.get(data_identifier, b"")

        if default_data:
            # updates session_data only with non_existent values
            stored_data = default_data | self.deserialize_data(serialized_session, ttl)
        else:
            stored_data = self.deserialize_data(serialized_session, ttl)

        return stored_data


    def override_data(self, data_to_store, data_identifier='form_data'):
        """
        Stores data in the cookie that is associated with the currect session. The data is serialized before it is stored.

        :param data_to_store: The data that is overriding the existing data in the cookie
        :param cookie_data_identifier: A string used to identify what data should be taken from the cookie
        """
        session[data_identifier] = self.serialize_data(data_to_store)