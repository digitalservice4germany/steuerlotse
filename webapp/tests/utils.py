import secrets

from app.data_access.user_controller import create_user, find_user
from app.forms.flows.multistep_flow import serialize_session_data


def gen_random_key(length=32):
    return secrets.token_urlsafe(length)


def create_session_form_data(data):
    return serialize_session_data(data)


def create_and_activate_user(idnr, dob, request_id, unlock_code):
    create_user(idnr, dob, request_id)
    find_user(idnr).activate(unlock_code)
