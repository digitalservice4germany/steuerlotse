import datetime as dt
import unittest
from unittest.mock import patch

import pytest
from freezegun import freeze_time

from app.commands import _delete_outdated_not_activated_users, _delete_outdated_users_with_completed_process, \
    _delete_inactive_users, _delete_outdated_users
from app.data_access.user_controller import create_user, user_exists, store_pdf_and_transfer_ticket, activate_user
from app.extensions import db


class TestDeleteOutdatedNotActivatedUsers(unittest.TestCase):
    @pytest.fixture(autouse=True)
    def attach_fixtures(self, transactional_session):
        self.session = transactional_session

    def setUp(self):
        self.non_outdated_idnr = "04452397687"
        self.non_outdated_user = create_user(self.non_outdated_idnr, '1985-01-01', '123')
        self.outdated_idnr = "02293417683"
        self.outdated_user = create_user(self.outdated_idnr, '1985-01-01', '123')

    def test_if_user_not_activated_and_older_than_90_days_then_delete_user(self):
        self.outdated_user.last_modified = dt.datetime.now(dt.timezone.utc) - dt.timedelta(days=91)
        _delete_outdated_not_activated_users()
        self.assertFalse(user_exists(self.outdated_idnr))
        self.assertTrue(user_exists(self.non_outdated_idnr))

    def test_if_user_activated_and_older_than_90_days_then_do_not_delete_user(self):
        self.non_outdated_user.activate('1234')
        self.non_outdated_user.last_modified = dt.datetime.now(dt.timezone.utc) - dt.timedelta(days=89)

        _delete_outdated_not_activated_users()

        self.assertTrue(user_exists(self.non_outdated_idnr))
        self.assertTrue(user_exists(self.outdated_idnr))

    def test_if_user_not_activated_and_newer_than_90_days_then_do_not_delete_user(self):
        self.non_outdated_user.last_modified = dt.datetime.now(dt.timezone.utc) - dt.timedelta(days=89)
        _delete_outdated_not_activated_users()
        self.assertTrue(user_exists(self.non_outdated_idnr))
        self.assertTrue(user_exists(self.outdated_idnr))

    def test_if_user_activated_and_newer_than_90_days_then_do_not_delete_user(self):
        self.non_outdated_user.activate('1234')
        self.non_outdated_user.last_modified = dt.datetime.now(dt.timezone.utc) - dt.timedelta(days=89)

        _delete_outdated_not_activated_users()

        self.assertTrue(user_exists(self.non_outdated_idnr))
        self.assertTrue(user_exists(self.outdated_idnr))


class TestDeleteOutdatedUsersWithCompletedProcess(unittest.TestCase):
    @pytest.fixture(autouse=True)
    def attach_fixtures(self, transactional_session):
        self.session = transactional_session

    def setUp(self):
        self.outdated_idnr = "02293417683"
        self.outdated_user = create_user(self.outdated_idnr, '1985-01-01', '123')
        self.non_outdated_idnr = "04452397687"
        self.non_outdated_user = create_user(self.non_outdated_idnr, '1985-01-01', '123')

    def test_if_user_process_completed_and_older_than_10_minutes_then_delete_user(self):
        self.outdated_user.pdf = b'thisisapdf'
        self.outdated_user.last_modified = dt.datetime.now(dt.timezone.utc) - dt.timedelta(minutes=11)

        with patch('app.elster_client.elster_client.send_unlock_code_revocation_with_elster') as revoke_fun:
            _delete_outdated_users_with_completed_process()

        self.assertFalse(user_exists(self.outdated_idnr))
        self.assertTrue(user_exists(self.non_outdated_idnr))
        revoke_fun.assert_called_once()

    def test_if_user_process_not_completed_and_older_than_10_minutes_then_do_not_delete_user(self):
        self.non_outdated_user.last_modified = dt.datetime.now(dt.timezone.utc) - dt.timedelta(minutes=11)
        _delete_outdated_users_with_completed_process()
        self.assertTrue(user_exists(self.non_outdated_idnr))
        self.assertTrue(user_exists(self.outdated_idnr))

    def test_if_user_process_completed_and_newer_than_10_minutes_then_do_not_delete_user(self):
        store_pdf_and_transfer_ticket(self.non_outdated_user, b'thisisapdf', 'transfer_ticket')
        self.non_outdated_user.last_modified = dt.datetime.now(dt.timezone.utc) - dt.timedelta(minutes=9)

        _delete_outdated_users_with_completed_process()

        self.assertTrue(user_exists(self.non_outdated_idnr))
        self.assertTrue(user_exists(self.outdated_idnr))

    def test_if_user_process_not_completed_and_newer_than_10_minutes_then_do_not_delete_user(self):
        self.non_outdated_user.last_modified = dt.datetime.now(dt.timezone.utc) - dt.timedelta(minutes=9)
        _delete_outdated_users_with_completed_process()
        self.assertTrue(user_exists(self.non_outdated_idnr))
        self.assertTrue(user_exists(self.outdated_idnr))


