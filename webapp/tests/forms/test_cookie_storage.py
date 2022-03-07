import copy
import unittest
from unittest.mock import patch, MagicMock

import pytest
from flask.sessions import SecureCookieSession

from app.data_access.storage.cookie_storage import CookieStorage
from app.data_access.storage.form_storage import FormStorage
from tests.utils import create_session_form_data


@pytest.fixture
def cookie_data_identifier():
    return 'form_data'


@pytest.fixture
def prefilled_cookie_data():
    return {"name": "Peach", "sister": "Daisy", "husband": "Mario"}


class TestGetCookieStorage:

    def test_if_cookie_data_then_return_cookie_data(self, cookie_data_identifier, prefilled_cookie_data, test_request_context):
        test_request_context.session = SecureCookieSession({cookie_data_identifier: create_session_form_data(prefilled_cookie_data)})
        cookie_data = CookieStorage.get_data(cookie_data_identifier)

        assert prefilled_cookie_data == cookie_data

    def test_if_cookie_data_and_default_data_different_then_update_cookie_data(self, cookie_data_identifier, prefilled_cookie_data, test_request_context):
        default_data = {"brother": "Luigi"}
        expected_data = {**prefilled_cookie_data, **default_data}

        test_request_context.session = SecureCookieSession({cookie_data_identifier: create_session_form_data(prefilled_cookie_data)})

        cookie_data = CookieStorage.get_data(cookie_data_identifier, default_data=default_data)

        assert expected_data == cookie_data

    def test_if_cookie_data_in_incorrect_identifier_then_return_only_data_from_correct_identifier(self, cookie_data_identifier, test_request_context):
        form_data = {"brother": "Luigi"}
        incorrect_identifier_data = {"enemy": "Bowser"}
        expected_data = {**form_data}

        test_request_context.session = SecureCookieSession(
            {cookie_data_identifier: create_session_form_data(form_data),
                "INCORRECT_IDENTIFIER": create_session_form_data(incorrect_identifier_data)})

        cookie_data = CookieStorage.get_data(cookie_data_identifier)

        assert expected_data == cookie_data

    def test_if_only_data_in_incorrect_identifier_then_return_empty_data(self, cookie_data_identifier, test_request_context):
        incorrect_identifier = {"enemy": "Bowser"}

        test_request_context.session = SecureCookieSession({"INCORRECT_IDENTIFIER": create_session_form_data(incorrect_identifier)})

        cookie_data = CookieStorage.get_data(cookie_data_identifier)

        assert {} == cookie_data

    def test_if_no_form_data_in_cookie_then_return_default_data(self, cookie_data_identifier, test_request_context):
        default_data = {"brother": "Luigi"}
        test_request_context.session = SecureCookieSession({})
        cookie_data = CookieStorage.get_data(cookie_data_identifier, default_data=default_data)

        assert default_data == cookie_data

    @pytest.mark.usefixtures("test_request_context")
    def test_if_no_cookie_data_and_debug_data_provided_then_return_copy(self, cookie_data_identifier):
        original_default_data = {}
        cookie_data = CookieStorage.get_data(cookie_data_identifier, default_data=original_default_data)

        assert original_default_data is not cookie_data

    @pytest.mark.usefixtures("test_request_context")
    def test_if_no_cookie_data_and_no_debug_data_then_return_empty_dict(self, cookie_data_identifier):
        cookie_data = CookieStorage.get_data(cookie_data_identifier)

        assert {} == cookie_data

    def test_if_cookie_data_then_keep_data_in_cookie(self, cookie_data_identifier, prefilled_cookie_data, app, test_request_context):
        test_request_context.session = SecureCookieSession({'form_data': create_session_form_data(prefilled_cookie_data)})

        CookieStorage.get_data(cookie_data_identifier)

        assert 'form_data' in test_request_context.session
        assert prefilled_cookie_data == FormStorage.deserialize_data(test_request_context.session['form_data'], app.config['PERMANENT_SESSION_LIFETIME'])

    def test_if_some_cookie_data_then_do_not_change_with_debug_data(self, cookie_data_identifier, prefilled_cookie_data, app, test_request_context):
        cookie_data_without_all_keys = copy.deepcopy(prefilled_cookie_data)
        cookie_data_without_all_keys.pop(list(cookie_data_without_all_keys.keys())[0])

        test_request_context.session = SecureCookieSession({'form_data': create_session_form_data(cookie_data_without_all_keys)})

        found_data = CookieStorage.get_data(cookie_data_identifier, default_data={"brother": "Luigi", "husband": "Mario"})

        assert found_data == cookie_data_without_all_keys


class TestOverrideCookieStorage:

    def test_data_is_saved_to_empty_cookie(self, test_request_context):
        new_data = {'brother': 'Luigi'}
        with patch('app.data_access.storage.cookie_storage.CookieStorage.serialize_data', MagicMock(side_effect=lambda _: _)):
            assert 'form_data' not in test_request_context.session
            CookieStorage.override_data(new_data)
            assert 'form_data' in test_request_context.session
            assert new_data == test_request_context.session['form_data']

    def test_data_is_saved_to_prefilled_cookie(self, test_request_context):
        new_data = {'brother': 'Luigi'}
        with patch('app.data_access.storage.cookie_storage.CookieStorage.serialize_data', MagicMock(side_effect=lambda _: _)):
            test_request_context.session = {'form_data': {'brother': 'Mario', 'pet': 'Yoshi'}}
            assert 'form_data' in test_request_context.session
            CookieStorage.override_data(new_data)
            assert 'form_data' in test_request_context.session
            assert new_data == test_request_context.session['form_data']

    def test_if_data_stored_with_other_identifier_then_it_is_not_changed(self, test_request_context):
        new_data = {'brother': 'Luigi'}
        other_data = {'enemy': 'Bowser'}
        with patch('app.data_access.storage.cookie_storage.CookieStorage.serialize_data', MagicMock(side_effect=lambda _: _)):
            test_request_context.session = {'form_data': {'brother': 'Mario', 'pet': 'Yoshi'}, 'OTHER_IDENTIFIER': other_data}
            CookieStorage.override_data(new_data, 'form_data')
            assert other_data == test_request_context.session['OTHER_IDENTIFIER']

    def test_if_stored_data_identifier_is_set_then_override_storage_data_in_cookie_with_that_new_identifier(self, test_request_context):
        new_data = {'brother': 'Luigi'}
        other_data = {'enemy': 'Bowser'}
        new_identifier = "NEW_IDENTIFIER"
        with patch('app.data_access.storage.cookie_storage.CookieStorage.serialize_data', MagicMock(side_effect=lambda _: _)):
            test_request_context.session = {'form_data': {'brother': 'Mario', 'pet': 'Yoshi'}, 'OTHER_IDENTIFIER': other_data}
            CookieStorage.override_data(new_data, new_identifier)
            assert new_data == test_request_context.session[new_identifier]
