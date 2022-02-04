import datetime
import unittest
from copy import deepcopy
from decimal import Decimal
from unittest.mock import patch, MagicMock

import pytest
from flask import Flask, get_flashed_messages, session
from flask.sessions import SecureCookieSession
from werkzeug.datastructures import ImmutableMultiDict
from werkzeug.exceptions import NotFound

from app.forms.flows.multistep_flow import RenderInfo
from app.forms.session_data import deserialize_session_data, get_session_data
from app.forms.flows.step_chooser import StepChooser
from app.forms.steps.steuerlotse_step import RedirectSteuerlotseStep
from tests.forms.mock_steuerlotse_steps import MockStartStep, MockMiddleStep, MockFinalStep, MockFormWithInputStep, \
    MockRenderStep, MockFormStep, MockYesNoStep, MockStepWithPrecondition, \
    MockStepWithPreconditionAndMessage, MockSecondPreconditionModelWithMessage


@pytest.fixture
def test_step_chooser():
    testing_steps = [MockStartStep, MockFormWithInputStep, MockRenderStep, MockFormStep, MockFinalStep]
    return StepChooser(title="Testing StepChooser", steps=testing_steps, endpoint="lotse")


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


@pytest.mark.usefixtures('test_request_context')
class TestGetPossibleRedirect:
    @pytest.fixture
    def step_chooser(self):
        testing_steps = [MockStartStep, MockRenderStep, MockFormWithInputStep, MockStepWithPreconditionAndMessage, MockFinalStep]
        self.endpoint_correct = "lotse"
        yield StepChooser(title="Testing StepChooser", steps=testing_steps,
                          endpoint=self.endpoint_correct, overview_step=MockFormWithInputStep)

    def test_if_step_not_in_step_list_then_return_404(self, step_chooser):
        with pytest.raises(NotFound):
            step_chooser._get_possible_redirect('INVALID_STEP_NAME', {})

    def test_if_step_name_is_start_then_return_first_in_list(self, step_chooser):
        step_to_redirect_to = step_chooser._get_possible_redirect('start', {})
        assert step_to_redirect_to == MockStartStep.name

    def test_if_step_has_redirection_set_and_not_met_then_return_step_to_redirect_to(self, step_chooser):
        step_to_redirect_to = step_chooser._get_possible_redirect(MockStepWithPreconditionAndMessage.name,
                                                                  {'second_precondition_met': False})
        assert step_to_redirect_to == MockStartStep.name

    def test_if_step_has_redirection_set_and_not_met_then_flash(self, step_chooser):
        assert '_flashes' not in session

        step_chooser._get_possible_redirect(MockStepWithPreconditionAndMessage.name,
                                            {'second_precondition_met': False})

        flashed_messages = session['_flashes']
        assert len(flashed_messages) == 1
        assert flashed_messages[0][1] == MockSecondPreconditionModelWithMessage._message_to_flash

    def test_if_step_has_redirection_set_but_met_then_return_none(self, step_chooser):
        step_to_redirect_to = step_chooser._get_possible_redirect(MockStepWithPreconditionAndMessage.name,
                                                                  {'second_precondition_met': True})
        assert step_to_redirect_to is None

    def test_if_step_has_redirection_set_but_met_then_do_not_flash(self, step_chooser):
        step_chooser._get_possible_redirect(MockStepWithPreconditionAndMessage.name,
                                            {'second_precondition_met': True})
        assert '_flashes' not in session

    def test_if_step_in_list_and_has_no_redirection_set_then_return_none(self, step_chooser):
        step_to_redirect_to = step_chooser._get_possible_redirect(MockRenderStep.name, {})
        assert step_to_redirect_to is None

    def test_if_step_in_list_and_has_no_redirection_set_then_do_not_flash(self, step_chooser):
        step_chooser._get_possible_redirect(MockRenderStep.name, {})
        assert '_flashes' not in session


