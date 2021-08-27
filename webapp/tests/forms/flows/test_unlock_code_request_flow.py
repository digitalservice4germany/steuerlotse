import copy
import unittest
import datetime as dt
from unittest.mock import patch, call

import pytest
from flask import json
from werkzeug.exceptions import NotFound
from werkzeug.utils import redirect

from app.data_access.user_controller import create_user, user_exists, find_user
from app.elster_client.elster_errors import ElsterProcessNotSuccessful
from app.forms.flows.multistep_flow import RenderInfo
from app.forms.flows.unlock_code_request_flow import UnlockCodeRequestMultiStepFlow
from app.forms.steps.unlock_code_request_steps import UnlockCodeRequestFailureStep, UnlockCodeRequestSuccessStep, \
    UnlockCodeRequestInputStep
from tests.forms.mock_steps import MockStartStep, MockMiddleStep, MockFinalStep, MockRenderStep, MockFormStep, \
    MockUnlockCodeRequestFailureStep, MockUnlockCodeRequestSuccessStep, MockUnlockCodeRequestInputStep


class UnlockCodeRequestInit(unittest.TestCase):
    @pytest.fixture(autouse=True)
    def attach_fixtures(self, transactional_session, app, test_request_context):
        self.session = transactional_session
        self.app = app
        self.req = test_request_context

    def setUp(self):
        self.testing_steps = [MockStartStep, MockMiddleStep, MockFinalStep]
        self.endpoint_correct = "unlock_code_request"
        self.incorrect_session = "r2D2"
        self.set_link_overview = "True"
        self.expected_steps = [
            UnlockCodeRequestInputStep,
            UnlockCodeRequestFailureStep,
            UnlockCodeRequestSuccessStep
        ]

    def test_if_request_has_params_then_set_attributes_correctly(self):
        # Only current link_overview is set from request
        self.req.request.args = {'link_overview': self.set_link_overview}

        flow = UnlockCodeRequestMultiStepFlow(endpoint=self.endpoint_correct)

        self.assertTrue(flow.has_link_overview)
        self.assertEqual(self.expected_steps, list(flow.steps.values()))
        self.assertEqual(self.expected_steps[0], flow.first_step)
        self.assertIsNone(flow.overview_step)

    def test_if_request_has_no_params_then_set_correct_defaults(self):
        flow = UnlockCodeRequestMultiStepFlow(endpoint=self.endpoint_correct)

        self.assertFalse(flow.has_link_overview)
        self.assertEqual(self.expected_steps[0], flow.first_step)
        self.assertIsNone(flow.overview_step)


class TestUnlockCodeRequestHandle(unittest.TestCase):
    @pytest.fixture(autouse=True)
    def attach_fixtures(self, transactional_session, app, test_request_context):
        self.session = transactional_session
        self.app = app
        self.req = test_request_context

    def setUp(self):
        testing_steps = [MockStartStep, MockRenderStep, MockFormStep, MockFinalStep]
        testing_steps = {s.name: s for s in testing_steps}
        self.endpoint_correct = "unlock_code_request"
        self.flow = UnlockCodeRequestMultiStepFlow(endpoint=self.endpoint_correct)
        self.flow.steps = testing_steps
        self.flow.first_step = next(iter(testing_steps.values()))
        self.stored_data = self.flow.default_data()

        # We need to set a different get_flow_nav_function that fits the used mocked steps
        self.flow._get_flow_nav = lambda step: []

        # Set sessions up
        self.existing_session = "sessionAvailable"
        self.session_data = {'idnr': '04452397687', 'dob': '1985-01-01',  'registration_confirm_incomes': True,
                                'registration_confirm_data_privacy': True, 'registration_confirm_e_data': True,
                                'registration_confirm_terms_of_service': True}

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
                method='GET'):
            response = self.flow.handle(MockRenderStep.name)

            self.assertEqual(200, response.status_code)
            # Check response data because that's where our Mock returns. Decode because response stores as bytestring
            self.assertEqual(self.session_data, json.loads(str(response.get_data(), 'utf-8'))[0])


