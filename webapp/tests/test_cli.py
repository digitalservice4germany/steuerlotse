import datetime as dt
import unittest
from unittest.mock import patch

from app import db
from app.commands import _delete_outdated_not_activated_users, _delete_outdated_users_with_completed_process, \
    _delete_inactive_users, _delete_outdated_users
from app.data_access.user_controller import create_user, user_exists, store_pdf_and_transfer_ticket


class TestDeleteOutdatedNotActivatedUsers(unittest.TestCase):
    def setUp(self):
        db.create_all()

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

    def tearDown(self):
        db.drop_all()


class TestDeleteOutdatedUsersWithCompletedProcess(unittest.TestCase):
    def setUp(self):
        db.create_all()

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

    def tearDown(self):
        db.drop_all()


class TestDeleteInactiveUsers(unittest.TestCase):
    def setUp(self):
        db.create_all()

        self.non_outdated_idnr = "04452397687"
        self.non_outdated_user = create_user(self.non_outdated_idnr, '1985-01-01', '123')
        self.outdated_idnr = "02293417683"
        self.outdated_user = create_user(self.outdated_idnr, '1985-01-01', '123')

    def test_if_user_older_than_60_days_then_delete_user(self):
        self.outdated_user.last_modified = dt.datetime.now(dt.timezone.utc) - dt.timedelta(days=101)

        with patch('app.elster_client.elster_client.send_unlock_code_revocation_with_elster') as revoke_fun:
            _delete_inactive_users()

        self.assertFalse(user_exists(self.outdated_idnr))
        self.assertTrue(user_exists(self.non_outdated_idnr))
        revoke_fun.assert_called_once()

    def test_if_user_newer_than_60_days_then_do_not_delete_user(self):
        self.non_outdated_user.last_modified = dt.datetime.now(dt.timezone.utc) - dt.timedelta(days=59)
        _delete_inactive_users()
        self.assertTrue(user_exists(self.non_outdated_idnr))
        self.assertTrue(user_exists(self.outdated_idnr))

    def tearDown(self):
        db.drop_all()


class TestDeleteOutdatedUsers(unittest.TestCase):
    def setUp(self):
        db.create_all()

        self.inactive_non_activated_idnr = "04452397680"
        self.inactive_non_activated_user = create_user(self.inactive_non_activated_idnr, '1985-01-01', '123')
        self.inactive_non_activated_user.last_modified = dt.datetime.now(dt.timezone.utc) - dt.timedelta(days=101)

    def test_if_user_matches_two_rules_then_delete_user_without_errors(self):
        with patch('app.elster_client.elster_client.send_unlock_code_revocation_with_elster'):
            _delete_outdated_users()

        self.assertFalse(user_exists(self.inactive_non_activated_idnr))

    def test_commit_is_called(self):
        with patch('app.elster_client.elster_client.send_unlock_code_revocation_with_elster'),\
             patch('app.db.session.commit') as commit_fun:
            _delete_outdated_users()
        commit_fun.assert_called()

    def tearDown(self):
        db.drop_all()
