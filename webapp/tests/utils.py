import os
import secrets

import pytest
from flask import current_app

from app.config import Config, ProductionConfig, StagingConfig
from app.data_access.user_controller import create_user, find_user
from app.forms.session_data import serialize_session_data


def gen_random_key(length=32):
    return secrets.token_urlsafe(length)


def create_session_form_data(data):
    return serialize_session_data(data)


def create_and_activate_user(idnr, dob, request_id, unlock_code):
    create_user(idnr, dob, request_id)
    find_user(idnr).activate(unlock_code)


@pytest.fixture
def production_flask_env():
    current_configuration_value = os.environ.get('FLASK_ENV')
    os.environ['FLASK_ENV'] = 'production'

    yield current_app

    os.environ['FLASK_ENV'] = current_configuration_value


@pytest.fixture
def staging_flask_env():
    current_configuration_value = os.environ.get('FLASK_ENV')
    os.environ['FLASK_ENV'] = 'staging'

    yield current_app

    os.environ['FLASK_ENV'] = current_configuration_value