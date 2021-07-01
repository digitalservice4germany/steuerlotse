import datetime
import copy
import unittest
from decimal import Decimal
from unittest.mock import patch, MagicMock, call

from flask import json
from flask.sessions import SecureCookieSession
from flask_babel import _, lazy_gettext as _l
from flask_login import login_user
from pydantic.error_wrappers import ErrorWrapper, ValidationError
from pydantic.errors import MissingError
from werkzeug.datastructures import ImmutableMultiDict
from werkzeug.routing import BuildError
from werkzeug.utils import redirect
from wtforms import Field
from wtforms.fields.core import UnboundField, IntegerField, SelectField, RadioField

from app import db, app
from app.crypto.pw_hashing import global_salt_hash
from app.data_access.user_controller import find_user
from app.elster_client.elster_errors import ElsterTransferError, ElsterGlobalValidationError, EricaIsMissingFieldError, \
    ElsterInvalidBufaNumberError
from app.forms.fields import YesNoField, SteuerlotseStringField, SteuerlotseDateField, EntriesField, EuroField
from app.forms.flows.lotse_flow import LotseMultiStepFlow, SPECIAL_RESEND_TEST_IDNRS, show_person_b
from app.forms.flows.multistep_flow import RenderInfo
from app.forms.steps.lotse.confirmation_steps import StepConfirmation, StepSummary, StepFiling, StepAck
from app.forms.steps.lotse.declaration_steps import StepDeclarationIncomes, StepDeclarationEdaten, StepSessionNote
from app.forms.steps.lotse.personal_data_steps import StepFamilienstand, StepSteuernummer, StepPersonA, StepPersonB, \
    StepIban
from app.forms.steps.lotse.steuerminderungen_steps import StepSteuerminderungYesNo, StepVorsorge, StepAussergBela, \
    StepHaushaltsnahe, StepHandwerker, StepGemeinsamerHaushalt, StepReligion, StepSpenden
from app.forms.steps.step import Step, Section
from app.model.form_data import ConfirmationMissingInputValidationError, MandatoryFieldMissingValidationError, \
    InputDataInvalidError, IdNrMismatchInputValidationError, MandatoryFormData
from tests.forms.mock_steps import MockStartStep, MockMiddleStep, MockFinalStep, MockRenderStep, MockFormStep, \
    MockForm, MockFilingStep, MockSummaryStep, MockPersonAStep, MockStrMindYNStep, MockHandwerkerStep, MockIbanStep, \
    MockPersonBStep, MockGemeinsamerHaushaltStep, MockReligionStep, MockFamilienstandStep, MockHaushaltsnaheStep, \
    MockConfirmationStep, MockDeclarationEdatenStep, MockDeclarationIncomesStep
from tests.utils import create_session_form_data, create_and_activate_user


class TestComputeValue(unittest.TestCase):

    def test_if_radio_field_and_choice_set_then_return_correct_label_and_computed_value(self):
        data_label = 'lightsaber color'
        choices = [('pr', 'purple'), ('yl', 'yellow')]
        expected_result = (data_label, 'purple')
        field = UnboundField(
            field_class=RadioField, render_kw={'data_label': data_label}, choices=choices)

        actual_result = LotseMultiStepFlow._generate_value_representation(field, 'pr')

        self.assertEqual(expected_result, actual_result)

    def test_if_select_field_and_choice_set_then_return_correct_label_and_computed_value(self):
        data_label = 'lightsaber color'
        choices = [('pr', 'purple'), ('yl', 'yellow')]
        expected_result = (data_label, 'purple')
        field = UnboundField(
            field_class=SelectField, render_kw={'data_label': data_label}, choices=choices)

        actual_result = LotseMultiStepFlow._generate_value_representation(field, 'pr')

        self.assertEqual(expected_result, actual_result)

    def test_if_yes_no_field_and_choice_set_then_return_correct_label_and_computed_value(self):
        data_label = 'Is this a test?'
        expected_result = (data_label, 'Ja')
        field = UnboundField(
            field_class=YesNoField, render_kw={'data_label': data_label})

        actual_result = LotseMultiStepFlow._generate_value_representation(field, 'yes')

        self.assertEqual(expected_result, actual_result)

    def test_if_string_field_then_return_correct_label_and_input_value(self):
        data_label = 'Mahatma Ghandi'
        quote = 'Relationships are based on four principles: respect, understanding, acceptance and appreciation.'
        expected_result = (data_label, quote)
        field = UnboundField(
            field_class=SteuerlotseStringField, render_kw={'data_label': data_label})

        actual_result = LotseMultiStepFlow._generate_value_representation(field, quote)

        self.assertEqual(expected_result, actual_result)

    def test_if_date_field_then_return_correct_label_and_formatted_date(self):
        data_label = "Mahatma Gandhi's birthday"
        date = datetime.date(1869, 10, 2)
        expected_result = (data_label, date.strftime("%d.%m.%Y"))
        field = UnboundField(
            field_class=SteuerlotseDateField, render_kw={'data_label': data_label})

        actual_result = LotseMultiStepFlow._generate_value_representation(field, date)

        self.assertEqual(expected_result, actual_result)

    def test_if_integer_field_then_return_correct_label_and_input_value(self):
        data_label = "Number of years Gandhi spent in prison"
        expected_result = (data_label, 8)
        field = UnboundField(
            field_class=IntegerField, render_kw={'data_label': data_label})

        actual_result = LotseMultiStepFlow._generate_value_representation(field, 8)

        self.assertEqual(expected_result, actual_result)

    def test_if_entries_field_then_return_correct_label_and_entries_comma_separated(self):
        data_label = "Numbers"
        entries = ["1", "2", "3"]
        expected_result = (data_label, "1, 2, 3")
        field = UnboundField(
            field_class=EntriesField, render_kw={'data_label': data_label})

        actual_result = LotseMultiStepFlow._generate_value_representation(field, entries)

        self.assertEqual(expected_result, actual_result)

    def test_if_euro_field_then_return_correct_label_and_value_with_euro_sign(self):
        data_label = "Exchange rate for one Galleon"
        price = Decimal(5.58)
        expected_result = (data_label, str(price) + " €")
        field = UnboundField(
            field_class=EuroField, render_kw={'data_label': data_label})

        actual_result = LotseMultiStepFlow._generate_value_representation(field, price)

        self.assertEqual(expected_result, actual_result)

    def test_if_no_value_given_then_return_correct_label_and_none(self):
        data_label = 'No answer given'
        potential_none_values = [None, 'none', '', _('form.lotse.no_answer')]
        expected_result = (data_label, None)
        field = UnboundField(
            field_class=SteuerlotseStringField, render_kw={'data_label': data_label})

        for none_value in potential_none_values:
            actual_result = LotseMultiStepFlow._generate_value_representation(field, none_value)
            self.assertEqual(expected_result, actual_result)

    def test_if_unkown_field_class_given_then_raise_value_error(self):
        data_label = "Unknown"
        field = UnboundField(
            field_class=Field, render_kw={'data_label': data_label})

        self.assertRaises(ValueError, LotseMultiStepFlow._generate_value_representation, field, 'value')


class TestLotseInit(unittest.TestCase):

    def setUp(self):
        self.testing_steps = [MockStartStep, MockMiddleStep, MockFinalStep]
        self.endpoint_correct = "lotse"
        self.incorrect_session = "r2D2"
        self.set_link_overview = "True"
        self.expected_steps = [
            StepDeclarationIncomes,
            StepDeclarationEdaten,
            StepSessionNote,

            StepFamilienstand,
            StepSteuernummer,
            StepPersonA,
            StepPersonB,
            StepIban,

            StepSteuerminderungYesNo,
            StepVorsorge,
            StepAussergBela,
            StepHaushaltsnahe,
            StepHandwerker,
            StepGemeinsamerHaushalt,
            StepReligion,
            StepSpenden,

            StepSummary,
            StepConfirmation,
            StepFiling,
            StepAck
        ]

    def test_if_request_has_params_then_set_attributes_correctly(self):
        # Only current session and link_overview are set from request
        with app.app_context() and app.test_request_context() as req:
            req.request.args = {'link_overview': self.set_link_overview}

            flow = LotseMultiStepFlow(endpoint=self.endpoint_correct)

            self.assertTrue(flow.has_link_overview)
            self.assertEqual(self.expected_steps, list(flow.steps.values()))
            self.assertEqual(self.expected_steps[0], flow.first_step)
            self.assertEqual(StepSummary, flow.overview_step)

    def test_if_request_has_no_params_then_set_correct_defaults(self):
        # Only current session and link_overview are set from request
        with app.app_context() and app.test_request_context():
            flow = LotseMultiStepFlow(endpoint=self.endpoint_correct)

            self.assertFalse(flow.has_link_overview)
            self.assertEqual(self.expected_steps[0], flow.first_step)
            self.assertEqual(StepSummary, flow.overview_step)


class TestLotseHandle(unittest.TestCase):

    def setUp(self):
        with app.app_context() and app.test_request_context():
            testing_steps = [MockStartStep, MockRenderStep, MockFormStep, MockFinalStep]
            testing_steps = {s.name: s for s in testing_steps}
            self.endpoint_correct = "lotse"
            self.flow = LotseMultiStepFlow(endpoint=self.endpoint_correct)
            self.flow.steps = testing_steps
            self.flow.first_step = next(iter(testing_steps.values()))

            # We need to set a different get_flow_nav_function that fits the used mocked steps
            self.flow._get_flow_nav = lambda step: []

            # Set sessions up
            self.existing_session = "sessionAvailable"
            self.session_data = {"name": "Peach", "sister": "Daisy", "husband": "Mario"}

    def test_if_correct_step_name_then_return_code_correct(self):
        with app.app_context() and app.test_request_context() as req:
            req.session = SecureCookieSession({'form_data': create_session_form_data(self.session_data)})
            response = self.flow.handle(MockRenderStep.name)

            self.assertEqual(200, response.status_code)

    def test_if_incorrect_step_name_then_raise_exception(self):
        with app.app_context() and app.test_request_context():
            self.assertRaises(Exception, self.flow.handle, "Incorrect Step Name")

    def test_if_start_step_and_debug_ok_then_return_redirect_to_debug_step(self):
        with app.app_context() and app.test_request_context():
            response = self.flow.handle("start")

            self.assertEqual(
                redirect(
                    "/" + self.endpoint_correct + "/step/" + self.flow.default_data()[0].name
                    + "?link_overview=" + str(self.flow.has_link_overview)).location,
                response.location
            )

    def test_if_start_step_and_debug_none_then_return_redirect_to_first_step(self):
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
            self.assertTrue(set(self.session_data).issubset(set(json.loads(str(response.get_data(), 'utf-8'))[0])))


