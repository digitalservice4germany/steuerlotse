import json
import unittest
from json import JSONDecodeError
from unittest.mock import patch, MagicMock

import pytest

from app.data_access.audit_log_controller import create_audit_log_entry, create_audit_log_confirmation_entry, \
    create_audit_log_address_entry
from tests.elster_client.mock_erica import MockResponse


class TestCreateAuditLogEntry(unittest.TestCase):
    @pytest.fixture(autouse=True)
    def attach_fixtures(self, transactional_session):
        self.session = transactional_session

    def setUp(self):
        self.event_name = 'great get-together'
        self.ip_address = '127.0.0.1'
        self.idnr = '04452397687'
        self.transfer_ticket = 'some cryptic transfer ticket stuff'
        self.elster_request_id = 'some cryptic request id stuff'
        self.pyeric_response_with_request_id = MockResponse({'transfer_ticket': self.transfer_ticket,
                                                             'elster_request_id': self.elster_request_id}, 200)
        self.pyeric_response_without_request_id = MockResponse({'transfer_ticket': self.transfer_ticket}, 200)

    def test_calls_session_commit(self):
        with (
            patch('app.data_access.audit_log_controller.hybrid_encrypt', MagicMock(side_effect=lambda _: _)),
            patch('app.data_access.audit_log_controller.db.session.commit') as session_commit_fun
        ):
            create_audit_log_entry(self.event_name, self.ip_address, self.idnr,
                                   self.pyeric_response_with_request_id.json())
            session_commit_fun.assert_called()

    def test_log_data_is_json(self):
        with patch('app.data_access.audit_log_controller.hybrid_encrypt', MagicMock(side_effect=lambda _: _)):
            new_entry = create_audit_log_entry(self.event_name, self.ip_address, self.idnr,
                                               self.pyeric_response_with_request_id.json())
        try:
            json.loads(new_entry)
        except JSONDecodeError:
            self.fail('log_data does not seem to be a valid json.')

    def test_log_data_includes_correct_data(self):
        with patch('app.data_access.audit_log_controller.hybrid_encrypt', MagicMock(side_effect=lambda _: _)):
            new_entry = create_audit_log_entry(self.event_name, self.ip_address, self.idnr,
                                               self.pyeric_response_with_request_id.json()['transfer_ticket'],
                                               self.pyeric_response_with_request_id.json()['elster_request_id'])
        json_data = json.loads(new_entry)
        self.assertEqual(self.event_name, json_data['event_name'])
        self.assertTrue(json_data['timestamp'])
        self.assertEqual(self.ip_address, json_data['ip_address'])
        self.assertEqual(self.idnr, json_data['idnr'])
        self.assertEqual(self.transfer_ticket, json_data['transfer_ticket'])
        self.assertEqual(self.elster_request_id, json_data['elster_request_id'])

    def test_if_elster_request_id_not_set_set_to_empty_string(self):
        with patch('app.data_access.audit_log_controller.hybrid_encrypt', MagicMock(side_effect=lambda _: _)):
            new_entry = create_audit_log_entry(self.event_name, self.ip_address, self.idnr,
                                               self.pyeric_response_without_request_id.json())
        json_data = json.loads(new_entry)
        self.assertEqual('', json_data['elster_request_id'])

    def test_calls_hybrid_encryption_method(self):
        with patch('app.data_access.audit_log_controller.hybrid_encrypt', MagicMock(side_effect=lambda _: _)) as hybrid_encryption_fun:
            create_audit_log_entry(self.event_name, self.ip_address, self.idnr, self.pyeric_response_without_request_id.json())
            hybrid_encryption_fun.assert_called_once()


