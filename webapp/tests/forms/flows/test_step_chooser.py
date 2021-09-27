import datetime
import unittest
from unittest.mock import patch

import pytest
from flask import Flask
from flask.sessions import SecureCookieSession
from werkzeug.datastructures import ImmutableMultiDict
from werkzeug.exceptions import NotFound

from app.forms.session_data import serialize_session_data, deserialize_session_data
from app.forms.flows.step_chooser import StepChooser
from app.forms.steps.steuerlotse_step import RedirectSteuerlotseStep
from tests.forms.mock_steuerlotse_steps import MockStartStep, MockMiddleStep, MockFinalStep, MockFormWithInputStep, \
    MockRenderStep, MockFormStep, MockYesNoStep, MockStepWithRedirection
from tests.utils import create_session_form_data


class TestStepChooserInit(unittest.TestCase):
    @pytest.fixture(autouse=True)
    def attach_fixtures(self, test_request_context):
        self.req = test_request_context

    def setUp(self):
        self.testing_steps = [MockStartStep, MockMiddleStep, MockFinalStep]
        self.endpoint_correct = "lotse"

    def test_set_attributes_correctly(self):
        step_chooser = StepChooser(title="Testing StepChooser", steps=self.testing_steps,
                                    endpoint=self.endpoint_correct)
        self.assertEqual(self.testing_steps[0], step_chooser.first_step)
        self.assertEqual(self.testing_steps, list(step_chooser.steps.values()))
        self.assertEqual(self.endpoint_correct, step_chooser.endpoint)
        self.assertEqual(None, step_chooser.overview_step)


class TestGetPossibleRedirect:
    @pytest.fixture
    def step_chooser(self):
        testing_steps = [MockStartStep, MockRenderStep, MockFormWithInputStep, MockStepWithRedirection, MockFinalStep]
        self.endpoint_correct = "lotse"
        yield StepChooser(title="Testing StepChooser", steps=testing_steps,
                          endpoint=self.endpoint_correct, overview_step=MockFormWithInputStep)

    def test_if_step_not_in_step_list_return_404(self, step_chooser):
        with pytest.raises(NotFound):
            step_chooser._get_possible_redirect('INVALID_STEP_NAME', {})

    def test_if_step_name_is_start_then_return_first_in_list(self, step_chooser):
        step_to_redirect_to = step_chooser._get_possible_redirect('start', {})
        assert step_to_redirect_to == MockStartStep.name

    def test_if_step_has_redirection_set_and_not_met_then_return_step_to_redirect_to(self, step_chooser):
        step_to_redirect_to = step_chooser._get_possible_redirect(MockStepWithRedirection.name,
                                                                  {'precondition_met': False})
        assert step_to_redirect_to == MockStartStep.name

    def test_if_step_has_redirection_set_but_met_then_return_none(self, step_chooser):
        step_to_redirect_to = step_chooser._get_possible_redirect(MockStepWithRedirection.name,
                                                                  {'precondition_met': True})
        assert step_to_redirect_to is None


class TestStepChooserGetCorrectStep(unittest.TestCase):
    @pytest.fixture(autouse=True)
    def attach_fixtures(self, test_request_context):
        self.req = test_request_context

    def setUp(self) -> None:
        testing_steps = [MockStartStep, MockRenderStep, MockFormWithInputStep, MockYesNoStep, MockFinalStep]
        self.endpoint_correct = "lotse"
        self.step_chooser = StepChooser(title="Testing StepChooser", steps=testing_steps,
                                        endpoint=self.endpoint_correct, overview_step=MockFormWithInputStep)

    def test_if_correct_step_name_then_return_step_correctly_initialised(self):
        chosen_step = self.step_chooser.get_correct_step(MockRenderStep.name)

        self.assertIsInstance(chosen_step, MockRenderStep)
        self.assertEqual(MockRenderStep.name, chosen_step.name)
        self.assertEqual(self.endpoint_correct, chosen_step.endpoint)
        self.assertEqual(self.step_chooser.overview_step, chosen_step.overview_step)
        self.assertEqual(MockStartStep, chosen_step._prev_step)
        self.assertEqual(MockFormWithInputStep, chosen_step._next_step)

    def test_if_incorrect_step_name_then_raise_404_exception(self):
        self.assertRaises(NotFound, self.step_chooser.get_correct_step, "Incorrect Step Name")

    def test_if_start_step_then_return_redirect_to_first_step(self):
        chosen_step = self.step_chooser.get_correct_step("start")

        self.assertIsInstance(chosen_step, RedirectSteuerlotseStep)
        self.assertEqual(chosen_step.redirection_step_name, self.step_chooser.first_step.name)

    def test_if_step_in_list_of_steps_return_correct_steps(self):
        simple_step_chooser = StepChooser(title="Testing StepChooser",
                                            steps=[MockStartStep, MockMiddleStep, MockFinalStep],
                                            endpoint=self.endpoint_correct)

        chosen_step = simple_step_chooser.get_correct_step(MockStartStep.name)
        self.assertIsInstance(chosen_step, MockStartStep)
        self.assertEqual(MockMiddleStep, chosen_step._next_step)

        chosen_step = simple_step_chooser.get_correct_step(MockMiddleStep.name)
        self.assertEqual(MockStartStep, chosen_step._prev_step)
        self.assertIsInstance(chosen_step, MockMiddleStep)
        self.assertEqual(MockFinalStep, chosen_step._next_step)

        chosen_step = simple_step_chooser.get_correct_step(MockFinalStep.name)
        self.assertEqual(MockMiddleStep, chosen_step._prev_step)
        self.assertIsInstance(chosen_step, MockFinalStep)

    def test_if_step_at_ends_then_return_empty_string(self):
        chosen_step_at_begin = self.step_chooser.get_correct_step(MockStartStep.name)
        chosen_step_at_end = self.step_chooser.get_correct_step(MockFinalStep.name)
        self.assertIsNone(chosen_step_at_begin._prev_step)
        self.assertIsNone(chosen_step_at_end._next_step)

    def test_update_data_is_called_if_update_data_set(self):
        with patch('app.forms.steps.steuerlotse_step.FormSteuerlotseStep.update_data') as update_mock:
            self.step_chooser.get_correct_step(MockFormWithInputStep.name, update_data=True)

        update_mock.assert_called_once()

    def test_update_data_is_not_called_if_update_data_not_set(self):
        with patch('app.forms.steps.steuerlotse_step.FormSteuerlotseStep.update_data') as update_mock:
            self.step_chooser.get_correct_step(MockFormWithInputStep.name, update_data=False)

        update_mock.assert_not_called()


