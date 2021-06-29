import copy
import unittest
from unittest.mock import patch

from flask import json
from flask.sessions import SecureCookieSession
from flask_babel import lazy_gettext as _l
from werkzeug.routing import BuildError
from werkzeug.utils import redirect
from werkzeug.exceptions import NotFound

from app import app
from app.forms.flows.eligibility_flow import EligibilityMultiStepFlow, IncorrectEligibilityData
from app.forms.flows.eligibility_flow import _validate_eligibility
from app.forms.flows.multistep_flow import RenderInfo
from app.forms.steps.eligibility_steps import EligibilityStepIncomes, EligibilityStepStart, EligibilityStepResult
from tests.forms.mock_steps import MockStartStep, MockMiddleStep, MockFinalStep, MockRenderStep, MockFormStep, \
    MockEligibilityIncomeStep, MockEligibilityResultStep
from tests.utils import create_session_form_data


class TestEligibilityInit(unittest.TestCase):

    def setUp(self):
        self.testing_steps = [MockStartStep, MockMiddleStep, MockFinalStep]
        self.endpoint_correct = "eligibility"
        self.incorrect_session = "r2D2"
        self.set_link_overview = "True"
        self.expected_steps = [
            EligibilityStepStart,
            EligibilityStepIncomes,
            EligibilityStepResult
        ]

    def test_if_request_has_params_then_set_attributes_correctly(self):
        # Only current session and link_overview are set from request
        with app.app_context() and app.test_request_context() as req:
            req.request.args = {'link_overview': self.set_link_overview}

            flow = EligibilityMultiStepFlow(endpoint=self.endpoint_correct)

            self.assertTrue(flow.has_link_overview)
            self.assertEqual(self.expected_steps, list(flow.steps.values()))
            self.assertEqual(self.expected_steps[0], flow.first_step)
            self.assertIsNone(flow.overview_step)

    def test_if_request_has_no_params_then_set_correct_defaults(self):
        # Only current session and link_overview are set from request
        with app.app_context() and app.test_request_context():
            flow = EligibilityMultiStepFlow(endpoint=self.endpoint_correct)

            self.assertFalse(flow.has_link_overview)
            self.assertEqual(self.expected_steps[0], flow.first_step)
            self.assertIsNone(flow.overview_step)


