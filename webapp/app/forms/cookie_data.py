import logging
from typing import Optional
from flask import session, json

from app.forms.session_data import deserialize_session_data, serialize_session_data

logger = logging.getLogger(__name__)


def get_data_from_cookie(cookie_data_identifier, ttl: Optional[int] = None, default_data=None):
    """
    Gets data from the cookie that is associated with the currect session. The data is return deserialized.

    :param cookie_data_identifier: A string used to identify what data should be taken from the cookie
    :param ttl: The time to live for the cookie
    """
    serialized_session = session.get(cookie_data_identifier, b"")

    if default_data:
        # updates session_data only with non_existent values
        stored_data = default_data | _deserialize_cookie_data(serialized_session, ttl)
    else:
        stored_data = _deserialize_cookie_data(serialized_session, ttl)

    return stored_data


def override_data_in_cookie(data_to_store, cookie_data_identifier='form_data'):
    """
    Stores data in the cookie that is associated with the currect session. The data is serialized before it is stored.

    :param data_to_store: The data that is overriding the existing data in the cookie
    :param cookie_data_identifier: A string used to identify what data should be taken from the cookie
    """
    session[cookie_data_identifier] = _serialize_cookie_data(data_to_store)


def _serialize_cookie_data(data):
    return serialize_session_data(data)


def _deserialize_cookie_data(serialized_session, ttl: Optional[int] = None):
    return deserialize_session_data(serialized_session, ttl)