@pytest.mark.usefixtures("test_request_context", "testing_current_user")
class TestStepChooserGetCorrectStep:

    def test_if_correct_step_name_then_return_step_correctly_initialised(self, test_step_chooser):
        chosen_step = test_step_chooser.get_correct_step(MockRenderStep.name, False, ImmutableMultiDict({}))

        assert isinstance(chosen_step, MockRenderStep) is True
        assert chosen_step.name == MockRenderStep.name
        assert chosen_step.endpoint == "lotse"
        assert chosen_step.overview_step == test_step_chooser.overview_step
        assert chosen_step._prev_step == MockFormWithInputStep
        assert chosen_step._next_step == MockFormStep

    def test_if_incorrect_step_name_then_raise_404_exception(self, test_step_chooser):
        with pytest.raises(NotFound):
            test_step_chooser.get_correct_step("Incorrect Step Name", False, ImmutableMultiDict({}))

    def test_if_start_step_then_return_redirect_to_first_step(self, test_step_chooser):
        chosen_step = test_step_chooser.get_correct_step("start", False, ImmutableMultiDict({}))

        assert isinstance(chosen_step, RedirectSteuerlotseStep) is True
        assert test_step_chooser.first_step.name == chosen_step.redirection_step_name

    def test_if_step_in_list_of_steps_then_return_correct_steps(self, test_step_chooser):
        simple_step_chooser = StepChooser(title="Testing StepChooser",
                                            steps=[MockStartStep, MockMiddleStep, MockFinalStep],
                                            endpoint="lotse")

        chosen_step = simple_step_chooser.get_correct_step(MockStartStep.name, False, ImmutableMultiDict({}))
        assert isinstance(chosen_step, MockStartStep) is True
        assert chosen_step._next_step == MockMiddleStep

        chosen_step = simple_step_chooser.get_correct_step(MockMiddleStep.name, False, ImmutableMultiDict({}))
        assert chosen_step._prev_step == MockStartStep
        assert isinstance(chosen_step, MockMiddleStep) is True
        assert chosen_step._next_step == MockFinalStep

        chosen_step = simple_step_chooser.get_correct_step(MockFinalStep.name, False, ImmutableMultiDict({}))
        assert chosen_step._prev_step == MockMiddleStep
        assert isinstance(chosen_step, MockFinalStep) is True

    def test_if_step_at_ends_then_return_empty_string(self, test_step_chooser):
        chosen_step_at_begin = test_step_chooser.get_correct_step(MockStartStep.name, False, ImmutableMultiDict({}))
        chosen_step_at_end = test_step_chooser.get_correct_step(MockFinalStep.name, False, ImmutableMultiDict({}))
        assert chosen_step_at_begin._prev_step is None
        assert chosen_step_at_end._next_step is None

    def test_if_data_given_then_call_prepare_render_info_with_correct_data(self, test_step_chooser):
        form_data = ImmutableMultiDict({'Title': 'Happiness begins', 'Year': '2019'})
        with patch('app.forms.steps.steuerlotse_step.FormSteuerlotseStep.prepare_render_info') as preparation_mock:
            test_step_chooser.get_correct_step(MockFormWithInputStep.name, should_update_data=True,
                                               form_data=form_data)

        assert preparation_mock.call_args == call({}, form_data, True)

    def test_if_prepare_render_info_returns_render_info_then_set_it_correctly(self, test_step_chooser):
        render_info = RenderInfo(step_title="Lines, Vines and Trying Times",
                                 step_intro="The fourth album",
                                 form=None,
                                 prev_url=None,
                                 next_url=None,
                                 submit_url=None,
                                 overview_url=None)
        with patch('app.forms.steps.steuerlotse_step.FormSteuerlotseStep.prepare_render_info', MagicMock(return_value=render_info)):
            step = test_step_chooser.get_correct_step(MockFormWithInputStep.name, should_update_data=True,
                                               form_data=ImmutableMultiDict({}))

        assert step.render_info == render_info