class TestCreateAuditLogConfirmationEntry(unittest.TestCase):
    @pytest.fixture(autouse=True)
    def attach_fixtures(self, transactional_session):
        self.session = transactional_session

    def setUp(self):
        self.event_name = 'great get-together'
        self.ip_address = '127.0.0.1'
        self.idnr = '04452397687'
        self.confirmation_field = 'confirmation_field'
        self.confirmation_value = True

    def test_calls_session_commit(self):
        with (
            patch('app.data_access.audit_log_controller.hybrid_encrypt', MagicMock(side_effect=lambda _: _)),
            patch('app.data_access.audit_log_controller.db.session.commit') as session_commit_fun
        ):
            create_audit_log_confirmation_entry(self.event_name, self.ip_address, self.idnr,
                                                self.confirmation_field, self.confirmation_value)
            session_commit_fun.assert_called()

    def test_log_data_is_json(self):
        with patch('app.data_access.audit_log_controller.hybrid_encrypt', MagicMock(side_effect=lambda _: _)):
            new_entry = create_audit_log_confirmation_entry(self.event_name, self.ip_address, self.idnr,
                                                            self.confirmation_field, self.confirmation_value)
        try:
            json.loads(new_entry)
        except JSONDecodeError:
            self.fail('log_data does not seem to be a valid json.')

    def test_log_data_includes_correct_data(self):
        with patch('app.data_access.audit_log_controller.hybrid_encrypt', MagicMock(side_effect=lambda _: _)):
            new_entry = create_audit_log_confirmation_entry(self.event_name, self.ip_address, self.idnr,
                                                            self.confirmation_field, self.confirmation_value)
        json_data = json.loads(new_entry)
        self.assertEqual(self.event_name, json_data['event_name'])
        self.assertTrue(json_data['timestamp'])
        self.assertEqual(self.ip_address, json_data['ip_address'])
        self.assertEqual(self.idnr, json_data['idnr'])
        self.assertEqual(self.confirmation_field, json_data['confirmation_label'])
        self.assertEqual(self.confirmation_value, json_data['confirmation_value'])

    def test_calls_hybrid_encryption_method(self):
        with patch('app.data_access.audit_log_controller.hybrid_encrypt', MagicMock(side_effect=lambda _: _)) as hybrid_encryption_fun:
            create_audit_log_confirmation_entry(self.event_name, self.ip_address, self.idnr,
                                                self.confirmation_field, self.confirmation_value)
            hybrid_encryption_fun.assert_called_once()


class TestCreateAuditLogAddressEntry(unittest.TestCase):
    @pytest.fixture(autouse=True)
    def attach_fixtures(self, transactional_session):
        self.session = transactional_session

    def setUp(self):
        self.event_name = 'great get-together'
        self.ip_address = '127.0.0.1'
        self.idnr = '04452397687'
        self.address = 'address'

    def test_calls_session_commit(self):
        with (
            patch('app.data_access.audit_log_controller.hybrid_encrypt', MagicMock(side_effect=lambda _: _)),
            patch('app.data_access.audit_log_controller.db.session.commit') as session_commit_fun
        ):
            create_audit_log_address_entry(self.event_name, self.ip_address, self.idnr, self.address)
            session_commit_fun.assert_called()

    def test_log_data_is_json(self):
        with patch('app.data_access.audit_log_controller.hybrid_encrypt', MagicMock(side_effect=lambda _: _)):
            new_entry = create_audit_log_address_entry(self.event_name, self.ip_address, self.idnr, self.address)
        try:
            json.loads(new_entry)
        except JSONDecodeError:
            self.fail('log_data does not seem to be a valid json.')

    def test_log_data_includes_correct_data(self):
        with patch('app.data_access.audit_log_controller.hybrid_encrypt', MagicMock(side_effect=lambda _: _)):
            new_entry = create_audit_log_address_entry(self.event_name, self.ip_address, self.idnr, self.address)
        json_data = json.loads(new_entry)
        self.assertEqual(self.event_name, json_data['event_name'])
        self.assertTrue(json_data['timestamp'])
        self.assertEqual(self.ip_address, json_data['ip_address'])
        self.assertEqual(self.idnr, json_data['idnr'])
        self.assertEqual(self.address, json_data['address'])

    def test_calls_hybrid_encryption_method(self):
        with patch('app.data_access.audit_log_controller.hybrid_encrypt', MagicMock(side_effect=lambda _: _)) as hybrid_encryption_fun:
            create_audit_log_address_entry(self.event_name, self.ip_address, self.idnr, self.address)
            hybrid_encryption_fun.assert_called_once()