class TestCheckStepNeedsToBeSkipped(unittest.TestCase):
    class MockSkipStep(Step):
        name = "mock_skip_step"

        SKIP_COND = [
            ([('condition_middle', 'met')], MockMiddleStep.name,
             'condition_middle is met'),
            ([('condition_start', 'met')], MockStartStep.name,
             'condition_start is met'),
            ([('condition_none', None), ('haushaltsnahe_summe', None)], MockFinalStep.name,
             'condition_none is met')
        ]

        def __init__(self, **kwargs):
            super().__init__(
                title='The Skip',
                intro='The one where the empire decided to skip striking back',
                **kwargs)

    def setUp(self) -> None:
        testing_steps = {s.name: s for s in [MockStartStep, MockMiddleStep, self.MockSkipStep, MockFinalStep]}
        self.endpoint_correct = "lotse"
        with app.app_context() and app.test_request_context():
            self.flow = LotseMultiStepFlow(endpoint=self.endpoint_correct)
        self.flow.steps = testing_steps

    def test_if_condition_middle_met_then_return_url_for_correct_step_and_flash_message(self):
        expected_step_url = MockMiddleStep.name
        expected_reason = 'condition_middle is met'
        input_data = {'condition_middle': 'met', 'condition_start': 'not_met', 'condition_none': 'not_met'}

        with app.app_context() and app.test_request_context(), \
                patch('app.forms.flows.lotse_flow.flash') as mock_flash:
            actual_step_url = self.flow._check_step_needs_to_be_skipped(self.MockSkipStep.name, input_data)
            mock_flash.assert_called_with(expected_reason, 'warn')
            self.assertEqual(self.flow.url_for_step(expected_step_url), actual_step_url)

    def test_if_condition_start_met_then_return_url_for_correct_step_and_flash_message(self):
        expected_step_url = MockStartStep.name
        expected_reason = 'condition_start is met'
        input_data = {'condition_middle': 'not_met', 'condition_start': 'met', 'condition_none': 'not_met'}

        with app.app_context() and app.test_request_context(), \
                patch('app.forms.flows.lotse_flow.flash') as mock_flash:
            actual_step_url = self.flow._check_step_needs_to_be_skipped(self.MockSkipStep.name, input_data)
            mock_flash.assert_called_with(expected_reason, 'warn')
            self.assertEqual(self.flow.url_for_step(expected_step_url), actual_step_url)

    def test_if_condition_none_met_then_return_url_for_correct_step_and_flash_message(self):
        expected_step_url = MockFinalStep.name
        expected_reason = 'condition_none is met'
        input_data = {'condition_middle': 'not_met', 'condition_start': 'not_met'}

        with app.app_context() and app.test_request_context(), \
                patch('app.forms.flows.lotse_flow.flash') as mock_flash:
            actual_step_url = self.flow._check_step_needs_to_be_skipped(self.MockSkipStep.name, input_data)
            mock_flash.assert_called_with(expected_reason, 'warn')
            self.assertEqual(self.flow.url_for_step(expected_step_url), actual_step_url)

    def test_if_more_than_one_skip_cond_met_then_return_url_for_step_and_flash_message_for_first_cond(self):
        expected_step_url = MockMiddleStep.name
        expected_reason = 'condition_middle is met'
        input_data = {'condition_middle': 'met', 'condition_start': 'met'}

        with app.app_context() and app.test_request_context(), \
                patch('app.forms.flows.lotse_flow.flash') as mock_flash:
            actual_step_url = self.flow._check_step_needs_to_be_skipped(self.MockSkipStep.name, input_data)
            mock_flash.assert_called_with(expected_reason, 'warn')
            self.assertEqual(self.flow.url_for_step(expected_step_url), actual_step_url)

    def test_if_no_condition_met_then_return_none(self):
        input_data = {'condition_middle': 'not_met', 'condition_start': 'not_met', 'condition_none': 'not_met'}

        with app.app_context() and app.test_request_context():
            actual_step_url = self.flow._check_step_needs_to_be_skipped(self.MockSkipStep.name, input_data)

        self.assertIsNone(actual_step_url)


class TestLotseURLForStep(unittest.TestCase):

    @staticmethod
    def helper_build_test_url(endpoint, step):
        return "/" + endpoint + "/step/" + step.name

    def setUp(self):
        with app.app_context() and app.test_request_context():
            testing_steps = [MockStartStep, MockMiddleStep, MockFinalStep]
            testing_steps = {s.name: s for s in testing_steps}

            self.endpoint_correct = "lotse"
            self.endpoint_incorrect = "IT_IS_A_TRAP"
            self.correct_session = "C3PO"
            self.incorrect_session = "r2D2"
            self.set_link_overview = True

            self.flow = LotseMultiStepFlow(endpoint=self.endpoint_correct)
            self.flow.steps = testing_steps
            self.flow.first_step = next(iter(testing_steps.values()))
            self.flow.has_link_overview = True

            self.flow_empty_attributes = LotseMultiStepFlow(endpoint=self.endpoint_correct)
            self.flow_empty_attributes.steps = testing_steps
            self.flow_empty_attributes.first_step = next(iter(testing_steps.values()))
            self.flow_empty_attributes.has_link_overview = None

            self.flow_incorrect_endpoint = LotseMultiStepFlow(endpoint=self.endpoint_incorrect)
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


class TestLotseLoadStep(unittest.TestCase):

    def setUp(self):
        with app.app_context() and app.test_request_context():
            testing_steps = [MockStartStep, MockMiddleStep, MockFinalStep]
            testing_steps = {s.name: s for s in testing_steps}
            self.endpoint_correct = "lotse"
            self.flow = LotseMultiStepFlow(endpoint=self.endpoint_correct)
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


class TestLotseGetNav(unittest.TestCase):

    def setUp(self):
        with app.app_context() and app.test_request_context():
            self.endpoint_correct = "lotse"
            self.flow = LotseMultiStepFlow(endpoint=self.endpoint_correct)
            self.steps_in_list = [
                StepDeclarationIncomes,
                StepSteuernummer,
                StepSteuerminderungYesNo,
                StepSummary
            ]
            self.sub_step_of_SectionEinwilligung = StepDeclarationEdaten
            self.sub_step_of_SectionMeineDaten = StepSteuernummer
            self.sub_step_of_SectionSteuerminderung = StepReligion
            self.sub_step_of_SectionConfirmation = StepFiling

    def test_if_step_in_nav_list_then_set_active_flag_correctly(self):
        first_step_active = self.flow._get_flow_nav(self.steps_in_list[0])
        second_step_active = self.flow._get_flow_nav(self.steps_in_list[1])
        third_step_active = self.flow._get_flow_nav(self.steps_in_list[2])
        fourth_step_active = self.flow._get_flow_nav(self.steps_in_list[3])

        self.assertTrue(first_step_active[0].active)
        self.assertFalse(first_step_active[1].active)
        self.assertFalse(first_step_active[2].active)
        self.assertFalse(first_step_active[3].active)

        self.assertFalse(second_step_active[0].active)
        self.assertTrue(second_step_active[1].active)
        self.assertFalse(second_step_active[2].active)
        self.assertFalse(second_step_active[3].active)

        self.assertFalse(third_step_active[0].active)
        self.assertFalse(third_step_active[1].active)
        self.assertTrue(third_step_active[2].active)
        self.assertFalse(third_step_active[3].active)

        self.assertFalse(fourth_step_active[0].active)
        self.assertFalse(fourth_step_active[1].active)
        self.assertFalse(fourth_step_active[2].active)
        self.assertTrue(fourth_step_active[3].active)

    def test_if_step_substep_of_nav_list_then_set_active_flag_correctly(self):
        first_step_active = self.flow._get_flow_nav(self.sub_step_of_SectionEinwilligung)
        second_step_active = self.flow._get_flow_nav(self.sub_step_of_SectionMeineDaten)
        third_step_active = self.flow._get_flow_nav(self.sub_step_of_SectionSteuerminderung)
        fourth_step_active = self.flow._get_flow_nav(self.sub_step_of_SectionConfirmation)

        self.assertTrue(first_step_active[0].active)
        self.assertFalse(first_step_active[1].active)
        self.assertFalse(first_step_active[2].active)
        self.assertFalse(first_step_active[3].active)

        self.assertFalse(second_step_active[0].active)
        self.assertTrue(second_step_active[1].active)
        self.assertFalse(second_step_active[2].active)
        self.assertFalse(second_step_active[3].active)

        self.assertFalse(third_step_active[0].active)
        self.assertFalse(third_step_active[1].active)
        self.assertTrue(third_step_active[2].active)
        self.assertFalse(third_step_active[3].active)

        self.assertFalse(fourth_step_active[0].active)
        self.assertFalse(fourth_step_active[1].active)
        self.assertFalse(fourth_step_active[2].active)
        self.assertTrue(fourth_step_active[3].active)

    def test_if_step_not_in_nav_list_then_set_all_steps_inactive(self):
        all_inactive = self.flow._get_flow_nav(MockStartStep)

        self.assertFalse(all_inactive[0].active)
        self.assertFalse(all_inactive[1].active)
        self.assertFalse(all_inactive[2].active)
        self.assertFalse(all_inactive[3].active)

    def test_if_step_in_nav_list_then_set_correct_numbering_in_nav_items(self):
        nav_items = self.flow._get_flow_nav(self.steps_in_list[0])

        for index, nav in enumerate(nav_items):
            self.assertEqual(index + 1, nav.number)


class TestLotseGetSessionData(unittest.TestCase):

    def setUp(self):
        with app.app_context() and app.test_request_context():
            testing_steps = [MockStartStep, MockMiddleStep, MockFinalStep]
            testing_steps = {s.name: s for s in testing_steps}
            self.endpoint_correct = "lotse"
            self.flow = LotseMultiStepFlow(endpoint=self.endpoint_correct)
            self.flow.steps = testing_steps
            self.flow.first_step = next(iter(testing_steps.values()))
            self.stored_data = self.flow.default_data()

            # Set sessions up
            self.session_data = {"name": "Peach", "sister": "Daisy", "husband": "Mario"}

    def test_if_session_valid_then_return_updated_session_data(self):
        with app.app_context() and app.test_request_context() as req:
            req.session = SecureCookieSession({'form_data': create_session_form_data(self.session_data)})
            session_data = self.flow._get_session_data()

            self.assertTrue(set(self.session_data).issubset(set(session_data)))

    def test_if_no_form_data_in_session_then_return_default_data(self):
        with app.app_context() and app.test_request_context() as req:
            req.session = SecureCookieSession({})
            session_data = self.flow._get_session_data()

            self.assertEqual(self.flow.default_data()[1], session_data)


