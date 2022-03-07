import datetime
import time
import pytest
from unittest.mock import MagicMock, patch
from cryptography.fernet import InvalidToken

from app.data_access.storage.session_storage import SessionStorage
from tests.conftest import CURRENT_USER_IDNR

CURRENT_USER = "app.data_access.storage.session_storage.current_user"


class TestGetSessionStorage:

    def test_if_session_data_then_return_session_data(self):
        data = {"name": "Peach", "sister": "Daisy", "husband": "Mario"}
        storage = SessionStorage
        storage.override_data(data)
        stored_data = storage.get_data('form_data')
        assert data == stored_data

    def test_if_session_data_and_default_data_different_then_update_session_data(self):
        default_data = {"brother": "Luigi"}
        session_data = {"name": "Peach", "sister": "Daisy", "husband": "Mario"}
        expected_data = {**session_data, **default_data}
        storage = SessionStorage
        storage.override_data(session_data)
        session_data = storage.get_data('form_data', default_data=default_data)
        assert expected_data == session_data

    def test_if_session_data_for_the_current_user_is_returned(self, testing_current_user):
        form_data = {"brother": "Luigi"}
        other_form_data = {"enemy": "Bowser"}
        expected_data = {**other_form_data}
        storage = SessionStorage
        storage.override_data(form_data)
        with patch(CURRENT_USER, MagicMock(idnr_hashed="9876543210")):
            storage.override_data(other_form_data)
            session_data = storage.get_data('form_data')
            assert expected_data == session_data

    def test_if_no_form_data_in_session_and_no_default_data_then_return_nothing(self):
        session_data = SessionStorage.get_data('form_data')
        assert {} == session_data

    def test_if_no_form_data_in_session_then_return_default_data(self):
        default_data = {"brother": "Luigi"}
        session_data = SessionStorage.get_data('form_data', default_data=default_data)
        assert default_data == session_data

    def test_if_no_session_data_and_debug_data_provided_then_return_copy(self):
        original_default_data = {}
        session_data = SessionStorage.get_data('form_data', default_data=original_default_data)
        assert original_default_data is not session_data

    def test_if_some_cookie_set_data_then_do_not_change_with_debug_data(self, app, test_request_context):
        cookie_data_without_all_keys = {"name": "Peach", "sister": "Daisy", "husband": "Mario"}
        default_data = {"brother": "Luigi", "husband": "Mario"}

        test_request_context.session = SessionStorage.override_data(cookie_data_without_all_keys, 'form_data')

        found_data = SessionStorage.get_data('form_data', default_data=default_data)

        assert found_data == cookie_data_without_all_keys

    def test_if_session_data_in_incorrect_identifier_then_return_only_data_from_correct_identifier(self):
        form_data = {"brother": "Luigi"}
        incorrect_identifier_data = {"enemy": "Bowser"}
        expected_data = {**form_data}

        storage = SessionStorage
        storage.override_data(form_data)
        storage.override_data(incorrect_identifier_data, "INCORRECT_IDENTIFIER")

        session_data = storage.get_data("form_data")

        assert expected_data == session_data

    def test_if_only_data_in_incorrect_identifier_then_return_empty_data(self):
        incorrect_identifier_data = {"enemy": "Bowser"}

        storage = SessionStorage
        storage.override_data(incorrect_identifier_data, "INCORRECT_IDENTIFIER")

        session_data = storage.get_data("form_data")

        assert {} == session_data

    def test_if_create_key_returns_none_then_return_none(self):
        with patch('app.data_access.storage.session_storage.SessionStorage.create_key_identifier_with_user_id', MagicMock(return_value=None)):
            session_data = SessionStorage.get_data("form_data")

        assert session_data is None


class TestOverrideSessionStorage:

    def test_data_is_saved_as_new_form_data(self):
        storage = SessionStorage
        form_data = storage.get_data('form_data')
        assert form_data == {}
        new_data = {'brother': 'Luigi'}
        storage.override_data(new_data)
        form_data = storage.get_data('form_data')
        assert form_data == new_data

    def test_data_is_saved_as_update_form_data(self):
        storage = SessionStorage
        new_data = {'brother': 'Luigi'}
        storage.override_data(new_data)
        update_data = {'mother': 'daisy'}
        storage.override_data(update_data)
        form_data = storage.get_data('form_data')
        assert form_data != new_data
        assert form_data == update_data

    def test_if_data_stored_with_other_identifier_then_it_is_not_changed(self):
        storage = SessionStorage
        new_data = {'brother': 'Luigi'}
        storage.override_data(new_data)
        with patch(CURRENT_USER, MagicMock(idnr_hashed="9876543210")):
            other_data = {'enemy': 'Bowser'}
            storage.override_data(other_data)
        with patch(CURRENT_USER, MagicMock(idnr_hashed="0123456789")):
            form_data = storage.get_data('form_data')
        assert new_data == form_data

    @pytest.mark.usefixtures('testing_current_user')
    def test_if_create_key_returns_none_then_do_not_overwrite_session_data(self):
        storage = SessionStorage
        with patch('app.data_access.storage.session_storage.SessionStorage.create_key_identifier_with_user_id', MagicMock(return_value=None)):
            other_data = {'enemy': 'Bowser'}
            storage.override_data(other_data, 'form_data')

        session_data = storage.get_data('form_data')

        assert session_data == {}


