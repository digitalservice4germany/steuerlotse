import secrets

from app.data_access.user_controller import create_user, find_user
from app.data_access.storage.session_storage import SessionStorage


def gen_random_key(length=32):
    return secrets.token_urlsafe(length)


def create_session_form_data(data):
    return SessionStorage().serialize_data(data)


def create_and_activate_user(idnr, dob, request_id, unlock_code):
    create_user(idnr, dob, request_id)
    find_user(idnr).activate(unlock_code)