class TestLotseHandleSpecificsForStep(unittest.TestCase):

    def setUp(self):
        with app.app_context() and app.test_request_context():
            testing_steps = [MockStartStep, MockDeclarationIncomesStep, MockDeclarationEdatenStep,
                             MockFamilienstandStep, MockPersonAStep, MockPersonBStep, MockIbanStep,
                             MockStrMindYNStep,
                             MockHaushaltsnaheStep, MockHandwerkerStep, MockGemeinsamerHaushaltStep, MockReligionStep,
                             MockSummaryStep, MockConfirmationStep, MockFilingStep, MockMiddleStep, MockFormStep,
                             MockFinalStep]
            testing_steps = {s.name: s for s in testing_steps}
            self.endpoint_correct = "lotse"
            self.flow = LotseMultiStepFlow(endpoint=self.endpoint_correct)
            self.flow.steps = testing_steps
            self.flow.first_step = next(iter(testing_steps.values()))
            self.stored_data = self.flow.default_data()

            # We need to set a different get_flow_nav_function that fits the used mocked steps
            self.flow._get_flow_nav = lambda step: []

            # Set sessions up
            self.existing_session = "sessionAvailable"
            self.session_data = {"name": "Peach", "sister": "Daisy", "husband": "Mario"}

            self.ip_address = '127.0.0.1'
            self.valid_idnr = '02293417683'

            prev_step, self.middle_step, next_step = self.flow._generate_steps(MockMiddleStep.name)
            self.render_info_middle_step = RenderInfo(flow_title=self.flow.title, step_title=self.middle_step.title,
                                                      step_intro=self.middle_step.intro, form=None,
                                                      prev_url=self.flow.url_for_step(prev_step.name),
                                                      next_url=self.flow.url_for_step(next_step.name),
                                                      submit_url=self.flow.url_for_step(self.middle_step.name),
                                                      overview_url="Overview URL",
                                                      flow_nav=self.flow._get_flow_nav(self.middle_step))

            prev_step, self.form_step, next_step = self.flow._generate_steps(MockFormStep.name)
            self.render_info_form_step = RenderInfo(flow_title=self.flow.title, step_title=self.form_step.title,
                                                    step_intro=self.form_step.intro, form=None,
                                                    prev_url=self.flow.url_for_step(prev_step.name),
                                                    next_url=self.flow.url_for_step(next_step.name),
                                                    submit_url=self.flow.url_for_step(self.form_step.name),
                                                    overview_url="Overview URL",
                                                    flow_nav=self.flow._get_flow_nav(self.form_step))

            prev_step, self.confirmation_step, next_step = self.flow._generate_steps(MockConfirmationStep.name)
            self.render_info_confirmation_step = RenderInfo(flow_title=self.flow.title,
                                                            step_title=self.confirmation_step.title,
                                                            step_intro=self.confirmation_step.intro, form=None,
                                                            prev_url=None,
                                                            next_url=self.flow.url_for_step(next_step.name),
                                                            submit_url=self.flow.url_for_step(
                                                                self.confirmation_step.name),
                                                            overview_url="Overview URL",
                                                            flow_nav=self.flow._get_flow_nav(self.confirmation_step))

            prev_step, self.filing_step, next_step = self.flow._generate_steps(MockFilingStep.name)
            self.render_info_filing_step = RenderInfo(flow_title=self.flow.title, step_title=self.filing_step.title,
                                                      step_intro=self.filing_step.intro, form=None,
                                                      prev_url=None,
                                                      next_url=self.flow.url_for_step(next_step.name),
                                                      submit_url=self.flow.url_for_step(self.filing_step.name),
                                                      overview_url=None,  # do not display
                                                      flow_nav=self.flow._get_flow_nav(self.filing_step))
            self.ack_elster_data = {'was_successful': True,
                                    'pdf': 'PDF CONTENT',
                                    'eric_response': 'Could we get the bill, please?',
                                    'server_response': 'What do you want to drink?',
                                    'transfer_ticket': 'Passierschein A38'}

            prev_step, self.summary_step, next_step = self.flow._generate_steps(MockSummaryStep.name)
            self.render_info_summary_step = RenderInfo(flow_title=self.flow.title, step_title=self.filing_step.title,
                                                       step_intro=self.filing_step.intro, form=None,
                                                       prev_url=self.flow.url_for_step(prev_step.name),
                                                       next_url=self.flow.url_for_step(self.filing_step.name),
                                                       submit_url=self.flow.url_for_step(self.filing_step.name),
                                                       overview_url=None,
                                                       flow_nav=self.flow._get_flow_nav(self.filing_step))

            prev_step, self.declaration_incomes_step, next_step = self.flow._generate_steps(
                MockDeclarationIncomesStep.name)
            self.render_info_declaration_incomes_step = RenderInfo(flow_title=self.flow.title,
                                                                   step_title=self.declaration_incomes_step.title,
                                                                   step_intro=self.declaration_incomes_step.intro,
                                                                   form=None,
                                                                   prev_url=self.flow.url_for_step(prev_step.name),
                                                                   next_url=self.flow.url_for_step(next_step.name),
                                                                   submit_url=self.flow.url_for_step(
                                                                       self.declaration_incomes_step.name),
                                                                   overview_url="Overview URL",
                                                                   flow_nav=self.flow._get_flow_nav(
                                                                       self.declaration_incomes_step))

            prev_step, self.declaration_edaten_step, next_step = self.flow._generate_steps(
                MockDeclarationEdatenStep.name)
            self.render_info_declaration_edaten_step = RenderInfo(flow_title=self.flow.title,
                                                                  step_title=self.declaration_edaten_step.title,
                                                                  step_intro=self.declaration_edaten_step.intro,
                                                                  form=None,
                                                                  prev_url=self.flow.url_for_step(prev_step.name),
                                                                  next_url=self.flow.url_for_step(next_step.name),
                                                                  submit_url=self.flow.url_for_step(
                                                                      self.declaration_edaten_step.name),
                                                                  overview_url="Overview URL",
                                                                  flow_nav=self.flow._get_flow_nav(
                                                                      self.declaration_edaten_step))

            prev_step, self.familienstand_step, next_step = self.flow._generate_steps(MockFamilienstandStep.name)
            self.render_info_familienstand_step = RenderInfo(flow_title=self.flow.title,
                                                             step_title=self.familienstand_step.title,
                                                             step_intro=self.familienstand_step.intro, form=None,
                                                             prev_url=self.flow.url_for_step(prev_step.name),
                                                             next_url=self.flow.url_for_step(next_step.name),
                                                             submit_url=self.flow.url_for_step(
                                                                 self.familienstand_step.name),
                                                             overview_url="Overview URL",
                                                             flow_nav=self.flow._get_flow_nav(self.familienstand_step))

            prev_step, self.personA_step, next_step = self.flow._generate_steps(MockPersonAStep.name)
            self.render_info_personA_step = RenderInfo(flow_title=self.flow.title, step_title=self.personA_step.title,
                                                       step_intro=self.personA_step.intro, form=None,
                                                       prev_url=self.flow.url_for_step(prev_step.name),
                                                       next_url=self.flow.url_for_step(next_step.name),
                                                       submit_url=self.flow.url_for_step(self.personA_step.name),
                                                       overview_url="Overview URL",
                                                       flow_nav=self.flow._get_flow_nav(self.personA_step))

            prev_step, self.personB_step, next_step = self.flow._generate_steps(MockPersonBStep.name)
            self.render_info_personB_step = RenderInfo(flow_title=self.flow.title, step_title=self.personB_step.title,
                                                       step_intro=self.personB_step.intro, form=None,
                                                       prev_url=self.flow.url_for_step(prev_step.name),
                                                       next_url=self.flow.url_for_step(next_step.name),
                                                       submit_url=self.flow.url_for_step(self.personB_step.name),
                                                       overview_url="Overview URL",
                                                       flow_nav=self.flow._get_flow_nav(self.personB_step))

            prev_step, self.iban_step, next_step = self.flow._generate_steps(MockIbanStep.name)
            self.render_info_iban_step = RenderInfo(flow_title=self.flow.title, step_title=self.iban_step.title,
                                                    step_intro=self.iban_step.intro, form=None,
                                                    prev_url=self.flow.url_for_step(prev_step.name),
                                                    next_url=self.flow.url_for_step(next_step.name),
                                                    submit_url=self.flow.url_for_step(self.iban_step.name),
                                                    overview_url="Overview URL",
                                                    flow_nav=self.flow._get_flow_nav(self.iban_step))

            self.data_married = {'familienstand': 'married',
                                 'familienstand_married_lived_separated': 'no',
                                 'familienstand_confirm_zusammenveranlagung': True}
            self.data_not_married = {'familienstand': 'single'}
            self.personA_url = '/' + self.endpoint_correct + '/step/' + StepPersonA.name + \
                               '?link_overview=' + str(self.flow.has_link_overview)
            self.personB_url = '/' + self.endpoint_correct + '/step/' + StepPersonB.name + \
                               '?link_overview=' + str(self.flow.has_link_overview)
            self.IBAN_url = '/' + self.endpoint_correct + '/step/' + StepIban.name + \
                            '?link_overview=' + str(self.flow.has_link_overview)
            self.summary_url = '/' + self.endpoint_correct + '/step/' + StepSummary.name + \
                               '?link_overview=' + str(self.flow.has_link_overview)

            self.data_st_mind_yes = {'steuerminderung': 'yes'}
            self.data_st_mind_no = {'steuerminderung': 'no'}
            prev_step, self.st_mind_yesno_step, next_step = self.flow._generate_steps(MockStrMindYNStep.name)
            self.render_info_st_mind_yesno_step = RenderInfo(flow_title=self.flow.title,
                                                             step_title=self.st_mind_yesno_step.title,
                                                             step_intro=self.st_mind_yesno_step.intro, form=None,
                                                             prev_url=self.flow.url_for_step(prev_step.name),
                                                             next_url=None,
                                                             submit_url=self.flow.url_for_step(
                                                                 self.st_mind_yesno_step.name),
                                                             overview_url="Overview URL",
                                                             flow_nav=self.flow._get_flow_nav(self.st_mind_yesno_step))
            self.st_mind_yesno_url = '/' + self.endpoint_correct + '/step/' + StepSteuerminderungYesNo.name + \
                                     '?link_overview=' + str(self.flow.has_link_overview)
            self.st_mind_yes_url = self.render_info_st_mind_yesno_step.next_url
            self.st_mind_no_url = '/' + self.endpoint_correct + '/step/' + StepSummary.name + \
                                  '?link_overview=' + str(self.flow.has_link_overview)

            self.data_haushaltsnahe_yes = {'stmind_haushaltsnahe_summe': Decimal(1.0),
                                           'stmind_haushaltsnahe_entries': 'Dach'}
            self.data_haushaltsnahe_no = {}
            prev_step, self.haushaltsnahe_step, next_step = self.flow._generate_steps(MockHaushaltsnaheStep.name)
            self.render_info_haushaltsnahe_step = RenderInfo(flow_title=self.flow.title,
                                                             step_title=self.haushaltsnahe_step.title,
                                                             step_intro=self.haushaltsnahe_step.intro, form=None,
                                                             prev_url=self.flow.url_for_step(prev_step.name),
                                                             next_url=self.flow.url_for_step(next_step.name),
                                                             submit_url=self.flow.url_for_step(
                                                                 self.haushaltsnahe_step.name),
                                                             overview_url="Overview URL",
                                                             flow_nav=self.flow._get_flow_nav(self.haushaltsnahe_step))

            self.data_handwerker_yes = {'stmind_handwerker_summe': Decimal(1.0),
                                        'stmind_handwerker_entries': 'Badezimmer',
                                        'stmind_handwerker_lohn_etc_summe': Decimal(0.0)}
            self.data_handwerker_no = {}
            prev_step, self.handwerker_step, next_step = self.flow._generate_steps(MockHandwerkerStep.name)
            self.render_info_handwerker_step = RenderInfo(flow_title=self.flow.title,
                                                          step_title=self.handwerker_step.title,
                                                          step_intro=self.handwerker_step.intro, form=None,
                                                          prev_url=self.flow.url_for_step(prev_step.name),
                                                          next_url=self.flow.url_for_step(next_step.name),
                                                          submit_url=self.flow.url_for_step(self.handwerker_step.name),
                                                          overview_url="Overview URL",
                                                          flow_nav=self.flow._get_flow_nav(self.handwerker_step))
            self.handwerker_url = '/' + self.endpoint_correct + '/step/' + StepHandwerker.name + \
                                  '?link_overview=' + str(self.flow.has_link_overview)
            self.handwerker_yes_url = self.render_info_handwerker_step.next_url
            self.handwerker_no_url = '/' + self.endpoint_correct + '/step/' + StepReligion.name + \
                                     '?link_overview=' + str(self.flow.has_link_overview)

            self.gem_haushalt_url = '/' + self.endpoint_correct + '/step/' + StepGemeinsamerHaushalt.name + \
                                    '?link_overview=' + str(self.flow.has_link_overview)

            prev_step, self.religion_step, next_step = self.flow._generate_steps(MockReligionStep.name)
            self.render_info_religion_step = RenderInfo(flow_title=self.flow.title,
                                                        step_title=self.religion_step.title,
                                                        step_intro=self.religion_step.intro, form=None,
                                                        prev_url=self.flow.url_for_step(prev_step.name),
                                                        next_url=self.flow.url_for_step(next_step.name),
                                                        submit_url=self.flow.url_for_step(
                                                            self.religion_step.name),
                                                        overview_url="Overview URL",
                                                        flow_nav=self.flow._get_flow_nav(
                                                            self.religion_step))
            self.religion_url = '/' + self.endpoint_correct + '/step/' + StepReligion.name + \
                                '?link_overview=' + str(self.flow.has_link_overview)

    def test_if_step_not_form_step_then_return_render_info(self):
        with app.test_request_context():
            returned_data, _ = self.flow._handle_specifics_for_step(
                self.middle_step, copy.deepcopy(self.render_info_middle_step), self.session_data)

            self.assertEqual(vars(self.render_info_middle_step), vars(returned_data))

    def test_if_overview_button_set_then_set_next_url_to_overview_url(self):
        with app.test_request_context() as req:
            req.request.form = ImmutableMultiDict({'overview_button': ''})
            returned_data, _ = self.flow._handle_specifics_for_step(
                self.middle_step, copy.deepcopy(self.render_info_middle_step), self.session_data)

            self.assertEqual(self.summary_url, returned_data.next_url)

    def test_if_step_with_custom_next_url_and_overview_button_set_then_set_next_url_to_overview_url(self):
        with app.test_request_context() as req:
            req.request.form = ImmutableMultiDict({'overview_button': ''})
            returned_data, _ = self.flow._handle_specifics_for_step(
                self.personA_step, copy.deepcopy(self.render_info_personA_step), self.data_married)

            self.assertEqual(self.summary_url, returned_data.next_url)

    def test_if_step_is_form_step_then_return_render_info_and_correct_form(self):
        with app.app_context() and app.test_request_context():
            returned_data, _ = self.flow._handle_specifics_for_step(
                self.form_step, copy.deepcopy(self.render_info_form_step), self.session_data)

            self.assertIsInstance(returned_data.form, MockForm)
            self.render_info_form_step.form = returned_data.form
            self.assertEqual(vars(self.render_info_form_step), vars(returned_data))

    def test_if_step_is_confirmation_step_and_valid_form_then_call_create_auditlog_for_all_fields(self):
        valid_session_data = {'idnr': self.valid_idnr}
        with app.app_context() and app.test_request_context(method='POST',
                                                            environ_base={'REMOTE_ADDR': self.ip_address},
                                                            data={'confirm_data_privacy': True,
                                                                  'confirm_terms_of_service': True}):
            with patch("app.forms.flows.lotse_flow.create_audit_log_confirmation_entry") as \
                    create_audit_log_fun:
                returned_data, _ = self.flow._handle_specifics_for_step(
                    self.confirmation_step, copy.deepcopy(self.render_info_confirmation_step), valid_session_data)

                # Assert called for each confirmation field
                create_audit_log_fun.assert_has_calls([call('Confirmed data privacy', self.ip_address,
                                                            self.valid_idnr, 'confirm_data_privacy', True),
                                                       call('Confirmed terms of service', self.ip_address,
                                                            self.valid_idnr, 'confirm_terms_of_service', True)],
                                                      any_order=True)

    def test_if_step_is_confirmation_step_and_non_valid_form_then_do_not_call_create_auditlog(self):
        invalid_datas = [{}, {'confirm_terms_of_service': True}, {'confirm_data_privacy': True}]
        for invalid_data in invalid_datas:
            with app.app_context() and app.test_request_context(method='POST', data=invalid_data):
                with patch("app.forms.flows.lotse_flow.create_audit_log_confirmation_entry") as \
                        create_audit_log_fun:
                    returned_data, _ = self.flow._handle_specifics_for_step(
                        self.confirmation_step, copy.deepcopy(self.render_info_confirmation_step), self.session_data)

                    create_audit_log_fun.assert_not_called()

    def test_if_step_is_filing_step_and_user_has_completed_tax_return_before_then_do_not_send_to_elster_again(self):
        with app.app_context() and app.test_request_context():
            with patch("app.elster_client.elster_client.send_est_with_elster") as send_est_with_elster, \
                    patch('app.forms.flows.lotse_flow.current_user',
                          MagicMock(has_completed_tax_return=MagicMock(return_value=True))):
                _, _ = self.flow._handle_specifics_for_step(
                    self.filing_step, copy.deepcopy(self.render_info_filing_step), self.session_data)

                send_est_with_elster.assert_not_called()

    def test_if_step_is_filing_step_and_user_has_completed_tax_return_before_then_return_correct_render_info(self):
        mock_pdf = 'pdf'
        mock_transfer_ticket = 'transfer_ticket'
        with app.app_context() and app.test_request_context():
            with patch('app.forms.flows.lotse_flow.current_user',
                       MagicMock(has_completed_tax_return=MagicMock(return_value=True),
                                 pdf=mock_pdf, transfer_ticket=mock_transfer_ticket)):
                returned_render_info, _ = self.flow._handle_specifics_for_step(
                    self.filing_step, copy.deepcopy(self.render_info_filing_step), self.session_data)

                self.assertEqual(True, returned_render_info.additional_info['elster_data']['was_successful'])
                self.assertEqual(mock_pdf, returned_render_info.additional_info['elster_data']['pdf'])
                self.assertEqual(mock_transfer_ticket,
                                 returned_render_info.additional_info['elster_data']['transfer_ticket'])

    def test_if_step_is_filing_step_and_user_has_completed_tax_return_before_and_user_idnr_is_test_idnr_then_send_to_elster_again(
            self):
        for test_idr in SPECIAL_RESEND_TEST_IDNRS:
            hashed_test_idnr = global_salt_hash().hash(test_idr)
            with app.app_context() and app.test_request_context():
                with patch("app.elster_client.elster_client.send_est_with_elster",
                           MagicMock(return_value=copy.deepcopy(self.ack_elster_data))) as send_est_with_elster, \
                        patch('app.forms.flows.lotse_flow.current_user',
                              MagicMock(has_completed_tax_return=MagicMock(return_value=True),
                                        idnr_hashed=hashed_test_idnr)), \
                        patch("app.forms.flows.lotse_flow.store_pdf_and_transfer_ticket"), \
                        patch("app.forms.flows.lotse_flow.LotseMultiStepFlow._validate_input"):
                    _, _ = self.flow._handle_specifics_for_step(self.filing_step,
                                                                copy.deepcopy(self.render_info_filing_step),
                                                                self.session_data)

                    send_est_with_elster.assert_called()

    def test_if_step_is_filing_step_then_call_elster_send_function_and_return_render_info_with_additional_data_and_form(
            self):
        expected_elster_data = copy.deepcopy(self.ack_elster_data)
        expected_elster_data.pop('pdf')  # pdf data is expected to be deleted, when stored with the user
        expected_returned_data = copy.deepcopy(self.render_info_filing_step)
        expected_returned_data.additional_info['elster_data'] = expected_elster_data

        with app.app_context() and app.test_request_context():
            with patch("app.elster_client.elster_client.send_est_with_elster",
                       MagicMock(return_value=copy.deepcopy(self.ack_elster_data))) as send_est_with_elster, \
                    patch('app.forms.flows.lotse_flow.current_user',
                          MagicMock(has_completed_tax_return=MagicMock(return_value=False))), \
                    patch("app.forms.flows.lotse_flow.store_pdf_and_transfer_ticket"), \
                    patch("app.forms.flows.lotse_flow.LotseMultiStepFlow._validate_input"):
                returned_data, _ = self.flow._handle_specifics_for_step(
                    self.filing_step, copy.deepcopy(self.render_info_filing_step), self.session_data)

                send_est_with_elster.assert_called()
                self.assertEqual(vars(expected_returned_data), vars(returned_data))

    def test_if_step_is_filing_step_and_validation_error_raised_then_return_render_info_with_additional_data(self):
        with app.app_context() and app.test_request_context():
            raised_exception = ElsterGlobalValidationError()
            raised_exception.eric_response = 'Eric says'
            raised_exception.validation_problems = 'Well, that\'s just wrong'
            with patch("app.elster_client.elster_client.send_est_with_elster",
                       MagicMock(side_effect=raised_exception)), \
                    patch('app.forms.flows.lotse_flow.current_user',
                          MagicMock(has_completed_tax_return=MagicMock(return_value=False))), \
                    patch("app.forms.flows.lotse_flow.LotseMultiStepFlow._validate_input"):
                returned_data, _ = self.flow._handle_specifics_for_step(
                    self.filing_step, copy.deepcopy(self.render_info_filing_step), self.session_data)

                self.assertEqual(raised_exception.eric_response,
                                 returned_data.additional_info['elster_data']['eric_response'])
                self.assertEqual(raised_exception.validation_problems,
                                 returned_data.additional_info['elster_data']['validation_problems'])
                self.assertEqual(False,
                                 returned_data.additional_info['elster_data']['was_successful'])

    def test_if_step_is_filing_step_and_transfer_error_raised_then_return_render_info_with_additional_data(self):
        with app.app_context() and app.test_request_context():
            raised_exception = ElsterTransferError()
            raised_exception.eric_response = 'Eric says'
            raised_exception.server_response = 'Servcer says'
            with patch("app.elster_client.elster_client.send_est_with_elster",
                       MagicMock(side_effect=raised_exception)), \
                    patch('app.forms.flows.lotse_flow.current_user',
                          MagicMock(has_completed_tax_return=MagicMock(return_value=False))), \
                    patch("app.forms.flows.lotse_flow.LotseMultiStepFlow._validate_input"):
                returned_data, _ = self.flow._handle_specifics_for_step(
                    self.filing_step, copy.deepcopy(self.render_info_filing_step), self.session_data)

                self.assertEqual(raised_exception.eric_response,
                                 returned_data.additional_info['elster_data']['eric_response'])
                self.assertEqual(raised_exception.server_response,
                                 returned_data.additional_info['elster_data']['server_response'])
                self.assertEqual(False,
                                 returned_data.additional_info['elster_data']['was_successful'])

    def test_if_step_is_filing_step_and_elster_request_got_though_then_store_pdf_is_called_with_correct_arguments(self):
        with app.app_context() and app.test_request_context():
            with patch("app.elster_client.elster_client.send_est_with_elster",
                       MagicMock(return_value=copy.deepcopy(self.ack_elster_data))), \
                    patch('app.forms.flows.lotse_flow.current_user',
                          MagicMock(has_completed_tax_return=MagicMock(return_value=False))) as current_user_mock, \
                    patch("app.forms.flows.lotse_flow.store_pdf_and_transfer_ticket") as store_pdf_and_transfer_ticket, \
                    patch("app.forms.flows.lotse_flow.LotseMultiStepFlow._validate_input"):
                returned_render_info, _ = self.flow._handle_specifics_for_step(
                    self.filing_step, copy.deepcopy(self.render_info_filing_step), self.session_data)

                store_pdf_and_transfer_ticket.assert_called_with(current_user_mock, self.ack_elster_data['pdf'],
                                                                 self.ack_elster_data['transfer_ticket'])

    def test_if_step_is_filing_step_and_elster_request_got_though_then_elster_data_without_pdf(self):
        with app.app_context() and app.test_request_context():
            with patch("app.elster_client.elster_client.send_est_with_elster",
                       MagicMock(return_value=copy.deepcopy(self.ack_elster_data))), \
                    patch('app.forms.flows.lotse_flow.current_user',
                          MagicMock(has_completed_tax_return=MagicMock(return_value=False))), \
                    patch("app.forms.flows.lotse_flow.LotseMultiStepFlow._validate_input"), \
                    patch("app.forms.flows.lotse_flow.store_pdf_and_transfer_ticket"):
                returned_render_info, _ = self.flow._handle_specifics_for_step(
                    self.filing_step, copy.deepcopy(self.render_info_filing_step), self.session_data)

                self.assertNotIn('pdf', returned_render_info.additional_info['elster_data'])

    def test_if_step_is_summary_step_then_return_render_info_with_sectionsteps(self):
        expected_summary_session_steps = []
        with app.app_context() and app.test_request_context(), \
                patch("app.forms.flows.lotse_flow.LotseMultiStepFlow._get_overview_data",
                      MagicMock(return_value=expected_summary_session_steps)), \
                patch("app.forms.flows.lotse_flow.MandatoryFormData.parse_obj"):
            data = self.session_data.copy()
            data['steuerminderung'] = 'yes'  # to prevent adaption of prev_url
            returned_data, _ = self.flow._handle_specifics_for_step(
                self.summary_step, copy.deepcopy(self.render_info_summary_step), data)

            self.assertEqual(expected_summary_session_steps, returned_data.additional_info['section_steps'])

    def test_if_summary_step_then_set_prev_url_correct(self):
        with app.app_context() and app.test_request_context(method='POST'), \
                patch('app.forms.flows.lotse_flow.LotseMultiStepFlow._get_overview_data'):
            render_info, _ = self.flow._handle_specifics_for_step(
                self.summary_step, self.render_info_summary_step, self.data_st_mind_yes)
            self.assertEqual(self.religion_url, render_info.prev_url)

            render_info, _ = self.flow._handle_specifics_for_step(
                self.summary_step, self.render_info_summary_step, self.data_st_mind_no)
            self.assertEqual(self.st_mind_yesno_url, render_info.prev_url)

    def test_if_summary_step_and_data_missing_then_set_next_url_correct(self):
        data_with_missing_fields = {'steuernummer': 'C3P0'}

        with app.app_context() and app.test_request_context(method='POST'), \
                patch('app.forms.flows.lotse_flow.LotseMultiStepFlow._get_overview_data'):
            render_info, _ = self.flow._handle_specifics_for_step(
                self.summary_step, self.render_info_summary_step, data_with_missing_fields)

            self.assertEqual(self.flow.url_for_step(StepSummary.name), render_info.next_url)

    def test_if_summary_step_and_data_missing_then_call_get_overview_data_with_missing_fields(self):
        data_with_missing_fields = {'steuernummer': 'C3P0'}
        missing_fields = ['spacecraft', 'droids']

        with app.app_context() and app.test_request_context(method='POST'), \
                patch('app.forms.flows.lotse_flow.LotseMultiStepFlow._get_overview_data') as get_overview, \
                patch('app.forms.flows.lotse_flow.LotseMultiStepFlow._validate_mandatory_fields',
                      MagicMock(side_effect=MandatoryFieldMissingValidationError(missing_fields))):
            render_info, _ = self.flow._handle_specifics_for_step(
                self.summary_step, self.render_info_summary_step, data_with_missing_fields)

            get_overview.assert_called_once_with(data_with_missing_fields, missing_fields)

    def test_if_summary_step_and_data_missing_then_flash_message_with_missing_fields_once(self):
        data_with_missing_fields = {'steuernummer': 'C3P0'}
        missing_fields = ['spacecraft', 'droids']
        missing_fields_error = MandatoryFieldMissingValidationError(missing_fields)

        with patch('app.forms.flows.lotse_flow.flash') as mock_flash, \
            patch('app.forms.flows.lotse_flow.LotseMultiStepFlow._get_overview_data'), \
            patch('app.forms.flows.lotse_flow.LotseMultiStepFlow._validate_mandatory_fields',
                  MagicMock(side_effect=missing_fields_error)):
            with app.app_context() and app.test_request_context(method='POST'):
                render_info, _ = self.flow._handle_specifics_for_step(
                    self.summary_step, self.render_info_summary_step, data_with_missing_fields)

            with app.app_context() and app.test_request_context(method='GET'):
                render_info, _ = self.flow._handle_specifics_for_step(
                    self.summary_step, self.render_info_summary_step, data_with_missing_fields)

            mock_flash.assert_called_once_with(missing_fields_error.get_message(), 'warn')

    def test_if_summary_step_and_data_not_missing_then_set_next_url_correct(self):
        data_without_missing_fields = self.flow.default_data()[1]

        with app.app_context() and app.test_request_context(method='POST'), \
                patch('app.forms.flows.lotse_flow.LotseMultiStepFlow._get_overview_data'):
            render_info, _ = self.flow._handle_specifics_for_step(
                self.summary_step, self.render_info_summary_step, data_without_missing_fields)

            self.assertEqual(self.flow.url_for_step(self.filing_step.name), render_info.next_url)

    def test_if_step_is_declaration_incomes_step_and_valid_form_then_call_create_auditlog_for_all_fields(self):
        valid_session_data = {'idnr': '02293417683'}
        with app.app_context() and app.test_request_context(method='POST',
                                                            environ_base={'REMOTE_ADDR': self.ip_address},
                                                            data={'declaration_incomes': True}):
            with patch("app.forms.flows.lotse_flow.create_audit_log_confirmation_entry") as \
                    create_audit_log_fun:
                returned_data, _ = self.flow._handle_specifics_for_step(
                    self.declaration_incomes_step, copy.deepcopy(self.render_info_declaration_incomes_step),
                    valid_session_data)

                # Assert called for each confirmation field
                create_audit_log_fun.assert_has_calls([call('Confirmed incomes', self.ip_address,
                                                            self.valid_idnr, 'declaration_incomes', True)],
                                                      any_order=True)

    def test_if_step_is_declaration_incomes_step_and_non_valid_form_then_do_not_call_create_auditlog(self):
        with app.app_context() and app.test_request_context(method='POST', data={}):
            with patch("app.forms.flows.lotse_flow.create_audit_log_confirmation_entry") as \
                    create_audit_log_fun:
                returned_data, _ = self.flow._handle_specifics_for_step(
                    self.declaration_incomes_step, copy.deepcopy(self.render_info_declaration_incomes_step),
                    self.session_data)

                create_audit_log_fun.assert_not_called()

    def test_if_step_is_declaration_edaten_step_and_valid_form_then_call_create_auditlog_for_all_fields(self):
        valid_session_data = {'idnr': '02293417683'}
        with app.app_context() and app.test_request_context(method='POST',
                                                            environ_base={'REMOTE_ADDR': self.ip_address},
                                                            data={'declaration_edaten': True}):
            with patch("app.forms.flows.lotse_flow.create_audit_log_confirmation_entry") as \
                    create_audit_log_fun:
                returned_data, _ = self.flow._handle_specifics_for_step(
                    self.declaration_edaten_step, copy.deepcopy(self.render_info_declaration_edaten_step),
                    valid_session_data)

                # Assert called for each confirmation field
                create_audit_log_fun.assert_has_calls([call('Confirmed edata', self.ip_address,
                                                            self.valid_idnr, 'declaration_edaten', True)],
                                                      any_order=True)

    def test_if_step_is_declaration_edaten_step_and_non_valid_form_then_do_not_call_create_auditlog(self):
        with app.app_context() and app.test_request_context(method='POST', data={}):
            with patch("app.forms.flows.lotse_flow.create_audit_log_confirmation_entry") as \
                    create_audit_log_fun:
                returned_data, _ = self.flow._handle_specifics_for_step(
                    self.declaration_edaten_step, copy.deepcopy(self.render_info_declaration_edaten_step),
                    self.session_data)

                create_audit_log_fun.assert_not_called()

    def test_if_familienstand_step_then_delete_person_b_data_correctly(self):
        person_b_fields = ['person_b_same_address', 'person_b_dob', 'person_b_last_name', 'person_b_first_name',
                           'person_b_religion', 'person_b_street', 'person_b_street_number', 'person_b_idnr',
                           'person_b_street_number_ext', 'person_b_address_ext', 'person_b_plz',
                           'person_b_town', 'person_b_beh_grad', 'person_b_blind', 'person_b_gehbeh',
                           'is_person_a_account_holder']
        with app.app_context() and app.test_request_context(method='POST',
                                                            data={'familienstand': 'married',
                                                                  'familienstand_date': '1985-01-01'}):
            _, returned_data = self.flow._handle_specifics_for_step(
                self.familienstand_step, self.render_info_familienstand_step,
                copy.deepcopy(LotseMultiStepFlow._DEBUG_DATA[1]))

            self.assertIn('person_b_idnr', returned_data)
            self.assertIn('is_person_a_account_holder', returned_data)

        with app.app_context() and app.test_request_context(method='POST',
                                                            data={'familienstand': 'single'}):
            _, returned_data = self.flow._handle_specifics_for_step(
                self.familienstand_step, self.render_info_familienstand_step,
                copy.deepcopy(LotseMultiStepFlow._DEBUG_DATA[1]))
            for person_b_field in person_b_fields:
                self.assertNotIn(person_b_field, returned_data)

    def test_if_familienstand_step_then_delete_familienstand_date_correctly(self):
        with app.app_context() and app.test_request_context(method='POST',
                                                            data={'familienstand': 'married',
                                                                  'familienstand_date': '01.01.1985',
                                                                  'familienstand_married_lived_separated': 'no',
                                                                  'familienstand_confirm_zusammenveranlagung': True}):
            _, returned_data = self.flow._handle_specifics_for_step(
                self.familienstand_step, self.render_info_familienstand_step, {})
            self.assertIn('familienstand_date', returned_data)

        with app.app_context() and app.test_request_context(method='POST',
                                                            data={'familienstand': 'single',
                                                                  'familienstand_date': '01.01.1985'}):
            _, returned_data = self.flow._handle_specifics_for_step(
                self.familienstand_step, self.render_info_familienstand_step, {})
            self.assertNotIn('familienstand_date', returned_data)

    def test_if_familienstand_step_then_delete_gem_haushalt_correctly(self):
        with app.app_context() and app.test_request_context(method='POST',
                                                            data={'familienstand': 'married',
                                                                  'familienstand_date': '01.01.1985',
                                                                  'familienstand_married_lived_separated': 'no',
                                                                  'familienstand_confirm_zusammenveranlagung': True}):
            _, returned_data = self.flow._handle_specifics_for_step(
                self.familienstand_step, self.render_info_familienstand_step,
                {'stmind_gem_haushalt_entries': ['Helene Fischer'], 'stmind_gem_haushalt_count': 1})
            self.assertNotIn('stmind_gem_haushalt_entries', returned_data)
            self.assertNotIn('stmind_gem_haushalt_count', returned_data)

        with app.app_context() and app.test_request_context(method='POST',
                                                            data={'familienstand': 'single'}):
            _, returned_data = self.flow._handle_specifics_for_step(
                self.familienstand_step, self.render_info_familienstand_step,
                {'stmind_gem_haushalt_entries': ['Helene Fischer'], 'stmind_gem_haushalt_count': 1})
            self.assertIn('stmind_gem_haushalt_entries', returned_data)
            self.assertIn('stmind_gem_haushalt_count', returned_data)

    def test_if_person_a_step_then_set_next_url_correct(self):
        with app.app_context() and app.test_request_context(method='POST'):
            render_info, _ = self.flow._handle_specifics_for_step(
                self.personA_step, self.render_info_personA_step, self.data_married)
            self.assertEqual(self.personB_url, render_info.next_url)

            render_info, _ = self.flow._handle_specifics_for_step(
                self.personA_step, self.render_info_personA_step, self.data_not_married)
            self.assertEqual(self.IBAN_url, render_info.next_url)

    def test_if_person_b_step_then_delete_person_b_address_correctly(self):
        correct_person_b_data = {'person_b_idnr': '02293417683', 'person_b_dob': '25.02.1951',
                                 'person_b_first_name': 'Gerta', 'person_b_last_name': 'Mustername',
                                 'person_b_religion': 'rk',
                                 'person_b_street': 'Steuerweg', 'person_b_street_number': 42, 'person_b_plz': '20354',
                                 'person_b_town': 'Hamburg', 'person_b_same_address': 'no'}
        expected_person_b_data = {'person_b_idnr': '02293417683', 'person_b_dob': datetime.date(1951, 2, 25),
                                  'person_b_first_name': 'Gerta', 'person_b_last_name': 'Mustername',
                                  'person_b_religion': 'rk', 'person_b_blind': False, 'person_b_gehbeh': False,
                                  'person_b_street': 'Steuerweg', 'person_b_street_number': 42, 'person_b_plz': '20354',
                                  'person_b_town': 'Hamburg', 'person_b_same_address': 'no'}

        with app.app_context() and app.test_request_context(method='POST', data=correct_person_b_data):
            _, returned_data = self.flow._handle_specifics_for_step(self.personB_step,
                                                                    self.render_info_personB_step, {})
            self.assertTrue(
                all([(field, value) in returned_data.items() for field, value in expected_person_b_data.items()]))

        expected_data_no_address = {'person_b_idnr': '02293417683', 'person_b_dob': datetime.date(1951, 2, 25),
                                    'person_b_first_name': 'Gerta', 'person_b_last_name': 'Mustername',
                                    'person_b_religion': 'rk', 'person_b_blind': False, 'person_b_gehbeh': False,
                                    'person_b_beh_grad': None, 'person_b_same_address': 'yes'}

        correct_person_b_data['person_b_same_address'] = 'yes'
        with app.app_context() and app.test_request_context(method='POST', data=correct_person_b_data):
            correct_person_b_data['person_b_same_address'] = 'yes'
            _, returned_data = self.flow._handle_specifics_for_step(self.personB_step,
                                                                    self.render_info_personB_step, {})
            self.assertEqual(expected_data_no_address, returned_data)

    def test_if_iban_step_then_set_prev_url_correct(self):
        with app.app_context() and app.test_request_context(method='POST'):
            render_info, _ = self.flow._handle_specifics_for_step(
                self.iban_step, self.render_info_iban_step, self.data_married)
            self.assertEqual(self.personB_url, render_info.prev_url)

            render_info, _ = self.flow._handle_specifics_for_step(
                self.iban_step, self.render_info_iban_step, self.data_not_married)
            self.assertEqual(self.personA_url, render_info.prev_url)

    def test_if_st_mind_yesno_step_then_set_next_url_correct(self):
        with app.app_context() and app.test_request_context(method='POST'):
            render_info, _ = self.flow._handle_specifics_for_step(
                self.st_mind_yesno_step, self.render_info_st_mind_yesno_step, self.data_st_mind_yes)
            self.assertEqual(self.st_mind_yes_url, render_info.next_url)

            render_info, _ = self.flow._handle_specifics_for_step(
                self.st_mind_yesno_step, self.render_info_st_mind_yesno_step, self.data_st_mind_no)
            self.assertEqual(self.st_mind_no_url, render_info.next_url)

    def test_if_st_mind_yesno_step_and_steuerminderung_not_set_then_set_confirmation_step_as_next_url(self):
        with app.app_context() and app.test_request_context(method='POST'):
            render_info, _ = self.flow._handle_specifics_for_step(
                self.st_mind_yesno_step, self.render_info_st_mind_yesno_step, {})
            self.assertEqual(self.st_mind_no_url, render_info.next_url)

    def test_if_st_mind_yesno_step_and_steuerminderung_not_set_then_delete_all_st_mind_entries(self):
        data_before_st_mind_no = {
            'steuerminderung': 'no',
            'stmind_vorsorge_summe': 'some_value',

            'stmind_krankheitskosten_summe': 'some_value',
            'stmind_krankheitskosten_anspruch': 'some_value',
            'stmind_pflegekosten_summe': 'some_value',
            'stmind_pflegekosten_anspruch': 'some_value',
            'stmind_beh_aufw_summe': 'some_value',
            'stmind_beh_aufw_anspruch': 'some_value',
            'stmind_beh_kfz_summe': 'some_value',
            'stmind_beh_kfz_anspruch': 'some_value',
            'stmind_bestattung_summe': 'some_value',
            'stmind_bestattung_anspruch': 'some_value',
            'stmind_aussergbela_sonst_summe': 'some_value',
            'stmind_aussergbela_sonst_anspruch': 'some_value',

            'stmind_haushaltsnahe_entries': 'some_value',
            'stmind_haushaltsnahe_summe': 'some_value',
            'stmind_handwerker_entries': 'some_value',
            'stmind_handwerker_summe': 'some_value',
            'stmind_handwerker_lohn_etc_summe': 'some_value',

            'stmind_gem_haushalt': 'some_value',
            'stmind_religion_paid_summe': 'some_value',
            'stmind_religion_reimbursed_summe': 'some_value',
            'stmind_spenden_inland': 'some_value',
            'stmind_spenden_inland_parteien': 'some_value',

            'person_a_first_name': 'IWillStay'
        }
        expected_updated_data = {'steuerminderung': 'no', 'person_a_first_name': 'IWillStay'}
        with app.app_context() and app.test_request_context(method='POST'):
            _, updated_data = self.flow._handle_specifics_for_step(
                self.st_mind_yesno_step, self.render_info_st_mind_yesno_step, data_before_st_mind_no)

            self.assertEqual(expected_updated_data, updated_data)

    def test_if_haushaltsnahe_step_then_delete_stmind_gem_haushalt_correctly(self):
        with app.app_context() and app.test_request_context(method='POST', data=self.data_haushaltsnahe_yes):
            _, returned_data = self.flow._handle_specifics_for_step(
                self.haushaltsnahe_step, self.render_info_haushaltsnahe_step,
                {'familienstand': 'single', 'gem_haushalt_entries': ['Helene Fischer'], 'gem_haushalt_count': 1})
            self.assertIn('gem_haushalt_entries', returned_data)
            self.assertIn('gem_haushalt_count', returned_data)

        with app.app_context() and app.test_request_context(method='POST', data=self.data_haushaltsnahe_no):
            _, returned_data = self.flow._handle_specifics_for_step(
                self.haushaltsnahe_step, self.render_info_haushaltsnahe_step,
                {'familienstand': 'single', 'stmind_gem_haushalt_entries': ['Helene Fischer'],
                 'stmind_gem_haushalt_count': 1})
            self.assertNotIn('stmind_gem_haushalt_entries', returned_data)
            self.assertNotIn('stmind_gem_haushalt_count', returned_data)

    def test_if_handwerker_step_then_delete_stmind_gem_haushalt_correctly(self):
        with app.app_context() and app.test_request_context(method='POST', data=self.data_handwerker_yes):
            _, returned_data = self.flow._handle_specifics_for_step(
                self.handwerker_step, self.render_info_handwerker_step,
                {'familienstand': 'single', 'stmind_gem_haushalt_entries': ['Helene Fischer'],
                 'stmind_gem_haushalt_count': 1})
            self.assertIn('stmind_gem_haushalt_entries', returned_data)
            self.assertIn('stmind_gem_haushalt_count', returned_data)

        with app.app_context() and app.test_request_context(method='POST', data=self.data_handwerker_no):
            _, returned_data = self.flow._handle_specifics_for_step(
                self.handwerker_step, self.render_info_handwerker_step,
                {'familienstand': 'single', 'stmind_gem_haushalt_entries': ['Helene Fischer'],
                 'stmind_gem_haushalt_count': 1})
            self.assertNotIn('stmind_gem_haushalt_entries', returned_data)
            self.assertNotIn('stmind_gem_haushalt_count', returned_data)

    def test_if_handwerker_filled_then_set_next_url_correct(self):
        with app.app_context() and app.test_request_context(method='POST', data=self.data_handwerker_yes):
            render_info, _ = self.flow._handle_specifics_for_step(
                self.handwerker_step, self.render_info_handwerker_step, {'familienstand': 'single'})
            self.assertEqual(self.handwerker_yes_url, render_info.next_url)

        with app.app_context() and app.test_request_context(method='POST', data=self.data_handwerker_yes):
            render_info, _ = self.flow._handle_specifics_for_step(
                self.handwerker_step, self.render_info_handwerker_step, {'familienstand': 'married',
                                                                         'familienstand_married_lived_separated': 'no',
                                                                         'familienstand_confirm_zusammenveranlagung': True})
            self.assertEqual(self.handwerker_no_url, render_info.next_url)

    def test_if_haushaltsnahe_filled_then_set_next_url_correct(self):
        with app.app_context() and app.test_request_context(method='POST'):
            render_info, _ = self.flow._handle_specifics_for_step(
                self.handwerker_step, self.render_info_handwerker_step,
                {**{'familienstand': 'single'}, **self.data_haushaltsnahe_yes})
            self.assertEqual(self.handwerker_yes_url, render_info.next_url)

        with app.app_context() and app.test_request_context(method='POST'):
            render_info, _ = self.flow._handle_specifics_for_step(
                self.handwerker_step, self.render_info_handwerker_step,
                {**self.data_married, **self.data_haushaltsnahe_yes})
            self.assertEqual(self.handwerker_no_url, render_info.next_url)

    def test_if_handwerker_and_haushaltsnahe_not_filled_then_set_next_url_correct(self):
        with app.app_context() and app.test_request_context(method='POST'):
            render_info, _ = self.flow._handle_specifics_for_step(
                self.handwerker_step, self.render_info_handwerker_step,
                {**{'familienstand': 'single'}, **self.data_handwerker_no})
            self.assertEqual(self.handwerker_no_url, render_info.next_url)

    def test_if_religion_step_then_set_prev_url_correct(self):
        with app.app_context() and app.test_request_context(method='POST'):
            render_info, _ = self.flow._handle_specifics_for_step(
                self.religion_step, self.render_info_religion_step,
                {**{'familienstand': 'single'}, **self.data_handwerker_yes})
            self.assertEqual(self.gem_haushalt_url, render_info.prev_url)

            render_info, _ = self.flow._handle_specifics_for_step(
                self.religion_step, self.render_info_religion_step,
                {**{'familienstand': 'single'}, **self.data_handwerker_no})
            self.assertEqual(self.handwerker_url, render_info.prev_url)

            render_info, _ = self.flow._handle_specifics_for_step(
                self.religion_step, self.render_info_religion_step,
                {**self.data_married, **self.data_handwerker_yes})
            self.assertEqual(self.handwerker_url, render_info.prev_url)

            render_info, _ = self.flow._handle_specifics_for_step(
                self.religion_step, self.render_info_religion_step,
                {**self.data_married, **self.data_handwerker_no})
            self.assertEqual(self.handwerker_url, render_info.prev_url)

    def test_if_filing_step_and_validate_raises_confirmation_missing_then_flash_err_and_redirect_to_confirmation(
            self):
        with app.app_context() and app.test_request_context(), \
                patch('app.forms.flows.lotse_flow.current_user',
                      MagicMock(has_completed_tax_return=MagicMock(return_value=False))), \
                patch('app.forms.flows.lotse_flow.flash') as mock_flash, \
                patch('app.forms.flows.lotse_flow.LotseMultiStepFlow._validate_input',
                      MagicMock(side_effect=ConfirmationMissingInputValidationError)):
            returned_render_info, _ = self.flow._handle_specifics_for_step(
                self.filing_step, copy.deepcopy(self.render_info_filing_step), self.session_data)

            mock_flash.assert_called_once_with(ConfirmationMissingInputValidationError.message, 'warn')
            self.assertEqual(self.flow.url_for_step(StepConfirmation.name), returned_render_info.redirect_url)

    def test_if_filing_step_and_validate_raises_input_invalid_then_flash_err_and_redirect_to_summary(self):
        with app.app_context() and app.test_request_context(), \
                patch('app.forms.flows.lotse_flow.current_user',
                      MagicMock(has_completed_tax_return=MagicMock(return_value=False))), \
                patch('app.forms.flows.lotse_flow.flash') as mock_flash, \
                patch('app.forms.flows.lotse_flow.LotseMultiStepFlow._validate_input',
                      MagicMock(side_effect=InputDataInvalidError)):
            returned_render_info, _ = self.flow._handle_specifics_for_step(
                self.filing_step, copy.deepcopy(self.render_info_filing_step), self.session_data)

            mock_flash.assert_called_once_with(InputDataInvalidError.message, 'warn')
            self.assertEqual(self.flow.url_for_step(StepSummary.name), returned_render_info.redirect_url)

    def test_if_filing_step_and_send_est_with_elster_raises_erica_missing_field_then_flash_err_and_redirect_to_summary(
            self):
        with app.app_context() and app.test_request_context(), \
                patch('app.forms.flows.lotse_flow.current_user',
                      MagicMock(has_completed_tax_return=MagicMock(return_value=False))), \
                patch('app.forms.flows.lotse_flow.flash') as mock_flash, \
                patch('app.forms.flows.lotse_flow.LotseMultiStepFlow._validate_input'), \
                patch('app.elster_client.elster_client.send_est_with_elster',
                      MagicMock(side_effect=EricaIsMissingFieldError)):
            returned_render_info, _ = self.flow._handle_specifics_for_step(
                self.filing_step, copy.deepcopy(self.render_info_filing_step), self.session_data)

            mock_flash.assert_called_once_with(EricaIsMissingFieldError().message, 'warn')
            self.assertEqual(self.flow.url_for_step(StepSummary.name), returned_render_info.redirect_url)

    def test_if_filing_step_and_send_est_with_elster_raises_invalid_bufa_error_then_flash_err_and_redirect_to_summary(
            self):
        with app.app_context() and app.test_request_context(), \
                patch('app.forms.flows.lotse_flow.current_user', MagicMock(
                    has_completed_tax_return=MagicMock(return_value=False))), \
                patch('app.forms.flows.lotse_flow.flash') as mock_flash, \
                patch('app.forms.flows.lotse_flow.LotseMultiStepFlow._validate_input'), \
                patch('app.elster_client.elster_client.send_est_with_elster',
                      MagicMock(side_effect=ElsterInvalidBufaNumberError)):
            returned_render_info, _ = self.flow._handle_specifics_for_step(
                self.filing_step, copy.deepcopy(self.render_info_filing_step), self.session_data)

            mock_flash.assert_called_once_with(ElsterInvalidBufaNumberError().message, 'warn')
            self.assertEqual(self.flow.url_for_step(StepSummary.name), returned_render_info.redirect_url)


