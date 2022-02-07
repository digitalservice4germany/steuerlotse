import os
import unittest
from unittest.mock import patch, call

import pytest
from flask import json, make_response
from flask.sessions import SecureCookieSession
from werkzeug.exceptions import NotFound
from werkzeug.utils import redirect

from app.data_access.user_controller import create_user, find_user
from app.data_access.user_controller_errors import UserNotExistingError
from app.elster_client.elster_errors import ElsterProcessNotSuccessful, ElsterRequestIdUnkownError, \
    ElsterRequestAlreadyRevoked
from app.forms.flows.multistep_flow import RenderInfo
from app.forms.flows.unlock_code_revocation_flow import UnlockCodeRevocationMultiStepFlow
from app.forms.steps.unlock_code_revocation_steps import UnlockCodeRevocationFailureStep, \
    UnlockCodeRevocationSuccessStep, UnlockCodeRevocationInputStep
from tests.forms.mock_steps import MockStartStep, MockMiddleStep, MockFinalStep, MockRenderStep, MockFormStep, \
    MockUnlockCodeRevocationFailureStep, MockUnlockCodeRevocationSuccessStep, MockUnlockCodeRevocationInputStep

FIXTURES_PATH = os.path.dirname(os.path.abspath(__file__)) + '/../../samples/'


class UnlockCodeRevocationInit(unittest.TestCase):
    @pytest.fixture(autouse=True)
    def attach_fixtures(self, test_request_context):
        self.req = test_request_context

    def setUp(self):
        self.testing_steps = [MockStartStep, MockMiddleStep, MockFinalStep]
        self.endpoint_correct = "unlock_code_revocation"
        self.incorrect_session = "r2D2"
        self.set_link_overview = "True"
        self.expected_steps = [
            UnlockCodeRevocationInputStep,
            UnlockCodeRevocationFailureStep,
            UnlockCodeRevocationSuccessStep
        ]

    def test_if_request_has_params_then_set_attributes_correctly(self):
        # Only current link_overview is set from request
        correct_session = "C3PO"
        self.req.request.args = {'link_overview': self.set_link_overview}

        flow = UnlockCodeRevocationMultiStepFlow(endpoint=self.endpoint_correct)

        self.assertTrue(flow.has_link_overview)
        self.assertEqual(self.expected_steps, list(flow.steps.values()))
        self.assertEqual(self.expected_steps[0], flow.first_step)
        self.assertIsNone(flow.overview_step)

    def test_if_request_has_no_params_then_set_correct_defaults(self):
        flow = UnlockCodeRevocationMultiStepFlow(endpoint=self.endpoint_correct)

        self.assertFalse(flow.has_link_overview)
        self.assertEqual(self.expected_steps[0], flow.first_step)
        self.assertIsNone(flow.overview_step)


class TestUnlockCodeRevocationHandle(unittest.TestCase):
    @pytest.fixture(autouse=True)
    def attach_fixtures(self, app, test_request_context):
        self.app = app
        self.req = test_request_context

    def setUp(self):
        testing_steps = [MockStartStep, MockRenderStep, MockFormStep, MockFinalStep]
        testing_steps = {s.name: s for s in testing_steps}
        self.endpoint_correct = "unlock_code_revocation"
        self.flow = UnlockCodeRevocationMultiStepFlow(endpoint=self.endpoint_correct)
        self.flow.steps = testing_steps
        self.flow.first_step = next(iter(testing_steps.values()))
        self.stored_data = self.flow.default_data()

        # Set sessions up
        self.session_data = {'idnr': '04452397687', 'dob': '1985-01-01'}

    def test_if_correct_step_name_then_return_code_correct(self):
        response = self.flow.handle(MockRenderStep.name)

        self.assertEqual(200, response.status_code)

    def test_if_incorrect_step_name_then_raise_404_exception(self):
        self.assertRaises(NotFound, self.flow.handle, "Incorrect Step Name")

    def test_if_start_step_then_return_redirect_to_first_step(self):
        debug = self.flow.default_data
        self.flow.default_data = lambda: None
        response = self.flow.handle("start")

        self.assertEqual(
            redirect(
                "/" + self.endpoint_correct + "/step/" + MockStartStep.name
                + "?link_overview=" + str(self.flow.has_link_overview)).location,
            response.location
        )

        self.flow.default_data = debug

    def test_if_form_step_correct_and_post_then_return_redirect_to_next_step(self):
        with self.app.test_request_context(
                path="/" + self.endpoint_correct + "/step/" + MockFormStep.name,
                method='POST'):
            response = self.flow.handle(MockFormStep.name)

            self.assertEqual(
                redirect(
                    "/" + self.endpoint_correct + "/step/" + MockFinalStep.name
                    + "?link_overview=" + str(self.flow.has_link_overview)).location,
                response.location
            )

    def test_if_form_step_and_not_post_then_return_render(self):
        expected_data = {'The': '100'}
        render_return_value = make_response(json.dumps([expected_data], default=str), 200)
        with self.app.test_request_context(
                path="/" + self.endpoint_correct + "/step/" + MockRenderStep.name,
                method='GET'), \
                patch('tests.forms.mock_steps.MockRenderStep.render', return_value=render_return_value):
            response = self.flow.handle(MockRenderStep.name)

            self.assertEqual(200, response.status_code)
            # Check response data because that's what our Mock returns. Decode because response stored as bytestring
            self.assertEqual(expected_data, json.loads(str(response.get_data(), 'utf-8'))[0])