class TestSerializeSessionData:
    @pytest.fixture(autouse=True)
    def attach_fixtures(self, app, test_request_context):
        self.app = app
        self.req = test_request_context

    def test_deserialized_dict_should_equal_original(self):
        original_data = {"name": "Tom Riddle", "dob": datetime.date(1926, 12, 31)}
        serialized_data = SessionStorage.serialize_data(original_data)
        deserialized_data = SessionStorage.deserialize_data(serialized_data, self.app.config['PERMANENT_SESSION_LIFETIME'])
        assert original_data == deserialized_data

    def test_serialization_should_encrypt_and_compress(self):
        from zlib import compress
        from app.crypto.encryption import encrypt

        original_data = {"name": "Tom Riddle", "dob": datetime.date(1926, 12, 31)}

        with patch("app.data_access.storage.form_storage.encrypt", MagicMock(wraps=encrypt)) as encrypt_mock, \
                patch("app.data_access.storage.form_storage.zlib.compress", MagicMock(wraps=compress)) as compress_mock:
            SessionStorage.serialize_data(original_data)

            encrypt_mock.assert_called()
            compress_mock.assert_called()


class TestDeserializeSessionData:
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
            serialized_data = SessionStorage.serialize_data(original_data)

            mocked_time.return_value = passed_time
            deserialized_data = SessionStorage.deserialize_data(serialized_data, ttl)
            assert original_data == deserialized_data

    def test_if_ttl_greater_than_passed_time_then_return_empty_dict(self):
        original_data = {"name": "Tom Riddle", "dob": datetime.date(1926, 12, 31)}
        creation_time = time.time()
        passed_time = creation_time + 5
        ttl = 2

        with patch("time.time") as mocked_time:
            mocked_time.return_value = creation_time
            serialized_data = SessionStorage.serialize_data(original_data)

            mocked_time.return_value = passed_time
            deserialized_data = SessionStorage.deserialize_data(serialized_data, ttl)

            assert {} == deserialized_data

    def test_if_deserialize_raises_invalid_token_then_return_empty_dict(self):
        original_data = {"name": "Tom Riddle", "dob": datetime.date(1926, 12, 31)}
        serialized_data = SessionStorage.serialize_data(original_data)
        with patch("app.data_access.storage.form_storage.decrypt", MagicMock(side_effect=InvalidToken)):
            deserialized_data = SessionStorage.deserialize_data(serialized_data, self.app.config['PERMANENT_SESSION_LIFETIME'])
            assert {} == deserialized_data

    def test_if_session_data_empty_do_not_log_error(self):
        with patch("app.data_access.storage.form_storage.logger.warn") as log_fun:
            deserialized_data = SessionStorage.deserialize_data(b'', self.app.config['PERMANENT_SESSION_LIFETIME'])
            assert {} == deserialized_data
            log_fun.assert_not_called()


class TestCreateIdentifierWithKey:

    @pytest.mark.usefixtures("testing_current_user")
    def test_if_no_identifier_given_then_use_default_identifier(self):
        expected_identifier = CURRENT_USER_IDNR + "_default"
        
        created_identifier = SessionStorage.create_key_identifier_with_user_id(None)

        assert created_identifier == expected_identifier

    @pytest.mark.usefixtures("testing_current_user")
    def test_if_identifier_given_then_return_key_from_user_id_plus_identifier(self):
        identifier = "alohomora"
        expected_identifier = CURRENT_USER_IDNR + "_" + identifier

        created_identifier = SessionStorage.create_key_identifier_with_user_id(identifier)

        assert created_identifier == expected_identifier

    def test_if_current_user_has_no_idnr_hashed_then_return_none(self):
        mock_current_user_without_idnr_hashed = MagicMock()
        del mock_current_user_without_idnr_hashed.idnr_hashed

        with patch("app.data_access.storage.session_storage.current_user", mock_current_user_without_idnr_hashed):
            created_identifier = SessionStorage.create_key_identifier_with_user_id('alohomora')

        assert created_identifier is None