class TestLotseGenerateSteps(unittest.TestCase):

    def setUp(self):
        with app.app_context() and app.test_request_context():
            testing_steps = [MockStartStep, MockMiddleStep, MockFinalStep]
            testing_steps = {s.name: s for s in testing_steps}

            self.endpoint_correct = "lotse"
            self.flow = LotseMultiStepFlow(endpoint=self.endpoint_correct)
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


class TestLotseDebugData(unittest.TestCase):

    def setUp(self):
        with app.app_context() and app.test_request_context():
            self.flow = LotseMultiStepFlow(endpoint='')
        self.original_debug_data_config = app.config['DEBUG_DATA']

    def test_if_debug_data_true_then_debug_data_non_empty(self):
        app.config['DEBUG_DATA'] = True
        debug_data = self.flow.default_data()
        self.assertIsNotNone(debug_data[0])
        self.assertIsNotNone(debug_data[1])

    def test_if_debug_data_true_then_debug_data_correct_types(self):
        app.config['DEBUG_DATA'] = True
        debug_data = self.flow.default_data()
        self.assertIsInstance(debug_data[0], type)
        self.assertIsInstance(debug_data[1], dict)

    def test_if_debug_data_false_then_debug_data_none(self):
        app.config['DEBUG_DATA'] = False
        debug_data = self.flow.default_data()
        self.assertEqual({}, debug_data)

    def tearDown(self):
        app.config['DEBUG_DATA'] = self.original_debug_data_config