class TestGetEligibilityResult(unittest.TestCase):

    def setUp(self):
        self.invalid_data_without_all_keys = [{'notCorrect': 'I am your father'},
                                              {'pension': 'There is no trying'}]
        self.valid_data_without_all_keys = [{'renten': 'yes'}]
        self.data_valid_all_reasons = [{'renten': 'yes', 'kapitaleink_mit_steuerabzug': 'no',
                                        'kapitaleink_ohne_steuerabzug': 'no', 'kapitaleink_mit_pauschalbetrag': 'no',
                                        'kapitaleink_guenstiger': 'no', 'geringf': 'no', 'erwerbstaetigkeit': 'no',
                                        'unterhalt': 'no', 'ausland': 'no', 'other': 'no',
                                        'verheiratet_zusammenveranlagung': 'no', 'verheiratet_einzelveranlagung': 'no',
                                        'geschieden_zusammenveranlagung': 'no', 'elster_account': 'no'},
                                       {'renten': 'yes', 'kapitaleink_mit_steuerabzug': 'yes',
                                        'kapitaleink_ohne_steuerabzug': 'no', 'kapitaleink_mit_pauschalbetrag': 'yes',
                                        'kapitaleink_guenstiger': 'no', 'geringf': 'yes', 'erwerbstaetigkeit': 'no',
                                        'unterhalt': 'no', 'ausland': 'no', 'other': 'no',
                                        'verheiratet_zusammenveranlagung': 'yes', 'verheiratet_einzelveranlagung': 'no',
                                        'geschieden_zusammenveranlagung': 'no', 'elster_account': 'no'}]

        self.data_invalid_single_reasons = [{'renten': 'no', 'kapitaleink_mit_steuerabzug': 'yes',
                                             'kapitaleink_ohne_steuerabzug': 'no',
                                             'kapitaleink_mit_pauschalbetrag': 'yes',
                                             'kapitaleink_guenstiger': 'no',
                                             'geringf': 'yes', 'erwerbstaetigkeit': 'no', 'unterhalt': 'no',
                                             'ausland': 'no', 'other': 'no',
                                             'verheiratet_zusammenveranlagung': 'yes',
                                             'verheiratet_einzelveranlagung': 'no',
                                             'geschieden_zusammenveranlagung': 'no', 'elster_account': 'no'},
                                            {'renten': 'yes', 'kapitaleink_mit_steuerabzug': 'yes',
                                             'kapitaleink_ohne_steuerabzug': 'yes',
                                             'kapitaleink_mit_pauschalbetrag': 'yes',
                                             'kapitaleink_guenstiger': 'no',
                                             'geringf': 'yes', 'erwerbstaetigkeit': 'no', 'unterhalt': 'no',
                                             'ausland': 'no', 'other': 'no',
                                             'verheiratet_zusammenveranlagung': 'yes',
                                             'verheiratet_einzelveranlagung': 'no',
                                             'geschieden_zusammenveranlagung': 'no', 'elster_account': 'no'},
                                            {'renten': 'yes', 'kapitaleink_mit_steuerabzug': 'yes',
                                             'kapitaleink_ohne_steuerabzug': 'no',
                                             'kapitaleink_mit_pauschalbetrag': 'yes',
                                             'kapitaleink_guenstiger': 'yes',
                                             'geringf': 'yes', 'erwerbstaetigkeit': 'no', 'unterhalt': 'no',
                                             'ausland': 'no', 'other': 'no',
                                             'verheiratet_zusammenveranlagung': 'no',
                                             'verheiratet_einzelveranlagung': 'no',
                                             'geschieden_zusammenveranlagung': 'no', 'elster_account': 'no'},
                                            {'renten': 'yes', 'kapitaleink_mit_steuerabzug': 'yes',
                                             'kapitaleink_ohne_steuerabzug': 'no',
                                             'kapitaleink_mit_pauschalbetrag': 'yes',
                                             'kapitaleink_guenstiger': 'no',
                                             'geringf': 'yes', 'erwerbstaetigkeit': 'yes', 'unterhalt': 'no',
                                             'ausland': 'no', 'other': 'no',
                                             'verheiratet_zusammenveranlagung': 'yes',
                                             'verheiratet_einzelveranlagung': 'no',
                                             'geschieden_zusammenveranlagung': 'no', 'elster_account': 'no'},
                                            {'renten': 'yes', 'kapitaleink_mit_steuerabzug': 'yes',
                                             'kapitaleink_ohne_steuerabzug': 'no',
                                             'kapitaleink_mit_pauschalbetrag': 'yes',
                                             'kapitaleink_guenstiger': 'no',
                                             'geringf': 'yes', 'erwerbstaetigkeit': 'no', 'unterhalt': 'yes',
                                             'ausland': 'no', 'other': 'no',
                                             'verheiratet_zusammenveranlagung': 'yes',
                                             'verheiratet_einzelveranlagung': 'no',
                                             'geschieden_zusammenveranlagung': 'no', 'elster_account': 'no'},
                                            {'renten': 'yes', 'kapitaleink_mit_steuerabzug': 'yes',
                                             'kapitaleink_ohne_steuerabzug': 'no',
                                             'kapitaleink_mit_pauschalbetrag': 'yes',
                                             'kapitaleink_guenstiger': 'no',
                                             'geringf': 'yes', 'erwerbstaetigkeit': 'no', 'unterhalt': 'no',
                                             'ausland': 'yes', 'other': 'no',
                                             'verheiratet_zusammenveranlagung': 'no',
                                             'verheiratet_einzelveranlagung': 'no',
                                             'geschieden_zusammenveranlagung': 'no', 'elster_account': 'no'},
                                            {'renten': 'yes', 'kapitaleink_mit_steuerabzug': 'yes',
                                             'kapitaleink_ohne_steuerabzug': 'no',
                                             'kapitaleink_mit_pauschalbetrag': 'yes',
                                             'kapitaleink_guenstiger': 'no',
                                             'geringf': 'yes', 'erwerbstaetigkeit': 'no', 'unterhalt': 'no',
                                             'ausland': 'no', 'other': 'yes',
                                             'verheiratet_zusammenveranlagung': 'yes',
                                             'verheiratet_einzelveranlagung': 'no',
                                             'geschieden_zusammenveranlagung': 'no', 'elster_account': 'no'},
                                            {'renten': 'yes', 'kapitaleink_mit_steuerabzug': 'yes',
                                             'kapitaleink_ohne_steuerabzug': 'no',
                                             'kapitaleink_mit_pauschalbetrag': 'yes',
                                             'kapitaleink_guenstiger': 'no',
                                             'geringf': 'yes', 'erwerbstaetigkeit': 'no', 'unterhalt': 'no',
                                             'ausland': 'no', 'other': 'no',
                                             'verheiratet_zusammenveranlagung': 'no',
                                             'verheiratet_einzelveranlagung': 'yes',
                                             'geschieden_zusammenveranlagung': 'no', 'elster_account': 'no'},
                                            {'renten': 'yes', 'kapitaleink_mit_steuerabzug': 'yes',
                                             'kapitaleink_ohne_steuerabzug': 'no',
                                             'kapitaleink_mit_pauschalbetrag': 'yes',
                                             'kapitaleink_guenstiger': 'no',
                                             'geringf': 'yes', 'erwerbstaetigkeit': 'no', 'unterhalt': 'no',
                                             'ausland': 'no', 'other': 'no',
                                             'verheiratet_zusammenveranlagung': 'no',
                                             'verheiratet_einzelveranlagung': 'no',
                                             'geschieden_zusammenveranlagung': 'yes', 'elster_account': 'no'},
                                            {'renten': 'yes', 'kapitaleink_mit_steuerabzug': 'yes',
                                             'kapitaleink_ohne_steuerabzug': 'no',
                                             'kapitaleink_mit_pauschalbetrag': 'yes',
                                             'kapitaleink_guenstiger': 'no',
                                             'geringf': 'yes', 'erwerbstaetigkeit': 'no', 'unterhalt': 'no',
                                             'ausland': 'no', 'other': 'no',
                                             'verheiratet_zusammenveranlagung': 'no',
                                             'verheiratet_einzelveranlagung': 'no',
                                             'geschieden_zusammenveranlagung': 'no', 'elster_account': 'yes'}
                                            ]

        self.other_yes_reason = ['form.eligibility.error-other-income']
        self.single_reasons = [['form.eligibility.error-incorrect-renten'],
                               ['form.eligibility.error-incorrect-kapitaleink_ohne_steuerabzug'],
                               ['form.eligibility.error-incorrect-gunstiger'],
                               ['form.eligibility.error-incorrect-erwerbstaetigkeit'],
                               ['form.eligibility.error-incorrect-unterhalt'],
                               ['form.eligibility.error-incorrect-ausland'],
                               ['form.eligibility.error-incorrect-other'],
                               ['form.eligibility.error-incorrect-verheiratet_einzelveranlagung'],
                               ['form.eligibility.error-incorrect-geschieden_zusammenveranlagung'],
                               ['form.eligibility.error-incorrect-elster-account']]

        self.endpoint_correct = "eligibility"
        with app.app_context() and app.test_request_context():
            self.flow = EligibilityMultiStepFlow(endpoint=self.endpoint_correct)

    def test_if_all_keys_in_data_and_all_valid_then_return_empty_list(self):
        for valid_reasons in self.data_valid_all_reasons:
            result = _validate_eligibility(valid_reasons)
            self.assertEqual([], result)

    def test_if_keys_in_data_missing_and_all_given_values_valid_then_raise_error(self):
        for missing_key_data in self.valid_data_without_all_keys:
            self.assertRaises(IncorrectEligibilityData, _validate_eligibility, missing_key_data)

    def test_if_all_keys_in_data_but_invalid_then_return_error_reasons(self):
        for invalid_reasons in self.data_invalid_single_reasons:
            result = _validate_eligibility(invalid_reasons)
            self.assertTrue(len(result) > 0)

    def test_if_keys_in_data_missing_and_some_given_values_invalid_then_error_reasons(self):
        for missing_key_data in self.invalid_data_without_all_keys:
            self.assertRaises(IncorrectEligibilityData, _validate_eligibility, missing_key_data)

    def test_if_keys_in_data_then_return_correct_reasons(self):
        with patch("flask_babel._") as _:
            _.side_effect = lambda arg: arg

            for index, valid_reasons in enumerate(self.data_valid_all_reasons):
                result = _validate_eligibility(valid_reasons)
                self.assertEqual([], result)

            for index, data in enumerate(self.data_invalid_single_reasons):
                result = _validate_eligibility(data)
                self.assertEqual(self.single_reasons[index], result)