class TestDeterminePrevStep:
    @pytest.fixture
    def step_chooser_without_preconditions(self):
        testing_steps = [MockStartStep, MockMiddleStep, MockFormWithInputStep, MockFinalStep]
        yield StepChooser(title="Testing StepChooser", steps=testing_steps,
                          endpoint="lotse", overview_step=MockFormWithInputStep)

    @pytest.fixture
    def step_chooser_with_preconditions(self):
        testing_steps = [MockStartStep, MockStepWithPrecondition, MockFormWithInputStep, MockFinalStep]
        yield StepChooser(title="Testing StepChooser", steps=testing_steps,
                          endpoint="lotse", overview_step=MockFormWithInputStep)

    def test_if_previous_step_has_no_precondition_then_return_direct_predecessor(self, step_chooser_without_preconditions):
        expected_prev_step = MockMiddleStep
        actual_prev_step = step_chooser_without_preconditions.determine_prev_step(MockFormWithInputStep.name, {})
        assert actual_prev_step == expected_prev_step

    def test_if_previous_step_has_no_precondition_then_request_only_direct_predecessor(self, step_chooser_without_preconditions):
        with patch('tests.forms.mock_steuerlotse_steps.MockStartStep.check_precondition') as start_step_check, \
             patch('tests.forms.mock_steuerlotse_steps.MockMiddleStep.check_precondition') as middle_step_check, \
             patch('tests.forms.mock_steuerlotse_steps.MockFormWithInputStep.check_precondition') as input_step_check, \
             patch('tests.forms.mock_steuerlotse_steps.MockFinalStep.check_precondition') as final_step_check:
            step_chooser_without_preconditions.determine_prev_step(MockFormWithInputStep.name, {})
            start_step_check.assert_not_called()
            middle_step_check.assert_called_once()
            input_step_check.assert_not_called()
            final_step_check.assert_not_called()

    def test_if_previous_step_meets_precondition_then_return_direct_predecessor(self, step_chooser_with_preconditions):
        expected_prev_step = MockStepWithPrecondition
        actual_prev_step = step_chooser_with_preconditions.determine_prev_step(MockFormWithInputStep.name,
                                                                               {'precondition_met': True})
        assert actual_prev_step == expected_prev_step

    def test_if_previous_step_have_but_does_not_meet_precondition_then_return_step_before(self, step_chooser_with_preconditions):
        expected_prev_step = MockStartStep
        actual_prev_step = step_chooser_with_preconditions.determine_prev_step(MockFormWithInputStep.name,
                                                                               {'precondition_met': False})
        assert actual_prev_step == expected_prev_step

    def test_if_previous_step_has_but_does_not_meet_precondition_then_request_direct_predecessors(self, step_chooser_with_preconditions):
        with patch('tests.forms.mock_steuerlotse_steps.MockStartStep.check_precondition') as start_step_check, \
                patch('tests.forms.mock_steuerlotse_steps.MockStepWithPrecondition.check_precondition',
                      MagicMock(return_value=False)) as precondition_step_check, \
                patch(
                    'tests.forms.mock_steuerlotse_steps.MockFormWithInputStep.check_precondition') as input_step_check, \
                patch('tests.forms.mock_steuerlotse_steps.MockFinalStep.check_precondition') as final_step_check:
            step_chooser_with_preconditions.determine_prev_step(MockFormWithInputStep.name, {'precondition_met': False})
            start_step_check.assert_called_once()
            precondition_step_check.assert_called_once()
            input_step_check.assert_not_called()
            final_step_check.assert_not_called()

    def test_if_no_step_is_valid_prev_step_then_return_none(self, step_chooser_without_preconditions):
        returned_prev_step = step_chooser_without_preconditions.determine_prev_step(MockStartStep.name, {})
        assert returned_prev_step is None


