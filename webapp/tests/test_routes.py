import copy
import datetime

import pytest
from flask import Flask
from flask.sessions import SecureCookieSession
from werkzeug.datastructures import ImmutableMultiDict

from app.app import create_app
from app.config import Config, ProductionConfig, FunctionalTestingConfig
from app.forms.session_data import get_session_data

from app.routes import extract_information_from_request, register_testing_request_handlers


class TestExtractInformationFromRequest:

    def test_if_post_then_return_update_data_true(self, app):
        with app.test_request_context(method="POST"):
            update_data, _ = extract_information_from_request()

        assert update_data is True

    def test_if_get_then_return_update_data_false(self, app):
        with app.test_request_context(method="GET"):
            update_data, _ = extract_information_from_request()

        assert update_data is False

    def test_if_post_and_form_data_then_extract_correct_form_data(self, app):
        form_data = {'Slytherin': 'Loyalty'}
        with app.test_request_context(method="POST", data=form_data):
            update_data, extracted_form_data = extract_information_from_request()

        assert extracted_form_data == ImmutableMultiDict(form_data)


@pytest.fixture
def configuration_with_production_environment_testing_route_policy():
    in_production_value = Config.ALLOW_TESTING_ROUTES
    Config.ALLOW_TESTING_ROUTES = ProductionConfig.ALLOW_TESTING_ROUTES

    yield Config

    Config.ALLOW_TESTING_ROUTES = in_production_value


@pytest.fixture
def configuration_with_functional_environment_testing_route_policy():
    in_production_value = Config.ALLOW_TESTING_ROUTES
    Config.ALLOW_TESTING_ROUTES = FunctionalTestingConfig.ALLOW_TESTING_ROUTES

    yield Config

    Config.ALLOW_TESTING_ROUTES = in_production_value


class TestRegisterTestingRequestHandlers:

    @pytest.mark.usefixtures("configuration_with_production_environment_testing_route_policy")
    def test_if_production_environment_then_do_not_register_testing_routes(self):
        app = Flask(
            __name__.split(".")[0],
            static_url_path="",
        )
        old_view_functions = copy.deepcopy(app.view_functions)

        register_testing_request_handlers(app)

        assert app.view_functions == old_view_functions

    @pytest.mark.usefixtures("configuration_with_functional_environment_testing_route_policy")
    def test_if_staging_environment_then_register_testing_routes(self):
        app = Flask(
            __name__.split(".")[0],
            static_url_path="",
        )
        old_view_functions = copy.deepcopy(app.view_functions)

        register_testing_request_handlers(app)

        assert app.view_functions.keys() != [old_view_functions.keys(), 'set_data']


class TestSetTestingDataRoute:

    @pytest.mark.usefixtures("configuration_with_production_environment_testing_route_policy", "testing_current_user")
    def test_if_production_environment_then_return_405(self):
        identifier = "form_data"
        data = {'username': 'Frodo', 'ring': 'one'}
        app = create_app()

        with app.app_context(), app.test_client() as c:
            response = c.post(f'/testing/set_session_data/{identifier}', json=data)
            assert response.status_code == 405

    @pytest.mark.usefixtures("configuration_with_functional_environment_testing_route_policy", "testing_current_user")
    def test_if_staging_environment_then_return_set_data(self, app):
        identifier = "form_data"
        data = {'username': 'Frodo', 'ring': 'one'}

        with app.app_context(), app.test_client() as c:
            response = c.post(f'/testing/set_session_data/{identifier}', json=data)
        assert response.status_code == 200
        assert response.json == data

    @pytest.mark.usefixtures("configuration_with_functional_environment_testing_route_policy", "testing_current_user")
    def test_if_staging_environment_and_incorrect_identifier_then_return_set_data(self, app):
        identifier = "INCORRECT_IDENTIFIER"
        data = {'username': 'Frodo', 'ring': 'one'}

        with app.app_context(), app.test_client() as c:
            response = c.post(f'/testing/set_session_data/{identifier}', json=data)
        assert response.status_code == 200
        assert response.json is None
        assert response.data == b"Not allowed identifier"

    @pytest.mark.usefixtures("testing_current_user")
    def test_if_data_provided_then_set_session_correctly(self, app):
        identifier = "form_data"
        data = {'username': 'Frodo', 'ring': 'one'}
        with app.test_request_context(method="POST", json=data) as req:
            req.session = SecureCookieSession({})
            app.view_functions.get('set_data')(identifier)

            assert get_session_data(identifier) == data

    @pytest.mark.usefixtures("testing_current_user")
    def test_if_data_provided_with_date_then_set_session_correctly(self, app):
        identifier = "form_data"
        data = {'username': 'Frodo', 'date': '02.09.2022'}
        expected_data = {'username': 'Frodo', 'date': datetime.date(2022, 9, 2)}
        with app.test_request_context(method="POST", json=data) as req:
            req.session = SecureCookieSession({})
            app.view_functions.get('set_data')(identifier)

            assert get_session_data(identifier) == expected_data

    @pytest.mark.usefixtures("testing_current_user")
    def test_if_data_provided_with_bool_then_set_session_correctly(self, app):
        identifier = "form_data"
        data = {'username': 'Frodo', 'bool': True}
        with app.test_request_context(method="POST", json=data) as req:
            req.session = SecureCookieSession({})
            app.view_functions.get('set_data')(identifier)

            assert get_session_data(identifier) == data

    @pytest.mark.usefixtures("testing_current_user")
    def test_if_data_provided_with_int_then_set_session_correctly(self, app):
        identifier = "form_data"
        data = {'username': 'Frodo', 'int': 7531}
        with app.test_request_context(method="POST", json=data) as req:
            req.session = SecureCookieSession({})
            app.view_functions.get('set_data')(identifier)

            assert get_session_data(identifier) == data

    @pytest.mark.usefixtures("testing_current_user")
    def test_if_data_provided_but_incorrect_session_identifier_then_do_not_set_session(self, app):
        identifier = "INCORRECT_IDENTIFIER"
        data = {'username': 'Frodo', 'ring': 'one'}
        with app.test_request_context(method="POST", json=data) as req:
            req.session = SecureCookieSession({})
            app.view_functions.get('set_data')(identifier)

            assert get_session_data(identifier) == {}