class TestEligibilityHandle(unittest.TestCase):

    def setUp(self):
        with app.app_context() and app.test_request_context():
            testing_steps = [MockStartStep, MockRenderStep, MockFormStep, MockFinalStep]
            testing_steps = {s.name: s for s in testing_steps}
            self.endpoint_correct = "eligibility"
            self.flow = EligibilityMultiStepFlow(endpoint=self.endpoint_correct)
            self.flow.steps = testing_steps
            self.flow.first_step = next(iter(testing_steps.values()))
            self.stored_data = self.flow.default_data()

            # We need to set a different get_flow_nav_function that fits the used mocked steps
            self.flow._get_flow_nav = lambda step: []

            # Set sessions up
            self.existing_session = "sessionAvailable"
            self.session_data = {'renten': 'yes', 'pensionen': 'yes', 'geringf': 'yes',
                                 'kapitaleink': 'yes', 'other': 'no'}

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
        with app.app_context() and app.test_request_context(
                path="/" + self.endpoint_correct + "/step/" + MockRenderStep.name,
                method='GET') as req:
            req.session = SecureCookieSession({'form_data': create_session_form_data(self.session_data)})
            response = self.flow.handle(MockRenderStep.name)

            self.assertEqual(200, response.status_code)
            # Check response data because that's where our Mock returns. Decode because response stores as bytestring
            self.assertEqual(self.session_data, json.loads(str(response.get_data(), 'utf-8'))[0])