class TestInteractionBetweenSteps(unittest.TestCase):
    @pytest.fixture(autouse=True)
    def attach_fixtures(self, app, test_request_context):
        self.app = app
        self.req = test_request_context

    def test_if_form_step_after_render_step_then_keep_data_from_older_form_step(self):
        testing_steps = [MockStartStep, MockFormWithInputStep, MockRenderStep, MockFormStep, MockFinalStep]
        endpoint_correct = "lotse"
        session_data_identifier = 'form_data'
        original_data = {'pet': 'Yoshi', 'date': ['9', '7', '1981'], 'decimal': '60.000'}

        step_chooser = StepChooser(title="Testing StepChooser", steps=testing_steps, endpoint=endpoint_correct)
        step_chooser.session_data_identifier = session_data_identifier

        session = self.run_handle(self.app, step_chooser, MockFormWithInputStep.name, method='POST', form_data=original_data)
        session = self.run_handle(self.app, step_chooser, MockRenderStep.name, method='GET', session=session)
        session = self.run_handle(self.app, step_chooser, MockFormStep.name, method='GET', session=session)
        self.assertTrue(set(original_data).issubset(
            set(deserialize_session_data(session[session_data_identifier], self.app.config['PERMANENT_SESSION_LIFETIME']))))

    def test_if_form_step_after_form_step_then_keep_data_from_newer_form_step(self):
        testing_steps = [MockStartStep, MockFormWithInputStep, MockFormWithInputStep, MockRenderStep, MockFormStep, MockFinalStep]
        endpoint_correct = "lotse"
        session_data_identifier = 'form_data'
        original_data = {'pet': 'Yoshi', 'date': ['9', '7', '1981'], 'decimal': '60.000'}
        adapted_data = {'pet': 'Goomba', 'date': ['9', '7', '1981'], 'decimal': '60.000'}

        step_chooser = StepChooser(title="Testing StepChooser", steps=testing_steps, endpoint=endpoint_correct)
        step_chooser.session_data_identifier = session_data_identifier

        session = self.run_handle(self.app, step_chooser, MockFormWithInputStep.name, method='POST', form_data=original_data)
        session = self.run_handle(self.app, step_chooser, MockFormWithInputStep.name, method='POST', form_data=adapted_data, session=session)
        session = self.run_handle(self.app, step_chooser, MockRenderStep.name, method='GET', session=session)
        session = self.run_handle(self.app, step_chooser, MockFormStep.name, method='GET', session=session)
        self.assertTrue(set(adapted_data).issubset(
            set(deserialize_session_data(session[session_data_identifier], self.app.config['PERMANENT_SESSION_LIFETIME']))))

    @staticmethod
    def run_handle(app: Flask, step_chooser: StepChooser, step_name, method='GET', form_data=None, session=None):
        with app.test_request_context(method=method) as req:
            if not form_data:
                form_data = {}
            req.request.form = ImmutableMultiDict(form_data)
            if session is not None:
                req.session = session

            step_chooser.get_correct_step(step_name, method == 'POST').handle()

            return req.session