class TestLotseGetOverviewData(unittest.TestCase):

    def test_if_steps_set_and_input_data_given_then_return_correct_sections_with_input_data(self):
        with app.app_context() and app.test_request_context():
            flow = LotseMultiStepFlow(endpoint='lotse')
            flow.steps = {s.name: s for s in [StepIban, StepHaushaltsnahe, StepAck]}
            debug_data = flow.default_data()[1]
            expected_data = {
                'mandatory_data': Section(
                    StepIban.section_link.label,
                    flow.url_for_step(StepIban.section_link.beginning_step, _has_link_overview=True),
                    {
                        StepIban.name:
                            Section(
                                StepIban.label,
                                flow.url_for_step(StepIban.name, _has_link_overview=True),
                                {str(debug_data['iban']): debug_data['iban'],
                                 str(debug_data['is_person_a_account_holder']): debug_data[
                                     'is_person_a_account_holder']}
                            )
                    }
                ),
                'section_steuerminderung': Section(
                    StepHaushaltsnahe.section_link.label,
                    flow.url_for_step(StepHaushaltsnahe.section_link.beginning_step, _has_link_overview=True),
                    {
                        StepHaushaltsnahe.name: Section(
                            StepHaushaltsnahe.label,
                            flow.url_for_step(StepHaushaltsnahe.name, _has_link_overview=True),
                            {str(debug_data['stmind_haushaltsnahe_entries']): debug_data[
                                'stmind_haushaltsnahe_entries'],
                             str(debug_data['stmind_haushaltsnahe_summe']): debug_data[
                                 'stmind_haushaltsnahe_summe']}
                        )
                    }
                )
            }

            with patch('app.forms.flows.lotse_flow.LotseMultiStepFlow._generate_value_representation',
                       MagicMock(side_effect=lambda field, value: (str(value), value))):
                actual_data = flow._get_overview_data(debug_data)
            self.assertEqual(expected_data, actual_data)

    def test_if_missing_steps_are_missing_then_set_mandatory_missing_value(self):
        with app.app_context() and app.test_request_context():
            flow = LotseMultiStepFlow(endpoint='lotse')
            flow.steps = {s.name: s for s in [StepIban, StepHaushaltsnahe, StepAck]}
            debug_data = copy.deepcopy(flow.default_data()[1])
            missing_fields = ['iban', 'is_person_a_account_holder']
            for missing_field in missing_fields:
                debug_data.pop(missing_field)
            mandatory_data_missing_value = _l('form.lotse.missing_mandatory_field')
            expected_data = {
                'mandatory_data': Section(
                    StepIban.section_link.label,
                    flow.url_for_step(StepIban.section_link.beginning_step, _has_link_overview=True),
                    {
                        StepIban.name:
                            Section(
                                StepIban.label,
                                flow.url_for_step(StepIban.name, _has_link_overview=True),
                                {_l('form.lotse.field_iban.data_label'): mandatory_data_missing_value,
                                 _l(
                                     'form.lotse.field_is_person_a_account_holder.data_label'): mandatory_data_missing_value}
                            )
                    }
                ),
                'section_steuerminderung': Section(
                    StepHaushaltsnahe.section_link.label,
                    flow.url_for_step(StepHaushaltsnahe.section_link.beginning_step, _has_link_overview=True),
                    {
                        StepHaushaltsnahe.name:
                            Section(
                                StepHaushaltsnahe.label,
                                flow.url_for_step(StepHaushaltsnahe.name, _has_link_overview=True),
                                {str(debug_data['stmind_haushaltsnahe_entries']): debug_data[
                                    'stmind_haushaltsnahe_entries'],
                                 str(debug_data['stmind_haushaltsnahe_summe']): debug_data[
                                     'stmind_haushaltsnahe_summe']}
                            )
                    }
                )
            }

            with patch('app.forms.flows.lotse_flow.LotseMultiStepFlow._generate_value_representation',
                       MagicMock(side_effect=lambda field, value: (str(value), value))):
                actual_data = flow._get_overview_data(debug_data, missing_fields)
            self.assertEqual(expected_data, actual_data)


