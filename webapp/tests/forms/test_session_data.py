import unittest

from flask.sessions import SecureCookieSession

from app import app
from app.forms.flows.multistep_flow import serialize_session_data, deserialize_session_data
from app.forms.session_data import get_session_data
from tests.utils import create_session_form_data


class TestGetSessionData(unittest.TestCase):
    def setUp(self):
        with app.app_context() and app.test_request_context():
            self.session_data_identifier = 'form_data'

            # Set sessions up
            self.session_data = {"name": "Peach", "sister": "Daisy", "husband": "Mario"}

    def test_if_session_data_then_return_session_data(self):
        with app.app_context() and app.test_request_context() as req:
            req.session = SecureCookieSession(
                {self.session_data_identifier: create_session_form_data(self.session_data)})
            session_data = get_session_data(self.session_data_identifier)

            self.assertEqual(self.session_data, session_data)

    def test_if_session_data_and_default_data_different_then_update_session_data(self):
        default_data = {"brother": "Luigi"}
        expected_data = {**self.session_data, **default_data}

        with app.app_context() and app.test_request_context() as req:
            req.session = SecureCookieSession(
                {self.session_data_identifier: create_session_form_data(self.session_data)})

            session_data = get_session_data(self.session_data_identifier, default_data=default_data)

            self.assertEqual(expected_data, session_data)

    def test_if_session_data_in_incorrect_identifier_then_return_only_data_from_correct_identifier(self):
        form_data = {"brother": "Luigi"}
        incorrect_identifier_data = {"enemy": "Bowser"}
        expected_data = {**form_data}

        with app.app_context() and app.test_request_context() as req:
            req.session = SecureCookieSession(
                {self.session_data_identifier: create_session_form_data(form_data),
                 "INCORRECT_IDENTIFIER": create_session_form_data(incorrect_identifier_data)})

            session_data = get_session_data(self.session_data_identifier)

            self.assertEqual(expected_data, session_data)

    def test_if_only_data_in_incorrect_identifier_then_return_empty_data(self):
        incorrect_identifier = {"enemy": "Bowser"}

        with app.app_context() and app.test_request_context() as req:
            req.session = SecureCookieSession({"INCORRECT_IDENTIFIER": create_session_form_data(incorrect_identifier)})

            session_data = get_session_data(self.session_data_identifier)

            self.assertEqual({}, session_data)

    def test_if_no_form_data_in_session_then_return_default_data(self):
        default_data = {"brother": "Luigi"}
        with app.app_context() and app.test_request_context() as req:
            req.session = SecureCookieSession({})
            session_data = get_session_data(self.session_data_identifier, default_data=default_data)

            self.assertEqual(default_data, session_data)

    def test_if_no_session_data_and_debug_data_provided_then_return_copy(self):
        original_default_data = {}
        with app.app_context() and app.test_request_context():
            session_data = get_session_data(self.session_data_identifier, default_data=original_default_data)

            self.assertIsNot(original_default_data, session_data)

    def test_if_no_session_data_and_no_debug_data_then_return_empty_dict(self):
        with app.app_context() and app.test_request_context():
            session_data = get_session_data(self.session_data_identifier)

            self.assertEqual({}, session_data)

    def test_if_session_data_then_keep_data_in_session(self):
        with app.app_context() and app.test_request_context() as req:
            req.session = SecureCookieSession({'form_data': serialize_session_data(self.session_data)})

            get_session_data(self.session_data_identifier)

            self.assertIn('form_data', req.session)
            self.assertEqual(self.session_data, deserialize_session_data(req.session['form_data'],
                                                                         app.config['PERMANENT_SESSION_LIFETIME']))
