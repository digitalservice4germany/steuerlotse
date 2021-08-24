import unittest
from unittest.mock import patch

from flask import json
from flask.sessions import SecureCookieSession
from werkzeug.exceptions import NotFound
from werkzeug.utils import redirect

# TODO: replace with app factory / client fixture
from app import app, db
from app.data_access.user_controller import create_user, find_user
from app.elster_client.elster_errors import ElsterProcessNotSuccessful
from app.forms.flows.multistep_flow import RenderInfo
from app.forms.flows.unlock_code_activation_flow import UnlockCodeActivationMultiStepFlow
from app.forms.steps.unlock_code_activation_steps import UnlockCodeActivationFailureStep, UnlockCodeActivationInputStep
from tests.forms.mock_steps import MockStartStep, MockMiddleStep, MockFinalStep, MockRenderStep, MockFormStep, \
    MockUnlockCodeActivationFailureStep, MockUnlockCodeActivationInputStep
from tests.utils import create_session_form_data, create_and_activate_user


class UnlockCodeActivationInit(unittest.TestCase):

    def setUp(self):
        db.create_all()
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
        with app.app_context() and app.test_request_context() as req:
            req.request.args = {'link_overview': self.set_link_overview}

            flow = UnlockCodeActivationMultiStepFlow(endpoint=self.endpoint_correct)

            self.assertTrue(flow.has_link_overview)
            self.assertEqual(self.expected_steps, list(flow.steps.values()))
            self.assertEqual(self.expected_steps[0], flow.first_step)
            self.assertIsNone(flow.overview_step)

    def test_if_request_has_no_params_then_set_correct_defaults(self):
        with app.app_context() and app.test_request_context():
            flow = UnlockCodeActivationMultiStepFlow(endpoint=self.endpoint_correct)

            self.assertFalse(flow.has_link_overview)
            self.assertEqual(self.expected_steps[0], flow.first_step)
            self.assertIsNone(flow.overview_step)

    def tearDown(self):
        db.drop_all()


class TestUnlockCodeActivationHandle(unittest.TestCase):

    def setUp(self):
        db.create_all()
        with app.app_context() and app.test_request_context():
            testing_steps = [MockStartStep, MockRenderStep, MockFormStep, MockFinalStep]
            testing_steps = {s.name: s for s in testing_steps}
            self.endpoint_correct = "unlock_code_activation"
            self.flow = UnlockCodeActivationMultiStepFlow(endpoint=self.endpoint_correct)
            self.flow.steps = testing_steps
            self.flow.first_step = next(iter(testing_steps.values()))
            self.stored_data = self.flow.default_data()

            # We need to set a different get_flow_nav_function that fits the used mocked steps
            self.flow._get_flow_nav = lambda step: []

            # Set sessions up
            self.session_data = {'idnr': '04452397687', 'dob': '1985-01-01'}

    def test_if_correct_step_name_then_return_code_correct(self):
        with app.app_context() and app.test_request_context():
            response = self.flow.handle(MockRenderStep.name)

            self.assertEqual(200, response.status_code)

    def test_if_incorrect_step_name_then_raise_404_exception(self):
        with app.app_context() and app.test_request_context():
            self.assertRaises(NotFound, self.flow.handle, "Incorrect Step Name")

    def test_if_start_step_then_return_redirect_to_first_step(self):
        with app.app_context() and app.test_request_context():
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
        with app.app_context() and app.test_request_context(
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
        with app.app_context() and app.test_request_context(
                path="/" + self.endpoint_correct + "/step/" + MockRenderStep.name,
                method='GET') as req:
            req.session = SecureCookieSession({'form_data': create_session_form_data(self.session_data)})
            response = self.flow.handle(MockRenderStep.name)

            self.assertEqual(200, response.status_code)
            # Check response data because that's where our Mock returns. Decode because response stores as bytestring
            self.assertTrue(set(self.session_data).issubset(json.loads(str(response.get_data(), 'utf-8'))[0]))

    def tearDown(self):
        db.drop_all()


class TestUnlockCodeActivationHandleSpecificsForStep(unittest.TestCase):

    def setUp(self):
        db.create_all()
        with app.app_context() and app.test_request_context():
            testing_steps = [MockStartStep, MockUnlockCodeActivationInputStep, MockUnlockCodeActivationFailureStep,
                             MockFinalStep]
            testing_steps = {s.name: s for s in testing_steps}
            self.endpoint_correct = "unlock_code_activation"
            self.flow = UnlockCodeActivationMultiStepFlow(endpoint=self.endpoint_correct)
            self.flow.steps = testing_steps
            self.flow.first_step = next(iter(testing_steps.values()))

            # We need to set a different get_flow_nav_function that fits the used mocked steps
            self.flow._get_flow_nav = lambda step: []

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
        with app.app_context() and app.test_request_context(method='POST',
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
        with app.app_context() and app.test_request_context(method='POST',
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
        with app.app_context() and app.test_request_context(method='POST',
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

        with app.app_context() and app.test_request_context(method='POST',
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

        with app.app_context() and app.test_request_context(method='POST',
                                                            data={'idnr': existing_idnr,
                                                                  'unlock_code': unlock_code}):
            render_info, _ = self.flow._handle_specifics_for_step(
                    self.input_step, self.render_info_input_step, self.session_data)

            self.assertEqual(self.success_url, render_info.next_url)

    def test_if_user_is_active_and_unlock_code_incorrect_then_next_url_is_failure_step(self):
        existing_idnr = '04452397687'
        unlock_code = '0000-0000-0000'
        create_and_activate_user(existing_idnr, '0000', '1985-01-01', unlock_code)

        with app.app_context() and app.test_request_context(method='POST',
                                                            data={'idnr': existing_idnr,
                                                                  'unlock_code': '0000-0000-9999'}):
            render_info, _ = self.flow._handle_specifics_for_step(
                    self.input_step, self.render_info_input_step, self.session_data)

            self.assertEqual(self.failure_url, render_info.next_url)

    def test_if_user_not_existing_then_next_url_is_failure_step(self):
        not_existing_idnr = '04452397687'

        with app.app_context() and app.test_request_context(method='POST',
                                                            data={'idnr': not_existing_idnr,
                                                                  'unlock_code': '0000-0000-0000'}):
            render_info, _ = self.flow._handle_specifics_for_step(
                    self.input_step, self.render_info_input_step, self.session_data)

            self.assertEqual(self.failure_url, render_info.next_url)

    def tearDown(self):
        db.drop_all()
