import unittest

from flask.sessions import SecureCookieSession
from werkzeug.datastructures import ImmutableMultiDict
from werkzeug.exceptions import NotFound

# TODO: replace with app factory / client fixture
from app import app
from app.forms.session_data import serialize_session_data, deserialize_session_data
from app.forms.flows.step_chooser import StepChooser
from app.forms.steps.steuerlotse_step import RedirectSteuerlotseStep
from tests.forms.mock_steuerlotse_steps import MockStartStep, MockMiddleStep, MockFinalStep, MockFormWithInputStep, \
    MockRenderStep, MockFormStep
from tests.utils import create_session_form_data


class TestStepChooserInit(unittest.TestCase):

    def setUp(self):
        self.testing_steps = [MockStartStep, MockMiddleStep, MockFinalStep]
        self.endpoint_correct = "lotse"

    def test_set_attributes_correctly(self):
        with app.app_context() and app.test_request_context():

            step_chooser = StepChooser(title="Testing StepChooser", steps=self.testing_steps,
                                       endpoint=self.endpoint_correct)
            self.assertEqual(self.testing_steps[0], step_chooser.first_step)
            self.assertEqual(self.testing_steps, list(step_chooser.steps.values()))
            self.assertEqual(self.endpoint_correct, step_chooser.endpoint)
            self.assertEqual(None, step_chooser.overview_step)


class TestStepChooserGetCorrectStep(unittest.TestCase):

    def setUp(self) -> None:
        with app.app_context() and app.test_request_context():
            testing_steps = [MockStartStep, MockRenderStep, MockFormStep, MockFinalStep]
            self.endpoint_correct = "lotse"
            self.step_chooser = StepChooser(title="Testing StepChooser", steps=testing_steps,
                                            endpoint=self.endpoint_correct, overview_step=MockFormStep)

    def test_if_correct_step_name_then_return_step_correctly_initialised(self):
        with app.app_context() and app.test_request_context():
            chosen_step = self.step_chooser.get_correct_step(MockRenderStep.name)

            self.assertIsInstance(chosen_step, MockRenderStep)
            self.assertEqual(MockRenderStep.name, chosen_step.name)
            self.assertEqual(self.endpoint_correct, chosen_step.endpoint)
            self.assertEqual(self.step_chooser.overview_step, chosen_step.overview_step)
            self.assertEqual(MockStartStep, chosen_step._prev_step)
            self.assertEqual(MockFormStep, chosen_step._next_step)

    def test_if_incorrect_step_name_then_raise_404_exception(self):
        with app.app_context() and app.test_request_context():
            self.assertRaises(NotFound, self.step_chooser.get_correct_step, "Incorrect Step Name")

    def test_if_start_step_then_return_redirect_to_first_step(self):
        with app.app_context() and app.test_request_context():
            chosen_step = self.step_chooser.get_correct_step("start")

            self.assertIsInstance(chosen_step, RedirectSteuerlotseStep)
            self.assertEqual(chosen_step.redirection_step_name, self.step_chooser.first_step.name)

    def test_if_step_in_list_of_steps_return_correct_steps(self):
        with app.app_context() and app.test_request_context():

            simple_step_chooser = StepChooser(title="Testing StepChooser",
                                              steps=[MockStartStep, MockMiddleStep, MockFinalStep],
                                              endpoint=self.endpoint_correct)

        with app.app_context() and app.test_request_context():
            chosen_step = simple_step_chooser.get_correct_step(MockStartStep.name)
            self.assertIsInstance(chosen_step, MockStartStep)
            self.assertEqual(MockMiddleStep, chosen_step._next_step)

        with app.app_context() and app.test_request_context():
            chosen_step = simple_step_chooser.get_correct_step(MockMiddleStep.name)
            self.assertEqual(MockStartStep, chosen_step._prev_step)
            self.assertIsInstance(chosen_step, MockMiddleStep)
            self.assertEqual(MockFinalStep, chosen_step._next_step)

        with app.app_context() and app.test_request_context():
            chosen_step = simple_step_chooser.get_correct_step(MockFinalStep.name)
            self.assertEqual(MockMiddleStep, chosen_step._prev_step)
            self.assertIsInstance(chosen_step, MockFinalStep)

    def test_if_step_at_ends_then_return_empty_string(self):
        with app.app_context() and app.test_request_context():
            chosen_step_at_begin = self.step_chooser.get_correct_step(MockStartStep.name)
            chosen_step_at_end = self.step_chooser.get_correct_step(MockFinalStep.name)
            self.assertIsNone(chosen_step_at_begin._prev_step)
            self.assertIsNone(chosen_step_at_end._next_step)


class TestInteractionBetweenSteps(unittest.TestCase):

    def test_if_form_step_after_render_step_then_keep_data_from_older_form_step(self):
        testing_steps = [MockStartStep, MockFormWithInputStep, MockRenderStep, MockFormStep, MockFinalStep]
        endpoint_correct = "lotse"
        session_data_identifier = 'form_data'
        original_data = {'pet': 'Yoshi', 'date': ['9', '7', '1981'], 'decimal': '60.000'}

        with app.app_context() and app.test_request_context():
            step_chooser = StepChooser(title="Testing StepChooser", steps=testing_steps, endpoint=endpoint_correct)
            step_chooser.session_data_identifier = session_data_identifier

        session = self.run_handle(step_chooser, MockFormWithInputStep.name, method='POST', form_data=original_data)
        session = self.run_handle(step_chooser, MockRenderStep.name, method='GET', session=session)
        session = self.run_handle(step_chooser, MockFormStep.name, method='GET', session=session)
        self.assertTrue(set(original_data).issubset(
            set(deserialize_session_data(session[session_data_identifier], app.config['PERMANENT_SESSION_LIFETIME']))))

    def test_if_form_step_after_form_step_then_keep_data_from_newer_form_step(self):
        testing_steps = [MockStartStep, MockFormWithInputStep, MockFormWithInputStep, MockRenderStep, MockFormStep, MockFinalStep]
        endpoint_correct = "lotse"
        session_data_identifier = 'form_data'
        original_data = {'pet': 'Yoshi', 'date': ['9', '7', '1981'], 'decimal': '60.000'}
        adapted_data = {'pet': 'Goomba', 'date': ['9', '7', '1981'], 'decimal': '60.000'}

        with app.app_context() and app.test_request_context():
            step_chooser = StepChooser(title="Testing StepChooser", steps=testing_steps, endpoint=endpoint_correct)
            step_chooser.session_data_identifier = session_data_identifier

        session = self.run_handle(step_chooser, MockFormWithInputStep.name, method='POST', form_data=original_data)
        session = self.run_handle(step_chooser, MockFormWithInputStep.name, method='POST', form_data=adapted_data, session=session)
        session = self.run_handle(step_chooser, MockRenderStep.name, method='GET', session=session)
        session = self.run_handle(step_chooser, MockFormStep.name, method='GET', session=session)
        self.assertTrue(set(adapted_data).issubset(
            set(deserialize_session_data(session[session_data_identifier], app.config['PERMANENT_SESSION_LIFETIME']))))

    @staticmethod
    def run_handle(step_chooser: StepChooser, step_name, method='GET', form_data=None, session=None):
        with app.app_context() and app.test_request_context(method=method) as req:
            if not form_data:
                form_data = {}
            req.request.form = ImmutableMultiDict(form_data)
            if session is not None:
                req.session = session

            step_chooser.get_correct_step(step_name).handle()

            return req.session
