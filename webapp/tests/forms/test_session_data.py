import datetime
import time
import unittest
from unittest.mock import patch, MagicMock

import fakeredis
import pytest
from cryptography.fernet import InvalidToken

from app.data_access.form_data_controller import FormDataController
from app.forms.session_data import get_session_data, serialize_session_data, deserialize_session_data, \
    override_session_data

CURRENT_USER = "app.forms.session_data.current_user"


@pytest.fixture(autouse=True)
def testing_database(monkeypatch):
    # Using monkeypatch to replace the redis connection of the controller with a fake redis instance
    fakeredis_connection = fakeredis.FakeStrictRedis()
    monkeypatch.setattr(FormDataController, "_redis_connection", fakeredis_connection)
    # Also mocking the current_user
    monkeypatch.setattr(CURRENT_USER, MagicMock(idnr_hashed="0123456789"))
    yield monkeypatch
    fakeredis_connection.flushall()


class TestGetSessionData:

    def test_if_session_data_then_return_session_data(self):
        # given
        data = {"name": "Peach", "sister": "Daisy", "husband": "Mario"}
        override_session_data(data)
        # when
        stored_data = get_session_data('form_data')
        # then
        assert data == stored_data

    def test_if_session_data_and_default_data_different_then_update_session_data(self):
        # given
        default_data = {"brother": "Luigi"}
        session_data = {"name": "Peach", "sister": "Daisy", "husband": "Mario"}
        expected_data = {**session_data, **default_data}
        override_session_data(session_data)
        # when
        session_data = get_session_data('form_data', default_data=default_data)
        # then
        assert expected_data == session_data

    def test_if_session_data_for_the_current_user_is_returned(self, testing_database):
        # given
        form_data = {"brother": "Luigi"}
        other_form_data = {"enemy": "Bowser"}
        expected_data = {**other_form_data}
        override_session_data(form_data)
        testing_database.setattr(CURRENT_USER, MagicMock(idnr_hashed="9876543210"))
        override_session_data(other_form_data)
        # when
        session_data = get_session_data('form_data')
        # then
        assert expected_data == session_data

    def test_if_no_form_data_in_session_and_no_default_data_then_return_nothing(self):
        # given
        # when
        session_data = get_session_data('form_data')
        # then
        assert {} == session_data

    def test_if_no_form_data_in_session_then_return_default_data(self):
        # given
        default_data = {"brother": "Luigi"}
        # when
        session_data = get_session_data('form_data', default_data=default_data)
        # then
        assert default_data == session_data

    def test_if_no_session_data_and_debug_data_provided_then_return_copy(self):

        original_default_data = {}
        session_data = get_session_data('form_data', default_data=original_default_data)

        assert original_default_data is not session_data


class TestSerializeSessionData:

    @pytest.fixture(autouse=True)
    def attach_fixtures(self, app):
        self.app = app

    def test_deserialized_dict_should_equal_original(self):
        original_data = {"name": "Tom Riddle", "dob": datetime.date(1926, 12, 31)}
        serialized_data = serialize_session_data(original_data)
        deserialized_data = deserialize_session_data(serialized_data, self.app.config['PERMANENT_SESSION_LIFETIME'])
        assert original_data == deserialized_data

    def test_serialization_should_encrypt_and_compress(self):
        from zlib import compress
        from app.crypto.encryption import encrypt

        original_data = {"name": "Tom Riddle", "dob": datetime.date(1926, 12, 31)}

        with patch("app.forms.session_data.encrypt", MagicMock(wraps=encrypt)) as encrypt_mock, \
            patch("app.forms.session_data.zlib.compress", MagicMock(wraps=compress)) as compress_mock:

            serialize_session_data(original_data)

            encrypt_mock.assert_called()
            compress_mock.assert_called()


class TestDeserializeSessionData(unittest.TestCase):
    @pytest.fixture(autouse=True)
    def attach_fixtures(self, app, test_request_context):
        self.app = app
        self.req = test_request_context

    def test_if_ttl_smaller_than_passed_time_then_return_original_data(self):
        original_data = {"name": "Tom Riddle", "dob": datetime.date(1926, 12, 31)}
        creation_time = time.time()
        passed_time = creation_time + 5
        ttl = 5

        with patch("time.time") as mocked_time:
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

        with patch("time.time") as mocked_time:
            mocked_time.return_value = creation_time
            serialized_data = serialize_session_data(original_data)

            mocked_time.return_value = passed_time
            deserialized_data = deserialize_session_data(serialized_data, ttl)

            self.assertEqual({}, deserialized_data)

    def test_if_deserialize_raises_invalid_token_then_return_empty_dict(self):
        original_data = {"name": "Tom Riddle", "dob": datetime.date(1926, 12, 31)}

        with patch("app.forms.session_data.decrypt", MagicMock(side_effect=InvalidToken)):
            serialized_data = serialize_session_data(original_data)
            deserialized_data = deserialize_session_data(serialized_data, self.app.config['PERMANENT_SESSION_LIFETIME'])

            self.assertEqual({}, deserialized_data)

    def test_if_session_data_empty_do_not_log_error(self):
        with patch("app.forms.session_data.logger.warn") as log_fun:
            deserialized_data = deserialize_session_data(b'', self.app.config['PERMANENT_SESSION_LIFETIME'])

            self.assertEqual({}, deserialized_data)
            log_fun.assert_not_called()


class TestOverrideSessionData:

    def test_data_is_saved_as_new_form_data(self):
        form_data = get_session_data('form_data')
        assert form_data == {}
        new_data = {'brother': 'Luigi'}
        override_session_data(new_data)
        form_data = get_session_data('form_data')
        assert form_data == new_data

    def test_data_is_saved_as_update_form_data(self):
        new_data = {'brother': 'Luigi'}
        override_session_data(new_data)
        update_data = {'mother': 'daisy'}
        override_session_data(update_data)
        form_data = get_session_data('form_data')
        assert form_data != new_data
        assert form_data == update_data

    def test_if_data_stored_with_other_identifier_then_it_is_not_changed(self, testing_database):
        new_data = {'brother': 'Luigi'}
        override_session_data(new_data)
        testing_database.setattr(CURRENT_USER, MagicMock(idnr_hashed="9876543210"))
        other_data = {'enemy': 'Bowser'}
        override_session_data(other_data)
        testing_database.setattr(CURRENT_USER, MagicMock(idnr_hashed="0123456789"))
        form_data = get_session_data('form_data')
        assert new_data == form_data
