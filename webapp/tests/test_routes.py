import copy
from unittest.mock import patch

import pytest
from flask import Flask
from flask.sessions import SecureCookieSession
from werkzeug.datastructures import ImmutableMultiDict

from app import routes
from app.app import create_app
from app.forms.session_data import get_session_data
from tests.utils import production_flask_env, staging_flask_env


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


class TestRegisterTestingRequestHandlers:

    @pytest.mark.usefixtures("production_flask_env")
    def test_if_production_environment_then_do_not_register_testing_routes(self):
        app = Flask(
            __name__.split(".")[0],
            static_url_path="",
        )
        old_view_functions = copy.deepcopy(app.view_functions)

        register_testing_request_handlers(app)

        assert app.view_functions == old_view_functions

    @pytest.mark.usefixtures("staging_flask_env")
    def test_if_staging_environment_then_register_testing_routes(self, app):
        app = Flask(
            __name__.split(".")[0],
            static_url_path="",
        )
        old_view_functions = copy.deepcopy(app.view_functions)

        register_testing_request_handlers(app)

        assert app.view_functions.keys() != [old_view_functions.keys(), 'set_data']


class TestSetTestingDataRoute:

    @pytest.mark.usefixtures("production_flask_env")
    def test_if_production_environment_then_return_405(self):
        identifier = "form_data"
        data = {'username': 'Frodo', 'ring': 'one'}
        app = create_app()

        with app.app_context(), app.test_client() as c:
            response = c.post(f'/testing/set_data/{identifier}', json=data)
            assert response.status_code == 405

    @pytest.mark.usefixtures("staging_flask_env")
    def test_if_staging_environment_then_return_set_data(self):
        identifier = "form_data"
        data = {'username': 'Frodo', 'ring': 'one'}
        app = create_app()

        with app.app_context(), app.test_client() as c:
            response = c.post(f'/testing/set_data/{identifier}', json=data)
        assert response.status_code == 200
        assert response.json == data

    def test_if_data_provided_then_set_session_correctly(self, app):
        identifier = "form_data"
        data = {'username': 'Frodo', 'ring': 'one'}
        with app.test_request_context(method="POST", json=data) as req:
            req.session = SecureCookieSession({})
            app.view_functions.get('set_data')(identifier)

            assert get_session_data(identifier) == data