class TestEligibilityURLForStep(unittest.TestCase):

    @staticmethod
    def helper_build_test_url(endpoint, step):
        return "/" + endpoint + "/step/" + step.name

    def setUp(self):
        with app.app_context() and app.test_request_context():
            testing_steps = [MockStartStep, MockMiddleStep, MockFinalStep]
            testing_steps = {s.name: s for s in testing_steps}

            self.endpoint_correct = "eligibility"
            self.endpoint_incorrect = "IT_IS_A_TRAP"
            self.correct_session = "C3PO"
            self.incorrect_session = "r2D2"
            self.set_link_overview = True

            self.flow = EligibilityMultiStepFlow(endpoint=self.endpoint_correct)
            self.flow.steps = testing_steps
            self.flow.first_step = next(iter(testing_steps.values()))
            self.flow.has_link_overview = True

            self.flow_empty_attributes = EligibilityMultiStepFlow(endpoint=self.endpoint_correct)
            self.flow_empty_attributes.steps = testing_steps
            self.flow_empty_attributes.first_step = next(iter(testing_steps.values()))
            self.flow_empty_attributes.has_link_overview = None

            self.flow_incorrect_endpoint = EligibilityMultiStepFlow(endpoint=self.endpoint_incorrect)
            self.flow_incorrect_endpoint.steps = testing_steps
            self.flow_incorrect_endpoint.first_step = next(iter(testing_steps.values()))

            self.expected_url_params_if_attribute_set = "?link_overview=" + \
                                                        str(self.set_link_overview)
            self.expected_url_params_if_attributes_empty = "?link_overview=" + \
                                                           str(self.set_link_overview)
            self.empty_url_params = ""

    def test_if_step_given_then_return_correct_url(self):
        with app.app_context() and app.test_request_context():
            created_url = self.flow.url_for_step(MockStartStep.name)
            expected_url = self.helper_build_test_url(
                self.endpoint_correct, MockStartStep) + \
                           self.expected_url_params_if_attribute_set
            self.assertEqual(expected_url, created_url)

            created_url = self.flow.url_for_step(MockMiddleStep.name)
            expected_url = self.helper_build_test_url(
                self.endpoint_correct, MockMiddleStep) + \
                           self.expected_url_params_if_attribute_set
            self.assertEqual(expected_url, created_url)

            created_url = self.flow.url_for_step(MockFinalStep.name)
            expected_url = self.helper_build_test_url(
                self.endpoint_correct, MockFinalStep) + \
                           self.expected_url_params_if_attribute_set
            self.assertEqual(expected_url, created_url)

    def test_if_attributes_empty_then_correct_url(self):
        with app.app_context() and app.test_request_context():
            created_url = self.flow_empty_attributes.url_for_step(MockStartStep.name)
            expected_url = self.helper_build_test_url(self.endpoint_correct, MockStartStep) + self.empty_url_params
            self.assertEqual(expected_url, created_url)

    def test_if_attributes_correct_then_correct_url(self):
        with app.app_context() and app.test_request_context():
            created_url = self.flow.url_for_step(MockStartStep.name)
            expected_url = self.helper_build_test_url(self.endpoint_correct,
                                                      MockStartStep) + self.expected_url_params_if_attribute_set
            self.assertEqual(expected_url, created_url)

    def test_if_attributes_incorrect_then_correct_url(self):
        with app.app_context() and app.test_request_context():
            created_url = self.flow.url_for_step(MockStartStep.name)
            expected_url = self.helper_build_test_url(self.endpoint_correct,
                                                      MockStartStep) + self.expected_url_params_if_attributes_empty
            self.assertEqual(expected_url, created_url)

    def test_if_linkOverview_param_set_then_used_in_url(self):
        with app.app_context() and app.test_request_context():
            self.flow.has_link_overview = False
            created_url = self.flow_empty_attributes.url_for_step(MockStartStep.name, _has_link_overview=True)
            expected_url = self.helper_build_test_url(self.endpoint_correct, MockStartStep) + "?link_overview=True"
            self.assertEqual(expected_url, created_url)

    def test_if_incorrect_endpoint_then_throw_error(self):
        with app.app_context() and app.test_request_context():
            self.assertRaises(BuildError, self.flow_incorrect_endpoint.url_for_step, MockStartStep.name)


