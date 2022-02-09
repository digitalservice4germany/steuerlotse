import unittest
from unittest.mock import MagicMock, patch, call

import pytest
from flask import json
from flask.sessions import SecureCookieSession
from werkzeug.exceptions import NotFound
from werkzeug.utils import redirect

from app.data_access.user_controller import create_user, find_user
from app.elster_client.elster_errors import ElsterProcessNotSuccessful
from app.forms.flows.multistep_flow import RenderInfo
from app.forms.flows.unlock_code_activation_flow import UnlockCodeActivationMultiStepFlow, _store_id_in_server_session
from app.data_access.storage.session_storage import SessionStorage
from app.forms.steps.unlock_code_activation_steps import UnlockCodeActivationFailureStep, UnlockCodeActivationInputStep
from tests.forms.mock_steps import MockStartStep, MockMiddleStep, MockFinalStep, MockRenderStep, MockFormStep, \
    MockUnlockCodeActivationFailureStep, MockUnlockCodeActivationInputStep
from tests.utils import create_session_form_data, create_and_activate_user


class TestUnlockCodeActivationStoreIdInSession:

    def test_if_id_given_then_store_id_in_server_side_session(self):
        idnr = "007"
        _store_id_in_server_session(idnr)

        assert SessionStorage.get_data('form_data')['idnr'] == idnr


class TestUnlockCodeActivationInit(unittest.TestCase):
    @pytest.fixture(autouse=True)
    def attach_fixtures(self, transactional_session, test_request_context):
        self.session = transactional_session
        self.req = test_request_context

    def setUp(self):
        self.testing_steps = [MockStartStep, MockMiddleStep, MockFinalStep]
        self.endpoint_correct = "unlock_code_activation"
        self.incorrect_session = "r2D2"
        self.set_link_overview = "True"
        self.expected_steps = [
            UnlockCodeActivationInputStep,
            UnlockCodeActivationFailureStep
        ]

    def test_if_request_has_params_then_set_attributes_correctly(self):
        # Only current link_overview is set from request
        self.req.request.args = {'link_overview': self.set_link_overview}

        flow = UnlockCodeActivationMultiStepFlow(endpoint=self.endpoint_correct)

        self.assertTrue(flow.has_link_overview)
        self.assertEqual(self.expected_steps, list(flow.steps.values()))
        self.assertEqual(self.expected_steps[0], flow.first_step)
        self.assertIsNone(flow.overview_step)

    def test_if_request_has_no_params_then_set_correct_defaults(self):
        flow = UnlockCodeActivationMultiStepFlow(endpoint=self.endpoint_correct)

        self.assertFalse(flow.has_link_overview)
        self.assertEqual(self.expected_steps[0], flow.first_step)
        self.assertIsNone(flow.overview_step)


class TestUnlockCodeActivationHandle(unittest.TestCase):
    @pytest.fixture(autouse=True)
    def attach_fixtures(self, transactional_session, app, test_request_context):
        self.session = transactional_session
        self.app = app
        self.req = test_request_context

    def setUp(self):
        testing_steps = [MockStartStep, MockRenderStep, MockFormStep, MockFinalStep]
        testing_steps = {s.name: s for s in testing_steps}
        self.endpoint_correct = "unlock_code_activation"
        self.flow = UnlockCodeActivationMultiStepFlow(endpoint=self.endpoint_correct)
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
        with self.app.test_request_context(
                path="/" + self.endpoint_correct + "/step/" + MockRenderStep.name,
                method='GET') as req:
            req.session = SecureCookieSession({'form_data': create_session_form_data(self.session_data)})
            response = self.flow.handle(MockRenderStep.name)

            self.assertEqual(200, response.status_code)
            # Check response data because that's where our Mock returns. Decode because response stored as bytestring
            self.assertTrue(set(self.session_data).issubset(json.loads(str(response.get_data(), 'utf-8'))[0]))


