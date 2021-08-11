from typing import Optional

from flask import session

from app.forms.flows.multistep_flow import deserialize_session_data


def get_session_data(session_data_identifier, ttl: Optional[int] = None, default_data=None):
    serialized_session = session.get(session_data_identifier, b"")

    if default_data:
        # updates session_data only with non_existent values
        stored_data = default_data | deserialize_session_data(serialized_session, ttl)
    else:
        stored_data = deserialize_session_data(serialized_session, ttl)

    return stored_data
