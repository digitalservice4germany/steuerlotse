import datetime
import unittest
from decimal import Decimal
from unittest.mock import patch, MagicMock

import pytest
from flask import json
from flask.sessions import SecureCookieSession
from werkzeug.datastructures import ImmutableMultiDict
from werkzeug.exceptions import NotFound
from werkzeug.routing import BuildError
from werkzeug.utils import redirect

from app.forms.flows.multistep_flow import MultiStepFlow, RenderInfo
from app.forms.session_data import serialize_session_data, deserialize_session_data, override_session_data

from tests.forms.mock_steps import MockStartStep, MockMiddleStep, MockFinalStep, MockFormStep, MockForm, \
    MockRenderStep, MockFormWithInputStep, MockYesNoStep
from tests.utils import create_session_form_data


class TestMultiStepFlowInit(unittest.TestCase):
    @pytest.fixture(autouse=True)
    def attach_fixtures(self, test_request_context):
        self.req = test_request_context

    def setUp(self):
        self.testing_steps = [MockStartStep, MockMiddleStep, MockFinalStep]
        self.endpoint_correct = "lotse"
        self.set_link_overview = "True"

    def test_if_request_has_params_then_set_attributes_correctly(self):
        # Only current link_overview is set from request
        self.req.request.args = {'link_overview': self.set_link_overview}

        multi_step_flow = MultiStepFlow(title="Testing MultiStepFlow", steps=self.testing_steps,
                                        endpoint=self.endpoint_correct)

        self.assertTrue(multi_step_flow.has_link_overview)
        self.assertEqual(self.testing_steps[0], multi_step_flow.first_step)
        self.assertEqual(None, multi_step_flow.overview_step)

    def test_if_request_has_no_params_then_set_correct_defaults(self):
        # Only link_overview and session are set from request
        multi_step_flow = MultiStepFlow(title="Testing MultiStepFlow", steps=self.testing_steps,
                                        endpoint=self.endpoint_correct)

        self.assertFalse(multi_step_flow.has_link_overview)
        self.assertEqual(self.testing_steps[0], multi_step_flow.first_step)
        self.assertEqual(None, multi_step_flow.overview_step)


class TestMultiStepFlowHandle(unittest.TestCase):
    @pytest.fixture(autouse=True)
    def attach_fixtures(self, app, test_request_context):
        self.app = app
        self.req = test_request_context

    def setUp(self):
        testing_steps = [MockStartStep, MockRenderStep, MockFormStep, MockFinalStep]
        self.endpoint_correct = "lotse"
        self.flow = MultiStepFlow(title="Testing MultiStepFlow", steps=testing_steps,
                                    endpoint=self.endpoint_correct)
        self.stored_data = self.flow.default_data()

        # Set sessions up
        self.session_data = {"name": "Peach", "sister": "Daisy", "husband": "Mario"}

    def test_if_correct_step_name_then_return_code_correct(self):
        response = self.flow.handle(MockRenderStep.name)

        self.assertEqual(200, response.status_code)

    def test_if_incorrect_step_name_then_raise_404_exception(self):
        self.assertRaises(NotFound, self.flow.handle, "Incorrect Step Name")

    def test_if_start_step_then_return_redirect_to_first_step(self):
        response = self.flow.handle("start")

        self.assertEqual(
            redirect(
                "/" + self.endpoint_correct + "/step/" + MockStartStep.name
                + "?link_overview=" + str(self.flow.has_link_overview)).location,
            response.location
        )

    def test_if_form_step_correct_and_post_then_return_redirect_to_next_step(self):
        with self.app.test_request_context(
                path="/" + self.endpoint_correct + "/step/" + MockFormStep.name,
                method='POST') as req:
            req.session = SecureCookieSession({'form_data': create_session_form_data(self.session_data)})
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
            # Check response data because that's where our Mock returns. Decode because response stores as bytestring
            self.assertEqual(self.session_data, json.loads(str(response.get_data(), 'utf-8'))[0])

    def test_if_form_step_after_render_step_then_keep_data_from_older_form_step(self):
        testing_steps = [MockStartStep, MockFormWithInputStep, MockRenderStep, MockFormStep, MockFinalStep]
        endpoint_correct = "lotse"
        original_data = {'pet': 'Yoshi', 'date': ['9', '7', '1981'], 'decimal': '60.000'}

        with self.app.test_request_context():
            flow = MultiStepFlow(title="Testing MultiStepFlow", steps=testing_steps, endpoint=endpoint_correct)

        session = self.run_handle(self.app, flow, MockFormWithInputStep.name, method='POST', form_data=original_data)
        session = self.run_handle(self.app, flow, MockRenderStep.name, method='GET', session=session)
        session = self.run_handle(self.app, flow, MockFormStep.name, method='GET', session=session)
        self.assertTrue(set(original_data).issubset(
            set(deserialize_session_data(session['form_data'], self.app.config['PERMANENT_SESSION_LIFETIME']))))

    def test_update_session_data_is_called(self):
        expected_data = {'brother: Luigi'}
        with patch('app.forms.flows.multistep_flow.override_session_data') as update_fun, \
                patch('app.forms.flows.multistep_flow.MultiStepFlow._handle_specifics_for_step',
                    MagicMock(return_value=(
                            RenderInfo(step_title="Any", step_intro="Introduction", form=MockForm, prev_url="Prev",
                                        next_url="Next", submit_url="Submit", overview_url="Overview"), expected_data))):
            self.flow.handle(MockRenderStep.name)

            update_fun.assert_called_once_with(expected_data)

    def test_yes_no_field_content_overriden_if_empty(self):
        steps = [MockYesNoStep, MockFinalStep]
        flow_with_yes_no_field = MultiStepFlow('No_maybe', endpoint=self.endpoint_correct, steps=steps)
        resulting_session = self.run_handle(self.app, flow_with_yes_no_field, MockYesNoStep.name, 'POST', {'yes_no_field': 'yes'})
        resulting_session = self.run_handle(self.app, flow_with_yes_no_field, MockYesNoStep.name, 'POST', {}, resulting_session)
        self.assertEqual({'yes_no_field': None}, deserialize_session_data(resulting_session['form_data'],
                                                                        self.app.config['PERMANENT_SESSION_LIFETIME']))

    @staticmethod
    def run_handle(app, flow, step_name, method='GET', form_data=None, session=None):
        with app.test_request_context(method=method) as req:
            if not form_data:
                form_data = {}
            req.request.form = ImmutableMultiDict(form_data)
            if session is not None:
                req.session = session

            flow.handle(step_name)

            return req.session