class TestUnlockCodeRevocationHandleSpecificsForStep(unittest.TestCase):
    @pytest.fixture(autouse=True)
    def attach_fixtures(self, transactional_session, app, test_request_context):
        self.session = transactional_session
        self.app = app
        self.req = test_request_context

    def setUp(self):
        testing_steps = [MockStartStep, MockUnlockCodeRevocationInputStep, MockUnlockCodeRevocationFailureStep,
                            MockUnlockCodeRevocationSuccessStep, MockFinalStep]
        testing_steps = {s.name: s for s in testing_steps}
        self.endpoint_correct = "unlock_code_revocation"
        self.flow = UnlockCodeRevocationMultiStepFlow(endpoint=self.endpoint_correct)
        self.flow.steps = testing_steps
        self.flow.first_step = next(iter(testing_steps.values()))

        # Set sessions up
        self.existing_session = "sessionAvailable"
        self.session_data = {'idnr': '04452397687', 'dob': '01.01.1985'}

        self.failure_url = '/' + self.endpoint_correct + '/step/' + MockUnlockCodeRevocationFailureStep.name + \
                            '?link_overview=' + str(self.flow.has_link_overview)
        self.success_url = '/' + self.endpoint_correct + '/step/' + MockUnlockCodeRevocationSuccessStep.name + \
                            '?link_overview=' + str(self.flow.has_link_overview)

        prev_step, self.success_step, next_step = self.flow._generate_steps(
            MockUnlockCodeRevocationSuccessStep.name)
        self.render_info_success_step = RenderInfo(step_title=self.success_step.title,
                                                    step_intro=self.success_step.intro, form=None,
                                                    prev_url=self.flow.url_for_step(prev_step.name),
                                                    next_url=self.flow.url_for_step(next_step.name),
                                                    submit_url=self.flow.url_for_step(self.success_step.name),
                                                    overview_url="Overview URL")

        prev_step, self.input_step, next_step = self.flow._generate_steps(MockUnlockCodeRevocationInputStep.name)
        self.render_info_input_step = RenderInfo(step_title=self.input_step.title, step_intro=self.input_step.intro,
                                                    form=None, prev_url=self.flow.url_for_step(prev_step.name),
                                                    next_url=self.flow.url_for_step(next_step.name),
                                                    submit_url=self.flow.url_for_step(self.input_step.name),
                                                    overview_url="Overview URL")

    def test_if_user_exists_and_dob_correct_and_unlock_code_revocation_got_through_then_next_url_is_success_step(self):
        existing_idnr = '04452397687'
        correct_dob = ['1', '1', '1985']
        create_user(existing_idnr, '01.01.1985', '0000')
        with self.app.test_request_context(method='POST',
                                           data={'idnr': existing_idnr,
                                                 'dob': correct_dob}):
            with patch(
                    "app.forms.flows.unlock_code_revocation_flow.elster_client.send_unlock_code_revocation_with_elster") \
                    as fun_unlock_code_revocation:
                render_info, _ = self.flow._handle_specifics_for_step(
                    self.input_step, self.render_info_input_step, self.session_data)
                self.assertEqual(self.success_url, render_info.next_url)
                fun_unlock_code_revocation.assert_called_once()  # make sure not only default case is executed

    def test_if_user_exists_and_dob_correct_and_unlock_code_revocation_got_through_then_user_is_deleted(self):
        existing_idnr = '04452397687'
        correct_dob = ['1', '1', '1985']
        create_user(existing_idnr, '01.01.1985', '0000')
        with self.app.test_request_context(method='POST',
                                           data={'idnr': existing_idnr,
                                                 'dob': correct_dob}):
            with patch(
                    "app.forms.flows.unlock_code_revocation_flow.elster_client.send_unlock_code_revocation_with_elster"):
                self.flow._handle_specifics_for_step(
                    self.input_step, self.render_info_input_step, self.session_data)
                self.assertRaises(UserNotExistingError, find_user, existing_idnr)

    def test_if_user_exists_but_elster_returns_no_antrag_found_then_next_url_is_success_step(self):
        existing_idnr = '04452397687'
        date_of_birth = ['1', '1', '1985']
        create_user(existing_idnr, '01.01.1985', '0000')

        with open(FIXTURES_PATH + 'sample_vast_revocation_response_failure.xml') as failue_sample:
            failure_server_response = failue_sample.read()
        with self.app.test_request_context(method='POST', data={'idnr': existing_idnr, 'dob': date_of_birth}):
            with patch("app.forms.flows.unlock_code_revocation_flow.elster_client.send_unlock_code_revocation_with_elster") \
                    as fun_unlock_code_revocation:
                expected_error = ElsterRequestIdUnkownError()
                expected_error.eric_response = b''
                expected_error.server_response = failure_server_response
                fun_unlock_code_revocation.side_effect = expected_error

                render_info, _ = self.flow._handle_specifics_for_step(
                    self.input_step, self.render_info_input_step, self.session_data)
                self.assertEqual(self.success_url, render_info.next_url)
                fun_unlock_code_revocation.assert_called_once()  # make sure not only default case is executed

    def test_if_user_exists_but_elster_returns_no_antrag_found_then_user_is_deleted(self):
        existing_idnr = '04452397687'
        date_of_birth = ['1', '1', '1985']
        create_user(existing_idnr, '01.01.1985', '0000')

        with open(FIXTURES_PATH + 'sample_vast_revocation_response_failure.xml') as failue_sample:
            failure_server_response = failue_sample.read()
        with self.app.test_request_context(method='POST', data={'idnr': existing_idnr, 'dob': date_of_birth}):
            with patch("app.forms.flows.unlock_code_revocation_flow.elster_client.send_unlock_code_revocation_with_elster") \
                    as fun_unlock_code_revocation:
                expected_error = ElsterRequestIdUnkownError()
                expected_error.eric_response = b''
                expected_error.server_response = failure_server_response
                fun_unlock_code_revocation.side_effect = expected_error

                render_info, _ = self.flow._handle_specifics_for_step(
                    self.input_step, self.render_info_input_step, self.session_data)
                self.assertRaises(UserNotExistingError, find_user, existing_idnr)

    def test_if_user_exists_but_elster_returns_already_revoked_then_user_is_deleted(self):
        existing_idnr = '04452397687'
        date_of_birth = ['01', '01', '1985']
        create_user(existing_idnr, '01.01.1985', '0000')

        with open(FIXTURES_PATH + 'sample_vast_revocation_response_failure.xml') as failure_sample:
            failure_server_response = failure_sample.read()
        with self.app.test_request_context(method='POST', data={'idnr': existing_idnr, 'dob': date_of_birth}):
            with patch("app.forms.flows.unlock_code_revocation_flow.elster_client.send_unlock_code_revocation_with_elster") \
                    as fun_unlock_code_revocation:
                expected_error = ElsterRequestAlreadyRevoked()
                expected_error.eric_response = b''
                expected_error.server_response = failure_server_response
                fun_unlock_code_revocation.side_effect = expected_error

                render_info, _ = self.flow._handle_specifics_for_step(
                    self.input_step, self.render_info_input_step, self.session_data)
                self.assertRaises(UserNotExistingError, find_user, existing_idnr)

    def test_if_unlock_code_revocation_did_not_get_through_then_next_url_is_failure_step(self):
        existing_idnr = '04452397687'
        correct_dob = ['1', '1', '1985']
        create_user(existing_idnr, '01.01.1985', '0000')
        with self.app.test_request_context(method='POST',
                                           data={'idnr': existing_idnr,
                                                 'dob': correct_dob}):
            with patch(
                    "app.forms.flows.unlock_code_revocation_flow.elster_client.send_unlock_code_revocation_with_elster") \
                    as fun_unlock_code_revocation:
                fun_unlock_code_revocation.side_effect = ElsterProcessNotSuccessful()
                render_info, _ = self.flow._handle_specifics_for_step(
                        self.input_step, self.render_info_input_step, self.session_data)
                self.assertEqual(self.failure_url, render_info.next_url)
                fun_unlock_code_revocation.assert_called_once()

    def test_if_unlock_code_revocation_did_not_get_through_then_user_is_not_deleted(self):
        existing_idnr = '04452397687'
        correct_dob = ['1', '1', '1985']
        create_user(existing_idnr, '01.01.1985', '0000')
        with self.app.test_request_context(method='POST',
                                           data={'idnr': existing_idnr,
                                                 'dob': correct_dob}):
            with patch(
                    "app.forms.flows.unlock_code_revocation_flow.elster_client.send_unlock_code_revocation_with_elster") \
                    as fun_unlock_code_revocation:
                fun_unlock_code_revocation.side_effect = ElsterProcessNotSuccessful()
                self.flow._handle_specifics_for_step(
                        self.input_step, self.render_info_input_step, self.session_data)
                try:
                    find_user(existing_idnr)
                except UserNotExistingError:
                    self.fail('User was deleted unexpectedly.')
                fun_unlock_code_revocation.assert_called_once()

    def test_if_user_not_existing_then_next_url_is_failure_step(self):
        not_existing_idnr = '04452397687'

        with self.app.test_request_context(method='POST',
                                           data={'idnr': not_existing_idnr,
                                                 'dob': 'INCORRECT'}):
            with patch("app.forms.steps.step.FormStep.create_form"):
                render_info, _ = self.flow._handle_specifics_for_step(
                    self.input_step, self.render_info_input_step, self.session_data)

                self.assertEqual(self.failure_url, render_info.next_url)

    def test_if_user_exists_and_date_of_birth_incorrect_then_next_url_is_failure_step(self):
        existing_idnr = '04452397687'
        date_of_birth = '01.01.1985'
        create_user(existing_idnr, date_of_birth, '0000')

        with self.app.test_request_context(method='POST',
                                           data={'idnr': existing_idnr,
                                                 'dob': 'INCORRECT'}):
            render_info, _ = self.flow._handle_specifics_for_step(
                    self.input_step, self.render_info_input_step, self.session_data)

            self.assertEqual(self.failure_url, render_info.next_url)


@pytest.fixture
def unlock_code_revocation_flow():
    return UnlockCodeRevocationMultiStepFlow(endpoint="unlock_code_revocation")


class TestUnlockCodeActivationGetSessionData:

    @pytest.mark.usefixtures('test_request_context')
    def test_if_get_storage_data_called_then_get_cookie_data_function_called_with_correct_params(self, unlock_code_revocation_flow):
        with patch('app.data_access.storage.cookie_storage.CookieStorage.get_data') as patched_get_cookie_data:
            unlock_code_revocation_flow._get_storage_data(ttl=2)

        assert patched_get_cookie_data.call_args == call('form_data', 2)


class TestUnlockCodeActivationOverrideSessionData:

    @pytest.mark.usefixtures('test_request_context')
    def test_if_override_storage_data_called_then_cookie_override_function_called_with_correct_params(self, unlock_code_revocation_flow):
        with patch('app.data_access.storage.cookie_storage.CookieStorage.override_data') as patched_override:
            unlock_code_revocation_flow._override_storage_data(stored_data={'name': 'Ash'})

        assert patched_override.call_args == call({'name': 'Ash'}, data_identifier='form_data')