class TestUnlockCodeActivationHandleSpecificsForStep(unittest.TestCase):
    @pytest.fixture(autouse=True)
    def attach_fixtures(self, transactional_session, app, test_request_context):
        self.session = transactional_session
        self.app = app
        self.req = test_request_context

    def setUp(self):
        testing_steps = [MockStartStep, MockUnlockCodeActivationInputStep, MockUnlockCodeActivationFailureStep,
                            MockFinalStep]
        testing_steps = {s.name: s for s in testing_steps}
        self.endpoint_correct = "unlock_code_activation"
        self.flow = UnlockCodeActivationMultiStepFlow(endpoint=self.endpoint_correct)
        self.flow.steps = testing_steps
        self.flow.first_step = next(iter(testing_steps.values()))

        # Set sessions up
        self.existing_session = "sessionAvailable"
        self.session_data = {'idnr': '04452397687', 'dob': '1985-01-01'}

        self.failure_url = '/' + self.endpoint_correct + '/step/' + MockUnlockCodeActivationFailureStep.name + \
                            '?link_overview=' + str(self.flow.has_link_overview)
        self.success_url = '/lotse/step/start'

        prev_step, self.input_step, next_step = self.flow._generate_steps(MockUnlockCodeActivationInputStep.name)
        self.render_info_input_step = RenderInfo(step_title=self.input_step.title, step_intro=self.input_step.intro,
                                                    form=None, prev_url=self.flow.url_for_step(prev_step.name),
                                                    next_url=self.flow.url_for_step(next_step.name),
                                                    submit_url=self.flow.url_for_step(self.input_step.name),
                                                    overview_url="Overview URL")

    def test_if_user_inactive_and_unlock_code_request_got_through_then_next_url_is_success_step(self):
        existing_idnr = '04452397687'
        create_user(existing_idnr, '1985-01-01', '0000')
        with self.app.test_request_context(method='POST',
                                           data={'idnr': existing_idnr,
                                                 'unlock_code': '0000-0000-0000'}):
            with patch(
                    "app.forms.flows.unlock_code_activation_flow.elster_client.send_unlock_code_activation_with_elster") \
                    as fun_unlock_code_activation:
                render_info, _ = self.flow._handle_specifics_for_step(
                    self.input_step, self.render_info_input_step, self.session_data)
                self.assertEqual(self.success_url, render_info.next_url)
                fun_unlock_code_activation.assert_called_once()  # make sure not only default case is executed

    def test_if_user_inactive_and_unlock_code_request_got_through_then_user_is_active(self):
        existing_idnr = '04452397687'
        create_user(existing_idnr, '1985-01-01', '0000')
        with self.app.test_request_context(method='POST',
                                           data={'idnr': existing_idnr,
                                                 'unlock_code': '0000-0000-0000'}):
            with patch(
                    "app.forms.flows.unlock_code_activation_flow.elster_client.send_unlock_code_activation_with_elster"):
                self.flow._handle_specifics_for_step(
                    self.input_step, self.render_info_input_step, self.session_data)
                self.assertTrue(find_user(existing_idnr).is_active)

    def test_if_unlock_code_request_did_not_get_through_then_next_url_is_failure_step(self):
        existing_idnr = '04452397687'
        create_user(existing_idnr, '1985-01-01', '0000')
        with self.app.test_request_context(method='POST',
                                           data={'idnr': existing_idnr,
                                                 'unlock_code': '0000-0000-0000'}):
            with patch(
                    "app.forms.flows.unlock_code_activation_flow.elster_client.send_unlock_code_activation_with_elster") \
                    as fun_unlock_code_activation:
                fun_unlock_code_activation.side_effect = ElsterProcessNotSuccessful()

                render_info, _ = self.flow._handle_specifics_for_step(
                    self.input_step, self.render_info_input_step, self.session_data)
                self.assertEqual(self.failure_url, render_info.next_url)
                fun_unlock_code_activation.assert_called_once()

    def test_if_user_is_active_then_send_no_request_to_elster(self):
        existing_idnr = '04452397687'
        unlock_code = '0000-0000-0000'
        create_and_activate_user(existing_idnr, '0000', '1985-01-01', unlock_code)

        with self.app.test_request_context(method='POST',
                                           data={'idnr': existing_idnr,
                                                 'unlock_code': '0000-0000-9999'}):
            with patch(
                    "app.forms.flows.unlock_code_activation_flow.elster_client.send_unlock_code_activation_with_elster") \
                    as fun_unlock_code_activation:
                fun_unlock_code_activation.side_effect = ElsterProcessNotSuccessful()
                self.flow._handle_specifics_for_step(
                        self.input_step, self.render_info_input_step, self.session_data)

                fun_unlock_code_activation.assert_not_called()

    def test_if_user_is_active_and_unlock_code_correct_then_next_url_is_success_step(self):
        existing_idnr = '04452397687'
        unlock_code = '0000-0000-0000'
        create_and_activate_user(existing_idnr, '0000', '1985-01-01', unlock_code)

        with self.app.test_request_context(method='POST',
                                           data={'idnr': existing_idnr,
                                                 'unlock_code': unlock_code}):
            render_info, _ = self.flow._handle_specifics_for_step(
                    self.input_step, self.render_info_input_step, self.session_data)

            self.assertEqual(self.success_url, render_info.next_url)

    def test_if_user_is_active_and_unlock_code_incorrect_then_next_url_is_failure_step(self):
        existing_idnr = '04452397687'
        unlock_code = '0000-0000-0000'
        create_and_activate_user(existing_idnr, '0000', '1985-01-01', unlock_code)

        with self.app.test_request_context(method='POST',
                                           data={'idnr': existing_idnr,
                                                 'unlock_code': '0000-0000-9999'}):
            render_info, _ = self.flow._handle_specifics_for_step(
                    self.input_step, self.render_info_input_step, self.session_data)

            self.assertEqual(self.failure_url, render_info.next_url)

    def test_if_user_not_existing_then_next_url_is_failure_step(self):
        not_existing_idnr = '04452397687'

        with self.app.test_request_context(method='POST',
                                           data={'idnr': not_existing_idnr,
                                                 'unlock_code': '0000-0000-0000'}):
            render_info, _ = self.flow._handle_specifics_for_step(
                    self.input_step, self.render_info_input_step, self.session_data)

            self.assertEqual(self.failure_url, render_info.next_url)

@pytest.fixture
def unlock_code_activation_flow():
    return UnlockCodeActivationMultiStepFlow(endpoint="unlock_code_activation")


class TestUnlockCodeActivationGetSessionData:

    @pytest.mark.usefixtures('test_request_context')
    def test_if_get_storage_data_called_then_get_cookie_data_function_called_with_correct_params(self, unlock_code_activation_flow):
        with patch('app.data_access.storage.cookie_storage.CookieStorage.get_data') as patched_get_cookie_data:
            unlock_code_activation_flow._get_storage_data(ttl=2)

        assert patched_get_cookie_data.call_args == call('form_data', 2)


class TestUnlockCodeActivationOverrideSessionData:

    @pytest.mark.usefixtures('test_request_context')
    def test_if_override_storage_data_called_then_cookie_override_function_called_with_correct_params(self, unlock_code_activation_flow):
        with patch('app.data_access.storage.cookie_storage.CookieStorage.override_data') as patched_override:
            with patch('app.data_access.storage.cookie_storage.CookieStorage.get_data', MagicMock(return_value={'name': 'Ash'})):
                unlock_code_activation_flow.handle('data_input')

        assert patched_override.call_args == call({'name': 'Ash'}, data_identifier='form_data')
