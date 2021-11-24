import secrets

import pytest

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
def configuration_with_production_environment_testing_route_policy():
    current_configuration_value = Config.ALLOW_TESTING_ROUTES
    Config.ALLOW_TESTING_ROUTES = ProductionConfig.ALLOW_TESTING_ROUTES

    yield Config

    Config.ALLOW_TESTING_ROUTES = current_configuration_value


@pytest.fixture
def configuration_with_staging_environment_testing_route_policy():
    current_configuration_value = Config.ALLOW_TESTING_ROUTES
    Config.ALLOW_TESTING_ROUTES = StagingConfig.ALLOW_TESTING_ROUTES

    yield Config

    Config.ALLOW_TESTING_ROUTES = current_configuration_value