class TestEligibilityLoadStep(unittest.TestCase):

    def setUp(self):
        with app.app_context() and app.test_request_context():
            testing_steps = [MockStartStep, MockMiddleStep, MockFinalStep]
            testing_steps = {s.name: s for s in testing_steps}
            self.endpoint_correct = "eligibility"
            self.flow = EligibilityMultiStepFlow(endpoint=self.endpoint_correct)
            self.flow.steps = testing_steps
            self.flow.first_step = next(iter(testing_steps.values()))
            self.stored_data = self.flow.default_data()

    def test_if_correct_step_name_then_create_correct_step(self):
        returned_step = self.flow._load_step(MockMiddleStep.name)

        self.assertIsInstance(returned_step, MockMiddleStep)
        self.assertEqual(MockStartStep, returned_step.prev_step())
        self.assertEqual(MockFinalStep, returned_step.next_step())

    def test_if_incorrect_step_name_then_raise_value_error(self):
        self.assertRaises(ValueError, self.flow._load_step, "Incorrect Step Name")


class TestEligibilityGetSessionData(unittest.TestCase):

    def setUp(self):
        with app.app_context() and app.test_request_context():
            testing_steps = [MockStartStep, MockMiddleStep, MockFinalStep]
            testing_steps = {s.name: s for s in testing_steps}
            self.endpoint_correct = "eligibility"
            self.flow = EligibilityMultiStepFlow(endpoint=self.endpoint_correct)
            self.flow.steps = testing_steps
            self.flow.first_step = next(iter(testing_steps.values()))
            self.stored_data = self.flow.default_data()

            # Set sessions up
            self.session_data = {"name": "Peach", "sister": "Daisy", "husband": "Mario"}

    def test_if_session_valid_then_return_session_data(self):
        with app.app_context() and app.test_request_context() as req:
            req.session = SecureCookieSession({'form_data': create_session_form_data(self.session_data)})
            session_data = self.flow._get_session_data()

            self.assertEqual(self.session_data, session_data)

    def test_if_no_form_data_in_session_then_return_default_data(self):
        with app.app_context() and app.test_request_context() as req:
            req.session = SecureCookieSession({})
            session_data = self.flow._get_session_data()

            self.assertEqual({}, session_data)  # eligibility_flow has no default data


