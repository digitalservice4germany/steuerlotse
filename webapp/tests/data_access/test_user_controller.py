import unittest

from app.data_access.user_controller import *


class TestUserExists(unittest.TestCase):

    def setUp(self):
        db.create_all()
        self.existing_idnr = "123"
        create_user(self.existing_idnr, '1985-01-01', '789')

    def test_if_existing_idnr_then_return_true(self):
        response = user_exists(self.existing_idnr)
        self.assertTrue(response)

    def test_if_not_existing_idnr_then_return_true(self):
        response = user_exists('non_existent_user')
        self.assertFalse(response)

    def tearDown(self):
        db.drop_all()


class TestCreateUser(unittest.TestCase):

    def setUp(self):
        db.create_all()
        self.existing_idnr = "123"
        create_user(self.existing_idnr, '1985-01-01', '789')

    def test_if_idnr_exists_and_request_id_same_then_raise_error(self):
        self.assertRaises(UserAlreadyExistsError, create_user, self.existing_idnr, '1985-01-01', '789')

    def test_if_idnr_exists_and_request_id_different_then_raise_error(self):
        self.assertRaises(UserAlreadyExistsError, create_user, self.existing_idnr, '1985-01-01', '000')

    def test_if_idnr_exists_and_dob_same_then_raise_error(self):
        self.assertRaises(UserAlreadyExistsError, create_user, self.existing_idnr, '1985-01-01', '789')

    def test_if_idnr_exists_and_dob_different_then_raise_error(self):
        self.assertRaises(UserAlreadyExistsError, create_user, self.existing_idnr, '1999-01-01', '789')

    def test_if_new_idnr_then_save_user(self):
        new_idnr = '33602'
        create_user(new_idnr, '1985-01-01', '000')
        self.assertTrue(user_exists(new_idnr))

    def test_if_new_idnr_then_save_correct_attributes(self):
        new_idnr = '33604'
        dob = '1985-01-01'
        req_id = '000'

        create_user(new_idnr, dob, req_id)

        created_user = find_user(new_idnr)
        self.assertEqual(global_salt_hash().hash(new_idnr), created_user.idnr_hashed)
        self.assertTrue(indiv_salt_hash().verify(dob, created_user.dob_hashed))
        self.assertEqual(req_id, created_user.elster_request_id)
        self.assertFalse(created_user.is_active)

    def test_if_new_idnr_then_return_user_with_correct_attributes(self):
        new_idnr = '33605'
        dob = '1985-01-01'
        req_id = '000'

        created_user = create_user(new_idnr, dob, req_id)

        self.assertEqual(global_salt_hash().hash(new_idnr), created_user.idnr_hashed)
        self.assertTrue(indiv_salt_hash().verify(dob, created_user.dob_hashed))
        self.assertEqual(req_id, created_user.elster_request_id)
        self.assertFalse(created_user.is_active)

    def tearDown(self):
        db.drop_all()


class TestDeleteUser(unittest.TestCase):

    def setUp(self):
        db.create_all()
        create_user('Added_user', '1985-01-01', '123')

    def test_if_user_is_deleted_then_user_is_removed_from_storage(self):
        delete_user('Added_user')
        db.session.rollback()  # Verify changes have actually been written to the database.
        self.assertEqual(0, User.query.count())

    def tearDown(self):
        db.drop_all()


class TestActivateUser(unittest.TestCase):

    def setUp(self):
        db.create_all()
        self.user = create_user('1234', '1985-01-01', '5678')

    def test_activates_user_and_commits_changes(self):
        activate_user('1234', '5678')
        db.session.rollback()  # Verify changes have actually been written to the database.
        self.assertTrue(self.user.is_active)

    def test_activate_user_returns_an_activated_user(self):
        returned_user = activate_user('1234', '5678')
        self.assertTrue(returned_user.is_active)

    def tearDown(self):
        db.drop_all()


class TestStorePdfAndTransferTicket(unittest.TestCase):

    def setUp(self):
        db.create_all()

    def test_pdf_is_set_in_user(self):
        expected_pdf = b'thisisagreatPDFforya'
        user = User('123', '123', '123')
        store_pdf_and_transfer_ticket(user, expected_pdf, 'Passierschein A38')
        db.session.rollback()
        self.assertEqual(expected_pdf, user.pdf)

    def test_transfer_ticket_is_set_in_user(self):
        expected_transfer_ticket = 'Passierschein A38'
        user = User('123', '123', '123')
        store_pdf_and_transfer_ticket(user, b'pdf', expected_transfer_ticket)
        db.session.rollback()
        self.assertEqual(expected_transfer_ticket, user.transfer_ticket)

    def tearDown(self):
        db.drop_all()


class TestCheckIdnr(unittest.TestCase):
    def setUp(self):
        db.create_all()
        self.correct_idnr = '1234567890'
        self.existing_user = create_user(self.correct_idnr, '1985-01-01', '000')

    def test_if_idnr_correct_return_true(self):
        self.assertTrue(check_idnr(self.existing_user, self.correct_idnr))

    def test_if_idnr_incorrect_return_false(self):
        self.assertFalse(check_idnr(self.existing_user, 'INCORRECT'))

    def tearDown(self):
        db.drop_all()


class TestCheckDob(unittest.TestCase):
    def setUp(self):
        db.create_all()
        self.correct_dob = '1985-01-01'
        self.existing_user = create_user('1234', self.correct_dob, '000')

    def test_if_dob_correct_return_true(self):
        self.assertTrue(check_dob(self.existing_user, self.correct_dob))

    def test_if_dob_incorrect_return_false(self):
        self.assertFalse(check_dob(self.existing_user, 'INCORRECT'))

    def tearDown(self):
        db.drop_all()