class TestMultiStepFlowURLForStep(unittest.TestCase):
    @pytest.fixture(autouse=True)
    def attach_fixtures(self, test_request_context):
        self.req = test_request_context

    @staticmethod
    def helper_build_test_url(endpoint, step):
        return "/" + endpoint + "/step/" + step.name

    def setUp(self):
        testing_steps = [MockStartStep, MockMiddleStep, MockFinalStep]

        self.endpoint_correct = "lotse"
        self.endpoint_incorrect = "IT_IS_A_TRAP"
        self.correct_session = "C3PO"
        self.incorrect_session = "r2D2"
        self.set_link_overview = True

        self.multi_step_flow = MultiStepFlow(title="Testing MultiStepFlow", steps=testing_steps,
                                                endpoint=self.endpoint_correct)
        self.multi_step_flow.has_link_overview = True

        self.multi_step_flow_empty_attributes = MultiStepFlow(title="Testing MultiStepFlow", steps=testing_steps,
                                                                endpoint=self.endpoint_correct)
        self.multi_step_flow_empty_attributes.has_link_overview = None

        self.incorrect_endpoint_multi_step_flow = MultiStepFlow(title="Testing MultiStepFlow", steps=testing_steps,
                                                                endpoint=self.endpoint_incorrect)

        self.expected_url_params_if_attribute_set = "?link_overview=" + \
                                                    str(self.set_link_overview)
        self.empty_url_params = ""

    def test_if_step_given_and_attributes_correct_then_return_correct_url(self):
        created_url = self.multi_step_flow.url_for_step(MockStartStep.name)
        expected_url = self.helper_build_test_url(
            self.endpoint_correct, MockStartStep) + \
            self.expected_url_params_if_attribute_set
        self.assertEqual(expected_url, created_url)

        created_url = self.multi_step_flow.url_for_step(MockMiddleStep.name)
        expected_url = self.helper_build_test_url(
            self.endpoint_correct, MockMiddleStep) + \
            self.expected_url_params_if_attribute_set
        self.assertEqual(expected_url, created_url)

        created_url = self.multi_step_flow.url_for_step(MockFinalStep.name)
        expected_url = self.helper_build_test_url(
            self.endpoint_correct, MockFinalStep) + \
            self.expected_url_params_if_attribute_set
        self.assertEqual(expected_url, created_url)

    def test_if_attributes_empty_then_correct_url(self):
        created_url = self.multi_step_flow_empty_attributes.url_for_step(MockStartStep.name)
        expected_url = self.helper_build_test_url(self.endpoint_correct, MockStartStep) + self.empty_url_params
        self.assertEqual(expected_url, created_url)

    def test_if_attributes_correct_then_correct_url(self):
        created_url = self.multi_step_flow.url_for_step(MockStartStep.name)
        expected_url = self.helper_build_test_url(self.endpoint_correct,
                                                    MockStartStep) + self.expected_url_params_if_attribute_set
        self.assertEqual(expected_url, created_url)

    def test_if_linkOverview_param_set_then_used_in_url(self):
        self.multi_step_flow.has_link_overview = False
        created_url = self.multi_step_flow_empty_attributes.url_for_step(MockStartStep.name, _has_link_overview=True)
        expected_url = self.helper_build_test_url(self.endpoint_correct, MockStartStep) + "?link_overview=True"
        self.assertEqual(expected_url, created_url)

    def test_if_incorrect_endpoint_then_throw_error(self):
        self.assertRaises(BuildError, self.incorrect_endpoint_multi_step_flow.url_for_step, MockStartStep.name)

    def test_if_additional_attr_provided_then_append_to_url(self):
        created_url = self.multi_step_flow.url_for_step(MockStartStep.name,
                                                        additional_attr1="did_not_expect",
                                                        additional_attr2="to_see_you_here")
        expected_url = self.helper_build_test_url(self.endpoint_correct,
                                                    MockStartStep) + self.expected_url_params_if_attribute_set + \
                                                    "&additional_attr1=did_not_expect" \
                                                    "&additional_attr2=to_see_you_here"
        self.assertEqual(expected_url, created_url)