class TestDetermineNextStep:
    @pytest.fixture
    def step_chooser_without_preconditions(self):
        testing_steps = [MockStartStep, MockFormWithInputStep, MockMiddleStep, MockFinalStep]
        yield StepChooser(title="Testing StepChooser", steps=testing_steps,
                          endpoint="lotse", overview_step=MockFormWithInputStep)

    @pytest.fixture
    def step_chooser_with_preconditions(self):
        testing_steps = [MockStartStep, MockFormWithInputStep, MockStepWithPrecondition, MockFinalStep]
        yield StepChooser(title="Testing StepChooser", steps=testing_steps,
                          endpoint="lotse", overview_step=MockFormWithInputStep)

    def test_if_next_step_has_no_precondition_then_return_direct_successor(self, step_chooser_without_preconditions):
        expected_next_step = MockMiddleStep
        actual_next_step = step_chooser_without_preconditions.determine_next_step(MockFormWithInputStep.name, {})
        assert actual_next_step == expected_next_step

    def test_if_next_step_has_no_precondition_then_request_only_direct_successor(self, step_chooser_without_preconditions):
        with patch('tests.forms.mock_steuerlotse_steps.MockStartStep.check_precondition') as start_step_check, \
             patch('tests.forms.mock_steuerlotse_steps.MockFormWithInputStep.check_precondition') as input_step_check, \
             patch('tests.forms.mock_steuerlotse_steps.MockMiddleStep.check_precondition') as middle_step_check, \
             patch('tests.forms.mock_steuerlotse_steps.MockFinalStep.check_precondition') as final_step_check:
            step_chooser_without_preconditions.determine_next_step(MockFormWithInputStep.name, {})
            start_step_check.assert_not_called()
            input_step_check.assert_not_called()
            middle_step_check.assert_called_once()
            final_step_check.assert_not_called()

    def test_if_next_step_meets_precondition_then_return_direct_successor(self, step_chooser_with_preconditions):
        expected_next_step = MockStepWithPrecondition
        actual_next_step = step_chooser_with_preconditions.determine_next_step(MockFormWithInputStep.name,
                                                                               {'precondition_met': True})
        assert actual_next_step == expected_next_step

    def test_if_next_step_has_but_does_not_meet_precondition_then_return_step_after(self, step_chooser_with_preconditions):
        expected_next_step = MockFinalStep
        actual_next_step = step_chooser_with_preconditions.determine_next_step(MockFormWithInputStep.name,
                                                                               {'precondition_met': False})
        assert actual_next_step == expected_next_step

    def test_if_next_step_has_but_does_not_meet_precondition_then_request_direct_successors(self, step_chooser_with_preconditions):
        with patch('tests.forms.mock_steuerlotse_steps.MockStartStep.check_precondition') as start_step_check, \
                patch(
                    'tests.forms.mock_steuerlotse_steps.MockFormWithInputStep.check_precondition') as input_step_check, \
                patch('tests.forms.mock_steuerlotse_steps.MockStepWithPrecondition.check_precondition',
                      MagicMock(return_value=False)) as precondition_step_check, \
                patch('tests.forms.mock_steuerlotse_steps.MockFinalStep.check_precondition') as final_step_check:
            step_chooser_with_preconditions.determine_next_step(MockFormWithInputStep.name, {'precondition_met': False})
            start_step_check.assert_not_called()
            input_step_check.assert_not_called()
            precondition_step_check.assert_called_once()
            final_step_check.assert_called_once()

    def test_if_no_step_is_valid_next_step_then_return_none(self, step_chooser_without_preconditions):
        returned_next_step = step_chooser_without_preconditions.determine_next_step(MockFinalStep.name, {})
        assert returned_next_step is None


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
        self.run_handle(self.app, step_chooser, MockFormStep.name, method='GET', session=session)
        self.assertTrue(set(original_data).issubset(get_session_data(session_data_identifier)))

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
        self.assertTrue(set(original_data).issubset(get_session_data(session_data_identifier)))

    @staticmethod
    def run_handle(app: Flask, step_chooser: StepChooser, step_name, method='GET', form_data=None, session=None):
        with app.test_request_context(method=method) as req:
            if not form_data:
                form_data = {}
            req.request.form = ImmutableMultiDict(form_data)
            if session is not None:
                req.session = session

            step_chooser.get_correct_step(step_name, method == 'POST', req.request.form).handle()

            return req.session
