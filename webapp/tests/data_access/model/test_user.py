import unittest

from app import db
from app.crypto.pw_hashing import global_salt_hash, indiv_salt_hash
from app.data_access.db_model.user import User


class TestUserInit(unittest.TestCase):

    def test_if_idnr_given_then_set_idnr_hashed(self):
        idnr = '123456'
        user = User(idnr, '1985-01-01', '123')
        self.assertTrue(global_salt_hash().verify(idnr, user.idnr_hashed))

    def test_if_dob_given_then_set_dob_hashed(self):
        dob = '1985-01-01'
        user = User('123', dob, '123')
        self.assertTrue(indiv_salt_hash().verify(dob, user.dob_hashed))

    def test_if_req_id_given_then_set_req_id(self):
        req_id = '42123'
        user = User('123', '1985-01-01', req_id)
        self.assertEqual(req_id, user.elster_request_id)

    def test_if_user_generated_then_user_inactive(self):
        user = User('123', '1985-01-01', '123')
        self.assertFalse(user.is_active)

    def test_if_user_generated_then_pdf_is_none(self):
        user = User('123', '123', '123')
        self.assertIsNone(user.pdf)


class TestUserLastModified(unittest.TestCase):
    def setUp(self):
        db.create_all()

    def test_if_user_created_then_last_modified_is_set_to_current_time(self):
        import datetime

        user = User('1337', '123', '123')
        db.session.add(user)
        db.session.commit()

        self.assertGreater(user.last_modified, datetime.datetime.utcnow() - datetime.timedelta(seconds=1))
        self.assertLess(user.last_modified, datetime.datetime.utcnow())

    def test_activate_user_updates_last_modified(self):
        user = User('1337', '123', '123')
        db.session.add(user)
        db.session.commit()
        old_last_modified = user.last_modified

        user.activate('5678')
        db.session.commit()  # Verify changes have actually been written to the database.

        self.assertNotEqual(old_last_modified, user.last_modified)

    def test_updates_last_modified(self):
        user = User('1337', '123', '123')
        db.session.add(user)
        db.session.commit()
        old_last_modified = user.last_modified

        user.pdf = b'pdf'
        db.session.commit()  # Verify changes have actually been written to the database.

        self.assertNotEqual(old_last_modified, user.last_modified)

    def tearDown(self):
        db.drop_all()


class TestUserActivate(unittest.TestCase):

    def test_if_user_activated_then_is_active_true(self):
        inactive_user = User('Inactive_User', '1985-01-01', '123')
        inactive_user.activate("123")
        self.assertTrue(inactive_user.is_active)

    def test_if_activated_then_unlock_code_set_correctly(self):
        unlock_code = "123"
        inactive_user = User('Inactive_User', '1985-01-01', '123')
        inactive_user.activate(unlock_code)

        self.assertTrue(indiv_salt_hash().verify(unlock_code, inactive_user.unlock_code_hashed))


class TestHasCompletedTaxReturn(unittest.TestCase):
    def test_if_pdf_set_return_true(self):
        user = User('123456', '1985-01-01', '123')
        user.pdf = b'thisisapdf'
        has_completed_process = user.has_completed_tax_return()
        self.assertTrue(has_completed_process)

    def test_if_no_pdf_set_return_false(self):
        user = User('123456', '1985-01-01', '123')
        has_completed_process = user.has_completed_tax_return()
        self.assertFalse(has_completed_process)