class TestMultiStepFlowLoadStep(unittest.TestCase):
    @pytest.fixture(autouse=True)
    def attach_fixtures(self, test_request_context):
        self.req = test_request_context

    def setUp(self):
        testing_steps = [MockStartStep, MockMiddleStep, MockFinalStep]
        self.endpoint_correct = "lotse"
        self.flow = MultiStepFlow(title="Testing MultiStepFlow", steps=testing_steps,
                                    endpoint=self.endpoint_correct)
        self.stored_data = self.flow.default_data()

    def test_if_correct_step_name_then_create_correct_step(self):
        returned_step = self.flow._load_step(MockMiddleStep.name)

        self.assertIsInstance(returned_step, MockMiddleStep)
        self.assertEqual(MockStartStep, returned_step.prev_step())
        self.assertEqual(MockFinalStep, returned_step.next_step())

    def test_if_incorrect_step_name_then_raise_value_error(self):
        self.assertRaises(ValueError, self.flow._load_step, "Incorrect Step Name")


class TestMultiStepFlowGetSessionData(unittest.TestCase):
    @pytest.fixture(autouse=True)
    def attach_fixtures(self, app, test_request_context):
        self.app = app
        self.req = test_request_context

    def setUp(self):
        testing_steps = [MockStartStep, MockMiddleStep, MockFinalStep]
        self.endpoint_correct = "lotse"
        self.flow = MultiStepFlow(title="Testing MultiStepFlow", steps=testing_steps,
                                    endpoint=self.endpoint_correct)
        self.stored_data = self.flow.default_data()

        # Set sessions up
        self.session_data = {"name": "Peach", "sister": "Daisy", "husband": "Mario"}

    def test_if_session_data_then_return_session_data(self):
        self.req.session = SecureCookieSession({'form_data': create_session_form_data(self.session_data)})
        session_data = self.flow._get_session_data()

        self.assertEqual(self.session_data, session_data)

    def test_if_session_data_and_default_data_different_then_update_session_data(self):
        default_data = {"brother": "Luigi"}
        expected_data = {**self.session_data, **default_data}
        with patch("app.forms.flows.multistep_flow.MultiStepFlow.default_data", MagicMock(return_value=(None, default_data))):
            self.req.session = SecureCookieSession({'form_data': create_session_form_data(self.session_data)})

            session_data = self.flow._get_session_data()

            self.assertEqual(expected_data, session_data)

    def test_if_no_form_data_in_session_then_return_default_data(self):
        self.req.session = SecureCookieSession({})
        session_data = self.flow._get_session_data()

        self.assertEqual({}, session_data)  # multistep flow has no default data

    def test_if_no_session_data_and_debug_data_provided_then_return_copy(self):
        original_default_data = {}
        with patch("app.forms.flows.multistep_flow.MultiStepFlow.default_data", MagicMock(return_value=(MockFormStep, original_default_data))):
            session_data = self.flow._get_session_data()

            self.assertIsNot(original_default_data, session_data)

    def test_if_no_session_data_and_no_debug_data_then_return_empty_dict(self):
        with patch("app.forms.flows.multistep_flow.MultiStepFlow.default_data", MagicMock(return_value=None)):
            session_data = self.flow._get_session_data()

            self.assertEqual({}, session_data)

    def test_if_session_data_then_keep_data_in_session(self):
        self.req.session = SecureCookieSession({'form_data': serialize_session_data(self.session_data)})
        self.flow._get_session_data()

        self.assertIn('form_data', self.req.session)
        self.assertEqual(self.session_data, deserialize_session_data(self.req.session['form_data'], self.app.config['PERMANENT_SESSION_LIFETIME']))


