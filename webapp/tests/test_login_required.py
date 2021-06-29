import unittest
from unittest.mock import MagicMock, patch

from app import app, db
from app.data_access.user_controller import create_user
from app.elster_client.elster_errors import ElsterRequestIdUnkownError


class IntegrationTest(unittest.TestCase):
    def setUp(self):
        # Cf. https://flask.palletsprojects.com/en/1.1.x/config/#PROPAGATE_EXCEPTIONS
        self._propagate_exceptions_original = app.config['PROPAGATE_EXCEPTIONS']
        app.config['PROPAGATE_EXCEPTIONS'] = False

    def tearDown(self):
        app.config['PROPAGATE_EXCEPTIONS'] = self._propagate_exceptions_original


class TestLotseStepLoginRequired(IntegrationTest):
    def setUp(self):
        super().setUp()
        db.create_all()

    def test_if_user_does_not_exist_then_returns_redirect(self):
        with app.test_client() as client:
            res = client.get('/lotse/step/summary')
            self.assertEqual(302, res.status_code)
            self.assertIn("unlock_code_activation", res.headers[2][1])

    def test_if_user_does_exist_not_logged_in_then_returns_redirect(self):
        create_user('1234', '1985-01-01', '0000')
        with app.test_client() as client:
            res = client.get('/lotse/step/summary')
            self.assertEqual(302, res.status_code)
            self.assertIn("unlock_code_activation", res.headers[2][1])

    def test_if_user_active_not_logged_in_then_returns_redirect(self):
        user = create_user('1234', '1985-01-01', '0000')
        user.activate('789')
        with app.test_client() as client:
            res = client.get('/lotse/step/summary')
            self.assertEqual(302, res.status_code)
            self.assertIn("unlock_code_activation", res.headers[2][1])

    def test_if_logged_in_cookie_sent_then_returns_200(self):
        user = create_user('04452397687', '1985-01-01', '0000')
        user.activate('0000')
        with app.test_client() as client:
            res = client.post('/unlock_code_activation/step/data_input', data=dict(
                idnr='04452397687',
                unlock_code='0000')
                              )
            cookie = res.headers[4][1]
            res = client.post('/lotse/step/summary', data=dict(
                idnr='04452397687',
                unlock_code='0000'), headers={'Cookie': cookie}
                              )
            self.assertEqual(200, res.status_code)

    def tearDown(self):
        super().tearDown()
        db.drop_all()


class TestDownloadStepLoginRequired(IntegrationTest):
    def setUp(self):
        super().setUp()
        db.create_all()

    def test_if_user_does_not_exist_then_returns_redirect(self):
        with app.test_client() as client:
            res = client.get('/download_pdf/print.pdf')
            self.assertEqual(302, res.status_code)
            self.assertIn("unlock_code_activation", res.headers[2][1])

    def test_if_user_does_exist_not_logged_in_then_returns_redirect(self):
        create_user('1234', '1985-01-01', '0000')
        with app.test_client() as client:
            res = client.get('/download_pdf/print.pdf')
            self.assertEqual(302, res.status_code)
            self.assertIn("unlock_code_activation", res.headers[2][1])

    def test_if_user_active_not_logged_in_then_returns_redirect(self):
        user = create_user('1234', '1985-01-01', '0000')
        user.activate('789')
        with app.test_client() as client:
            res = client.get('/download_pdf/print.pdf')
            self.assertEqual(302, res.status_code)
            self.assertIn("unlock_code_activation", res.headers[2][1])

    def test_if_logged_in_cookie_sent_then_returns_404(self):
        user = create_user('04452397687', '1985-01-01', '0000')
        user.activate('0000')

        with app.test_client() as client:
            res = client.post('/unlock_code_activation/step/data_input', data=dict(
                idnr='04452397687',
                unlock_code='0000')
                              )
            cookie = res.headers[4][1]
            res = client.get('/download_pdf/print.pdf', data=dict(
                idnr='04452397687',
                unlock_code='0000'), headers={'Cookie': cookie}
                             )
            self.assertEqual(404, res.status_code)  # No pdf created

    def tearDown(self):
        super().tearDown()
        db.drop_all()


class TestUnlockCodeActivationStepLogin(IntegrationTest):
    def setUp(self):
        super().setUp()
        db.create_all()

    def test_if_user_does_not_exist_then_returns_unlock_code_failure(self):
        with app.test_client() as client:
            res = client.post('/unlock_code_activation/step/data_input', data=dict(
                idnr='03352419681',
                unlock_code='0000')
                              )
            self.assertEqual(302, res.status_code)
            self.assertIn("unlock_code_failure", res.headers[2][1])

    def test_if_user_does_exist_but_no_antrag_then_returns_unlock_code_failure(self):
        create_user('03352419681', '1985-01-01', '0000')
        with app.test_client() as client:
            with patch('app.elster_client.elster_client.send_unlock_code_activation_with_elster') as elster_fun:
                elster_fun.side_effect = ElsterRequestIdUnkownError()
                res = client.post('/unlock_code_activation/step/data_input', data=dict(
                    idnr='03352419681',
                    unlock_code='0000')
                                  )
            self.assertEqual(302, res.status_code)
            self.assertIn("unlock_code_failure", res.headers[2][1])

    def test_if_inactive_user_then_returns_unlock_code_failure(self):
        create_user('04452397687', '1985-01-01', '0000')
        with app.test_client() as client:
            res = client.post('/unlock_code_activation/step/data_input', data=dict(
                idnr='04452397687',
                unlock_code='0000')
                              )
            self.assertEqual(302, res.status_code)
            self.assertIn("unlock_code_failure", res.headers[2][1])

    def test_if_non_activated_user_with_successful_elster_request_then_returns_unlock_code_success_with_redirect_to_lotse_start(self):
        create_user('03352419681', '1985-01-01', '0000')
        with app.test_client() as client:
            with patch('app.elster_client.elster_client.send_unlock_code_activation_with_elster',
                       MagicMock(return_value={"elster_request_id": 'ABCDE',
                                               "idnr": '04452397687'})):
                res = client.post('/unlock_code_activation/step/data_input', data=dict(
                    idnr='03352419681',
                    unlock_code='0000')
                                  )
            self.assertEqual(302, res.status_code)
            self.assertIn("lotse/step/start", res.headers[2][1])

    def test_if_existent_activated_user_then_returns_unlock_code_success_with_redirect_to_lotse_start(self):
        user = create_user('03352419681', '1985-01-01',  '0000')
        user.activate('0000')
        with app.test_client() as client:
            res = client.post('/unlock_code_activation/step/data_input', data=dict(
                idnr='03352419681',
                unlock_code='0000')
                              )
            self.assertEqual(302, res.status_code)
            self.assertIn("lotse/step/start", res.headers[2][1])

    def tearDown(self):
        super().tearDown()
        db.drop_all()
