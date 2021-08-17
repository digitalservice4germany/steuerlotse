import datetime
import time
import unittest
from unittest.mock import patch, MagicMock

from cryptography.fernet import InvalidToken
from flask.sessions import SecureCookieSession

from app import app
from app.forms.session_data import get_session_data, serialize_session_data, deserialize_session_data, \
    override_session_data
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


class TestSerializeSessionData(unittest.TestCase):

    def test_deserialized_dict_should_equal_original(self):
        original_data = {"name": "Tom Riddle", "dob": datetime.date(1926, 12, 31)}
        with app.app_context() and app.test_request_context():
            serialized_data = serialize_session_data(original_data)
            deserialized_data = deserialize_session_data(serialized_data, app.config['PERMANENT_SESSION_LIFETIME'])
            self.assertEqual(original_data, deserialized_data)

    def test_serialization_should_encrypt_and_compress(self):
        from zlib import compress
        from app.crypto.encryption import encrypt

        original_data = {"name": "Tom Riddle", "dob": datetime.date(1926, 12, 31)}

        with app.app_context() and app.test_request_context(), \
            patch("app.forms.session_data.encrypt", MagicMock(wraps=encrypt)) as encrypt_mock, \
            patch("app.forms.session_data.zlib.compress", MagicMock(wraps=compress)) as compress_mock:

            serialize_session_data(original_data)

            encrypt_mock.assert_called()
            compress_mock.assert_called()


class TestDeserializeSessionData(unittest.TestCase):

    def test_if_ttl_smaller_than_passed_time_then_return_original_data(self):
        original_data = {"name": "Tom Riddle", "dob": datetime.date(1926, 12, 31)}
        creation_time = time.time()
        passed_time = creation_time + 5
        ttl = 5

        with app.app_context() and app.test_request_context(), \
             patch("time.time") as mocked_time:
            mocked_time.return_value = creation_time
            serialized_data = serialize_session_data(original_data)

            mocked_time.return_value = passed_time
            deserialized_data = deserialize_session_data(serialized_data, ttl)

            self.assertEqual(original_data, deserialized_data)

    def test_if_ttl_greater_than_passed_time_then_return_empty_dict(self):
        original_data = {"name": "Tom Riddle", "dob": datetime.date(1926, 12, 31)}
        creation_time = time.time()
        passed_time = creation_time + 5
        ttl = 2

        with app.app_context() and app.test_request_context(), \
             patch("time.time") as mocked_time:
            mocked_time.return_value = creation_time
            serialized_data = serialize_session_data(original_data)

            mocked_time.return_value = passed_time
            deserialized_data = deserialize_session_data(serialized_data, ttl)

            self.assertEqual({}, deserialized_data)

    def test_if_deserialize_raises_invalid_token_then_return_empty_dict(self):
        original_data = {"name": "Tom Riddle", "dob": datetime.date(1926, 12, 31)}

        with app.app_context() and app.test_request_context(), \
             patch("app.forms.session_data.decrypt", MagicMock(side_effect=InvalidToken)):
            serialized_data = serialize_session_data(original_data)
            deserialized_data = deserialize_session_data(serialized_data, app.config['PERMANENT_SESSION_LIFETIME'])

            self.assertEqual({}, deserialized_data)

    def test_if_session_data_empty_do_not_log_error(self):
        with app.app_context() and app.test_request_context(), \
                patch("app.forms.session_data.app.logger.warn") as log_fun:
            deserialized_data = deserialize_session_data(b'', app.config['PERMANENT_SESSION_LIFETIME'])

            self.assertEqual({}, deserialized_data)
            log_fun.assert_not_called()


class TestOverrideSessionData(unittest.TestCase):
    def test_data_is_saved_to_empty_session(self):
        new_data = {'brother': 'Luigi'}
        with app.app_context() and app.test_request_context() as req:
            with patch('app.forms.session_data.serialize_session_data', MagicMock(side_effect=lambda _: _)):
                self.assertNotIn('form_data', req.session)
                override_session_data(new_data)
                self.assertIn('form_data', req.session)
                self.assertEqual(new_data, req.session['form_data'])

    def test_data_is_saved_to_prefilled_session(self):
        new_data = {'brother': 'Luigi'}
        with app.app_context() and app.test_request_context() as req:
            with patch('app.forms.session_data.serialize_session_data', MagicMock(side_effect=lambda _: _)):
                req.session = {'form_data': {'brother': 'Mario', 'pet': 'Yoshi'}}
                self.assertIn('form_data', req.session)
                override_session_data(new_data)
                self.assertIn('form_data', req.session)
                self.assertEqual(new_data, req.session['form_data'])

    def test_if_data_stored_with_other_identifier_then_it_is_not_changed(self):
        new_data = {'brother': 'Luigi'}
        other_data = {'enemy': 'Bowser'}
        with app.app_context() and app.test_request_context() as req:
            with patch('app.forms.session_data.serialize_session_data', MagicMock(side_effect=lambda _: _)):
                req.session = {'form_data': {'brother': 'Mario', 'pet': 'Yoshi'},
                               'OTHER_IDENTIFIER': other_data}
                override_session_data(new_data, 'form_data')
                self.assertEqual(other_data, req.session['OTHER_IDENTIFIER'])

    def test_if_stored_data_identifier_is_set_then_override_session_data_with_that_new_identifier(self):
        new_data = {'brother': 'Luigi'}
        other_data = {'enemy': 'Bowser'}
        new_identifier = "NEW_IDENTIFIER"
        with app.app_context() and app.test_request_context() as req:
            with patch('app.forms.session_data.serialize_session_data', MagicMock(side_effect=lambda _: _)):
                req.session = {'form_data': {'brother': 'Mario', 'pet': 'Yoshi'},
                               'OTHER_IDENTIFIER': other_data}
                override_session_data(new_data, new_identifier)
                self.assertEqual(new_data, req.session[new_identifier])