class TestEligibilityHandleSpecificsForStep(unittest.TestCase):

    def setUp(self):
        with app.app_context() and app.test_request_context():
            testing_steps = [MockStartStep, MockEligibilityIncomeStep, MockEligibilityResultStep, MockFinalStep]
            testing_steps = {s.name: s for s in testing_steps}
            self.endpoint_correct = "eligibility"
            self.flow = EligibilityMultiStepFlow(endpoint=self.endpoint_correct)
            self.flow.steps = testing_steps
            self.flow.first_step = next(iter(testing_steps.values()))
            self.stored_data = self.flow.default_data()

            # We need to set a different get_flow_nav_function that fits the used mocked steps
            self.flow._get_flow_nav = lambda step: []

            # Set sessions up
            self.session_data = {"name": "Peach", "sister": "Daisy", "husband": "Mario"}

            self.data_without_all_keys = {'notCorrect': 'I am your father'}
            self.data_not_eligible = {'renten': 'no', 'kapitaleink_mit_steuerabzug': 'yes',
                                      'kapitaleink_ohne_steuerabzug': 'no', 'kapitaleink_mit_pauschalbetrag': 'yes',
                                      'kapitaleink_guenstiger': 'no', 'geringf': 'yes', 'erwerbstaetigkeit': 'yes',
                                      'unterhalt': 'yes', 'ausland': 'no', 'other': 'no',
                                      'verheiratet_zusammenveranlagung': 'yes', 'verheiratet_einzelveranlagung': 'no',
                                      'geschieden_zusammenveranlagung': 'no', 'elster_account': 'no'}
            self.data_eligible = {'renten': 'yes', 'kapitaleink_mit_steuerabzug': 'yes',
                                  'kapitaleink_ohne_steuerabzug': 'no', 'kapitaleink_mit_pauschalbetrag': 'yes',
                                  'kapitaleink_guenstiger': 'no', 'geringf': 'yes', 'erwerbstaetigkeit': 'no',
                                  'unterhalt': 'no', 'ausland': 'no', 'other': 'no',
                                  'verheiratet_zusammenveranlagung': 'yes', 'verheiratet_einzelveranlagung': 'no',
                                  'geschieden_zusammenveranlagung': 'no', 'elster_account': 'no'}

            self.not_eligible_errors = [_l('form.eligibility.error-incorrect-renten'),
                                        _l('form.eligibility.error-incorrect-erwerbstaetigkeit'),
                                        _l('form.eligibility.error-incorrect-unterhalt')]

            self.result_url = '/' + self.endpoint_correct + '/step/' + MockEligibilityResultStep.name + \
                              '?link_overview=' + str(self.flow.has_link_overview)
            self.income_url = '/' + self.endpoint_correct + '/step/' + MockEligibilityIncomeStep.name + \
                              '?link_overview=' + str(self.flow.has_link_overview)

            prev_step, self.result_step, next_step = self.flow._generate_steps(MockEligibilityResultStep.name)
            self.render_info_result_step = RenderInfo(flow_title=self.flow.title, step_title=self.result_step.title,
                                                      step_intro=self.result_step.intro, form=None,
                                                      prev_url=self.flow.url_for_step(prev_step.name),
                                                      next_url=self.flow.url_for_step(next_step.name),
                                                      submit_url=self.flow.url_for_step(self.result_step),
                                                      overview_url="Overview URL",
                                                      flow_nav=self.flow._get_flow_nav(self.result_step))

            prev_step, self.income_step, next_step = self.flow._generate_steps(MockEligibilityIncomeStep.name)
            self.render_info_income_step = RenderInfo(flow_title=self.flow.title, step_title=self.income_step.title,
                                                      step_intro=self.income_step.intro, form=None,
                                                      prev_url=self.flow.url_for_step(prev_step.name),
                                                      next_url=self.flow.url_for_step(next_step.name),
                                                      submit_url=self.flow.url_for_step(self.income_step.name),
                                                      overview_url="Overview URL",
                                                      flow_nav=self.flow._get_flow_nav(self.income_step))

    def test_if_result_step_and_eligible_then_add_no_errors(self):
        with patch("app.forms.flows.eligibility_flow._") as babel:
            babel.side_effect = lambda arg: arg

            with app.app_context() and app.test_request_context():
                render_info, _ = self.flow._handle_specifics_for_step(
                    self.result_step, copy.deepcopy(self.render_info_result_step), self.data_eligible)
                self.assertEqual([], render_info.additional_info['eligibility_errors'])

    def test_if_result_step_and_not_eligible_then_add_correct_errors(self):
        with patch("app.forms.flows.eligibility_flow._") as babel:
            babel.side_effect = lambda arg: arg

            with app.app_context() and app.test_request_context():
                render_info, _ = self.flow._handle_specifics_for_step(
                    self.result_step, copy.deepcopy(self.render_info_result_step), self.data_not_eligible)
                self.assertEqual(self.not_eligible_errors, render_info.additional_info['eligibility_errors'])

    def test_if_income_step_then_set_next_url_correct(self):
        with app.app_context() and app.test_request_context(method='POST'):
            render_info, _ = self.flow._handle_specifics_for_step(
                self.income_step, self.render_info_income_step, self.data_eligible)
            self.assertEqual(self.result_url, render_info.next_url)

    def test_if_income_step_then_set_no_additional_info(self):
        with app.app_context() and app.test_request_context():
            render_info, _ = self.flow._handle_specifics_for_step(
                self.income_step, self.render_info_income_step, self.data_not_eligible)
            self.assertRaises(KeyError, lambda: render_info.additional_info['eligibility_result'])

            render_info, _ = self.flow._handle_specifics_for_step(
                self.income_step, self.render_info_income_step, self.data_eligible)
            self.assertRaises(KeyError, lambda: render_info.additional_info['eligibility_result'])

    def test_if_keys_not_in_data_and_income_step_then_return_422(self):
        with app.app_context() and app.test_request_context(method='GET'):
            self.assertRaises(IncorrectEligibilityData,
                              self.flow._handle_specifics_for_step,
                              self.result_step, self.render_info_income_step, self.data_without_all_keys)