class TestShowPersonBLotseFlow(unittest.TestCase):
    def test_if_familienstand_not_given_return_false(self):
        data = {}
        is_shown = show_person_b(data)
        self.assertFalse(is_shown)

    def test_if_familienstand_given_familienstand_model_show_person_b_is_called(self):
        data = {'familienstand': 'single'}
        with patch('app.model.form_data.FamilienstandModel.show_person_b') as model_show_person_b_mock:
            show_person_b(data)
            model_show_person_b_mock.assert_called()


class TestLotseValidateInput(unittest.TestCase):

    def setUp(self) -> None:
        db.create_all()
        self.valid_data_single = {
            'steuernummer': '19811310010',
            'bundesland': 'BY',

            'familienstand': 'single',

            'person_a_dob': datetime.date(1950, 8, 16),
            'person_a_first_name': 'Manfred',
            'person_a_last_name': 'Mustername',
            'person_a_street': 'Steuerweg',
            'person_a_street_number': 42,
            'person_a_street_number_ext': 'a',
            'person_a_address_ext': 'Seitenflügel',
            'person_a_plz': '20354',
            'person_a_town': 'Hamburg',
            'person_a_religion': 'none',
            'person_a_beh_grad': 25,
            'person_a_blind': True,
            'person_a_gehbeh': True,

            'is_person_a_account_holder': 'yes',
            'iban': 'DE35133713370000012345',

            'steuerminderung': 'yes', }
        self.valid_data_married = {
            'steuernummer': '19811310010',
            'bundesland': 'BY',

            'familienstand': 'married',
            'familienstand_date': datetime.date(2000, 1, 31),
            'familienstand_married_lived_separated': 'no',
            'familienstand_confirm_zusammenveranlagung': True,

            'person_a_dob': datetime.date(1950, 8, 16),
            'person_a_first_name': 'Manfred',
            'person_a_last_name': 'Mustername',
            'person_a_street': 'Steuerweg',
            'person_a_street_number': 42,
            'person_a_street_number_ext': 'a',
            'person_a_address_ext': 'Seitenflügel',
            'person_a_plz': '20354',
            'person_a_town': 'Hamburg',
            'person_a_religion': 'none',
            'person_a_beh_grad': 25,
            'person_a_blind': True,
            'person_a_gehbeh': True,

            'person_b_dob': datetime.date(1951, 2, 25),
            'person_b_first_name': 'Gerta',
            'person_b_last_name': 'Mustername',
            'person_b_same_address': 'yes',
            'person_b_religion': 'rk',
            'person_b_blind': False,
            'person_b_gehbeh': False,

            'is_person_a_account_holder': 'yes',
            'iban': 'DE35133713370000012345',

            'steuerminderung': 'yes', }

    @staticmethod
    def _create_logged_in_user(idnr):
        create_and_activate_user(idnr, '0000', '1985-01-01', '123456')
        user = find_user(idnr)
        login_user(user)

    def test_if_no_persona_and_no_personb_then_raise_invalidation_error(self):
        with app.app_context() and app.test_request_context():
            existing_idnr = '04452397610'
            self._create_logged_in_user(existing_idnr)
            form_data = {**self.valid_data_single,
                         **{'confirm_complete_correct': True,
                            'confirm_data_privacy': True,
                            'confirm_terms_of_service': True}}

            self.assertRaises(IdNrMismatchInputValidationError, LotseMultiStepFlow._validate_input, form_data)

    def test_if_persona_idnr_not_current_user_idnr_and_no_personb_then_raise_invalidation_error(self):
        with app.app_context() and app.test_request_context():
            existing_idnr = '04452397610'
            self._create_logged_in_user(existing_idnr)
            form_data = {**self.valid_data_single,
                         **{'person_a_idnr': 'NotTheCorrectOne',
                            'confirm_complete_correct': True,
                            'confirm_data_privacy': True}}

            self.assertRaises(IdNrMismatchInputValidationError, LotseMultiStepFlow._validate_input, form_data)

    def test_if_persona_and_person_b_idnr_not_current_user_idnr_then_raise_invalidation_error(self):
        with app.app_context() and app.test_request_context():
            existing_idnr = '04452397610'
            self._create_logged_in_user(existing_idnr)
            form_data = {**self.valid_data_single,
                         **{'person_a_idnr': 'NotTheCorrectOne', 'person_b_idnr': 'NotTheCorrectOne'}}

            self.assertRaises(IdNrMismatchInputValidationError, LotseMultiStepFlow._validate_input, form_data)

    def test_if_persona_not_current_user_idnr_but_person_b_then_no_error(self):
        with app.app_context() and app.test_request_context():
            existing_idnr = '04452397610'
            self._create_logged_in_user(existing_idnr)
            form_data = {**self.valid_data_married,
                         **{'person_a_idnr': 'NotTheCorrectOne',
                            'person_b_idnr': existing_idnr,
                            'declaration_edaten': True,
                            'declaration_incomes': True,
                            'confirm_data_privacy': True,
                            'confirm_complete_correct': True,
                            'confirm_terms_of_service': True,
                            }}

            try:
                LotseMultiStepFlow._validate_input(form_data)
            except InputDataInvalidError as e:
                print(e)
                self.fail("_validate_input raised unexpected InputDataInvalidError")

    def test_if_summary_confirmations_not_set_to_true_then_raise_invalidation_error(self):
        expected_missing_fields = ['confirm_complete_correct']
        with app.app_context() and app.test_request_context():
            existing_idnr = '04452397610'
            self._create_logged_in_user(existing_idnr)
            form_data = {**self.valid_data_single,
                         **{'person_a_idnr': existing_idnr,

                            'confirm_complete_correct': False,
                            'declaration_edaten': True,
                            'declaration_incomes': True,
                            'confirm_data_privacy': True,
                            'confirm_terms_of_service': True, }}

            with self.assertRaises(MandatoryFieldMissingValidationError) as mandatory_exception:
                LotseMultiStepFlow._validate_input(form_data)
            self.assertEqual(expected_missing_fields, mandatory_exception.exception.missing_fields)

    def test_if_confirmations_step_confirmations_not_set_to_true_then_raise_confirmation_error(self):
        expected_missing_fields = ['confirm_data_privacy', 'confirm_terms_of_service']
        with app.app_context() and app.test_request_context():
            existing_idnr = '04452397610'
            self._create_logged_in_user(existing_idnr)
            form_data = {**self.valid_data_single,
                         **{'person_a_idnr': existing_idnr,
                            'steuernummer': '19811310010',
                            'bundesland': 'BY',

                            'confirm_complete_correct': True,
                            'declaration_edaten': True,
                            'declaration_incomes': True,
                            'confirm_data_privacy': False,
                            'confirm_terms_of_service': False, }}

            self.assertRaises(ConfirmationMissingInputValidationError, LotseMultiStepFlow._validate_input,
                              form_data)
            with self.assertRaises(ConfirmationMissingInputValidationError) as confirmation_exception:
                LotseMultiStepFlow._validate_input(form_data)
            self.assertEqual(expected_missing_fields, confirmation_exception.exception.missing_fields)

    def test_if_contains_not_all_confirmations_then_raise_invalidation_error(self):
        expected_missing_fields = ['declaration_edaten', 'declaration_incomes']
        with app.app_context() and app.test_request_context():
            existing_idnr = '04452397610'
            self._create_logged_in_user(existing_idnr)
            form_data = {**self.valid_data_single,
                         **{'person_a_idnr': existing_idnr,
                            'confirm_complete_correct': True,
                            }}

            with self.assertRaises(MandatoryFieldMissingValidationError) as mandatory_exception:
                LotseMultiStepFlow._validate_input(form_data)
            self.assertEqual(expected_missing_fields, mandatory_exception.exception.missing_fields)

    def test_if_summary_step_confirmations_are_missing_but_confirmation_step_confirmations_are_contained_then_raise_invalidation_error(
            self):
        expected_missing_fields = ['declaration_edaten', 'declaration_incomes']
        with app.app_context() and app.test_request_context():
            existing_idnr = '04452397610'
            self._create_logged_in_user(existing_idnr)
            form_data = {**self.valid_data_single,
                         **{'person_a_idnr': existing_idnr,

                            'confirm_complete_correct': True,
                            'confirm_data_privacy': False,
                            'confirm_terms_of_service': False,
                            }}

            with self.assertRaises(MandatoryFieldMissingValidationError) as mandatory_exception:
                LotseMultiStepFlow._validate_input(form_data)
            self.assertEqual(expected_missing_fields, mandatory_exception.exception.missing_fields)

    def test_if_only_confirmations_from_confirmation_step_missing_then_raise_confirmation_error(self):
        with app.app_context() and app.test_request_context():
            existing_idnr = '04452397610'
            self._create_logged_in_user(existing_idnr)
            form_data = {**self.valid_data_single,
                         **{'person_a_idnr': existing_idnr,

                            'confirm_complete_correct': True,
                            'declaration_edaten': True,
                            'declaration_incomes': True,
                            }}

            self.assertRaises(ConfirmationMissingInputValidationError, LotseMultiStepFlow._validate_input,
                              form_data)

    def test_if_contains_not_all_mandatory_fields_but_all_confirmations_then_raise_invalidation_error(self):
        expected_missing_fields = ['steuernummer', 'bundesland', 'familienstand', 'person_a_dob',
                                   'person_a_last_name', 'person_a_first_name', 'person_a_religion', 'person_a_street',
                                   'person_a_street_number', 'person_a_plz', 'person_a_town', 'person_a_blind',
                                   'person_a_gehbeh', 'steuerminderung', 'iban', 'is_person_a_account_holder', ]
        with app.app_context() and app.test_request_context():
            existing_idnr = '04452397610'
            self._create_logged_in_user(existing_idnr)
            form_data = {'person_a_idnr': existing_idnr,

                         'confirm_complete_correct': True,
                         'confirm_data_privacy': True,
                         'declaration_edaten': True,
                         'declaration_incomes': True,
                         'confirm_terms_of_service': True,
                         }

            with self.assertRaises(MandatoryFieldMissingValidationError) as mandatory_exception:
                LotseMultiStepFlow._validate_input(form_data)
            self.assertEqual(expected_missing_fields, mandatory_exception.exception.missing_fields)

    def test_if_familienstand_missing_then_raise_invalidation_error(self):
        expected_missing_fields = ['familienstand']

        with app.app_context() and app.test_request_context():
            existing_idnr = '04452397610'
            self._create_logged_in_user(existing_idnr)
            form_data = {**self.valid_data_single,
                         **{'person_a_idnr': existing_idnr,

                            'declaration_edaten': True,
                            'declaration_incomes': True,
                            'confirm_data_privacy': True,
                            'confirm_complete_correct': True,
                            'confirm_terms_of_service': True,
                            }}
            form_data.pop('familienstand')

            with self.assertRaises(MandatoryFieldMissingValidationError) as mandatory_exception:
                LotseMultiStepFlow._validate_input(form_data)
            self.assertEqual(expected_missing_fields, mandatory_exception.exception.missing_fields)

    def test_if_input_data_valid_then_raise_no_error(self):
        with app.app_context() and app.test_request_context():
            existing_idnr = '04452397610'
            self._create_logged_in_user(existing_idnr)
            form_data = {**self.valid_data_single,
                         **{'person_a_idnr': existing_idnr,

                            'declaration_edaten': True,
                            'declaration_incomes': True,
                            'confirm_data_privacy': True,
                            'confirm_complete_correct': True,
                            'confirm_terms_of_service': True,
                            }}
            try:
                LotseMultiStepFlow._validate_input(form_data)
            except InputDataInvalidError:
                self.fail("_validate_input raised unexpected InputDataInvalidError")

    def tearDown(self) -> None:
        db.drop_all()


