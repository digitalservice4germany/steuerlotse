import unittest
from unittest.mock import patch, MagicMock

import pytest
from flask import url_for, session

from app.forms.flows.multistep_flow import RenderInfo
from app.forms.flows.logout_flow import LogoutMultiStepFlow
from tests.forms.mock_steps import MockLogoutInputStep


class TestLogoutHandleSpecificsForStep(unittest.TestCase):
    @pytest.fixture(autouse=True)
    def attach_fixtures(self, app, test_request_context):
        self.app = app
        self.req = test_request_context

    def setUp(self):
        testing_steps = [MockLogoutInputStep]
        testing_steps = {s.name: s for s in testing_steps}
        self.endpoint_correct = "logout"
        self.flow = LogoutMultiStepFlow(endpoint=self.endpoint_correct)
        self.flow.steps = testing_steps
        self.flow.first_step = next(iter(testing_steps.values()))

        # We need to set a different get_flow_nav_function that fits the used mocked steps
        self.flow._get_flow_nav = lambda step: []

        # Set sessions up
        self.existing_session = "sessionAvailable"
        self.session_data = {'idnr': '04452397687', 'dob': '1985-01-01'}

        self.success_url = url_for('unlock_code_activation')

        _, self.input_step, _ = self.flow._generate_steps(MockLogoutInputStep.name)
        self.render_info_input_step = RenderInfo(step_title=self.input_step.title, step_intro=self.input_step.intro,
                                                    form=None, prev_url=None, next_url=None,
                                                    submit_url=self.flow.url_for_step(self.input_step.name),
                                                    overview_url="Overview URL")

    def test_removes_all_stored_data(self):
        with self.app.test_request_context(method='POST', data={'confirm_logout': True}):
            with patch('app.forms.flows.logout_flow.current_user',
                       MagicMock(has_completed_tax_return=MagicMock(return_value=False))):
                session['form_data'] = {'idnr': '1234567890'}
                _, stored_data = self.flow._handle_specifics_for_step(
                    self.input_step, self.render_info_input_step, self.session_data)
                self.assertEqual({}, stored_data)

    def test_calls_logout_user(self):
        with self.app.test_request_context(method='POST', data={'confirm_logout': True}):
            with patch('app.forms.flows.logout_flow.logout_user') as logout_mock,\
                    patch('app.forms.flows.logout_flow.current_user',
                          MagicMock(has_completed_tax_return=MagicMock(return_value=False))):
                render_info, _ = self.flow._handle_specifics_for_step(
                    self.input_step, self.render_info_input_step, self.session_data)

                logout_mock.assert_called_once()

    def test_next_url_is_unlock_code_activation(self):
        with self.app.test_request_context(method='POST', data={'confirm_logout': True}):
            with patch('app.forms.flows.logout_flow.current_user',
                       MagicMock(has_completed_tax_return=MagicMock(return_value=False))):
                render_info, _ = self.flow._handle_specifics_for_step(
                    self.input_step, self.render_info_input_step, self.session_data)

                self.assertEqual(self.success_url, render_info.next_url)

    def test_if_user_has_not_completed_process_then_do_not_delete_data_on_get(self):
        with self.app.test_request_context(method='GET'):
            with patch('app.forms.flows.logout_flow.current_user',
                       MagicMock(has_completed_tax_return=MagicMock(return_value=False))):
                _, stored_data = self.flow._handle_specifics_for_step(
                    self.input_step, self.render_info_input_step, self.session_data)

                self.assertEqual(self.session_data, stored_data)

    def test_if_user_has_completed_tax_return_then_delete_data_on_get(self):
        with self.app.test_request_context(method='GET'):
            with patch('app.forms.flows.logout_flow.current_user',
                       MagicMock(has_completed_tax_return=MagicMock(return_value=True))):
                _, stored_data = self.flow._handle_specifics_for_step(
                    self.input_step, self.render_info_input_step, self.session_data)

                self.assertEqual({}, stored_data)

    def test_if_user_has_completed_tax_return_then_redirect_to_index(self):
        with self.app.test_request_context(method='GET'):
            with patch('app.forms.flows.logout_flow.current_user',
                       MagicMock(has_completed_tax_return=MagicMock(return_value=True))):
                render_info, _ = self.flow._handle_specifics_for_step(
                    self.input_step, self.render_info_input_step, self.session_data)

                self.assertEqual('/', render_info.redirect_url)