class TestEligibilityGenerateSteps(unittest.TestCase):

    def setUp(self):
        with app.app_context() and app.test_request_context():
            testing_steps = [MockStartStep, MockMiddleStep, MockFinalStep]
            testing_steps = {s.name: s for s in testing_steps}

            self.endpoint_correct = "eligibility"
            self.flow = EligibilityMultiStepFlow(endpoint=self.endpoint_correct)
            self.flow.steps = testing_steps
            self.flow.first_step = next(iter(testing_steps.values()))
            self.stored_data = self.flow.default_data()

    def test_if_step_in_list_of_steps_return_correct_steps(self):
        prev_step, step, next_step = self.flow._generate_steps(MockStartStep.name)
        self.assertEqual('', prev_step)
        self.assertIsInstance(step, MockStartStep)
        self.assertEqual(MockMiddleStep, next_step)

        prev_step, step, next_step = self.flow._generate_steps(MockMiddleStep.name)
        self.assertEqual(MockStartStep, prev_step)
        self.assertIsInstance(step, MockMiddleStep)
        self.assertEqual(MockFinalStep, next_step)

        prev_step, step, next_step = self.flow._generate_steps(MockFinalStep.name)
        self.assertEqual(MockMiddleStep, prev_step)
        self.assertIsInstance(step, MockFinalStep)
        self.assertEqual('', next_step)

    def test_if_step_at_ends_then_return_empty_string(self):
        prev_step, _, _ = self.flow._generate_steps(MockStartStep.name)
        _, _, next_step = self.flow._generate_steps(MockFinalStep.name)
        self.assertEqual('', prev_step)
        self.assertEqual('', next_step)