class TestMultiStepFlowHandleSpecificsForStep(unittest.TestCase):
    @pytest.fixture(autouse=True)
    def attach_fixtures(self, app, test_request_context):
        self.app = app
        self.req = test_request_context

    def setUp(self):
        testing_steps = [MockStartStep, MockMiddleStep, MockFormStep, MockFinalStep]
        self.endpoint_correct = "lotse"
        self.flow = MultiStepFlow(title="Testing MultiStepFlow", steps=testing_steps,
                                    endpoint=self.endpoint_correct)
        self.stored_data = self.flow.default_data()

        input_steps = [MockStartStep, MockFormWithInputStep, MockFinalStep]
        self.flow_with_input = MultiStepFlow(title="Testing MultiStepFlow with Input", steps=input_steps,
                                                endpoint=self.endpoint_correct)

        # Set sessions up
        self.existing_session = "sessionAvailable"
        self.session_data = {"name": "Peach", "sister": "Daisy", "husband": "Mario"}

        prev_step, self.middle_step, next_step = self.flow._generate_steps(MockMiddleStep.name)
        self.render_info_middle_step = RenderInfo(step_title=self.middle_step.title,
                                                    step_intro=self.middle_step.intro, form=None,
                                                    prev_url=self.flow.url_for_step(prev_step.name),
                                                    next_url=self.flow.url_for_step(next_step.name),
                                                    submit_url=self.flow.url_for_step(self.middle_step.name),
                                                    overview_url="Overview URL")

        prev_step, self.form_step, next_step = self.flow._generate_steps(MockFormStep.name)
        self.render_info_form_step = RenderInfo(step_title=self.form_step.title, step_intro=self.form_step.intro,
                                                form=None, prev_url=self.flow.url_for_step(prev_step.name),
                                                next_url=self.flow.url_for_step(next_step.name),
                                                submit_url=self.flow.url_for_step(self.form_step.name),
                                                overview_url="Overview URL")

        prev_step, self.form_step_input, next_step = self.flow_with_input._generate_steps(
            MockFormWithInputStep.name)
        self.render_info_form_step_with_input = RenderInfo(step_title=self.form_step_input.title,
                                                            step_intro=self.form_step_input.intro, form=None,
                                                            prev_url=self.flow_with_input.url_for_step(
                                                                prev_step.name),
                                                            next_url=self.flow_with_input.url_for_step(
                                                                next_step.name),
                                                            submit_url=self.flow_with_input.url_for_step(
                                                                self.form_step_input.name),
                                                            overview_url="Overview URL")

    def test_if_step_not_form_step_then_return_render_info(self):
        returned_data, _ = self.flow._handle_specifics_for_step(
            self.middle_step, self.render_info_middle_step, self.session_data)

        self.assertEqual(self.render_info_middle_step, returned_data)

    def test_if_step_is_form_step_then_return_render_info_and_correct_form(self):
        returned_data, _ = self.flow._handle_specifics_for_step(
            self.form_step, self.render_info_form_step, self.session_data)

        self.assertIsInstance(returned_data.form, MockForm)
        self.render_info_form_step.form = returned_data.form
        self.assertEqual(self.render_info_form_step, returned_data)

    def test_if_step_is_form_step_and_form_data_then_return_updated_stored_data(self):
        original_data = {"name": "Peach"}
        with self.app.test_request_context(method='POST') as req:
            req.request.form = ImmutableMultiDict({'pet': 'Yoshi', 'date': ['9', '7', '1981'], 'decimal': '60.000'})
            returned_data, updated_data = self.flow._handle_specifics_for_step(
                self.form_step_input, self.render_info_form_step_with_input, original_data)

            self.assertEqual({"name": "Peach", 'date': datetime.date(1981, 7, 9), 'decimal': Decimal('60000'),
                              'pet': 'Yoshi'}, updated_data)

    def test_if_step_is_form_step_and_no_form_data_then_keep_old_stored_data(self):
        stored_data = {"name": "Peach", "sister": "Daisy", "husband": "Mario"}
        with self.app.test_request_context(method='POST'):
            returned_data, updated_data = self.flow._handle_specifics_for_step(
                                                self.form_step, self.render_info_form_step, stored_data)

            self.assertEqual(stored_data, updated_data)