class TestUnlockCodeRequestHandleSpecificsForStep(unittest.TestCase):
    @pytest.fixture(autouse=True)
    def attach_fixtures(self, transactional_session, app, test_request_context):
        self.session = transactional_session
        self.app = app
        self.req = test_request_context

    def setUp(self):
        testing_steps = [MockStartStep, MockUnlockCodeRequestInputStep, MockUnlockCodeRequestFailureStep,
                            MockUnlockCodeRequestSuccessStep]
        testing_steps = {s.name: s for s in testing_steps}
        self.endpoint_correct = "unlock_code_request"
        self.flow = UnlockCodeRequestMultiStepFlow(endpoint=self.endpoint_correct)
        self.flow.steps = testing_steps
        self.flow.first_step = next(iter(testing_steps.values()))

        # We need to set a different get_flow_nav_function that fits the used mocked steps
        self.flow._get_flow_nav = lambda step: []

        # Set sessions up
        self.valid_idnr = '04452397687'
        self.session_data = {'idnr': self.valid_idnr, 'dob': dt.date(1985, 1, 1)}
        self.valid_input_data = {'idnr': self.valid_idnr, 'dob': ['1', '1', '1980'],
                                    'registration_confirm_data_privacy': True,
                                    'registration_confirm_terms_of_service': True,
                                    'registration_confirm_incomes': True,
                                    'registration_confirm_e_data': True}

        prev_step, self.success_step, next_step = self.flow._generate_steps(MockUnlockCodeRequestSuccessStep.name)
        self.render_info_success_step = RenderInfo(step_title=self.success_step.title,
                                                    step_intro=self.success_step.intro, form=None,
                                                    prev_url=self.flow.url_for_step(prev_step.name),
                                                    next_url=self.flow.url_for_step(
                                                        next_step.name) if next_step else None,
                                                    submit_url=self.flow.url_for_step(self.success_step),
                                                    overview_url="Overview URL")

        prev_step, self.input_step, next_step = self.flow._generate_steps(MockUnlockCodeRequestInputStep.name)
        self.render_info_input_step = RenderInfo(step_title=self.input_step.title, step_intro=self.input_step.intro,
                                                    form=None, prev_url=self.flow.url_for_step(prev_step.name),
                                                    next_url=self.flow.url_for_step(
                                                        next_step.name) if next_step else None,
                                                    submit_url=self.flow.url_for_step(self.input_step),
                                                    overview_url="Overview URL")

    def test_if_success_step_then_remove_next_url(self):
        render_info, _ = self.flow._handle_specifics_for_step(
            self.success_step, self.render_info_success_step, self.session_data)
        self.assertEqual(None, render_info.next_url)

    def test_if_unlock_code_request_got_through_then_next_url_is_success_step(self):
        success_url = '/' + self.endpoint_correct + '/step/' + MockUnlockCodeRequestSuccessStep.name + \
                               '?link_overview=' + str(self.flow.has_link_overview)

        idnr = '04452397687'
        with self.app.test_request_context(method='POST', data=self.valid_input_data):
            with patch("app.forms.flows.unlock_code_request_flow.create_audit_log_confirmation_entry"),\
                    patch("app.forms.flows.unlock_code_request_flow.elster_client.send_unlock_code_request_with_elster") \
                    as fun_unlock_code_request:
                fun_unlock_code_request.return_value = {'idnr': idnr, 'elster_request_id': '000'}

                render_info, _ = self.flow._handle_specifics_for_step(
                    self.input_step, self.render_info_input_step, self.session_data)

                self.assertEqual(success_url, render_info.next_url)
                fun_unlock_code_request.assert_called_once()  # make sure not only default case is executed

    def test_if_unlock_code_request_got_through_then_user_is_saved(self):
        idnr = '04452397687'
        expected_elster_request_id = '12345'

        with self.app.test_request_context(method='POST', data=self.valid_input_data):
            with patch("app.forms.flows.unlock_code_request_flow.create_audit_log_confirmation_entry"),\
                    patch("app.forms.flows.unlock_code_request_flow.elster_client.send_unlock_code_request_with_elster") \
                    as fun_unlock_code_request:
                fun_unlock_code_request.return_value = {'idnr': idnr, 'elster_request_id': expected_elster_request_id}

                self.flow._handle_specifics_for_step(
                    self.input_step, self.render_info_input_step, self.session_data)

                self.assertTrue(user_exists(idnr))
                self.assertEqual(expected_elster_request_id, find_user(idnr).elster_request_id)

    def test_if_unlock_code_request_did_not_get_through_then_next_url_is_failure_step(self):
        failure_url = '/' + self.endpoint_correct + '/step/' + MockUnlockCodeRequestFailureStep.name + \
                               '?link_overview=' + str(self.flow.has_link_overview)

        with self.app.test_request_context(method='POST', data=self.valid_input_data):
            with patch("app.forms.flows.unlock_code_request_flow.create_audit_log_confirmation_entry"),\
                    patch("app.forms.flows.unlock_code_request_flow.elster_client.send_unlock_code_request_with_elster") \
                    as fun_unlock_code_request:
                fun_unlock_code_request.side_effect = ElsterProcessNotSuccessful()

                render_info, _ = self.flow._handle_specifics_for_step(
                    self.input_step, self.render_info_input_step, self.session_data)

                self.assertEqual(failure_url, render_info.next_url)
                fun_unlock_code_request.assert_called_once()

    def test_if_user_already_exists_then_next_url_is_failure_step(self):
        existing_idnr = '04452397687'
        create_user(existing_idnr, '1985-01-01', '0000')

        failure_url = '/' + self.endpoint_correct + '/step/' + MockUnlockCodeRequestFailureStep.name + \
                                '?link_overview=' + str(self.flow.has_link_overview)

        with self.app.test_request_context(method='POST', data=self.valid_input_data):
            with patch("app.forms.flows.unlock_code_request_flow.create_audit_log_confirmation_entry"),\
                    patch("app.forms.flows.unlock_code_request_flow.elster_client.send_unlock_code_request_with_elster") \
                    as fun_unlock_code_request:
                render_info, _ = self.flow._handle_specifics_for_step(
                        self.input_step, self.render_info_input_step, self.session_data)

                self.assertEqual(failure_url, render_info.next_url)
                fun_unlock_code_request.assert_not_called()

    def test_if_step_is_input_step_and_valid_form_then_call_create_auditlog_for_all_fields(self):
        ip_address = '127.0.0.1'
        with self.app.test_request_context(method='POST',
                                                            environ_base={'REMOTE_ADDR': ip_address},
                                                            data=self.valid_input_data):
            with patch("app.forms.flows.unlock_code_request_flow.elster_client.send_unlock_code_request_with_elster"),\
                    patch("app.forms.flows.unlock_code_request_flow.create_audit_log_confirmation_entry") as \
                    create_audit_log_fun:
                returned_data, _ = self.flow._handle_specifics_for_step(
                    self.input_step, copy.deepcopy(self.render_info_input_step), {})

                # Assert called for each confirmation field
                create_audit_log_fun.assert_has_calls([call('Confirmed registration data privacy', ip_address,
                                                            self.valid_idnr, 'registration_confirm_data_privacy',
                                                            True),
                                                       call('Confirmed registration terms of service', ip_address,
                                                            self.valid_idnr, 'registration_confirm_terms_of_service',
                                                            True),
                                                       call('Confirmed registration incomes', ip_address,
                                                            self.valid_idnr, 'registration_confirm_incomes',
                                                            True),
                                                       call('Confirmed registration edata', ip_address,
                                                            self.valid_idnr, 'registration_confirm_e_data',
                                                            True)],
                                                      any_order=True)

    def test_if_step_is_input_step_and_non_valid_form_then_do_not_call_create_auditlog(self):
        invalid_datas = [{'idnr': '04452397687', 'dob': '01.01.1980'},
                         {'idnr': '04452397687', 'dob': '01.01.1980',
                          'registration_confirm_terms_of_service': True,
                          'registration_confirm_incomes': True,
                          'registration_confirm_e_data': True},
                         {'idnr': '04452397687', 'dob': '01.01.1980',
                          'registration_confirm_data_privacy': True,
                          'registration_confirm_incomes': True,
                          'registration_confirm_e_data': True},
                         {'idnr': '04452397687', 'dob': '01.01.1980',
                          'registration_confirm_data_privacy': True,
                          'registration_confirm_terms_of_service': True,
                          'registration_confirm_e_data': True},
                         {'idnr': '04452397687', 'dob': '01.01.1980',
                          'registration_confirm_data_privacy': True,
                          'registration_confirm_terms_of_service': True,
                          'registration_confirm_incomes': True}]
        for invalid_data in invalid_datas:
            with self.app.test_request_context(method='POST', data=invalid_data):
                with patch("app.forms.flows.unlock_code_request_flow.elster_client.send_unlock_code_request_with_elster"),\
                        patch("app.forms.flows.unlock_code_request_flow.create_audit_log_confirmation_entry") as \
                        create_audit_log_fun:
                    returned_data, _ = self.flow._handle_specifics_for_step(
                        self.input_step, copy.deepcopy(self.render_info_input_step), {})

                    create_audit_log_fun.assert_not_called()