class TestDeleteInactiveUsers(unittest.TestCase):
    @pytest.fixture(autouse=True)
    def attach_fixtures(self, transactional_session):
        self.session = transactional_session

    def setUp(self):

        # 30 days before 2021-08-10
        with freeze_time("2021-07-11"):
            self.non_outdated_idnr = "04452397687"
            self.non_outdated_user = create_user(self.non_outdated_idnr, '1985-01-01', '123')
            self.non_outdated_user.last_modified = dt.datetime.now(dt.timezone.utc)
            self.non_outdated_activated_idnr = "06642573191"
            self.non_outdated_activated_user = create_user(self.non_outdated_activated_idnr, '1985-01-01', '123')
            self.non_outdated_activated_user.last_modified = dt.datetime.now(dt.timezone.utc)

        # 61 days before 2021-08-10
        with freeze_time("2021-06-10"):
            self.outdated_not_activated_idnr = "02293417683"
            self.outdated_not_activated_user = create_user(self.outdated_not_activated_idnr, '1985-01-01', '123')
            self.outdated_not_activated_user.last_modified = dt.datetime.now(dt.timezone.utc)
            self.outdated_activated_idnr = "02259417680"
            self.outdated_activated_user = create_user(self.outdated_activated_idnr, '1985-01-01', '123')
            activate_user(self.outdated_activated_idnr, "UNLO-CKCO-DE07")
            self.outdated_activated_user.last_modified = dt.datetime.now(dt.timezone.utc)

    @freeze_time("2021-08-11")
    def test_if_activated_user_older_than_60_days_then_delete_user(self):
        with patch('app.elster_client.elster_client.send_unlock_code_revocation_with_elster') as revoke_fun:
            _delete_inactive_users()

        self.assertFalse(user_exists(self.outdated_activated_idnr))
        revoke_fun.assert_called_once()

    @freeze_time("2021-08-10")
    def test_if_not_activated_user_older_than_60_days_then_do_not_delete_user(self):
        _delete_inactive_users()
        self.assertTrue(user_exists(self.outdated_not_activated_idnr))
        self.assertTrue(user_exists(self.non_outdated_idnr))

    @freeze_time("2021-08-10")
    def test_if_user_newer_than_60_days_then_do_not_delete_user(self):
        _delete_inactive_users()
        self.assertTrue(user_exists(self.non_outdated_idnr))
        self.assertTrue(user_exists(self.non_outdated_activated_idnr))
        self.assertTrue(user_exists(self.outdated_not_activated_idnr))


class TestDeleteOutdatedUsers(unittest.TestCase):
    @pytest.fixture(autouse=True)
    def attach_fixtures(self, transactional_session):
        self.session = transactional_session

    def setUp(self):
        self.inactive_non_activated_idnr = "04452397680"
        self.inactive_non_activated_user = create_user(self.inactive_non_activated_idnr, '1985-01-01', '123')
        self.inactive_non_activated_user.last_modified = dt.datetime.now(dt.timezone.utc) - dt.timedelta(days=101)

    def test_if_user_matches_two_rules_then_delete_user_without_errors(self):
        with patch('app.elster_client.elster_client.send_unlock_code_revocation_with_elster'):
            _delete_outdated_users()

        self.assertFalse(user_exists(self.inactive_non_activated_idnr))

    def test_commit_is_called(self):
        with patch('app.elster_client.elster_client.send_unlock_code_revocation_with_elster'),\
             patch('app.extensions.db.session.commit') as commit_fun:
            _delete_outdated_users()
        commit_fun.assert_called()