class TestMultiStepFlowGenerateSteps(unittest.TestCase):
    @pytest.fixture(autouse=True)
    def attach_fixtures(self, test_request_context):
        self.req = test_request_context

    def setUp(self):
        testing_steps = [MockStartStep, MockMiddleStep, MockFinalStep]

        self.endpoint_correct = "lotse"
        self.flow = MultiStepFlow(title="Testing MultiStepFlow", steps=testing_steps,
                                    endpoint=self.endpoint_correct)
        self.stored_data = self.flow.default_data()

    def test_if_step_in_list_of_steps_return_correct_steps(self):
        prev_step, step, next_step = self.flow._generate_steps(MockStartStep.name)
        self.assertIsInstance(step, MockStartStep)
        self.assertEqual(MockMiddleStep, next_step)

        prev_step, step, next_step = self.flow._generate_steps(MockMiddleStep.name)
        self.assertEqual(MockStartStep, prev_step)
        self.assertIsInstance(step, MockMiddleStep)
        self.assertEqual(MockFinalStep, next_step)

        prev_step, step, next_step = self.flow._generate_steps(MockFinalStep.name)
        self.assertEqual(MockMiddleStep, prev_step)
        self.assertIsInstance(step, MockFinalStep)

    def test_if_step_at_ends_then_return_empty_string(self):
        prev_step, _, _ = self.flow._generate_steps(MockStartStep.name)
        _, _, next_step = self.flow._generate_steps(MockFinalStep.name)
        self.assertEqual('', prev_step)
        self.assertEqual('', next_step)


class TestDeleteDependentData(unittest.TestCase):
    def setUp(self):
        self.example_data = {
            'animal': 'butterfly',
            'animagus': 'stag',
            'another_animal': 'pangolin',
            'yet_another_animal': 'penguin'
        }

    def test_single_matching_prefix_deleted(self):
        expected_data = {
            'another_animal': 'pangolin',
            'yet_another_animal': 'penguin'
        }
        returned_data = MultiStepFlow._delete_dependent_data(['ani'], self.example_data.copy())
        self.assertEqual(expected_data, returned_data)

    def test_single_complete_matching_item_deleted(self):
        expected_data = {
            'animagus': 'stag',
            'another_animal': 'pangolin',
            'yet_another_animal': 'penguin'
        }
        returned_data = MultiStepFlow._delete_dependent_data(['animal'], self.example_data.copy())
        self.assertEqual(expected_data, returned_data)

    def test_multiple_matching_prefix_deleted(self):
        expected_data = {
            'yet_another_animal': 'penguin'
        }
        returned_data = MultiStepFlow._delete_dependent_data(['ani', 'another'], self.example_data.copy())
        self.assertEqual(expected_data, returned_data)

    def test_multiple_complete_matching_items_deleted(self):
        expected_data = {
            'animagus': 'stag',
            'yet_another_animal': 'penguin'
        }
        returned_data = MultiStepFlow._delete_dependent_data(['animal', 'another_animal'], self.example_data.copy())
        self.assertEqual(expected_data, returned_data)

    def test_if_empty_list_then_nothing_is_deleted(self):
        returned_data = MultiStepFlow._delete_dependent_data([], self.example_data.copy())
        self.assertEqual(self.example_data, returned_data)

    def test_non_matching_prefixes_not_deleted(self):
        returned_data = MultiStepFlow._delete_dependent_data(['plant'], self.example_data.copy())
        self.assertEqual(self.example_data, returned_data)