class TestLotseValidateMandatoryFields(unittest.TestCase):

    def test_if_mandatory_form_data_raises_exception_then_raise_madatory_fields_error(self):
        form_data = {'person_a_idnr': 'ID_NR',
                     'steuernummer': 'STEUERNUMMER'}
        expected_missing_fields = ["first_missing_error", "second_missing_error"]
        validation_error = ValidationError([ErrorWrapper(MissingError(), loc=expected_missing_fields[0]),
                                            ErrorWrapper(MissingError(), loc=expected_missing_fields[1])],
                                           MandatoryFormData)

        with patch('app.forms.flows.lotse_flow.MandatoryFormData.parse_obj', MagicMock(side_effect=validation_error)):
            with self.assertRaises(MandatoryFieldMissingValidationError) as mandatory_exception:
                LotseMultiStepFlow._validate_mandatory_fields(form_data)
            self.assertEqual(expected_missing_fields, mandatory_exception.exception.missing_fields)

    def test_if_mandatory_form_data_raises_no_exception_then_raise_no_mandatory_fields_error(self):
        form_data = {'person_a_idnr': 'ID_NR',
                     'steuernummer': 'STEUERNUMMER'}
        with patch('app.forms.flows.lotse_flow.MandatoryFormData.parse_obj'):
            try:
                LotseMultiStepFlow._validate_mandatory_fields(form_data)
            except MandatoryFieldMissingValidationError:
                self.fail("_validate_mandatory_fields raised unexpected MandatoryFieldMissingValidationError")
