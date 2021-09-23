import unittest
from unittest.mock import patch, MagicMock

import pytest
from flask.sessions import SecureCookieSession
from flask_babel import ngettext
from pydantic import ValidationError
from werkzeug.datastructures import ImmutableMultiDict
from werkzeug.exceptions import NotFound

from app.forms.flows.eligibility_step_chooser import EligibilityStepChooser, _ELIGIBILITY_DATA_KEY
from app.forms.session_data import deserialize_session_data
from app.forms.steps.eligibility_steps import MarriedJointTaxesEligibilityFailureDisplaySteuerlotseStep, \
    MarriedJointTaxesDecisionEligibilityInputFormSteuerlotseStep, \
    MarriedAlimonyDecisionEligibilityInputFormSteuerlotseStep, IncorrectEligibilityData, \
    UserAElsterAccountEligibilityInputFormSteuerlotseStep, MarriedAlimonyEligibilityFailureDisplaySteuerlotseStep, \
    UserBElsterAccountDecisionEligibilityInputFormSteuerlotseStep, PensionDecisionEligibilityInputFormSteuerlotseStep, \
    DivorcedJointTaxesDecisionEligibilityInputFormSteuerlotseStep, \
    DivorcedJointTaxesEligibilityFailureDisplaySteuerlotseStep, \
    SingleAlimonyDecisionEligibilityInputFormSteuerlotseStep, SingleAlimonyEligibilityFailureDisplaySteuerlotseStep, \
    SingleElsterAccountDecisionEligibilityInputFormSteuerlotseStep, PensionEligibilityFailureDisplaySteuerlotseStep, \
    InvestmentIncomeDecisionEligibilityInputFormSteuerlotseStep, EmploymentDecisionEligibilityInputFormSteuerlotseStep, \
    TaxedInvestmentIncomeEligibilityFailureDisplaySteuerlotseStep, \
    MinimalInvestmentIncomeDecisionEligibilityInputFormSteuerlotseStep, \
    TaxedInvestmentIncomeDecisionEligibilityInputFormSteuerlotseStep, \
    CheaperCheckDecisionEligibilityInputFormSteuerlotseStep, CheaperCheckEligibilityFailureDisplaySteuerlotseStep, \
    MarginalEmploymentIncomeDecisionEligibilityInputFormSteuerlotseStep, \
    IncomeOtherDecisionEligibilityInputFormSteuerlotseStep, \
    MarginalEmploymentIncomeEligibilityFailureDisplaySteuerlotseStep, \
    IncomeOtherEligibilityFailureDisplaySteuerlotseStep, ForeignCountriesDecisionEligibilityInputFormSteuerlotseStep, \
    ForeignCountriesEligibilityFailureDisplaySteuerlotseStep, EligibilitySuccessDisplaySteuerlotseStep, \
    SeparatedEligibilityInputFormSteuerlotseStep, MaritalStatusInputFormSteuerlotseStep, \
    EligibilityStepMixin, SeparatedLivedTogetherEligibilityInputFormSteuerlotseStep, \
    EligibilityStartDisplaySteuerlotseStep, SeparatedJointTaxesEligibilityInputFormSteuerlotseStep, \
    data_fits_data_model_from_list, data_fits_data_model, \
    ElsterRegistrationMethodEligibilityDecisionStep, ElsterRegistrationMethodEligibilityFailureStep
from app.forms.steps.steuerlotse_step import RedirectSteuerlotseStep
from app.model.recursive_data import PreviousFieldsMissingError
from tests.forms.mock_steuerlotse_steps import MockRenderStep, MockStartStep, MockFormStep, MockFinalStep, \
    MockDecisionEligibilityInputFormSteuerlotseStep
from tests.utils import create_session_form_data

FULL_SESSION_DATA = {'marital_status_eligibility': 'single',
                     'separated_since_last_year_eligibility': 'no',
                     'separated_lived_together_eligibility': 'no',
                     'separated_joint_taxes_eligibility': 'no',
                     'joint_taxes_eligibility': 'no',
                     'alimony_eligibility': 'no',
                     'user_a_has_elster_account_eligibility': 'no',
                     'user_b_has_elster_account_eligibility': 'no',
                     'elster_registration_method_eligibility': 'none',
                     'pension_eligibility': 'yes',
                     'investment_income_eligibility': 'no',
                     'minimal_investment_income_eligibility': 'yes',
                     'taxed_investment_income_eligibility': 'no',
                     'cheaper_check_eligibility': 'no',
                     'employment_income_eligibility': 'no',
                     'marginal_employment_eligibility': 'yes',
                     'other_income_eligibility': 'no',
                     'foreign_country_eligibility': 'no'}


class TestEligibilityStepChooser(unittest.TestCase):
    @pytest.fixture(autouse=True)
    def attach_fixtures(self, test_request_context):
        self.req = test_request_context

    def setUp(self):
        testing_steps = [MockStartStep, MockRenderStep, MockFormStep, MockFinalStep]
        testing_steps_dict = {s.name: s for s in testing_steps}
        self.endpoint_correct = "eligibility"
        self.step_chooser = EligibilityStepChooser(endpoint=self.endpoint_correct)
        self.step_chooser.steps = testing_steps_dict
        self.step_chooser.step_order = [s.name for s in testing_steps]
        self.step_chooser.first_step = next(iter(testing_steps_dict.values()))
        self.stored_data = self.step_chooser.default_data()

        # Set sessions up
        self.existing_session = "sessionAvailable"
        self.session_data = {'renten': 'yes', 'pensionen': 'yes', 'geringf': 'yes',
                             'kapitaleink': 'yes', 'other': 'no'}

    def test_if_correct_step_name_then_return_correct_step(self):
        response_step = self.step_chooser.get_correct_step(MockRenderStep.name)

        self.assertIsInstance(response_step, MockRenderStep)

    def test_if_incorrect_step_name_then_raise_404_exception(self):
        self.assertRaises(NotFound, self.step_chooser.get_correct_step, "Incorrect Step Name")

    def test_if_start_step_then_return_redirect_step(self):
        self.step_chooser.default_data = lambda: None
        response_step = self.step_chooser.get_correct_step("start")

        self.assertIsInstance(response_step, RedirectSteuerlotseStep)
        self.assertEqual(response_step.redirection_step_name, MockStartStep.name)
        self.assertEqual(response_step.endpoint, self.endpoint_correct)


class TestEligibilityStepSpecificsMixin(unittest.TestCase):

    def test_if_married_and_joint_taxes_false_then_return_2(self):
        input_data = {'marital_status_eligibility': 'married',
                      'separated_since_last_year_eligibility': 'no',
                      'joint_taxes_eligibility': 'yes', }
        num_of_users = EligibilityStepMixin().number_of_users(input_data)

        self.assertEqual(2, num_of_users)

    def test_if_married_and_joint_taxes_true_then_return_2(self):
        input_data = {'marital_status_eligibility': 'married',
                      'separated_since_last_year_eligibility': 'no',
                      'joint_taxes_eligibility': 'yes', }
        num_of_users = EligibilityStepMixin().number_of_users(input_data)

        self.assertEqual(2, num_of_users)

    def test_if_data_incorrect_then_return_1(self):
        input_data = {'marital_status_eligibility': 'widowed'}
        num_of_users = EligibilityStepMixin().number_of_users(input_data)

        self.assertEqual(1, num_of_users)


class TestDataFitsDataModel:

    def test_if_model_fails_then_return_false(self):
        failing_model = MagicMock(parse_obj=MagicMock(side_effect=ValidationError([], None)))
        result = data_fits_data_model(failing_model, {})

        assert result is False

    def test_if_model_does_not_fail_then_return_true(self):
        succeeding_model = MagicMock()
        result = data_fits_data_model(succeeding_model, {})

        assert result is True


class TestDataFitsOneDataModel:

    def test_if_all_models_fail_then_return_false(self):
        failing_model = MagicMock(parse_obj=MagicMock(side_effect=ValidationError([], None)))
        models = [failing_model, failing_model, failing_model]
        result = data_fits_data_model_from_list(models, {})

        assert result is False

    def test_if_one_model_does_not_fail_then_return_true(self):
        failing_model = MagicMock(parse_obj=MagicMock(side_effect=ValidationError([], None)))
        succeeding_model = MagicMock()
        models = [failing_model, succeeding_model, failing_model]
        result = data_fits_data_model_from_list(models, {})

        assert result is True

    def test_if_all_models_does_not_fail_then_return_true(self):
        succeeding_model = MagicMock()
        models = [succeeding_model, succeeding_model, succeeding_model]
        result = data_fits_data_model_from_list(models, {})

        assert result is True


class TestEligibilityInputFormSteuerlotseStepIsPreviousStep(unittest.TestCase):
    def setUp(self):
        self.step = MockDecisionEligibilityInputFormSteuerlotseStep
        self.valid_data_model = MagicMock(parse_obj=MagicMock(return_value=None))
        self.invalid_data_model = MagicMock(parse_obj=MagicMock(side_effect=ValidationError([], None)))

    def test_if_one_model_and_data_valid_for_model_then_return_true(self):
        self.step.next_step_data_models = [(self.valid_data_model, 'next_step_model')]
        return_value = self.step.is_previous_step('next_step_model', {})
        self.assertTrue(return_value)

    def test_if_one_model_and_data_invalid_for_model_then_return_false(self):
        self.step.next_step_data_models = [(self.invalid_data_model, 'next_step_model')]
        return_value = self.step.is_previous_step('next_step_model', {})
        self.assertFalse(return_value)

    def test_if_multiple_models_and_data_valid_for_one_model_then_return_true(self):
        self.step.next_step_data_models = [(self.valid_data_model, 'next_step_model_1'),
                                           (self.invalid_data_model, 'next_step_model_2')]
        return_value = self.step.is_previous_step('next_step_model_1', {})
        self.assertTrue(return_value)

        self.step.next_step_data_models = [(self.invalid_data_model, 'next_step_model_1'),
                                           (self.valid_data_model, 'next_step_model_2')]
        return_value = self.step.is_previous_step('next_step_model_2', {})
        self.assertTrue(return_value)

    def test_if_multiple_models_and_data_valid_for_both_models_then_return_true_for_first_model(self):
        self.step.next_step_data_models = [(self.valid_data_model, 'next_step_model_1'),
                                           (self.valid_data_model, 'next_step_model_2')]
        return_value = self.step.is_previous_step('next_step_model_1', {})
        self.assertTrue(return_value)

    def test_if_multiple_models_and_data_valid_for_both_models_then_return_true_for_second_model(self):
        self.step.next_step_data_models = [(self.valid_data_model, 'next_step_model_1'),
                                           (self.valid_data_model, 'next_step_model_2')]
        return_value = self.step.is_previous_step('next_step_model_2', {})
        self.assertTrue(return_value)

    def test_if_multiple_models_and_data_invalid_for_both_models_then_return_false(self):
        self.step.next_step_data_models = [(self.invalid_data_model, 'next_step_model_1'),
                                           (self.invalid_data_model, 'next_step_model_2')]
        return_value = self.step.is_previous_step('next_step_model_1', {})
        self.assertFalse(return_value)

    def test_if_multiple_models_and_data_valid_for_both_models_but_next_step_not_matching_then_return_false(self):
        self.step.next_step_data_models = [(self.valid_data_model, 'next_step_model_1'),
                                           (self.valid_data_model, 'next_step_model_2')]
        return_value = self.step.is_previous_step('next_step_model_3', {})
        self.assertFalse(return_value)

    def test_if_given_step_name_is_not_in_next_step_list_then_return_false(self):
        self.step.next_step_data_models = [(self.valid_data_model, 'next_step_1'),
                                           (self.invalid_data_model, 'next_step_model_2')]
        return_value = self.step.is_previous_step('DIFFERENT_STEP', {})
        self.assertFalse(return_value)

    def test_if_matching_model_is_not_given_next_step_name_then_return_false(self):
        self.step.next_step_data_models = [(self.valid_data_model, 'not_actual_next_step'),
                                           (self.invalid_data_model, 'next_step_model_2')]
        return_value = self.step.is_previous_step('actual_next_step', {})
        self.assertFalse(return_value)


class TestEligibilityStartDisplaySteuerlotseStep(unittest.TestCase):
    @pytest.fixture(autouse=True)
    def attach_fixtures(self, app):
        self.app = app

    def test_sets_correct_session_data_to_empty_dict(self):
        session_data = {
            _ELIGIBILITY_DATA_KEY: create_session_form_data({'marital_status_eligibility': 'single'})
        }
        with self.app.test_request_context(method='GET') as req:
            req.session = SecureCookieSession(session_data)
            step = EligibilityStepChooser('eligibility').get_correct_step(
                EligibilityStartDisplaySteuerlotseStep.name)
            step.handle()

            self.assertEqual({}, deserialize_session_data(req.session[_ELIGIBILITY_DATA_KEY]))

    def test_does_not_change_other_session_data(self):
        other_session_key = 'OTHER_SESSION_KEY'
        other_session_data = {'Galileo': 'Figaro - magnificoo'}
        another_session_key = 'ANOTHER_SESSION_KEY'
        another_session_data = {'Scaramouch': 'Fandango'}
        session_data = {
            _ELIGIBILITY_DATA_KEY: create_session_form_data({'marital_status_eligibility': 'single'}),
            other_session_key: create_session_form_data(other_session_data),
            another_session_key: create_session_form_data(another_session_data)
        }

        with self.app.test_request_context(method='GET') as req:
            req.session = SecureCookieSession(session_data)
            step = EligibilityStepChooser('eligibility').get_correct_step(
                EligibilityStartDisplaySteuerlotseStep.name)
            step.handle()

            self.assertEqual(other_session_data, deserialize_session_data(req.session[other_session_key]))
            self.assertEqual(another_session_data, deserialize_session_data(req.session[another_session_key]))

    def test_does_not_add_data_to_empty_session_data(self):
        session_data = {}
        with self.app.test_request_context(method='GET') as req:
            req.session = SecureCookieSession(session_data)
            step = EligibilityStepChooser('eligibility').get_correct_step(
                EligibilityStartDisplaySteuerlotseStep.name)
            step.handle()

            self.assertEqual({}, deserialize_session_data(req.session[_ELIGIBILITY_DATA_KEY]))

    def test_leaves_session_data_without_correct_key_untouched(self):
        other_session_key = 'OTHER_SESSION_KEY'
        other_session_data = {'Galileo': 'Figaro - magnificoo'}
        session_data = {
            other_session_key: create_session_form_data(other_session_data)
        }
        with self.app.test_request_context(method='GET') as req:
            req.session = SecureCookieSession(session_data)
            step = EligibilityStepChooser('eligibility').get_correct_step(
                EligibilityStartDisplaySteuerlotseStep.name)
            step.handle()

            self.assertEqual(other_session_data, deserialize_session_data(req.session[other_session_key]))


class TestMaritalStatusInputFormSteuerlotseStep(unittest.TestCase):
    @pytest.fixture(autouse=True)
    def attach_fixtures(self, app):
        self.app = app

    def test_if_post_and_married_then_set_next_step_correct(self):
        with self.app.test_request_context(method='POST', data={'marital_status_eligibility': 'married'}):
            step = EligibilityStepChooser('eligibility').get_correct_step(
                MaritalStatusInputFormSteuerlotseStep.name)
            expected_url = step.url_for_step(SeparatedEligibilityInputFormSteuerlotseStep.name)
            step.handle()

        self.assertEqual(expected_url, step.render_info.next_url)

    def test_if_post_and_widowed_then_set_next_step_correct(self):
        with self.app.test_request_context(method='POST', data={'marital_status_eligibility': 'widowed'}):
            step = EligibilityStepChooser('eligibility').get_correct_step(
                MaritalStatusInputFormSteuerlotseStep.name)
            expected_url = step.url_for_step(SingleAlimonyDecisionEligibilityInputFormSteuerlotseStep.name)
            step.handle()

        self.assertEqual(expected_url, step.render_info.next_url)

    def test_if_post_and_single_then_set_next_step_correct(self):
        with self.app.test_request_context(method='POST', data={'marital_status_eligibility': 'single'}):
            step = EligibilityStepChooser('eligibility').get_correct_step(
                MaritalStatusInputFormSteuerlotseStep.name)
            expected_url = step.url_for_step(SingleAlimonyDecisionEligibilityInputFormSteuerlotseStep.name)
            step.handle()

        self.assertEqual(expected_url, step.render_info.next_url)

    def test_if_post_and_divorced_then_set_next_step_correct(self):
        with self.app.test_request_context(method='POST', data={'marital_status_eligibility': 'divorced'}):
            step = EligibilityStepChooser('eligibility').get_correct_step(
                MaritalStatusInputFormSteuerlotseStep.name)
            expected_url = step.url_for_step(DivorcedJointTaxesDecisionEligibilityInputFormSteuerlotseStep.name)
            step.handle()

        self.assertEqual(expected_url, step.render_info.next_url)

    def test_set_prev_input_step_correctly(self):
        with self.app.test_request_context(method='GET') as req:
            step = EligibilityStepChooser('eligibility').get_correct_step(
                MaritalStatusInputFormSteuerlotseStep.name)
            expected_url = step.url_for_step(EligibilityStartDisplaySteuerlotseStep.name)
            step.handle()
        self.assertEqual(expected_url, step.render_info.prev_url)

    def test_if_get_and_incorrect_data_from_session_then_delete_incorrect_data(self):
        session_data = {'marital_status_eligibility': 'single', }
        session_data_with_incorrect_key = {**session_data, **{'INCORRECT_KEY': 'UNNECESSARY_VALUE'}}
        with self.app.test_request_context(method='GET') as req:
            req.session = SecureCookieSession(
                {_ELIGIBILITY_DATA_KEY: create_session_form_data(session_data_with_incorrect_key)})
            step = EligibilityStepChooser('eligibility').get_correct_step(
                MaritalStatusInputFormSteuerlotseStep.name)
            step.handle()

            self.assertEqual(session_data,
                             deserialize_session_data(req.session[_ELIGIBILITY_DATA_KEY]))

    def test_if_get_and_correct_data_from_session_then_do_not_delete_any_data(self):
        session_data = {'marital_status_eligibility': 'single', }
        with self.app.test_request_context(method='GET') as req:
            req.session = SecureCookieSession({_ELIGIBILITY_DATA_KEY: create_session_form_data(session_data)})
            step = EligibilityStepChooser('eligibility').get_correct_step(
                MaritalStatusInputFormSteuerlotseStep.name)
            step.handle()

            self.assertEqual(session_data,
                             deserialize_session_data(req.session[_ELIGIBILITY_DATA_KEY]))

    def test_if_get_and_full_data_from_session_then_delete_unnecessary_data(self):
        only_necessary_data = {'marital_status_eligibility': 'single', }
        with self.app.test_request_context(method='GET') as req:
            req.session = SecureCookieSession({_ELIGIBILITY_DATA_KEY: create_session_form_data(FULL_SESSION_DATA)})
            step = EligibilityStepChooser('eligibility').get_correct_step(
                MaritalStatusInputFormSteuerlotseStep.name)
            step.handle()

            self.assertEqual(only_necessary_data,
                             deserialize_session_data(req.session[_ELIGIBILITY_DATA_KEY]))


class TestSeparatedEligibilityInputFormSteuerlotseStep(unittest.TestCase):
    @pytest.fixture(autouse=True)
    def attach_fixtures(self, app):
        self.app = app

    def setUp(self):
        self.correct_session_data = {'marital_status_eligibility': 'married'}

    def test_if_post_and_session_data_correct_and_input_data_correct_than_set_next_input_step(self):
        with self.app.test_request_context(method='POST', data={'separated_since_last_year_eligibility': 'yes'}) as req:
            req.session = SecureCookieSession(
                {_ELIGIBILITY_DATA_KEY: create_session_form_data(self.correct_session_data)})
            step = EligibilityStepChooser('eligibility').get_correct_step(
                SeparatedEligibilityInputFormSteuerlotseStep.name)
            expected_url = step.url_for_step(SeparatedLivedTogetherEligibilityInputFormSteuerlotseStep.name)
            step.handle()

        self.assertEqual(expected_url, step.render_info.next_url)

    def test_if_post_and_session_data_correct_and_input_data_incorrect_than_set_next_url_to_alternative_step(self):
        with self.app.test_request_context(method='POST', data={'separated_since_last_year_eligibility': 'no'}) as req:
            req.session = SecureCookieSession(
                {_ELIGIBILITY_DATA_KEY: create_session_form_data(self.correct_session_data)})
            step = EligibilityStepChooser('eligibility').get_correct_step(
                SeparatedEligibilityInputFormSteuerlotseStep.name)
            expected_url = step.url_for_step(MarriedJointTaxesDecisionEligibilityInputFormSteuerlotseStep.name)
            step.handle()

        self.assertEqual(expected_url, step.render_info.next_url)

    def test_if_session_data_correct_then_set_prev_input_step_correctly(self):
        with self.app.test_request_context(method='GET') as req:
            req.session = SecureCookieSession(
                {_ELIGIBILITY_DATA_KEY: create_session_form_data(self.correct_session_data)})
            step = EligibilityStepChooser('eligibility').get_correct_step(
                SeparatedEligibilityInputFormSteuerlotseStep.name)
            expected_url = step.url_for_step(MaritalStatusInputFormSteuerlotseStep.name)
            step.handle()
        self.assertEqual(expected_url, step.render_info.prev_url)

    def test_if_post_and_data_from_before_invalid_then_raise_incorrect_eligibility_data_error(self):
        with self.app.test_request_context(method='POST', data={'separated_since_last_year_eligibility': 'yes'}), \
                patch('app.model.recursive_data.RecursiveDataModel.one_previous_field_has_to_be_set',
                      MagicMock(side_effect=PreviousFieldsMissingError)):
            step = EligibilityStepChooser('eligibility').get_correct_step(
                SeparatedEligibilityInputFormSteuerlotseStep.name)

            self.assertRaises(IncorrectEligibilityData, step.handle)

    def test_if_get_and_incorrect_data_from_session_then_delete_incorrect_data(self):
        session_data = {'marital_status_eligibility': 'single',
                        'separated_since_last_year_eligibility': 'no', }
        session_data_with_incorrect_key = {**session_data, **{'INCORRECT_KEY': 'UNNECESSARY_VALUE'}}
        with self.app.test_request_context(method='GET') as req:
            req.session = SecureCookieSession(
                {_ELIGIBILITY_DATA_KEY: create_session_form_data(session_data_with_incorrect_key)})
            step = EligibilityStepChooser('eligibility').get_correct_step(
                SeparatedEligibilityInputFormSteuerlotseStep.name)
            step.handle()

            self.assertEqual(session_data,
                             deserialize_session_data(req.session[_ELIGIBILITY_DATA_KEY]))

    def test_if_get_and_correct_data_from_session_then_do_not_delete_any_data(self):
        session_data = {'marital_status_eligibility': 'single',
                        'separated_since_last_year_eligibility': 'no', }
        with self.app.test_request_context(method='GET') as req:
            req.session = SecureCookieSession({_ELIGIBILITY_DATA_KEY: create_session_form_data(session_data)})
            step = EligibilityStepChooser('eligibility').get_correct_step(
                SeparatedEligibilityInputFormSteuerlotseStep.name)
            step.handle()

            self.assertEqual(session_data,
                             deserialize_session_data(req.session[_ELIGIBILITY_DATA_KEY]))

    def test_if_get_and_full_data_from_session_then_delete_unnecessary_data(self):
        only_necessary_data = {'marital_status_eligibility': 'single',
                               'separated_since_last_year_eligibility': 'no', }
        with self.app.test_request_context(method='GET') as req:
            req.session = SecureCookieSession({_ELIGIBILITY_DATA_KEY: create_session_form_data(FULL_SESSION_DATA)})
            step = EligibilityStepChooser('eligibility').get_correct_step(
                SeparatedEligibilityInputFormSteuerlotseStep.name)
            step.handle()

            self.assertEqual(only_necessary_data,
                             deserialize_session_data(req.session[_ELIGIBILITY_DATA_KEY]))


class TestSeparatedLivedTogetherEligibilityInputFormSteuerlotseStep(unittest.TestCase):
    @pytest.fixture(autouse=True)
    def attach_fixtures(self, app):
        self.app = app

    def setUp(self):
        self.correct_session_data = {'marital_status_eligibility': 'married',
                                     'separated_since_last_year_eligibility': 'yes'}

    def test_if_post_and_session_data_correct_and_input_data_correct_then_set_next_input_step(self):
        with self.app.test_request_context(method='POST', data={'separated_lived_together_eligibility': 'yes'}) as req:
            req.session = SecureCookieSession(
                {_ELIGIBILITY_DATA_KEY: create_session_form_data(self.correct_session_data)})
            step = EligibilityStepChooser('eligibility').get_correct_step(
                SeparatedLivedTogetherEligibilityInputFormSteuerlotseStep.name)
            expected_url = step.url_for_step(SeparatedJointTaxesEligibilityInputFormSteuerlotseStep.name)
            step.handle()

        self.assertEqual(expected_url, step.render_info.next_url)

    def test_if_post_and_session_data_correct_and_input_data_incorrect_than_set_next_url_to_alternative_step(self):
        with self.app.test_request_context(method='POST', data={'separated_lived_together_eligibility': 'no'}) as req:
            req.session = SecureCookieSession(
                {_ELIGIBILITY_DATA_KEY: create_session_form_data(self.correct_session_data)})
            step = EligibilityStepChooser('eligibility').get_correct_step(
                SeparatedLivedTogetherEligibilityInputFormSteuerlotseStep.name)
            expected_url = step.url_for_step(SingleAlimonyDecisionEligibilityInputFormSteuerlotseStep.name)
            step.handle()

        self.assertEqual(expected_url, step.render_info.next_url)

    def test_if_session_data_correct_then_set_prev_input_step_correctly(self):
        with self.app.test_request_context(method='GET') as req:
            req.session = SecureCookieSession(
                {_ELIGIBILITY_DATA_KEY: create_session_form_data(self.correct_session_data)})
            step = EligibilityStepChooser('eligibility').get_correct_step(
                SeparatedLivedTogetherEligibilityInputFormSteuerlotseStep.name)
            expected_url = step.url_for_step(SeparatedEligibilityInputFormSteuerlotseStep.name)
            step.handle()
        self.assertEqual(expected_url, step.render_info.prev_url)

    def test_if_post_and_data_from_before_invalid_then_raise_incorrect_eligibility_data_error(self):
        with self.app.test_request_context(method='POST', data={'separated_lived_together_eligibility': 'yes'}), \
                patch('app.model.recursive_data.RecursiveDataModel.one_previous_field_has_to_be_set',
                      MagicMock(side_effect=PreviousFieldsMissingError)):
            step = EligibilityStepChooser('eligibility').get_correct_step(
                SeparatedLivedTogetherEligibilityInputFormSteuerlotseStep.name)

            self.assertRaises(IncorrectEligibilityData, step.handle)

    def test_if_get_and_incorrect_data_from_session_then_delete_incorrect_data(self):
        session_data = {'marital_status_eligibility': 'married',
                        'separated_since_last_year_eligibility': 'yes', }
        session_data_with_incorrect_key = {**session_data, **{'INCORRECT_KEY': 'UNNECESSARY_VALUE'}}
        with self.app.test_request_context(method='GET') as req:
            req.session = SecureCookieSession(
                {_ELIGIBILITY_DATA_KEY: create_session_form_data(session_data_with_incorrect_key)})
            step = EligibilityStepChooser('eligibility').get_correct_step(
                SeparatedLivedTogetherEligibilityInputFormSteuerlotseStep.name)
            step.handle()

            self.assertEqual(session_data,
                             deserialize_session_data(req.session[_ELIGIBILITY_DATA_KEY]))

    def test_if_get_and_correct_data_from_session_then_do_not_delete_any_data(self):
        with self.app.test_request_context(method='GET') as req:
            req.session = SecureCookieSession(
                {_ELIGIBILITY_DATA_KEY: create_session_form_data(self.correct_session_data)})
            step = EligibilityStepChooser('eligibility').get_correct_step(
                SeparatedLivedTogetherEligibilityInputFormSteuerlotseStep.name)
            step.handle()

            self.assertEqual(self.correct_session_data,
                             deserialize_session_data(req.session[_ELIGIBILITY_DATA_KEY]))

    def test_if_get_and_full_data_from_session_then_delete_unnecessary_data(self):
        only_necessary_data = {'marital_status_eligibility': 'single',
                               'separated_since_last_year_eligibility': 'no',
                               'separated_lived_together_eligibility': 'no', }
        with self.app.test_request_context(method='GET') as req:
            req.session = SecureCookieSession({_ELIGIBILITY_DATA_KEY: create_session_form_data(FULL_SESSION_DATA)})
            step = EligibilityStepChooser('eligibility').get_correct_step(
                SeparatedLivedTogetherEligibilityInputFormSteuerlotseStep.name)
            step.handle()

            self.assertEqual(only_necessary_data,
                             deserialize_session_data(req.session[_ELIGIBILITY_DATA_KEY]))


class TestSeparatedJointTaxesEligibilityInputFormSteuerlotseStep(unittest.TestCase):
    @pytest.fixture(autouse=True)
    def attach_fixtures(self, app):
        self.app = app

    def setUp(self):
        self.correct_session_data = {'marital_status_eligibility': 'married',
                                     'separated_since_last_year_eligibility': 'yes',
                                     'separated_lived_together_eligibility': 'yes'}

    def test_if_post_and_session_data_correct_and_input_data_correct_then_set_next_input_step(self):
        with self.app.test_request_context(method='POST', data={'separated_joint_taxes_eligibility': 'yes'}) as req:
            req.session = SecureCookieSession(
                {_ELIGIBILITY_DATA_KEY: create_session_form_data(self.correct_session_data)})
            step = EligibilityStepChooser('eligibility').get_correct_step(
                SeparatedJointTaxesEligibilityInputFormSteuerlotseStep.name)
            expected_url = step.url_for_step(MarriedAlimonyDecisionEligibilityInputFormSteuerlotseStep.name)
            step.handle()

        self.assertEqual(expected_url, step.render_info.next_url)

    def test_if_post_and_session_data_correct_and_input_data_incorrect_than_set_next_url_to_alternative_step(self):
        with self.app.test_request_context(method='POST', data={'separated_joint_taxes_eligibility': 'no'}) as req:
            req.session = SecureCookieSession(
                {_ELIGIBILITY_DATA_KEY: create_session_form_data(self.correct_session_data)})
            step = EligibilityStepChooser('eligibility').get_correct_step(
                SeparatedJointTaxesEligibilityInputFormSteuerlotseStep.name)
            expected_url = step.url_for_step(SingleAlimonyDecisionEligibilityInputFormSteuerlotseStep.name)
            step.handle()

        self.assertEqual(expected_url, step.render_info.next_url)

    def test_if_session_data_correct_then_set_prev_input_step_correctly(self):
        with self.app.test_request_context(method='GET') as req:
            req.session = SecureCookieSession(
                {_ELIGIBILITY_DATA_KEY: create_session_form_data(self.correct_session_data)})
            step = EligibilityStepChooser('eligibility').get_correct_step(
                SeparatedJointTaxesEligibilityInputFormSteuerlotseStep.name)
            expected_url = step.url_for_step(SeparatedLivedTogetherEligibilityInputFormSteuerlotseStep.name)
            step.handle()
        self.assertEqual(expected_url, step.render_info.prev_url)

    def test_if_post_and_data_from_before_invalid_then_raise_incorrect_eligibility_data_error(self):
        with self.app.test_request_context(method='POST', data={'separated_joint_taxes_eligibility': 'yes'}), \
                patch('app.model.recursive_data.RecursiveDataModel.one_previous_field_has_to_be_set',
                      MagicMock(side_effect=PreviousFieldsMissingError)):
            step = EligibilityStepChooser('eligibility').get_correct_step(
                SeparatedJointTaxesEligibilityInputFormSteuerlotseStep.name)

            self.assertRaises(IncorrectEligibilityData, step.handle)

    def test_if_get_and_incorrect_data_from_session_then_delete_incorrect_data(self):
        session_data_with_incorrect_key = {**self.correct_session_data, **{'INCORRECT_KEY': 'UNNECESSARY_VALUE'}}
        with self.app.test_request_context(method='GET') as req:
            req.session = SecureCookieSession(
                {_ELIGIBILITY_DATA_KEY: create_session_form_data(session_data_with_incorrect_key)})
            step = EligibilityStepChooser('eligibility').get_correct_step(
                SeparatedJointTaxesEligibilityInputFormSteuerlotseStep.name)
            step.handle()

            self.assertEqual(self.correct_session_data,
                             deserialize_session_data(req.session[_ELIGIBILITY_DATA_KEY]))

    def test_if_get_and_correct_data_from_session_then_do_not_delete_any_data(self):
        with self.app.test_request_context(method='GET') as req:
            req.session = SecureCookieSession(
                {_ELIGIBILITY_DATA_KEY: create_session_form_data(self.correct_session_data)})
            step = EligibilityStepChooser('eligibility').get_correct_step(
                SeparatedJointTaxesEligibilityInputFormSteuerlotseStep.name)
            step.handle()

            self.assertEqual(self.correct_session_data,
                             deserialize_session_data(req.session[_ELIGIBILITY_DATA_KEY]))

    def test_if_get_and_full_data_from_session_then_delete_unnecessary_data(self):
        only_necessary_data = {'marital_status_eligibility': 'single',
                               'separated_since_last_year_eligibility': 'no',
                               'separated_lived_together_eligibility': 'no',
                               'separated_joint_taxes_eligibility': 'no', }
        with self.app.test_request_context(method='GET') as req:
            req.session = SecureCookieSession({_ELIGIBILITY_DATA_KEY: create_session_form_data(FULL_SESSION_DATA)})
            step = EligibilityStepChooser('eligibility').get_correct_step(
                SeparatedJointTaxesEligibilityInputFormSteuerlotseStep.name)
            step.handle()

            self.assertEqual(only_necessary_data,
                             deserialize_session_data(req.session[_ELIGIBILITY_DATA_KEY]))


class TestMarriedJointTaxesEligibilityFailureDisplaySteuerlotseStep(unittest.TestCase):
    @pytest.fixture(autouse=True)
    def attach_fixtures(self, app):
        self.app = app

    def test_handle_sets_correct_prev_url(self):
        with self.app.test_request_context():
            step = MarriedJointTaxesEligibilityFailureDisplaySteuerlotseStep(endpoint='eligibility')
            expected_url = step.url_for_step(MarriedJointTaxesDecisionEligibilityInputFormSteuerlotseStep.name)
            step.handle()

        self.assertEqual(expected_url, step.render_info.prev_url)


class TestMarriedJointTaxesDecisionEligibilityInputFormSteuerlotseStep(unittest.TestCase):
    @pytest.fixture(autouse=True)
    def attach_fixtures(self, app):
        self.app = app

    def setUp(self):
        self.correct_session_data = {'marital_status_eligibility': 'married',
                                     'separated_since_last_year_eligibility': 'no'}

    def test_if_post_and_session_data_correct_and_input_data_correct_than_set_next_input_step(self):
        with self.app.test_request_context(method='POST', data={'joint_taxes_eligibility': 'yes'}) as req:
            req.session = SecureCookieSession(
                {_ELIGIBILITY_DATA_KEY: create_session_form_data(self.correct_session_data)})
            step = EligibilityStepChooser('eligibility').get_correct_step(
                MarriedJointTaxesDecisionEligibilityInputFormSteuerlotseStep.name)
            expected_url = step.url_for_step(MarriedAlimonyDecisionEligibilityInputFormSteuerlotseStep.name)
            step.handle()

        self.assertEqual(expected_url, step.render_info.next_url)

    def test_if_post_and_session_data_correct_and_input_data_incorrect_than_set_next_url_to_failure_step(self):
        with self.app.test_request_context(method='POST', data={'joint_taxes_eligibility': 'no'}) as req:
            req.session = SecureCookieSession(
                {_ELIGIBILITY_DATA_KEY: create_session_form_data(self.correct_session_data)})
            step = EligibilityStepChooser('eligibility').get_correct_step(
                MarriedJointTaxesDecisionEligibilityInputFormSteuerlotseStep.name)
            expected_url = step.url_for_step(MarriedJointTaxesEligibilityFailureDisplaySteuerlotseStep.name)
            step.handle()

        self.assertEqual(expected_url, step.render_info.next_url)

    def test_if_session_data_correct_then_set_prev_input_step_correctly(self):
        with self.app.test_request_context(method='GET') as req:
            req.session = SecureCookieSession(
                {_ELIGIBILITY_DATA_KEY: create_session_form_data(self.correct_session_data)})
            step = EligibilityStepChooser('eligibility').get_correct_step(
                MarriedJointTaxesDecisionEligibilityInputFormSteuerlotseStep.name)
            expected_url = step.url_for_step(SeparatedEligibilityInputFormSteuerlotseStep.name)
            step.handle()
        self.assertEqual(expected_url, step.render_info.prev_url)

    def test_if_post_and_data_from_before_invalid_then_raise_incorrect_eligibility_data_error(self):
        with self.app.test_request_context(method='POST', data={'joint_taxes_eligibility': 'yes'}), \
                patch('app.model.recursive_data.RecursiveDataModel.one_previous_field_has_to_be_set',
                      MagicMock(side_effect=PreviousFieldsMissingError)):
            step = EligibilityStepChooser('eligibility').get_correct_step(
                MarriedJointTaxesDecisionEligibilityInputFormSteuerlotseStep.name)

            self.assertRaises(IncorrectEligibilityData, step.handle)

    def test_if_get_and_incorrect_data_from_session_then_delete_incorrect_data(self):
        session_data = {'marital_status_eligibility': 'single',
                        'separated_since_last_year_eligibility': 'no',
                        'joint_taxes_eligibility': 'no', }
        session_data_with_incorrect_key = {**session_data, **{'INCORRECT_KEY': 'UNNECESSARY_VALUE'}}
        with self.app.test_request_context(method='GET') as req:
            req.session = SecureCookieSession(
                {_ELIGIBILITY_DATA_KEY: create_session_form_data(session_data_with_incorrect_key)})
            step = EligibilityStepChooser('eligibility').get_correct_step(
                MarriedJointTaxesDecisionEligibilityInputFormSteuerlotseStep.name)
            step.handle()

            self.assertEqual(session_data,
                             deserialize_session_data(req.session[_ELIGIBILITY_DATA_KEY]))

    def test_if_get_and_correct_data_from_session_then_do_not_delete_any_data(self):
        session_data = {'marital_status_eligibility': 'single',
                        'separated_since_last_year_eligibility': 'no',
                        'joint_taxes_eligibility': 'no', }
        with self.app.test_request_context(method='GET') as req:
            req.session = SecureCookieSession({_ELIGIBILITY_DATA_KEY: create_session_form_data(session_data)})
            step = EligibilityStepChooser('eligibility').get_correct_step(
                MarriedJointTaxesDecisionEligibilityInputFormSteuerlotseStep.name)
            step.handle()

            self.assertEqual(session_data,
                             deserialize_session_data(req.session[_ELIGIBILITY_DATA_KEY]))

    def test_if_get_and_full_data_from_session_then_delete_unnecessary_data(self):
        only_necessary_data = {'marital_status_eligibility': 'single',
                               'separated_since_last_year_eligibility': 'no',
                               'joint_taxes_eligibility': 'no', }
        with self.app.test_request_context(method='GET') as req:
            req.session = SecureCookieSession({_ELIGIBILITY_DATA_KEY: create_session_form_data(FULL_SESSION_DATA)})
            step = EligibilityStepChooser('eligibility').get_correct_step(
                MarriedJointTaxesDecisionEligibilityInputFormSteuerlotseStep.name)
            step.handle()

            self.assertEqual(only_necessary_data,
                             deserialize_session_data(req.session[_ELIGIBILITY_DATA_KEY]))


class TestMarriedAlimonyEligibilityFailureDisplaySteuerlotseStep(unittest.TestCase):
    @pytest.fixture(autouse=True)
    def attach_fixtures(self, test_request_context):
        self.test_request_context = test_request_context

    def test_handle_sets_correct_prev_url(self):
        step = MarriedAlimonyEligibilityFailureDisplaySteuerlotseStep(endpoint='eligibility')
        expected_url = step.url_for_step(MarriedAlimonyDecisionEligibilityInputFormSteuerlotseStep.name)
        step.handle()

        self.assertEqual(expected_url, step.render_info.prev_url)


class TestMarriedAlimonyDecisionEligibilityInputFormSteuerlotseStep(unittest.TestCase):
    @pytest.fixture(autouse=True)
    def attach_fixtures(self, app):
        self.app = app

    def setUp(self):
        self.correct_session_data = {'marital_status_eligibility': 'married',
                                     'separated_since_last_year_eligibility': 'no',
                                     'joint_taxes_eligibility': 'yes'}

    def test_if_post_and_session_data_correct_and_input_data_correct_than_set_next_input_step(self):
        with self.app.test_request_context(method='POST', data={'alimony_eligibility': 'no'}) as req:
            req.session = SecureCookieSession(
                {_ELIGIBILITY_DATA_KEY: create_session_form_data(self.correct_session_data)})
            step = EligibilityStepChooser('eligibility').get_correct_step(
                MarriedAlimonyDecisionEligibilityInputFormSteuerlotseStep.name)
            expected_url = step.url_for_step(UserAElsterAccountEligibilityInputFormSteuerlotseStep.name)
            step.handle()

        self.assertEqual(expected_url, step.render_info.next_url)

    def test_if_post_and_session_data_correct_and_input_data_incorrect_than_set_next_url_to_failure_step(self):
        with self.app.test_request_context(method='POST', data={'alimony_eligibility': 'yes'}) as req:
            req.session = SecureCookieSession(
                {_ELIGIBILITY_DATA_KEY: create_session_form_data(self.correct_session_data)})
            step = EligibilityStepChooser('eligibility').get_correct_step(
                MarriedAlimonyDecisionEligibilityInputFormSteuerlotseStep.name)
            expected_url = step.url_for_step(MarriedAlimonyEligibilityFailureDisplaySteuerlotseStep.name)
            step.handle()

        self.assertEqual(expected_url, step.render_info.next_url)

    def test_if_not_separated_then_set_prev_input_step_correctly(self):
        with self.app.test_request_context(method='GET') as req:
            req.session = SecureCookieSession(
                {_ELIGIBILITY_DATA_KEY: create_session_form_data(self.correct_session_data)})
            step = EligibilityStepChooser('eligibility').get_correct_step(
                MarriedAlimonyDecisionEligibilityInputFormSteuerlotseStep.name)
            expected_url = step.url_for_step(MarriedJointTaxesDecisionEligibilityInputFormSteuerlotseStep.name)
            step.handle()
        self.assertEqual(expected_url, step.render_info.prev_url)

    def test_if_separated_correct_session_data_then_set_prev_input_step_correctly(self):
        alternative_data = {**self.correct_session_data, **{'separated_since_last_year_eligibility': 'yes',
                                                            'separated_lived_together_eligibility': 'yes',
                                                            'separated_joint_taxes_eligibility': 'yes'}}
        with self.app.test_request_context(method='GET') as req:
            req.session = SecureCookieSession({_ELIGIBILITY_DATA_KEY: create_session_form_data(alternative_data)})
            step = EligibilityStepChooser('eligibility').get_correct_step(
                MarriedAlimonyDecisionEligibilityInputFormSteuerlotseStep.name)
            expected_url = step.url_for_step(SeparatedJointTaxesEligibilityInputFormSteuerlotseStep.name)
            step.handle()
        self.assertEqual(expected_url, step.render_info.prev_url)

    def test_if_post_and_data_from_before_invalid_then_raise_incorrect_eligibility_data_error(self):
        with self.app.test_request_context(method='POST', data={'alimony_eligibility': 'no'}), \
                patch('app.model.recursive_data.RecursiveDataModel.one_previous_field_has_to_be_set',
                      MagicMock(side_effect=PreviousFieldsMissingError)):
            step = EligibilityStepChooser('eligibility').get_correct_step(
                MarriedAlimonyDecisionEligibilityInputFormSteuerlotseStep.name)

            self.assertRaises(IncorrectEligibilityData, step.handle)

    def test_if_get_and_incorrect_data_from_session_then_delete_incorrect_data(self):
        session_data = {'marital_status_eligibility': 'single',
                        'separated_since_last_year_eligibility': 'no',
                        'joint_taxes_eligibility': 'no',
                        'alimony_eligibility': 'no', }
        session_data_with_incorrect_key = {**session_data, **{'INCORRECT_KEY': 'UNNECESSARY_VALUE'}}
        with self.app.test_request_context(method='GET') as req:
            req.session = SecureCookieSession(
                {_ELIGIBILITY_DATA_KEY: create_session_form_data(session_data_with_incorrect_key)})
            step = EligibilityStepChooser('eligibility').get_correct_step(
                MarriedAlimonyDecisionEligibilityInputFormSteuerlotseStep.name)
            step.handle()

            self.assertEqual(session_data,
                             deserialize_session_data(req.session[_ELIGIBILITY_DATA_KEY]))

    def test_if_get_and_correct_data_from_session_then_do_not_delete_any_data(self):
        session_data = {'marital_status_eligibility': 'single',
                        'separated_since_last_year_eligibility': 'no',
                        'joint_taxes_eligibility': 'no',
                        'alimony_eligibility': 'no', }
        with self.app.test_request_context(method='GET') as req:
            req.session = SecureCookieSession({_ELIGIBILITY_DATA_KEY: create_session_form_data(session_data)})
            step = EligibilityStepChooser('eligibility').get_correct_step(
                MarriedAlimonyDecisionEligibilityInputFormSteuerlotseStep.name)
            step.handle()

            self.assertEqual(session_data,
                             deserialize_session_data(req.session[_ELIGIBILITY_DATA_KEY]))

    def test_if_get_and_full_data_from_session_then_delete_unnecessary_data(self):
        only_necessary_data = {'marital_status_eligibility': 'single',
                               'separated_since_last_year_eligibility': 'no',
                               'separated_joint_taxes_eligibility': 'no',
                               'separated_lived_together_eligibility': 'no',
                               'joint_taxes_eligibility': 'no',
                               'alimony_eligibility': 'no', }
        with self.app.test_request_context(method='GET') as req:
            req.session = SecureCookieSession({_ELIGIBILITY_DATA_KEY: create_session_form_data(FULL_SESSION_DATA)})
            step = EligibilityStepChooser('eligibility').get_correct_step(
                MarriedAlimonyDecisionEligibilityInputFormSteuerlotseStep.name)
            step.handle()

            self.assertEqual(only_necessary_data,
                             deserialize_session_data(req.session[_ELIGIBILITY_DATA_KEY]))

    def test_if_multiple_users_then_show_multiple_text(self):
        session_data = {'marital_status_eligibility': 'married',
                        'separated_since_last_year_eligibility': 'no',
                        'joint_taxes_eligibility': 'yes'}
        expected_number_of_users = 2
        expected_choices = [('yes', ngettext('form.eligibility.alimony.yes', 'form.eligibility.alimony.yes', num=expected_number_of_users)),
                            ('no', ngettext('form.eligibility.alimony.no', 'form.eligibility.alimony.no', num=expected_number_of_users))]
        with self.app.test_request_context(method='GET') as req:
            req.session = SecureCookieSession({_ELIGIBILITY_DATA_KEY: create_session_form_data(session_data)})
            step = EligibilityStepChooser('eligibility').get_correct_step(
                MarriedAlimonyDecisionEligibilityInputFormSteuerlotseStep.name)
            step._pre_handle()

        self.assertEqual(expected_choices, step.form.alimony_eligibility.kwargs['choices'])

    def test_if_single_user_then_show_single_text(self):
        session_data = {'marital_status_eligibility': 'single',
                        'separated_since_last_year_eligibility': 'no',
                        'joint_taxes_eligibility': 'no'}
        expected_number_of_users = 1
        expected_choices = [('yes', ngettext('form.eligibility.alimony.yes', 'form.eligibility.alimony.yes', num=expected_number_of_users)),
                            ('no', ngettext('form.eligibility.alimony.no', 'form.eligibility.alimony.no', num=expected_number_of_users))]
        with self.app.test_request_context(method='GET') as req:
            req.session = SecureCookieSession({_ELIGIBILITY_DATA_KEY: create_session_form_data(session_data)})
            step = EligibilityStepChooser('eligibility').get_correct_step(
                MarriedAlimonyDecisionEligibilityInputFormSteuerlotseStep.name)
            step._pre_handle()

        self.assertEqual(expected_choices, step.form.alimony_eligibility.kwargs['choices'])


class TestUserAElsterAccountEligibilityInputFormSteuerlotseStep(unittest.TestCase):
    @pytest.fixture(autouse=True)
    def attach_fixtures(self, app):
        self.app = app

    def setUp(self):
        self.correct_session_data = {'marital_status_eligibility': 'married',
                                     'separated_since_last_year_eligibility': 'no',
                                     'joint_taxes_eligibility': 'yes',
                                     'alimony_eligibility': 'no'}

    def test_if_post_and_session_data_correct_and_input_data_correct_than_set_next_input_step(self):
        with self.app.test_request_context(method='POST', data={'user_a_has_elster_account_eligibility': 'no'}) as req:
            req.session = SecureCookieSession(
                {_ELIGIBILITY_DATA_KEY: create_session_form_data(self.correct_session_data)})
            step = EligibilityStepChooser('eligibility').get_correct_step(
                UserAElsterAccountEligibilityInputFormSteuerlotseStep.name)
            expected_url = step.url_for_step(PensionDecisionEligibilityInputFormSteuerlotseStep.name)
            step.handle()

        self.assertEqual(expected_url, step.render_info.next_url)

    def test_if_post_and_session_data_correct_and_input_data_incorrect_than_set_next_url_to_alternative_step(self):
        with self.app.test_request_context(method='POST', data={'user_a_has_elster_account_eligibility': 'yes'}) as req:
            req.session = SecureCookieSession(
                {_ELIGIBILITY_DATA_KEY: create_session_form_data(self.correct_session_data)})
            step = EligibilityStepChooser('eligibility').get_correct_step(
                UserAElsterAccountEligibilityInputFormSteuerlotseStep.name)
            expected_url = step.url_for_step(UserBElsterAccountDecisionEligibilityInputFormSteuerlotseStep.name)
            step.handle()

        self.assertEqual(expected_url, step.render_info.next_url)

    def test_if_session_data_correct_then_set_prev_input_step_correctly(self):
        with self.app.test_request_context(method='GET') as req:
            req.session = SecureCookieSession(
                {_ELIGIBILITY_DATA_KEY: create_session_form_data(self.correct_session_data)})
            step = EligibilityStepChooser('eligibility').get_correct_step(
                UserAElsterAccountEligibilityInputFormSteuerlotseStep.name)
            expected_url = step.url_for_step(MarriedAlimonyDecisionEligibilityInputFormSteuerlotseStep.name)
            step.handle()
        self.assertEqual(expected_url, step.render_info.prev_url)

    def test_if_post_and_data_from_before_invalid_then_raise_incorrect_eligibility_data_error(self):
        with self.app.test_request_context(method='POST', data={'user_a_has_elster_account_eligibility': 'no'}), \
                patch('app.model.recursive_data.RecursiveDataModel.one_previous_field_has_to_be_set',
                      MagicMock(side_effect=PreviousFieldsMissingError)):
            step = EligibilityStepChooser('eligibility').get_correct_step(
                UserAElsterAccountEligibilityInputFormSteuerlotseStep.name)

            self.assertRaises(IncorrectEligibilityData, step.handle)

    def test_if_get_and_incorrect_data_from_session_then_delete_incorrect_data(self):
        session_data = {'marital_status_eligibility': 'single',
                        'separated_since_last_year_eligibility': 'no',
                        'user_a_has_elster_account_eligibility': 'no',
                        'joint_taxes_eligibility': 'no',
                        'alimony_eligibility': 'no', }
        session_data_with_incorrect_key = {**session_data, **{'INCORRECT_KEY': 'UNNECESSARY_VALUE'}}
        with self.app.test_request_context(method='GET') as req:
            req.session = SecureCookieSession(
                {_ELIGIBILITY_DATA_KEY: create_session_form_data(session_data_with_incorrect_key)})
            step = EligibilityStepChooser('eligibility').get_correct_step(
                UserAElsterAccountEligibilityInputFormSteuerlotseStep.name)
            step.handle()

            self.assertEqual(session_data,
                             deserialize_session_data(req.session[_ELIGIBILITY_DATA_KEY]))

    def test_if_get_and_correct_data_from_session_then_do_not_delete_any_data(self):
        session_data = {'marital_status_eligibility': 'single',
                        'separated_since_last_year_eligibility': 'no',
                        'user_a_has_elster_account_eligibility': 'no',
                        'joint_taxes_eligibility': 'no',
                        'alimony_eligibility': 'no', }
        with self.app.test_request_context(method='GET') as req:
            req.session = SecureCookieSession({_ELIGIBILITY_DATA_KEY: create_session_form_data(session_data)})
            step = EligibilityStepChooser('eligibility').get_correct_step(
                UserAElsterAccountEligibilityInputFormSteuerlotseStep.name)
            step.handle()

            self.assertEqual(session_data,
                             deserialize_session_data(req.session[_ELIGIBILITY_DATA_KEY]))

    def test_if_get_and_full_data_from_session_then_delete_unnecessary_data(self):
        only_necessary_data = {'marital_status_eligibility': 'single',
                               'separated_since_last_year_eligibility': 'no',
                               'separated_joint_taxes_eligibility': 'no',
                               'separated_lived_together_eligibility': 'no',
                               'user_a_has_elster_account_eligibility': 'no',
                               'joint_taxes_eligibility': 'no',
                               'alimony_eligibility': 'no', }
        with self.app.test_request_context(method='GET') as req:
            req.session = SecureCookieSession({_ELIGIBILITY_DATA_KEY: create_session_form_data(FULL_SESSION_DATA)})
            step = EligibilityStepChooser('eligibility').get_correct_step(
                UserAElsterAccountEligibilityInputFormSteuerlotseStep.name)
            step.handle()

            self.assertEqual(only_necessary_data,
                             deserialize_session_data(req.session[_ELIGIBILITY_DATA_KEY]))


class TestUserBElsterAccountDecisionEligibilityInputFormSteuerlotseStep(unittest.TestCase):
    @pytest.fixture(autouse=True)
    def attach_fixtures(self, app):
        self.app = app

    def setUp(self):
        self.correct_session_data = {'marital_status_eligibility': 'married',
                                     'separated_since_last_year_eligibility': 'no',
                                     'joint_taxes_eligibility': 'yes',
                                     'alimony_eligibility': 'no',
                                     'user_a_has_elster_account_eligibility': 'yes'}

    def test_if_post_and_session_data_correct_and_input_data_correct_than_set_next_input_step(self):
        with self.app.test_request_context(method='POST', data={'user_b_has_elster_account_eligibility': 'no'}) as req:
            req.session = SecureCookieSession(
                {_ELIGIBILITY_DATA_KEY: create_session_form_data(self.correct_session_data)})
            step = EligibilityStepChooser('eligibility').get_correct_step(
                UserBElsterAccountDecisionEligibilityInputFormSteuerlotseStep.name)
            expected_url = step.url_for_step(PensionDecisionEligibilityInputFormSteuerlotseStep.name)
            step.handle()

        self.assertEqual(expected_url, step.render_info.next_url)

    def test_if_post_and_session_data_correct_and_input_data_incorrect_than_set_next_url_to_alternative_step(self):
        with self.app.test_request_context(method='POST', data={'user_b_has_elster_account_eligibility': 'yes'}) as req:
            req.session = SecureCookieSession(
                {_ELIGIBILITY_DATA_KEY: create_session_form_data(self.correct_session_data)})
            step = EligibilityStepChooser('eligibility').get_correct_step(
                UserBElsterAccountDecisionEligibilityInputFormSteuerlotseStep.name)
            expected_url = step.url_for_step(ElsterRegistrationMethodEligibilityDecisionStep.name)
            step.handle()

        self.assertEqual(expected_url, step.render_info.next_url)

    def test_if_session_data_correct_then_set_prev_input_step_correctly(self):
        with self.app.test_request_context(method='GET') as req:
            req.session = SecureCookieSession(
                {_ELIGIBILITY_DATA_KEY: create_session_form_data(self.correct_session_data)})
            step = EligibilityStepChooser('eligibility').get_correct_step(
                UserBElsterAccountDecisionEligibilityInputFormSteuerlotseStep.name)
            expected_url = step.url_for_step(UserAElsterAccountEligibilityInputFormSteuerlotseStep.name)
            step.handle()
        self.assertEqual(expected_url, step.render_info.prev_url)

    def test_if_post_and_data_from_before_invalid_then_raise_incorrect_eligibility_data_error(self):
        with self.app.test_request_context(method='POST', data={'user_b_has_elster_account_eligibility': 'no'}), \
                patch('app.model.recursive_data.RecursiveDataModel.one_previous_field_has_to_be_set',
                      MagicMock(side_effect=PreviousFieldsMissingError)):
            step = EligibilityStepChooser('eligibility').get_correct_step(
                UserBElsterAccountDecisionEligibilityInputFormSteuerlotseStep.name)

            self.assertRaises(IncorrectEligibilityData, step.handle)

    def test_if_get_and_incorrect_data_from_session_then_delete_incorrect_data(self):
        session_data = {'marital_status_eligibility': 'single',
                        'separated_since_last_year_eligibility': 'no',
                        'user_a_has_elster_account_eligibility': 'no',
                        'user_b_has_elster_account_eligibility': 'no',
                        'joint_taxes_eligibility': 'no',
                        'alimony_eligibility': 'no', }
        session_data_with_incorrect_key = {**session_data, **{'INCORRECT_KEY': 'UNNECESSARY_VALUE'}}
        with self.app.test_request_context(method='GET') as req:
            req.session = SecureCookieSession(
                {_ELIGIBILITY_DATA_KEY: create_session_form_data(session_data_with_incorrect_key)})
            step = EligibilityStepChooser('eligibility').get_correct_step(
                UserBElsterAccountDecisionEligibilityInputFormSteuerlotseStep.name)
            step.handle()

            self.assertEqual(session_data,
                             deserialize_session_data(req.session[_ELIGIBILITY_DATA_KEY]))

    def test_if_get_and_correct_data_from_session_then_do_not_delete_any_data(self):
        session_data = {'marital_status_eligibility': 'single',
                        'separated_since_last_year_eligibility': 'no',
                        'user_a_has_elster_account_eligibility': 'no',
                        'user_b_has_elster_account_eligibility': 'no',
                        'joint_taxes_eligibility': 'no',
                        'alimony_eligibility': 'no', }
        with self.app.test_request_context(method='GET') as req:
            req.session = SecureCookieSession({_ELIGIBILITY_DATA_KEY: create_session_form_data(session_data)})
            step = EligibilityStepChooser('eligibility').get_correct_step(
                UserBElsterAccountDecisionEligibilityInputFormSteuerlotseStep.name)
            step.handle()

            self.assertEqual(session_data,
                             deserialize_session_data(req.session[_ELIGIBILITY_DATA_KEY]))

    def test_if_get_and_full_data_from_session_then_delete_unnecessary_data(self):
        only_necessary_data = {'marital_status_eligibility': 'single',
                               'separated_since_last_year_eligibility': 'no',
                               'separated_joint_taxes_eligibility': 'no',
                               'separated_lived_together_eligibility': 'no',
                               'user_a_has_elster_account_eligibility': 'no',
                               'user_b_has_elster_account_eligibility': 'no',
                               'joint_taxes_eligibility': 'no',
                               'alimony_eligibility': 'no', }
        with self.app.test_request_context(method='GET') as req:
            req.session = SecureCookieSession({_ELIGIBILITY_DATA_KEY: create_session_form_data(FULL_SESSION_DATA)})
            step = EligibilityStepChooser('eligibility').get_correct_step(
                UserBElsterAccountDecisionEligibilityInputFormSteuerlotseStep.name)
            step.handle()

            self.assertEqual(only_necessary_data,
                             deserialize_session_data(req.session[_ELIGIBILITY_DATA_KEY]))


class TestDivorcedJointTaxesEligibilityFailureDisplaySteuerlotseStep(unittest.TestCase):
    @pytest.fixture(autouse=True)
    def attach_fixtures(self, test_request_context):
        self.req = test_request_context

    def test_handle_sets_correct_prev_url(self):
        step = DivorcedJointTaxesEligibilityFailureDisplaySteuerlotseStep(endpoint='eligibility')
        expected_url = step.url_for_step(DivorcedJointTaxesDecisionEligibilityInputFormSteuerlotseStep.name)
        step.handle()

        self.assertEqual(expected_url, step.render_info.prev_url)


class TestDivorcedJointTaxesDecisionEligibilityInputFormSteuerlotseStep(unittest.TestCase):
    @pytest.fixture(autouse=True)
    def attach_fixtures(self, app):
        self.app = app

    def setUp(self):
        self.correct_session_data = {'marital_status_eligibility': 'divorced'}

    def test_if_post_and_session_data_correct_and_input_data_correct_than_set_next_input_step(self):
        with self.app.test_request_context(method='POST', data={'joint_taxes_eligibility': 'no'}) as req:
            req.session = SecureCookieSession(
                {_ELIGIBILITY_DATA_KEY: create_session_form_data(self.correct_session_data)})
            step = EligibilityStepChooser('eligibility').get_correct_step(
                DivorcedJointTaxesDecisionEligibilityInputFormSteuerlotseStep.name)
            expected_url = step.url_for_step(SingleAlimonyDecisionEligibilityInputFormSteuerlotseStep.name)
            step.handle()

        self.assertEqual(expected_url, step.render_info.next_url)

    def test_if_post_and_session_data_correct_and_input_data_incorrect_than_set_next_url_to_alternative_step(self):
        with self.app.test_request_context(method='POST', data={'joint_taxes_eligibility': 'yes'}) as req:
            req.session = SecureCookieSession(
                {_ELIGIBILITY_DATA_KEY: create_session_form_data(self.correct_session_data)})
            step = EligibilityStepChooser('eligibility').get_correct_step(
                DivorcedJointTaxesDecisionEligibilityInputFormSteuerlotseStep.name)
            expected_url = step.url_for_step(DivorcedJointTaxesEligibilityFailureDisplaySteuerlotseStep.name)
            step.handle()

        self.assertEqual(expected_url, step.render_info.next_url)

    def test_if_session_data_correct_then_set_prev_input_step_correctly(self):
        with self.app.test_request_context(method='GET') as req:
            req.session = SecureCookieSession(
                {_ELIGIBILITY_DATA_KEY: create_session_form_data(self.correct_session_data)})
            step = EligibilityStepChooser('eligibility').get_correct_step(
                DivorcedJointTaxesDecisionEligibilityInputFormSteuerlotseStep.name)
            expected_url = step.url_for_step(MaritalStatusInputFormSteuerlotseStep.name)
            step.handle()
        self.assertEqual(expected_url, step.render_info.prev_url)

    def test_if_post_and_data_from_before_invalid_then_raise_incorrect_eligibility_data_error(self):
        with self.app.test_request_context(method='POST', data={'joint_taxes_eligibility': 'no'}), \
                patch('app.model.recursive_data.RecursiveDataModel.one_previous_field_has_to_be_set',
                      MagicMock(side_effect=PreviousFieldsMissingError)):
            step = EligibilityStepChooser('eligibility').get_correct_step(
                DivorcedJointTaxesDecisionEligibilityInputFormSteuerlotseStep.name)

            self.assertRaises(IncorrectEligibilityData, step.handle)

    def test_if_get_and_incorrect_data_from_session_then_delete_incorrect_data(self):
        session_data = {'marital_status_eligibility': 'single',
                        'joint_taxes_eligibility': 'no', }
        session_data_with_incorrect_key = {**session_data, **{'INCORRECT_KEY': 'UNNECESSARY_VALUE'}}
        with self.app.test_request_context(method='GET') as req:
            req.session = SecureCookieSession(
                {_ELIGIBILITY_DATA_KEY: create_session_form_data(session_data_with_incorrect_key)})
            step = EligibilityStepChooser('eligibility').get_correct_step(
                DivorcedJointTaxesDecisionEligibilityInputFormSteuerlotseStep.name)
            step.handle()

            self.assertEqual(session_data,
                             deserialize_session_data(req.session[_ELIGIBILITY_DATA_KEY]))

    def test_if_get_and_correct_data_from_session_then_do_not_delete_any_data(self):
        session_data = {'marital_status_eligibility': 'single',
                        'joint_taxes_eligibility': 'no', }
        with self.app.test_request_context(method='GET') as req:
            req.session = SecureCookieSession({_ELIGIBILITY_DATA_KEY: create_session_form_data(session_data)})
            step = EligibilityStepChooser('eligibility').get_correct_step(
                DivorcedJointTaxesDecisionEligibilityInputFormSteuerlotseStep.name)
            step.handle()

            self.assertEqual(session_data,
                             deserialize_session_data(req.session[_ELIGIBILITY_DATA_KEY]))

    def test_if_get_and_full_data_from_session_then_delete_unnecessary_data(self):
        only_necessary_data = {'marital_status_eligibility': 'single',
                               'joint_taxes_eligibility': 'no', }
        with self.app.test_request_context(method='GET') as req:
            req.session = SecureCookieSession({_ELIGIBILITY_DATA_KEY: create_session_form_data(FULL_SESSION_DATA)})
            step = EligibilityStepChooser('eligibility').get_correct_step(
                DivorcedJointTaxesDecisionEligibilityInputFormSteuerlotseStep.name)
            step.handle()

            self.assertEqual(only_necessary_data,
                             deserialize_session_data(req.session[_ELIGIBILITY_DATA_KEY]))


class TestSingleAlimonyEligibilityFailureDisplaySteuerlotseStep(unittest.TestCase):
    @pytest.fixture(autouse=True)
    def attach_fixtures(self, test_request_context):
        self.req = test_request_context

    def test_handle_sets_correct_prev_url(self):
        step = SingleAlimonyEligibilityFailureDisplaySteuerlotseStep(endpoint='eligibility')
        expected_url = step.url_for_step(SingleAlimonyDecisionEligibilityInputFormSteuerlotseStep.name)
        step.handle()

        self.assertEqual(expected_url, step.render_info.prev_url)


class TestSingleAlimonyDecisionEligibilityInputFormSteuerlotseStep(unittest.TestCase):
    @pytest.fixture(autouse=True)
    def attach_fixtures(self, app):
        self.app = app

    def setUp(self):
        self.correct_session_data = {'marital_status_eligibility': 'divorced',
                                     'joint_taxes_eligibility': 'no'}

    def test_if_post_and_session_data_correct_and_input_data_correct_than_set_next_input_step(self):
        with self.app.test_request_context(method='POST', data={'alimony_eligibility': 'no'}) as req:
            req.session = SecureCookieSession(
                {_ELIGIBILITY_DATA_KEY: create_session_form_data(self.correct_session_data)})
            step = EligibilityStepChooser('eligibility').get_correct_step(
                SingleAlimonyDecisionEligibilityInputFormSteuerlotseStep.name)
            expected_url = step.url_for_step(SingleElsterAccountDecisionEligibilityInputFormSteuerlotseStep.name)
            step.handle()

        self.assertEqual(expected_url, step.render_info.next_url)

    def test_if_post_and_session_data_correct_and_input_data_incorrect_than_set_next_url_to_alternative_step(self):
        with self.app.test_request_context(method='POST', data={'alimony_eligibility': 'yes'}) as req:
            req.session = SecureCookieSession(
                {_ELIGIBILITY_DATA_KEY: create_session_form_data(self.correct_session_data)})
            step = EligibilityStepChooser('eligibility').get_correct_step(
                SingleAlimonyDecisionEligibilityInputFormSteuerlotseStep.name)
            expected_url = step.url_for_step(SingleAlimonyEligibilityFailureDisplaySteuerlotseStep.name)
            step.handle()

        self.assertEqual(expected_url, step.render_info.next_url)

    def test_if_divorced_session_data_correct_then_set_prev_input_step_correctly(self):
        with self.app.test_request_context(method='GET') as req:
            req.session = SecureCookieSession(
                {_ELIGIBILITY_DATA_KEY: create_session_form_data(self.correct_session_data)})
            step = EligibilityStepChooser('eligibility').get_correct_step(
                SingleAlimonyDecisionEligibilityInputFormSteuerlotseStep.name)
            expected_url = step.url_for_step(DivorcedJointTaxesDecisionEligibilityInputFormSteuerlotseStep.name)
            step.handle()
        self.assertEqual(expected_url, step.render_info.prev_url)

    def test_if_single_session_data_correct_then_set_prev_input_step_correctly(self):
        alternative_data = {'marital_status_eligibility': 'single'}
        with self.app.test_request_context(method='GET') as req:
            req.session = SecureCookieSession({_ELIGIBILITY_DATA_KEY: create_session_form_data(alternative_data)})
            step = EligibilityStepChooser('eligibility').get_correct_step(
                SingleAlimonyDecisionEligibilityInputFormSteuerlotseStep.name)
            expected_url = step.url_for_step(MaritalStatusInputFormSteuerlotseStep.name)
            step.handle()
        self.assertEqual(expected_url, step.render_info.prev_url)

    def test_if_widowed_session_data_correct_then_set_prev_input_step_correctly(self):
        alternative_data = {'marital_status_eligibility': 'widowed'}
        with self.app.test_request_context(method='GET') as req:
            req.session = SecureCookieSession({_ELIGIBILITY_DATA_KEY: create_session_form_data(alternative_data)})
            step = EligibilityStepChooser('eligibility').get_correct_step(
                SingleAlimonyDecisionEligibilityInputFormSteuerlotseStep.name)
            expected_url = step.url_for_step(MaritalStatusInputFormSteuerlotseStep.name)
            step.handle()
        self.assertEqual(expected_url, step.render_info.prev_url)

    def test_if_separated_not_lived_together_session_data_correct_then_set_prev_input_step_correctly(self):
        alternative_data = {'marital_status_eligibility': 'married',
                            'separated_since_last_year_eligibility': 'yes',
                            'separated_lived_together_eligibility': 'no'}
        with self.app.test_request_context(method='GET') as req:
            req.session = SecureCookieSession({_ELIGIBILITY_DATA_KEY: create_session_form_data(alternative_data)})
            step = EligibilityStepChooser('eligibility').get_correct_step(
                SingleAlimonyDecisionEligibilityInputFormSteuerlotseStep.name)
            expected_url = step.url_for_step(SeparatedLivedTogetherEligibilityInputFormSteuerlotseStep.name)
            step.handle()
        self.assertEqual(expected_url, step.render_info.prev_url)

    def test_if_separated_not_joint_taxes_session_data_correct_then_set_prev_input_step_correctly(self):
        alternative_data = {'marital_status_eligibility': 'married',
                            'separated_since_last_year_eligibility': 'yes',
                            'separated_lived_together_eligibility': 'yes',
                            'separated_joint_taxes_eligibility': 'no'}
        with self.app.test_request_context(method='GET') as req:
            req.session = SecureCookieSession({_ELIGIBILITY_DATA_KEY: create_session_form_data(alternative_data)})
            step = EligibilityStepChooser('eligibility').get_correct_step(
                SingleAlimonyDecisionEligibilityInputFormSteuerlotseStep.name)
            expected_url = step.url_for_step(SeparatedJointTaxesEligibilityInputFormSteuerlotseStep.name)
            step.handle()
        self.assertEqual(expected_url, step.render_info.prev_url)

    def test_if_post_and_data_from_before_invalid_then_raise_incorrect_eligibility_data_error(self):
        with self.app.test_request_context(method='POST', data={'alimony_eligibility': 'no'}), \
                patch('app.model.recursive_data.RecursiveDataModel.one_previous_field_has_to_be_set',
                      MagicMock(side_effect=PreviousFieldsMissingError)):
            step = EligibilityStepChooser('eligibility').get_correct_step(
                SingleAlimonyDecisionEligibilityInputFormSteuerlotseStep.name)

            self.assertRaises(IncorrectEligibilityData, step.handle)

    def test_if_get_and_incorrect_data_from_session_then_delete_incorrect_data(self):
        session_data = {'marital_status_eligibility': 'single',
                        'joint_taxes_eligibility': 'no',
                        'alimony_eligibility': 'no', }
        session_data_with_incorrect_key = {**session_data, **{'INCORRECT_KEY': 'UNNECESSARY_VALUE'}}
        with self.app.test_request_context(method='GET') as req:
            req.session = SecureCookieSession(
                {_ELIGIBILITY_DATA_KEY: create_session_form_data(session_data_with_incorrect_key)})
            step = EligibilityStepChooser('eligibility').get_correct_step(
                SingleAlimonyDecisionEligibilityInputFormSteuerlotseStep.name)
            step.handle()

            self.assertEqual(session_data,
                             deserialize_session_data(req.session[_ELIGIBILITY_DATA_KEY]))

    def test_if_get_and_correct_data_from_session_then_do_not_delete_any_data(self):
        session_data = {'marital_status_eligibility': 'single',
                        'joint_taxes_eligibility': 'no',
                        'alimony_eligibility': 'no', }
        with self.app.test_request_context(method='GET') as req:
            req.session = SecureCookieSession({_ELIGIBILITY_DATA_KEY: create_session_form_data(session_data)})
            step = EligibilityStepChooser('eligibility').get_correct_step(
                SingleAlimonyDecisionEligibilityInputFormSteuerlotseStep.name)
            step.handle()

            self.assertEqual(session_data,
                             deserialize_session_data(req.session[_ELIGIBILITY_DATA_KEY]))

    def test_if_get_and_full_data_from_session_then_delete_unnecessary_data(self):
        only_necessary_data = {'marital_status_eligibility': 'single',
                               'joint_taxes_eligibility': 'no',
                               'separated_since_last_year_eligibility': 'no',
                               'separated_joint_taxes_eligibility': 'no',
                               'separated_lived_together_eligibility': 'no',
                               'alimony_eligibility': 'no', }
        with self.app.test_request_context(method='GET') as req:
            req.session = SecureCookieSession({_ELIGIBILITY_DATA_KEY: create_session_form_data(FULL_SESSION_DATA)})
            step = EligibilityStepChooser('eligibility').get_correct_step(
                SingleAlimonyDecisionEligibilityInputFormSteuerlotseStep.name)
            step.handle()

            self.assertEqual(only_necessary_data,
                             deserialize_session_data(req.session[_ELIGIBILITY_DATA_KEY]))


class TestSingleElsterAccountDecisionEligibilityInputFormSteuerlotseStep(unittest.TestCase):
    @pytest.fixture(autouse=True)
    def attach_fixtures(self, app):
        self.app = app

    def setUp(self):
        self.correct_session_data = {'marital_status_eligibility': 'divorced',
                                     'joint_taxes_eligibility': 'no',
                                     'alimony_eligibility': 'no'}

    def test_if_post_and_session_data_correct_and_input_data_correct_than_set_next_input_step(self):
        with self.app.test_request_context(method='POST', data={'user_a_has_elster_account_eligibility': 'no'}) as req:
            req.session = SecureCookieSession(
                {_ELIGIBILITY_DATA_KEY: create_session_form_data(self.correct_session_data)})
            step = EligibilityStepChooser('eligibility').get_correct_step(
                SingleElsterAccountDecisionEligibilityInputFormSteuerlotseStep.name)
            expected_url = step.url_for_step(PensionDecisionEligibilityInputFormSteuerlotseStep.name)
            step.handle()

        self.assertEqual(expected_url, step.render_info.next_url)

    def test_if_post_and_session_data_correct_and_input_data_incorrect_than_set_next_url_to_alternative_step(self):
        with self.app.test_request_context(method='POST', data={'user_a_has_elster_account_eligibility': 'yes'}) as req:
            req.session = SecureCookieSession(
                {_ELIGIBILITY_DATA_KEY: create_session_form_data(self.correct_session_data)})
            step = EligibilityStepChooser('eligibility').get_correct_step(
                SingleElsterAccountDecisionEligibilityInputFormSteuerlotseStep.name)
            expected_url = step.url_for_step(ElsterRegistrationMethodEligibilityDecisionStep.name)
            step.handle()

        self.assertEqual(expected_url, step.render_info.next_url)

    def test_if_session_data_correct_then_set_prev_input_step_correctly(self):
        with self.app.test_request_context(method='GET') as req:
            req.session = SecureCookieSession(
                {_ELIGIBILITY_DATA_KEY: create_session_form_data(self.correct_session_data)})
            step = EligibilityStepChooser('eligibility').get_correct_step(
                SingleElsterAccountDecisionEligibilityInputFormSteuerlotseStep.name)
            expected_url = step.url_for_step(SingleAlimonyDecisionEligibilityInputFormSteuerlotseStep.name)
            step.handle()
        self.assertEqual(expected_url, step.render_info.prev_url)

    def test_if_post_and_data_from_before_invalid_then_raise_incorrect_eligibility_data_error(self):
        with self.app.test_request_context(method='POST', data={'user_a_has_elster_account_eligibility': 'no'}), \
                patch('app.model.recursive_data.RecursiveDataModel.one_previous_field_has_to_be_set',
                      MagicMock(side_effect=PreviousFieldsMissingError)):
            step = EligibilityStepChooser('eligibility').get_correct_step(
                SingleElsterAccountDecisionEligibilityInputFormSteuerlotseStep.name)

            self.assertRaises(IncorrectEligibilityData, step.handle)

    def test_if_get_and_incorrect_data_from_session_then_delete_incorrect_data(self):
        session_data = {'marital_status_eligibility': 'single',
                        'user_a_has_elster_account_eligibility': 'no',
                        'joint_taxes_eligibility': 'no',
                        'alimony_eligibility': 'no', }
        session_data_with_incorrect_key = {**session_data, **{'INCORRECT_KEY': 'UNNECESSARY_VALUE'}}
        with self.app.test_request_context(method='GET') as req:
            req.session = SecureCookieSession(
                {_ELIGIBILITY_DATA_KEY: create_session_form_data(session_data_with_incorrect_key)})
            step = EligibilityStepChooser('eligibility').get_correct_step(
                SingleElsterAccountDecisionEligibilityInputFormSteuerlotseStep.name)
            step.handle()

            self.assertEqual(session_data,
                             deserialize_session_data(req.session[_ELIGIBILITY_DATA_KEY]))

    def test_if_get_and_correct_data_from_session_then_do_not_delete_any_data(self):
        session_data = {'marital_status_eligibility': 'single',
                        'user_a_has_elster_account_eligibility': 'no',
                        'joint_taxes_eligibility': 'no',
                        'alimony_eligibility': 'no', }
        with self.app.test_request_context(method='GET') as req:
            req.session = SecureCookieSession({_ELIGIBILITY_DATA_KEY: create_session_form_data(session_data)})
            step = EligibilityStepChooser('eligibility').get_correct_step(
                SingleElsterAccountDecisionEligibilityInputFormSteuerlotseStep.name)
            step.handle()

            self.assertEqual(session_data,
                             deserialize_session_data(req.session[_ELIGIBILITY_DATA_KEY]))

    def test_if_get_and_full_data_from_session_then_delete_unnecessary_data(self):
        only_necessary_data = {'marital_status_eligibility': 'single',
                               'separated_since_last_year_eligibility': 'no',
                               'separated_joint_taxes_eligibility': 'no',
                               'separated_lived_together_eligibility': 'no',
                               'user_a_has_elster_account_eligibility': 'no',
                               'joint_taxes_eligibility': 'no',
                               'alimony_eligibility': 'no', }
        with self.app.test_request_context(method='GET') as req:
            req.session = SecureCookieSession({_ELIGIBILITY_DATA_KEY: create_session_form_data(FULL_SESSION_DATA)})
            step = EligibilityStepChooser('eligibility').get_correct_step(
                SingleElsterAccountDecisionEligibilityInputFormSteuerlotseStep.name)
            step.handle()

            self.assertEqual(only_necessary_data,
                             deserialize_session_data(req.session[_ELIGIBILITY_DATA_KEY]))


class TestElsterRegistrationMethodEligibilityDecisionStep:
    @pytest.fixture(autouse=True)
    def attach_fixtures(self, app, test_request_context):
        self.app = app
        self.correct_session_data = {'marital_status_eligibility': 'divorced',
                                     'joint_taxes_eligibility': 'no',
                                     'alimony_eligibility': 'no',
                                     'user_a_has_elster_account_eligibility': 'yes'}

    def test_if_post_and_session_data_correct_and_input_data_software_then_set_next_input_step(self):
        with self.app.test_request_context(method='POST',
                                           data={'elster_registration_method_eligibility': 'software'}) as req:
            req.session = SecureCookieSession(
                {_ELIGIBILITY_DATA_KEY: create_session_form_data(self.correct_session_data)})
            step = EligibilityStepChooser('eligibility')\
                .get_correct_step(ElsterRegistrationMethodEligibilityDecisionStep.name)
            # TODO change!
            expected_url = step.url_for_step(PensionDecisionEligibilityInputFormSteuerlotseStep.name)

            step.handle()
        assert step.render_info.next_url == expected_url

    def test_if_post_and_session_data_correct_and_input_data_none_then_set_next_input_step(self):
        with self.app.test_request_context(method='POST',
                                           data={'elster_registration_method_eligibility': 'none'}) as req:
            req.session = SecureCookieSession(
                {_ELIGIBILITY_DATA_KEY: create_session_form_data(self.correct_session_data)})
            step = EligibilityStepChooser('eligibility')\
                .get_correct_step(ElsterRegistrationMethodEligibilityDecisionStep.name)
            expected_url = step.url_for_step(PensionDecisionEligibilityInputFormSteuerlotseStep.name)

            step.handle()
        assert step.render_info.next_url == expected_url

    def test_if_post_and_session_data_correct_and_input_data_incorrect_then_set_next_step_failure_step(self):
        with self.app.test_request_context(method='POST',
                                           data={'elster_registration_method_eligibility': 'id_card'}) as req:
            req.session = SecureCookieSession(
                {_ELIGIBILITY_DATA_KEY: create_session_form_data(self.correct_session_data)})
            step = EligibilityStepChooser('eligibility')\
                .get_correct_step(ElsterRegistrationMethodEligibilityDecisionStep.name)
            expected_url = step.url_for_step(ElsterRegistrationMethodEligibilityFailureStep.name)

            step.handle()
        assert step.render_info.next_url == expected_url

    def test_if_session_data_correct_single_then_set_prev_input_step_correctly(self):
        with self.app.test_request_context(method='GET') as req:
            req.session = SecureCookieSession(
                {_ELIGIBILITY_DATA_KEY: create_session_form_data(self.correct_session_data)})
            step = EligibilityStepChooser('eligibility').get_correct_step(
                ElsterRegistrationMethodEligibilityDecisionStep.name)
            expected_url = step.url_for_step(SingleElsterAccountDecisionEligibilityInputFormSteuerlotseStep.name)
            step.handle()
        assert step.render_info.prev_url == expected_url

    def test_if_session_data_correct_partner_then_set_prev_input_step_correctly(self):
        married_data = {**self.correct_session_data,
                        **{'marital_status_eligibility': 'married',
                           'separated_since_last_year_eligibility': 'no',
                           'joint_taxes_eligibility': 'yes',
                           'alimony_eligibility': 'no',
                           'user_a_has_elster_account_eligibility': 'yes',
                           'user_b_has_elster_account_eligibility': 'yes'}}
        with self.app.test_request_context(method='GET') as req:
            req.session = SecureCookieSession(
                {_ELIGIBILITY_DATA_KEY: create_session_form_data(married_data)})
            step = EligibilityStepChooser('eligibility').get_correct_step(
                ElsterRegistrationMethodEligibilityDecisionStep.name)
            expected_url = step.url_for_step(UserBElsterAccountDecisionEligibilityInputFormSteuerlotseStep.name)
            step.handle()
        assert step.render_info.prev_url == expected_url

    def test_if_post_and_data_from_before_invalid_then_raise_incorrect_eligibility_data_error(self):
        with self.app.test_request_context(method='POST', data={'elster_registration_method_eligibility': 'none'}), \
                patch('app.model.recursive_data.RecursiveDataModel.one_previous_field_has_to_be_set',
                      MagicMock(side_effect=PreviousFieldsMissingError)):
            step = EligibilityStepChooser('eligibility').get_correct_step(
                ElsterRegistrationMethodEligibilityDecisionStep.name)

            with pytest.raises(IncorrectEligibilityData):
                step.handle()

    def test_if_get_and_incorrect_data_from_session_then_delete_incorrect_data(self):
        session_data_with_incorrect_key = {**self.correct_session_data, **{'INCORRECT_KEY': 'UNNECESSARY_VALUE'}}
        with self.app.test_request_context(method='GET') as req:
            req.session = SecureCookieSession(
                {_ELIGIBILITY_DATA_KEY: create_session_form_data(session_data_with_incorrect_key)})
            step = EligibilityStepChooser('eligibility').get_correct_step(
                ElsterRegistrationMethodEligibilityDecisionStep.name)
            step.handle()

        assert deserialize_session_data(req.session[_ELIGIBILITY_DATA_KEY]) == self.correct_session_data

    def test_if_get_and_correct_data_from_session_then_do_not_delete_any_data(self):
        with self.app.test_request_context(method='GET') as req:
            req.session = SecureCookieSession({_ELIGIBILITY_DATA_KEY: create_session_form_data(self.correct_session_data)})
            step = EligibilityStepChooser('eligibility').get_correct_step(
                ElsterRegistrationMethodEligibilityDecisionStep.name)
            step.handle()

        assert deserialize_session_data(req.session[_ELIGIBILITY_DATA_KEY]) == self.correct_session_data

    def test_if_get_and_full_data_from_session_then_delete_unnecessary_data(self):
        only_necessary_data = {'marital_status_eligibility': 'single',
                               'separated_since_last_year_eligibility': 'no',
                               'separated_joint_taxes_eligibility': 'no',
                               'separated_lived_together_eligibility': 'no',
                               'user_a_has_elster_account_eligibility': 'no',
                               'user_b_has_elster_account_eligibility': 'no',
                               'elster_registration_method_eligibility': 'none',
                               'joint_taxes_eligibility': 'no',
                               'alimony_eligibility': 'no', }
        with self.app.test_request_context(method='GET') as req:
            req.session = SecureCookieSession({_ELIGIBILITY_DATA_KEY: create_session_form_data(FULL_SESSION_DATA)})
            step = EligibilityStepChooser('eligibility').get_correct_step(
                ElsterRegistrationMethodEligibilityDecisionStep.name)
            step.handle()

        assert deserialize_session_data(req.session[_ELIGIBILITY_DATA_KEY]) == only_necessary_data


class TestPensionEligibilityFailureDisplaySteuerlotseStep(unittest.TestCase):
    @pytest.fixture(autouse=True)
    def attach_fixtures(self, test_request_context):
        self.req = test_request_context

    def test_handle_sets_correct_prev_url(self):
        step = PensionEligibilityFailureDisplaySteuerlotseStep(endpoint='eligibility')
        expected_url = step.url_for_step(PensionDecisionEligibilityInputFormSteuerlotseStep.name)
        step.handle()

        self.assertEqual(expected_url, step.render_info.prev_url)


class TestPensionDecisionEligibilityInputFormSteuerlotseStep(unittest.TestCase):
    @pytest.fixture(autouse=True)
    def attach_fixtures(self, app):
        self.app = app

    def setUp(self):
        self.correct_session_data = {'marital_status_eligibility': 'divorced',
                                     'joint_taxes_eligibility': 'no',
                                     'alimony_eligibility': 'no',
                                     'user_a_has_elster_account_eligibility': 'no'}

    def test_if_post_and_session_data_correct_and_input_data_correct_than_set_next_input_step(self):
        with self.app.test_request_context(method='POST', data={'pension_eligibility': 'yes'}) as req:
            req.session = SecureCookieSession(
                {_ELIGIBILITY_DATA_KEY: create_session_form_data(self.correct_session_data)})
            step = EligibilityStepChooser('eligibility').get_correct_step(
                PensionDecisionEligibilityInputFormSteuerlotseStep.name)
            expected_url = step.url_for_step(InvestmentIncomeDecisionEligibilityInputFormSteuerlotseStep.name)
            step.handle()

        self.assertEqual(expected_url, step.render_info.next_url)

    def test_if_post_and_session_data_correct_and_input_data_incorrect_than_set_next_url_to_alternative_step(self):
        with self.app.test_request_context(method='POST', data={'pension_eligibility': 'no'}) as req:
            req.session = SecureCookieSession(
                {_ELIGIBILITY_DATA_KEY: create_session_form_data(self.correct_session_data)})
            step = EligibilityStepChooser('eligibility').get_correct_step(
                PensionDecisionEligibilityInputFormSteuerlotseStep.name)
            expected_url = step.url_for_step(PensionEligibilityFailureDisplaySteuerlotseStep.name)
            step.handle()

        self.assertEqual(expected_url, step.render_info.next_url)

    def test_if_no_joint_taxes_session_data_correct_then_set_prev_input_step_correctly(self):
        with self.app.test_request_context(method='GET') as req:
            req.session = SecureCookieSession(
                {_ELIGIBILITY_DATA_KEY: create_session_form_data(self.correct_session_data)})
            step = EligibilityStepChooser('eligibility').get_correct_step(
                PensionDecisionEligibilityInputFormSteuerlotseStep.name)
            expected_url = step.url_for_step(SingleElsterAccountDecisionEligibilityInputFormSteuerlotseStep.name)
            step.handle()
        self.assertEqual(expected_url, step.render_info.prev_url)

    def test_if_joint_taxes_user_a_no_elster_account_session_data_correct_then_set_prev_input_step_correctly(self):
        alternative_data = {'marital_status_eligibility': 'married',
                            'separated_since_last_year_eligibility': 'no',
                            'joint_taxes_eligibility': 'yes',
                            'alimony_eligibility': 'no',
                            'user_a_has_elster_account_eligibility': 'no'}

        with self.app.test_request_context(method='GET') as req:
            req.session = SecureCookieSession({_ELIGIBILITY_DATA_KEY: create_session_form_data(alternative_data)})
            step = EligibilityStepChooser('eligibility').get_correct_step(
                PensionDecisionEligibilityInputFormSteuerlotseStep.name)
            expected_url = step.url_for_step(UserAElsterAccountEligibilityInputFormSteuerlotseStep.name)
            step.handle()
        self.assertEqual(expected_url, step.render_info.prev_url)

    def test_if_joint_taxes_user_b_no_elster_account_session_data_correct_then_set_prev_input_step_correctly(self):
        alternative_data = {'marital_status_eligibility': 'married',
                            'separated_since_last_year_eligibility': 'no',
                            'joint_taxes_eligibility': 'yes',
                            'alimony_eligibility': 'no',
                            'user_a_has_elster_account_eligibility': 'yes',
                            'user_b_has_elster_account_eligibility': 'no'}
        with self.app.test_request_context(method='GET') as req:
            req.session = SecureCookieSession({_ELIGIBILITY_DATA_KEY: create_session_form_data(alternative_data)})
            step = EligibilityStepChooser('eligibility').get_correct_step(
                PensionDecisionEligibilityInputFormSteuerlotseStep.name)
            expected_url = step.url_for_step(UserBElsterAccountDecisionEligibilityInputFormSteuerlotseStep.name)
            step.handle()
        self.assertEqual(expected_url, step.render_info.prev_url)

    def test_if_elster_registration_method_none_session_data_correct_then_set_prev_input_step_correctly(self):
        alternative_data = {'marital_status_eligibility': 'married',
                            'separated_since_last_year_eligibility': 'no',
                            'joint_taxes_eligibility': 'yes',
                            'alimony_eligibility': 'no',
                            'user_a_has_elster_account_eligibility': 'yes',
                            'user_b_has_elster_account_eligibility': 'yes',
                            'elster_registration_method_eligibility': 'none'}
        with self.app.test_request_context(method='GET') as req:
            req.session = SecureCookieSession({_ELIGIBILITY_DATA_KEY: create_session_form_data(alternative_data)})
            step = EligibilityStepChooser('eligibility').get_correct_step(
                PensionDecisionEligibilityInputFormSteuerlotseStep.name)
            expected_url = step.url_for_step(ElsterRegistrationMethodEligibilityDecisionStep.name)
            step.handle()
        self.assertEqual(expected_url, step.render_info.prev_url)

    def test_if_post_and_data_from_before_invalid_then_raise_incorrect_eligibility_data_error(self):
        with self.app.test_request_context(method='POST', data={'pension_eligibility': 'yes'}), \
                patch('app.model.recursive_data.RecursiveDataModel.one_previous_field_has_to_be_set',
                      MagicMock(side_effect=PreviousFieldsMissingError)):
            step = EligibilityStepChooser('eligibility').get_correct_step(
                PensionDecisionEligibilityInputFormSteuerlotseStep.name)

            self.assertRaises(IncorrectEligibilityData, step.handle)

    def test_if_get_and_incorrect_data_from_session_then_delete_incorrect_data(self):
        session_data = {'marital_status_eligibility': 'single',
                        'separated_since_last_year_eligibility': 'no',
                        'user_a_has_elster_account_eligibility': 'no',
                        'user_b_has_elster_account_eligibility': 'no',
                        'joint_taxes_eligibility': 'no',
                        'alimony_eligibility': 'no',
                        'pension_eligibility': 'yes', }
        session_data_with_incorrect_key = {**session_data, **{'INCORRECT_KEY': 'UNNECESSARY_VALUE'}}
        with self.app.test_request_context(method='GET') as req:
            req.session = SecureCookieSession(
                {_ELIGIBILITY_DATA_KEY: create_session_form_data(session_data_with_incorrect_key)})
            step = EligibilityStepChooser('eligibility').get_correct_step(
                PensionDecisionEligibilityInputFormSteuerlotseStep.name)
            step.handle()

            self.assertEqual(session_data,
                             deserialize_session_data(req.session[_ELIGIBILITY_DATA_KEY]))

    def test_if_get_and_correct_data_from_session_then_do_not_delete_any_data(self):
        session_data = {'marital_status_eligibility': 'single',
                        'separated_since_last_year_eligibility': 'no',
                        'user_a_has_elster_account_eligibility': 'no',
                        'user_b_has_elster_account_eligibility': 'no',
                        'joint_taxes_eligibility': 'no',
                        'alimony_eligibility': 'no',
                        'pension_eligibility': 'yes', }
        with self.app.test_request_context(method='GET') as req:
            req.session = SecureCookieSession({_ELIGIBILITY_DATA_KEY: create_session_form_data(session_data)})
            step = EligibilityStepChooser('eligibility').get_correct_step(
                PensionDecisionEligibilityInputFormSteuerlotseStep.name)
            step.handle()

            self.assertEqual(session_data,
                             deserialize_session_data(req.session[_ELIGIBILITY_DATA_KEY]))

    def test_if_get_and_full_data_from_session_then_delete_unnecessary_data(self):
        only_necessary_data = {'marital_status_eligibility': 'single',
                               'separated_since_last_year_eligibility': 'no',
                               'separated_joint_taxes_eligibility': 'no',
                               'separated_lived_together_eligibility': 'no',
                               'user_a_has_elster_account_eligibility': 'no',
                               'user_b_has_elster_account_eligibility': 'no',
                               'elster_registration_method_eligibility': 'none',
                               'joint_taxes_eligibility': 'no',
                               'alimony_eligibility': 'no',
                               'pension_eligibility': 'yes', }
        with self.app.test_request_context(method='GET') as req:
            req.session = SecureCookieSession({_ELIGIBILITY_DATA_KEY: create_session_form_data(FULL_SESSION_DATA)})
            step = EligibilityStepChooser('eligibility').get_correct_step(
                PensionDecisionEligibilityInputFormSteuerlotseStep.name)
            step.handle()

            self.assertEqual(only_necessary_data,
                             deserialize_session_data(req.session[_ELIGIBILITY_DATA_KEY]))

    def test_if_multiple_users_then_show_multiple_text(self):
        session_data = {'marital_status_eligibility': 'married',
                        'separated_since_last_year_eligibility': 'no',
                        'joint_taxes_eligibility': 'yes',
                        'user_a_has_elster_account_eligibility': 'no',
                        'user_b_has_elster_account_eligibility': 'no',
                        'alimony_eligibility': 'no',}
        expected_number_of_users = 2
        expected_choices = [('yes', ngettext('form.eligibility.pension.yes', 'form.eligibility.pension.yes', num=expected_number_of_users)),
                            ('no', ngettext('form.eligibility.pension.no', 'form.eligibility.pension.no', num=expected_number_of_users))]
        with self.app.test_request_context(method='GET') as req:
            req.session = SecureCookieSession({_ELIGIBILITY_DATA_KEY: create_session_form_data(session_data)})
            step = EligibilityStepChooser('eligibility').get_correct_step(
                PensionDecisionEligibilityInputFormSteuerlotseStep.name)
            step._pre_handle()

        self.assertEqual(expected_choices, step.form.pension_eligibility.kwargs['choices'])

    def test_if_single_user_then_show_single_text(self):
        session_data = {'marital_status_eligibility': 'single',
                        'separated_since_last_year_eligibility': 'no',
                        'user_a_has_elster_account_eligibility': 'no',
                        'user_b_has_elster_account_eligibility': 'no',
                        'joint_taxes_eligibility': 'no',
                        'alimony_eligibility': 'no'}
        expected_number_of_users = 1
        expected_choices = [('yes', ngettext('form.eligibility.pension.yes', 'form.eligibility.pension.yes', num=expected_number_of_users)),
                            ('no', ngettext('form.eligibility.pension.no', 'form.eligibility.pension.no', num=expected_number_of_users))]
        with self.app.test_request_context(method='GET') as req:
            req.session = SecureCookieSession({_ELIGIBILITY_DATA_KEY: create_session_form_data(session_data)})
            step = EligibilityStepChooser('eligibility').get_correct_step(
                PensionDecisionEligibilityInputFormSteuerlotseStep.name)
            step._pre_handle()

        self.assertEqual(expected_choices, step.form.pension_eligibility.kwargs['choices'])


class TestInvestmentIncomeDecisionEligibilityInputFormSteuerlotseStep(unittest.TestCase):
    @pytest.fixture(autouse=True)
    def attach_fixtures(self, app):
        self.app = app

    def setUp(self):
        self.correct_session_data = {'marital_status_eligibility': 'divorced',
                                     'joint_taxes_eligibility': 'no',
                                     'alimony_eligibility': 'no',
                                     'user_a_has_elster_account_eligibility': 'no',
                                     'pension_eligibility': 'yes'}

    def test_if_post_and_session_data_correct_and_input_data_correct_than_set_next_input_step(self):
        with self.app.test_request_context(method='POST', data={'investment_income_eligibility': 'yes'}) as req:
            req.session = SecureCookieSession(
                {_ELIGIBILITY_DATA_KEY: create_session_form_data(self.correct_session_data)})
            step = EligibilityStepChooser('eligibility').get_correct_step(
                InvestmentIncomeDecisionEligibilityInputFormSteuerlotseStep.name)
            expected_url = step.url_for_step(MinimalInvestmentIncomeDecisionEligibilityInputFormSteuerlotseStep.name)
            step.handle()

        self.assertEqual(expected_url, step.render_info.next_url)

    def test_if_post_and_session_data_correct_and_input_data_incorrect_than_set_next_url_to_alternative_step(self):
        with self.app.test_request_context(method='POST', data={'investment_income_eligibility': 'no'}) as req:
            req.session = SecureCookieSession(
                {_ELIGIBILITY_DATA_KEY: create_session_form_data(self.correct_session_data)})
            step = EligibilityStepChooser('eligibility').get_correct_step(
                InvestmentIncomeDecisionEligibilityInputFormSteuerlotseStep.name)
            expected_url = step.url_for_step(EmploymentDecisionEligibilityInputFormSteuerlotseStep.name)
            step.handle()

        self.assertEqual(expected_url, step.render_info.next_url)

    def test_if_session_data_correct_then_set_prev_input_step_correctly(self):
        with self.app.test_request_context(method='GET') as req:
            req.session = SecureCookieSession(
                {_ELIGIBILITY_DATA_KEY: create_session_form_data(self.correct_session_data)})
            step = EligibilityStepChooser('eligibility').get_correct_step(
                InvestmentIncomeDecisionEligibilityInputFormSteuerlotseStep.name)
            expected_url = step.url_for_step(PensionDecisionEligibilityInputFormSteuerlotseStep.name)
            step.handle()
        self.assertEqual(expected_url, step.render_info.prev_url)

    def test_if_post_and_data_from_before_invalid_then_raise_incorrect_eligibility_data_error(self):
        with self.app.test_request_context(method='POST', data={'investment_income_eligibility': 'yes'}), \
                patch('app.model.recursive_data.RecursiveDataModel.one_previous_field_has_to_be_set',
                      MagicMock(side_effect=PreviousFieldsMissingError)):
            step = EligibilityStepChooser('eligibility').get_correct_step(
                InvestmentIncomeDecisionEligibilityInputFormSteuerlotseStep.name)

            self.assertRaises(IncorrectEligibilityData, step.handle)

    def test_if_get_and_incorrect_data_from_session_then_delete_incorrect_data(self):
        session_data = {'marital_status_eligibility': 'single',
                        'separated_since_last_year_eligibility': 'no',
                        'user_a_has_elster_account_eligibility': 'no',
                        'user_b_has_elster_account_eligibility': 'no',
                        'joint_taxes_eligibility': 'no',
                        'alimony_eligibility': 'no',
                        'pension_eligibility': 'yes',
                        'investment_income_eligibility': 'no', }
        session_data_with_incorrect_key = {**session_data, **{'INCORRECT_KEY': 'UNNECESSARY_VALUE'}}
        with self.app.test_request_context(method='GET') as req:
            req.session = SecureCookieSession(
                {_ELIGIBILITY_DATA_KEY: create_session_form_data(session_data_with_incorrect_key)})
            step = EligibilityStepChooser('eligibility').get_correct_step(
                InvestmentIncomeDecisionEligibilityInputFormSteuerlotseStep.name)
            step.handle()

            self.assertEqual(session_data,
                             deserialize_session_data(req.session[_ELIGIBILITY_DATA_KEY]))

    def test_if_get_and_correct_data_from_session_then_do_not_delete_any_data(self):
        session_data = {'marital_status_eligibility': 'single',
                        'separated_since_last_year_eligibility': 'no',
                        'user_a_has_elster_account_eligibility': 'no',
                        'user_b_has_elster_account_eligibility': 'no',
                        'joint_taxes_eligibility': 'no',
                        'alimony_eligibility': 'no',
                        'pension_eligibility': 'yes',
                        'investment_income_eligibility': 'no', }
        with self.app.test_request_context(method='GET') as req:
            req.session = SecureCookieSession({_ELIGIBILITY_DATA_KEY: create_session_form_data(session_data)})
            step = EligibilityStepChooser('eligibility').get_correct_step(
                InvestmentIncomeDecisionEligibilityInputFormSteuerlotseStep.name)
            step.handle()

            self.assertEqual(session_data,
                             deserialize_session_data(req.session[_ELIGIBILITY_DATA_KEY]))

    def test_if_get_and_full_data_from_session_then_delete_unnecessary_data(self):
        only_necessary_data = {'marital_status_eligibility': 'single',
                               'separated_since_last_year_eligibility': 'no',
                               'separated_joint_taxes_eligibility': 'no',
                               'separated_lived_together_eligibility': 'no',
                               'user_a_has_elster_account_eligibility': 'no',
                               'user_b_has_elster_account_eligibility': 'no',
                               'elster_registration_method_eligibility': 'none',
                               'joint_taxes_eligibility': 'no',
                               'alimony_eligibility': 'no',
                               'pension_eligibility': 'yes',
                               'investment_income_eligibility': 'no', }
        with self.app.test_request_context(method='GET') as req:
            req.session = SecureCookieSession({_ELIGIBILITY_DATA_KEY: create_session_form_data(FULL_SESSION_DATA)})
            step = EligibilityStepChooser('eligibility').get_correct_step(
                InvestmentIncomeDecisionEligibilityInputFormSteuerlotseStep.name)
            step.handle()

            self.assertEqual(only_necessary_data,
                             deserialize_session_data(req.session[_ELIGIBILITY_DATA_KEY]))

    def test_if_multiple_users_then_show_multiple_text(self):
        session_data = {'marital_status_eligibility': 'married',
                        'separated_since_last_year_eligibility': 'no',
                        'joint_taxes_eligibility': 'yes',
                        'user_a_has_elster_account_eligibility': 'no',
                        'user_b_has_elster_account_eligibility': 'no',
                        'alimony_eligibility': 'no',
                        'pension_eligibility': 'yes'}
        expected_number_of_users = 2
        expected_choices = [('yes', ngettext('form.eligibility.investment_income.yes', 'form.eligibility.investment_income.yes', num=expected_number_of_users)),
                            ('no', ngettext('form.eligibility.investment_income.no', 'form.eligibility.investment_income.no', num=expected_number_of_users))]
        with self.app.test_request_context(method='GET') as req:
            req.session = SecureCookieSession({_ELIGIBILITY_DATA_KEY: create_session_form_data(session_data)})
            step = EligibilityStepChooser('eligibility').get_correct_step(
                InvestmentIncomeDecisionEligibilityInputFormSteuerlotseStep.name)
            step._pre_handle()

        self.assertEqual(expected_choices, step.form.investment_income_eligibility.kwargs['choices'])

    def test_if_single_user_then_show_single_text(self):
        session_data = {'marital_status_eligibility': 'single',
                        'separated_since_last_year_eligibility': 'no',
                        'user_a_has_elster_account_eligibility': 'no',
                        'user_b_has_elster_account_eligibility': 'no',
                        'joint_taxes_eligibility': 'no',
                        'alimony_eligibility': 'no',
                        'pension_eligibility': 'yes',}
        expected_number_of_users = 1
        expected_choices = [('yes', ngettext('form.eligibility.investment_income.yes', 'form.eligibility.investment_income.yes', num=expected_number_of_users)),
                            ('no', ngettext('form.eligibility.investment_income.no', 'form.eligibility.investment_income.no', num=expected_number_of_users))]
        with self.app.test_request_context(method='GET') as req:
            req.session = SecureCookieSession({_ELIGIBILITY_DATA_KEY: create_session_form_data(session_data)})
            step = EligibilityStepChooser('eligibility').get_correct_step(
                InvestmentIncomeDecisionEligibilityInputFormSteuerlotseStep.name)
            step._pre_handle()

        self.assertEqual(expected_choices, step.form.investment_income_eligibility.kwargs['choices'])


class TestMinimalInvestmentIncomeDecisionEligibilityInputFormSteuerlotseStep(unittest.TestCase):
    @pytest.fixture(autouse=True)
    def attach_fixtures(self, app):
        self.app = app

    def setUp(self):
        self.correct_session_data = {'marital_status_eligibility': 'divorced',
                                     'joint_taxes_eligibility': 'no',
                                     'alimony_eligibility': 'no',
                                     'user_a_has_elster_account_eligibility': 'no',
                                     'pension_eligibility': 'yes',
                                     'investment_income_eligibility': 'yes'}

    def test_if_post_and_session_data_correct_and_input_data_correct_than_set_next_input_step(self):
        with self.app.test_request_context(method='POST', data={'minimal_investment_income_eligibility': 'yes'}) as req:
            req.session = SecureCookieSession(
                {_ELIGIBILITY_DATA_KEY: create_session_form_data(self.correct_session_data)})
            step = EligibilityStepChooser('eligibility').get_correct_step(
                MinimalInvestmentIncomeDecisionEligibilityInputFormSteuerlotseStep.name)
            expected_url = step.url_for_step(EmploymentDecisionEligibilityInputFormSteuerlotseStep.name)
            step.handle()

        self.assertEqual(expected_url, step.render_info.next_url)

    def test_if_post_and_session_data_correct_and_input_data_incorrect_than_set_next_url_to_alternative_step(self):
        with self.app.test_request_context(method='POST', data={'minimal_investment_income_eligibility': 'no'}) as req:
            req.session = SecureCookieSession(
                {_ELIGIBILITY_DATA_KEY: create_session_form_data(self.correct_session_data)})
            step = EligibilityStepChooser('eligibility').get_correct_step(
                MinimalInvestmentIncomeDecisionEligibilityInputFormSteuerlotseStep.name)
            expected_url = step.url_for_step(TaxedInvestmentIncomeDecisionEligibilityInputFormSteuerlotseStep.name)
            step.handle()

        self.assertEqual(expected_url, step.render_info.next_url)

    def test_if_session_data_correct_then_set_prev_input_step_correctly(self):
        with self.app.test_request_context(method='GET') as req:
            req.session = SecureCookieSession(
                {_ELIGIBILITY_DATA_KEY: create_session_form_data(self.correct_session_data)})
            step = EligibilityStepChooser('eligibility').get_correct_step(
                MinimalInvestmentIncomeDecisionEligibilityInputFormSteuerlotseStep.name)
            expected_url = step.url_for_step(InvestmentIncomeDecisionEligibilityInputFormSteuerlotseStep.name)
            step.handle()
        self.assertEqual(expected_url, step.render_info.prev_url)

    def test_if_post_and_data_from_before_invalid_then_raise_incorrect_eligibility_data_error(self):
        with self.app.test_request_context(method='POST',
                                           data={'investment_income_eligibility': 'yes',
                                                 'minimal_investment_income_eligibility': 'no'}), \
                patch('app.model.recursive_data.RecursiveDataModel.one_previous_field_has_to_be_set',
                      MagicMock(side_effect=PreviousFieldsMissingError)):
            step = EligibilityStepChooser('eligibility').get_correct_step(
                MinimalInvestmentIncomeDecisionEligibilityInputFormSteuerlotseStep.name)

            self.assertRaises(IncorrectEligibilityData, step.handle)

    def test_if_get_and_incorrect_data_from_session_then_delete_incorrect_data(self):
        session_data = {'marital_status_eligibility': 'single',
                        'separated_since_last_year_eligibility': 'no',
                        'user_a_has_elster_account_eligibility': 'no',
                        'user_b_has_elster_account_eligibility': 'no',
                        'joint_taxes_eligibility': 'no',
                        'alimony_eligibility': 'no',
                        'pension_eligibility': 'yes',
                        'investment_income_eligibility': 'no',
                        'minimal_investment_income_eligibility': 'yes'}
        session_data_with_incorrect_key = {**session_data, **{'INCORRECT_KEY': 'UNNECESSARY_VALUE'}}
        with self.app.test_request_context(method='GET') as req:
            req.session = SecureCookieSession(
                {_ELIGIBILITY_DATA_KEY: create_session_form_data(session_data_with_incorrect_key)})
            step = EligibilityStepChooser('eligibility').get_correct_step(
                MinimalInvestmentIncomeDecisionEligibilityInputFormSteuerlotseStep.name)
            step.handle()

            self.assertEqual(session_data,
                             deserialize_session_data(req.session[_ELIGIBILITY_DATA_KEY]))

    def test_if_get_and_correct_data_from_session_then_do_not_delete_any_data(self):
        session_data = {'marital_status_eligibility': 'single',
                        'separated_since_last_year_eligibility': 'no',
                        'user_a_has_elster_account_eligibility': 'no',
                        'user_b_has_elster_account_eligibility': 'no',
                        'joint_taxes_eligibility': 'no',
                        'alimony_eligibility': 'no',
                        'pension_eligibility': 'yes',
                        'investment_income_eligibility': 'no',
                        'minimal_investment_income_eligibility': 'yes'}
        with self.app.test_request_context(method='GET') as req:
            req.session = SecureCookieSession({_ELIGIBILITY_DATA_KEY: create_session_form_data(session_data)})
            step = EligibilityStepChooser('eligibility').get_correct_step(
                MinimalInvestmentIncomeDecisionEligibilityInputFormSteuerlotseStep.name)
            step.handle()

            self.assertEqual(session_data,
                             deserialize_session_data(req.session[_ELIGIBILITY_DATA_KEY]))

    def test_if_get_and_full_data_from_session_then_delete_unnecessary_data(self):
        only_necessary_data = {'marital_status_eligibility': 'single',
                               'separated_since_last_year_eligibility': 'no',
                               'separated_lived_together_eligibility': 'no',
                               'separated_joint_taxes_eligibility': 'no',
                               'user_a_has_elster_account_eligibility': 'no',
                               'user_b_has_elster_account_eligibility': 'no',
                               'elster_registration_method_eligibility': 'none',
                               'joint_taxes_eligibility': 'no',
                               'alimony_eligibility': 'no',
                               'pension_eligibility': 'yes',
                               'investment_income_eligibility': 'no',
                               'minimal_investment_income_eligibility': 'yes'}
        with self.app.test_request_context(method='GET') as req:
            req.session = SecureCookieSession({_ELIGIBILITY_DATA_KEY: create_session_form_data(FULL_SESSION_DATA)})
            step = EligibilityStepChooser('eligibility').get_correct_step(
                MinimalInvestmentIncomeDecisionEligibilityInputFormSteuerlotseStep.name)
            step.handle()

            self.assertEqual(only_necessary_data,
                             deserialize_session_data(req.session[_ELIGIBILITY_DATA_KEY]))

    def test_if_multiple_users_then_show_multiple_text(self):
        session_data = {'marital_status_eligibility': 'married',
                        'separated_since_last_year_eligibility': 'no',
                        'joint_taxes_eligibility': 'yes',
                        'user_a_has_elster_account_eligibility': 'no',
                        'user_b_has_elster_account_eligibility': 'no',
                        'alimony_eligibility': 'no',
                        'pension_eligibility': 'yes',
                        'investment_income_eligibility': 'no',}
        expected_number_of_users = 2
        expected_choices = [('yes', ngettext('form.eligibility.minimal_investment_income.yes', 'form.eligibility.minimal_investment_income.yes', num=expected_number_of_users)),
                            ('no', ngettext('form.eligibility.minimal_investment_income.no', 'form.eligibility.minimal_investment_income.no', num=expected_number_of_users))]
        with self.app.test_request_context(method='GET') as req:
            req.session = SecureCookieSession({_ELIGIBILITY_DATA_KEY: create_session_form_data(session_data)})
            step = EligibilityStepChooser('eligibility').get_correct_step(
                MinimalInvestmentIncomeDecisionEligibilityInputFormSteuerlotseStep.name)
            step._pre_handle()

        self.assertEqual(expected_choices, step.form.minimal_investment_income_eligibility.kwargs['choices'])

    def test_if_single_user_then_show_single_text(self):
        session_data = {'marital_status_eligibility': 'single',
                        'separated_since_last_year_eligibility': 'no',
                        'user_a_has_elster_account_eligibility': 'no',
                        'user_b_has_elster_account_eligibility': 'no',
                        'joint_taxes_eligibility': 'no',
                        'alimony_eligibility': 'no',
                        'pension_eligibility': 'yes',
                        'investment_income_eligibility': 'no',}
        expected_number_of_users = 1
        expected_choices = [('yes', ngettext('form.eligibility.minimal_investment_income.yes', 'form.eligibility.minimal_investment_income.yes', num=expected_number_of_users)),
                            ('no', ngettext('form.eligibility.minimal_investment_income.no', 'form.eligibility.minimal_investment_income.no', num=expected_number_of_users))]
        with self.app.test_request_context(method='GET') as req:
            req.session = SecureCookieSession({_ELIGIBILITY_DATA_KEY: create_session_form_data(session_data)})
            step = EligibilityStepChooser('eligibility').get_correct_step(
                MinimalInvestmentIncomeDecisionEligibilityInputFormSteuerlotseStep.name)
            step._pre_handle()

        self.assertEqual(expected_choices, step.form.minimal_investment_income_eligibility.kwargs['choices'])


class TestTaxedInvestmentIncomeEligibilityFailureDisplaySteuerlotseStep(unittest.TestCase):
    @pytest.fixture(autouse=True)
    def attach_fixtures(self, test_request_context):
        self.req = test_request_context

    def test_handle_sets_correct_prev_url(self):
        step = TaxedInvestmentIncomeEligibilityFailureDisplaySteuerlotseStep(endpoint='eligibility')
        expected_url = step.url_for_step(TaxedInvestmentIncomeDecisionEligibilityInputFormSteuerlotseStep.name)
        step.handle()

        self.assertEqual(expected_url, step.render_info.prev_url)


class TestTaxedInvestmentIncomeDecisionEligibilityInputFormSteuerlotseStep(unittest.TestCase):
    @pytest.fixture(autouse=True)
    def attach_fixtures(self, app):
        self.app = app

    def setUp(self):
        self.correct_session_data = {'marital_status_eligibility': 'divorced',
                                     'joint_taxes_eligibility': 'no',
                                     'alimony_eligibility': 'no',
                                     'user_a_has_elster_account_eligibility': 'no',
                                     'pension_eligibility': 'yes',
                                     'investment_income_eligibility': 'yes',
                                     'minimal_investment_income_eligibility': 'no'}

    def test_if_post_and_session_data_correct_and_input_data_correct_than_set_next_input_step(self):
        with self.app.test_request_context(method='POST', data={'taxed_investment_income_eligibility': 'yes'}) as req:
            req.session = SecureCookieSession(
                {_ELIGIBILITY_DATA_KEY: create_session_form_data(self.correct_session_data)})
            step = EligibilityStepChooser('eligibility').get_correct_step(
                TaxedInvestmentIncomeDecisionEligibilityInputFormSteuerlotseStep.name)
            expected_url = step.url_for_step(CheaperCheckDecisionEligibilityInputFormSteuerlotseStep.name)
            step.handle()

        self.assertEqual(expected_url, step.render_info.next_url)

    def test_if_post_and_session_data_correct_and_input_data_incorrect_than_set_next_url_to_alternative_step(self):
        with self.app.test_request_context(method='POST', data={'taxed_investment_income_eligibility': 'no'}) as req:
            req.session = SecureCookieSession(
                {_ELIGIBILITY_DATA_KEY: create_session_form_data(self.correct_session_data)})
            step = EligibilityStepChooser('eligibility').get_correct_step(
                TaxedInvestmentIncomeDecisionEligibilityInputFormSteuerlotseStep.name)
            expected_url = step.url_for_step(TaxedInvestmentIncomeEligibilityFailureDisplaySteuerlotseStep.name)
            step.handle()

        self.assertEqual(expected_url, step.render_info.next_url)

    def test_if_session_data_correct_then_set_prev_input_step_correctly(self):
        with self.app.test_request_context(method='GET') as req:
            req.session = SecureCookieSession(
                {_ELIGIBILITY_DATA_KEY: create_session_form_data(self.correct_session_data)})
            step = EligibilityStepChooser('eligibility').get_correct_step(
                TaxedInvestmentIncomeDecisionEligibilityInputFormSteuerlotseStep.name)
            expected_url = step.url_for_step(MinimalInvestmentIncomeDecisionEligibilityInputFormSteuerlotseStep.name)
            step.handle()
        self.assertEqual(expected_url, step.render_info.prev_url)

    def test_if_post_and_data_from_before_invalid_then_raise_incorrect_eligibility_data_error(self):
        with self.app.test_request_context(method='POST', data={'taxed_investment_income_eligibility': 'yes'}), \
                patch('app.model.recursive_data.RecursiveDataModel.one_previous_field_has_to_be_set',
                      MagicMock(side_effect=PreviousFieldsMissingError)):
            step = EligibilityStepChooser('eligibility').get_correct_step(
                TaxedInvestmentIncomeDecisionEligibilityInputFormSteuerlotseStep.name)

            self.assertRaises(IncorrectEligibilityData, step.handle)

    def test_if_get_and_incorrect_data_from_session_then_delete_incorrect_data(self):
        session_data = {'marital_status_eligibility': 'single',
                        'separated_since_last_year_eligibility': 'no',
                        'user_a_has_elster_account_eligibility': 'no',
                        'user_b_has_elster_account_eligibility': 'no',
                        'joint_taxes_eligibility': 'no',
                        'alimony_eligibility': 'no',
                        'pension_eligibility': 'yes',
                        'investment_income_eligibility': 'no',
                        'minimal_investment_income_eligibility': 'yes',
                        'taxed_investment_income_eligibility': 'no'}
        session_data_with_incorrect_key = {**session_data, **{'INCORRECT_KEY': 'UNNECESSARY_VALUE'}}
        with self.app.test_request_context(method='GET') as req:
            req.session = SecureCookieSession(
                {_ELIGIBILITY_DATA_KEY: create_session_form_data(session_data_with_incorrect_key)})
            step = EligibilityStepChooser('eligibility').get_correct_step(
                TaxedInvestmentIncomeDecisionEligibilityInputFormSteuerlotseStep.name)
            step.handle()

            self.assertEqual(session_data,
                             deserialize_session_data(req.session[_ELIGIBILITY_DATA_KEY]))

    def test_if_get_and_correct_data_from_session_then_do_not_delete_any_data(self):
        session_data = {'marital_status_eligibility': 'single',
                        'separated_since_last_year_eligibility': 'no',
                        'user_a_has_elster_account_eligibility': 'no',
                        'user_b_has_elster_account_eligibility': 'no',
                        'joint_taxes_eligibility': 'no',
                        'alimony_eligibility': 'no',
                        'pension_eligibility': 'yes',
                        'investment_income_eligibility': 'no',
                        'minimal_investment_income_eligibility': 'yes',
                        'taxed_investment_income_eligibility': 'no'}
        with self.app.test_request_context(method='GET') as req:
            req.session = SecureCookieSession({_ELIGIBILITY_DATA_KEY: create_session_form_data(session_data)})
            step = EligibilityStepChooser('eligibility').get_correct_step(
                TaxedInvestmentIncomeDecisionEligibilityInputFormSteuerlotseStep.name)
            step.handle()

            self.assertEqual(session_data,
                             deserialize_session_data(req.session[_ELIGIBILITY_DATA_KEY]))

    def test_if_get_and_full_data_from_session_then_delete_unnecessary_data(self):
        only_necessary_data = {'marital_status_eligibility': 'single',
                               'separated_since_last_year_eligibility': 'no',
                               'separated_lived_together_eligibility': 'no',
                               'separated_joint_taxes_eligibility': 'no',
                               'user_a_has_elster_account_eligibility': 'no',
                               'user_b_has_elster_account_eligibility': 'no',
                               'elster_registration_method_eligibility': 'none',
                               'joint_taxes_eligibility': 'no',
                               'alimony_eligibility': 'no',
                               'pension_eligibility': 'yes',
                               'investment_income_eligibility': 'no',
                               'minimal_investment_income_eligibility': 'yes',
                               'taxed_investment_income_eligibility': 'no'}
        with self.app.test_request_context(method='GET') as req:
            req.session = SecureCookieSession({_ELIGIBILITY_DATA_KEY: create_session_form_data(FULL_SESSION_DATA)})
            step = EligibilityStepChooser('eligibility').get_correct_step(
                TaxedInvestmentIncomeDecisionEligibilityInputFormSteuerlotseStep.name)
            step.handle()

            self.assertEqual(only_necessary_data,
                             deserialize_session_data(req.session[_ELIGIBILITY_DATA_KEY]))


class TestCheaperCheckEligibilityFailureDisplaySteuerlotseStep(unittest.TestCase):
    @pytest.fixture(autouse=True)
    def attach_fixtures(self, test_request_context):
        self.req = test_request_context

    def test_handle_sets_correct_prev_url(self):
        step = CheaperCheckEligibilityFailureDisplaySteuerlotseStep(endpoint='eligibility')
        expected_url = step.url_for_step(CheaperCheckDecisionEligibilityInputFormSteuerlotseStep.name)
        step.handle()

        self.assertEqual(expected_url, step.render_info.prev_url)


class TestCheaperCheckDecisionEligibilityInputFormSteuerlotseStep(unittest.TestCase):
    @pytest.fixture(autouse=True)
    def attach_fixtures(self, app):
        self.app = app

    def setUp(self):
        self.correct_session_data = {'marital_status_eligibility': 'divorced',
                                     'joint_taxes_eligibility': 'no',
                                     'alimony_eligibility': 'no',
                                     'user_a_has_elster_account_eligibility': 'no',
                                     'pension_eligibility': 'yes',
                                     'investment_income_eligibility': 'yes',
                                     'minimal_investment_income_eligibility': 'no',
                                     'taxed_investment_income_eligibility': 'yes'}

    def test_if_post_and_session_data_correct_and_input_data_correct_than_set_next_input_step(self):
        with self.app.test_request_context(method='POST', data={'cheaper_check_eligibility': 'no'}) as req:
            req.session = SecureCookieSession(
                {_ELIGIBILITY_DATA_KEY: create_session_form_data(self.correct_session_data)})
            step = EligibilityStepChooser('eligibility').get_correct_step(
                CheaperCheckDecisionEligibilityInputFormSteuerlotseStep.name)
            expected_url = step.url_for_step(EmploymentDecisionEligibilityInputFormSteuerlotseStep.name)
            step.handle()

        self.assertEqual(expected_url, step.render_info.next_url)

    def test_if_post_and_session_data_correct_and_input_data_incorrect_than_set_next_url_to_alternative_step(self):
        with self.app.test_request_context(method='POST', data={'cheaper_check_eligibility': 'yes'}) as req:
            req.session = SecureCookieSession(
                {_ELIGIBILITY_DATA_KEY: create_session_form_data(self.correct_session_data)})
            step = EligibilityStepChooser('eligibility').get_correct_step(
                CheaperCheckDecisionEligibilityInputFormSteuerlotseStep.name)
            expected_url = step.url_for_step(CheaperCheckEligibilityFailureDisplaySteuerlotseStep.name)
            step.handle()

        self.assertEqual(expected_url, step.render_info.next_url)

    def test_if_session_data_correct_then_set_prev_input_step_correctly(self):
        with self.app.test_request_context(method='GET') as req:
            req.session = SecureCookieSession(
                {_ELIGIBILITY_DATA_KEY: create_session_form_data(self.correct_session_data)})
            step = EligibilityStepChooser('eligibility').get_correct_step(
                CheaperCheckDecisionEligibilityInputFormSteuerlotseStep.name)
            expected_url = step.url_for_step(TaxedInvestmentIncomeDecisionEligibilityInputFormSteuerlotseStep.name)
            step.handle()
        self.assertEqual(expected_url, step.render_info.prev_url)

    def test_if_post_and_data_from_before_invalid_then_raise_incorrect_eligibility_data_error(self):
        with self.app.test_request_context(method='POST', data={'cheaper_check_eligibility': 'no'}), \
                patch('app.model.recursive_data.RecursiveDataModel.one_previous_field_has_to_be_set',
                      MagicMock(side_effect=PreviousFieldsMissingError)):
            step = EligibilityStepChooser('eligibility').get_correct_step(
                CheaperCheckDecisionEligibilityInputFormSteuerlotseStep.name)

            self.assertRaises(IncorrectEligibilityData, step.handle)

    def test_if_get_and_incorrect_data_from_session_then_delete_incorrect_data(self):
        session_data = {'marital_status_eligibility': 'single',
                        'separated_since_last_year_eligibility': 'no',
                        'user_a_has_elster_account_eligibility': 'no',
                        'user_b_has_elster_account_eligibility': 'no',
                        'joint_taxes_eligibility': 'no',
                        'alimony_eligibility': 'no',
                        'pension_eligibility': 'yes',
                        'investment_income_eligibility': 'no',
                        'minimal_investment_income_eligibility': 'yes',
                        'taxed_investment_income_eligibility': 'no',
                        'cheaper_check_eligibility': 'no', }
        session_data_with_incorrect_key = {**session_data, **{'INCORRECT_KEY': 'UNNECESSARY_VALUE'}}
        with self.app.test_request_context(method='GET') as req:
            req.session = SecureCookieSession(
                {_ELIGIBILITY_DATA_KEY: create_session_form_data(session_data_with_incorrect_key)})
            step = EligibilityStepChooser('eligibility').get_correct_step(
                CheaperCheckDecisionEligibilityInputFormSteuerlotseStep.name)
            step.handle()

            self.assertEqual(session_data,
                             deserialize_session_data(req.session[_ELIGIBILITY_DATA_KEY]))

    def test_if_get_and_correct_data_from_session_then_do_not_delete_any_data(self):
        session_data = {'marital_status_eligibility': 'single',
                        'separated_since_last_year_eligibility': 'no',
                        'user_a_has_elster_account_eligibility': 'no',
                        'user_b_has_elster_account_eligibility': 'no',
                        'joint_taxes_eligibility': 'no',
                        'alimony_eligibility': 'no',
                        'pension_eligibility': 'yes',
                        'investment_income_eligibility': 'no',
                        'minimal_investment_income_eligibility': 'yes',
                        'taxed_investment_income_eligibility': 'no',
                        'cheaper_check_eligibility': 'no', }
        with self.app.test_request_context(method='GET') as req:
            req.session = SecureCookieSession({_ELIGIBILITY_DATA_KEY: create_session_form_data(session_data)})
            step = EligibilityStepChooser('eligibility').get_correct_step(
                CheaperCheckDecisionEligibilityInputFormSteuerlotseStep.name)
            step.handle()

            self.assertEqual(session_data,
                             deserialize_session_data(req.session[_ELIGIBILITY_DATA_KEY]))

    def test_if_get_and_full_data_from_session_then_delete_unnecessary_data(self):
        only_necessary_data = {'marital_status_eligibility': 'single',
                               'separated_since_last_year_eligibility': 'no',
                               'separated_lived_together_eligibility': 'no',
                               'separated_joint_taxes_eligibility': 'no',
                               'user_a_has_elster_account_eligibility': 'no',
                               'user_b_has_elster_account_eligibility': 'no',
                               'elster_registration_method_eligibility': 'none',
                               'joint_taxes_eligibility': 'no',
                               'alimony_eligibility': 'no',
                               'pension_eligibility': 'yes',
                               'investment_income_eligibility': 'no',
                               'minimal_investment_income_eligibility': 'yes',
                               'taxed_investment_income_eligibility': 'no',
                               'cheaper_check_eligibility': 'no', }
        with self.app.test_request_context(method='GET') as req:
            req.session = SecureCookieSession({_ELIGIBILITY_DATA_KEY: create_session_form_data(FULL_SESSION_DATA)})
            step = EligibilityStepChooser('eligibility').get_correct_step(
                CheaperCheckDecisionEligibilityInputFormSteuerlotseStep.name)
            step.handle()

            self.assertEqual(only_necessary_data,
                             deserialize_session_data(req.session[_ELIGIBILITY_DATA_KEY]))

    def test_if_multiple_users_then_show_multiple_text(self):
        session_data = {'marital_status_eligibility': 'married',
                        'separated_since_last_year_eligibility': 'no',
                        'joint_taxes_eligibility': 'yes',
                        'user_a_has_elster_account_eligibility': 'no',
                        'user_b_has_elster_account_eligibility': 'no',
                        'alimony_eligibility': 'no',
                        'pension_eligibility': 'yes',
                        'investment_income_eligibility': 'no',
                        'taxed_investment_income_eligibility': 'no'}
        expected_number_of_users = 2
        expected_choices = [('yes', ngettext('form.eligibility.cheaper_check_eligibility.yes', 'form.eligibility.cheaper_check_eligibility.yes', num=expected_number_of_users)),
                            ('no', ngettext('form.eligibility.cheaper_check_eligibility.no', 'form.eligibility.cheaper_check_eligibility.no', num=expected_number_of_users))]
        with self.app.test_request_context(method='GET') as req:
            req.session = SecureCookieSession({_ELIGIBILITY_DATA_KEY: create_session_form_data(session_data)})
            step = EligibilityStepChooser('eligibility').get_correct_step(
                CheaperCheckDecisionEligibilityInputFormSteuerlotseStep.name)
            step._pre_handle()

        self.assertEqual(expected_choices, step.form.cheaper_check_eligibility.kwargs['choices'])

    def test_if_single_user_then_show_single_text(self):
        session_data = {'marital_status_eligibility': 'single',
                        'separated_since_last_year_eligibility': 'no',
                        'user_a_has_elster_account_eligibility': 'no',
                        'user_b_has_elster_account_eligibility': 'no',
                        'joint_taxes_eligibility': 'no',
                        'alimony_eligibility': 'no',
                        'pension_eligibility': 'yes',
                        'investment_income_eligibility': 'no',
                        'taxed_investment_income_eligibility': 'no'}
        expected_number_of_users = 1
        expected_choices = [('yes', ngettext('form.eligibility.cheaper_check_eligibility.yes', 'form.eligibility.cheaper_check_eligibility.yes', num=expected_number_of_users)),
                            ('no', ngettext('form.eligibility.cheaper_check_eligibility.no', 'form.eligibility.cheaper_check_eligibility.no', num=expected_number_of_users))]
        with self.app.test_request_context(method='GET') as req:
            req.session = SecureCookieSession({_ELIGIBILITY_DATA_KEY: create_session_form_data(session_data)})
            step = EligibilityStepChooser('eligibility').get_correct_step(
                CheaperCheckDecisionEligibilityInputFormSteuerlotseStep.name)
            step._pre_handle()

        self.assertEqual(expected_choices, step.form.cheaper_check_eligibility.kwargs['choices'])


class TestEmploymentDecisionEligibilityInputFormSteuerlotseStep(unittest.TestCase):
    @pytest.fixture(autouse=True)
    def attach_fixtures(self, app):
        self.app = app

    def setUp(self):
        self.correct_session_data = {'marital_status_eligibility': 'divorced',
                                     'joint_taxes_eligibility': 'no',
                                     'alimony_eligibility': 'no',
                                     'user_a_has_elster_account_eligibility': 'no',
                                     'pension_eligibility': 'yes',
                                     'investment_income_eligibility': 'yes',
                                     'minimal_investment_income_eligibility': 'no',
                                     'taxed_investment_income_eligibility': 'yes',
                                     'cheaper_check_eligibility': 'no'}

    def test_if_post_and_session_data_correct_and_input_data_correct_than_set_next_input_step(self):
        with self.app.test_request_context(method='POST', data={'employment_income_eligibility': 'no'}) as req:
            req.session = SecureCookieSession(
                {_ELIGIBILITY_DATA_KEY: create_session_form_data(self.correct_session_data)})
            step = EligibilityStepChooser('eligibility').get_correct_step(
                EmploymentDecisionEligibilityInputFormSteuerlotseStep.name)
            expected_url = step.url_for_step(IncomeOtherDecisionEligibilityInputFormSteuerlotseStep.name)
            step.handle()

        self.assertEqual(expected_url, step.render_info.next_url)

    def test_if_post_and_session_data_correct_and_input_data_incorrect_than_set_next_url_to_alternative_step(self):
        with self.app.test_request_context(method='POST', data={'employment_income_eligibility': 'yes'}) as req:
            req.session = SecureCookieSession(
                {_ELIGIBILITY_DATA_KEY: create_session_form_data(self.correct_session_data)})
            step = EligibilityStepChooser('eligibility').get_correct_step(
                EmploymentDecisionEligibilityInputFormSteuerlotseStep.name)
            expected_url = step.url_for_step(MarginalEmploymentIncomeDecisionEligibilityInputFormSteuerlotseStep.name)
            step.handle()

        self.assertEqual(expected_url, step.render_info.next_url)

    def test_if_incomes_but_no_cheaper_check_session_data_correct_then_set_prev_input_step_correctly(self):
        with self.app.test_request_context(method='GET') as req:
            req.session = SecureCookieSession(
                {_ELIGIBILITY_DATA_KEY: create_session_form_data(self.correct_session_data)})
            step = EligibilityStepChooser('eligibility').get_correct_step(
                EmploymentDecisionEligibilityInputFormSteuerlotseStep.name)
            expected_url = step.url_for_step(CheaperCheckDecisionEligibilityInputFormSteuerlotseStep.name)
            step.handle()
        self.assertEqual(expected_url, step.render_info.prev_url)

    def test_if_incomes_but_minimal_investment_session_data_correct_then_set_prev_input_step_correctly(self):
        alternative_data = {**self.correct_session_data.copy(), **{'minimal_investment_income_eligibility': 'yes'}}
        with self.app.test_request_context(method='GET') as req:
            req.session = SecureCookieSession({_ELIGIBILITY_DATA_KEY: create_session_form_data(alternative_data)})
            step = EligibilityStepChooser('eligibility').get_correct_step(
                EmploymentDecisionEligibilityInputFormSteuerlotseStep.name)
            expected_url = step.url_for_step(MinimalInvestmentIncomeDecisionEligibilityInputFormSteuerlotseStep.name)
            step.handle()
        self.assertEqual(expected_url, step.render_info.prev_url)

    def test_if_no_incomes_session_data_correct_then_set_prev_input_step_correctly(self):
        alternative_data = {**self.correct_session_data.copy(), **{'investment_income_eligibility': 'no'}}
        with self.app.test_request_context(method='GET') as req:
            req.session = SecureCookieSession({_ELIGIBILITY_DATA_KEY: create_session_form_data(alternative_data)})
            step = EligibilityStepChooser('eligibility').get_correct_step(
                EmploymentDecisionEligibilityInputFormSteuerlotseStep.name)
            expected_url = step.url_for_step(InvestmentIncomeDecisionEligibilityInputFormSteuerlotseStep.name)
            step.handle()
        self.assertEqual(expected_url, step.render_info.prev_url)

    def test_if_post_and_data_from_before_invalid_then_raise_incorrect_eligibility_data_error(self):
        with self.app.test_request_context(method='POST', data={'employment_income_eligibility': 'no'}), \
                patch('app.model.recursive_data.RecursiveDataModel.one_previous_field_has_to_be_set',
                      MagicMock(side_effect=PreviousFieldsMissingError)):
            step = EligibilityStepChooser('eligibility').get_correct_step(
                EmploymentDecisionEligibilityInputFormSteuerlotseStep.name)

            self.assertRaises(IncorrectEligibilityData, step.handle)

    def test_if_get_and_incorrect_data_from_session_then_delete_incorrect_data(self):
        session_data = {'marital_status_eligibility': 'single',
                        'separated_since_last_year_eligibility': 'no',
                        'user_a_has_elster_account_eligibility': 'no',
                        'user_b_has_elster_account_eligibility': 'no',
                        'joint_taxes_eligibility': 'no',
                        'alimony_eligibility': 'no',
                        'pension_eligibility': 'yes',
                        'investment_income_eligibility': 'no',
                        'minimal_investment_income_eligibility': 'yes',
                        'taxed_investment_income_eligibility': 'no',
                        'cheaper_check_eligibility': 'no',
                        'employment_income_eligibility': 'no', }
        session_data_with_incorrect_key = {**session_data, **{'INCORRECT_KEY': 'UNNECESSARY_VALUE'}}
        with self.app.test_request_context(method='GET') as req:
            req.session = SecureCookieSession(
                {_ELIGIBILITY_DATA_KEY: create_session_form_data(session_data_with_incorrect_key)})
            step = EligibilityStepChooser('eligibility').get_correct_step(
                EmploymentDecisionEligibilityInputFormSteuerlotseStep.name)
            step.handle()

            self.assertEqual(session_data,
                             deserialize_session_data(req.session[_ELIGIBILITY_DATA_KEY]))

    def test_if_get_and_correct_data_from_session_then_do_not_delete_any_data(self):
        session_data = {'marital_status_eligibility': 'single',
                        'separated_since_last_year_eligibility': 'no',
                        'user_a_has_elster_account_eligibility': 'no',
                        'user_b_has_elster_account_eligibility': 'no',
                        'joint_taxes_eligibility': 'no',
                        'alimony_eligibility': 'no',
                        'pension_eligibility': 'yes',
                        'investment_income_eligibility': 'no',
                        'minimal_investment_income_eligibility': 'yes',
                        'taxed_investment_income_eligibility': 'no',
                        'cheaper_check_eligibility': 'no',
                        'employment_income_eligibility': 'no', }
        with self.app.test_request_context(method='GET') as req:
            req.session = SecureCookieSession({_ELIGIBILITY_DATA_KEY: create_session_form_data(session_data)})
            step = EligibilityStepChooser('eligibility').get_correct_step(
                EmploymentDecisionEligibilityInputFormSteuerlotseStep.name)
            step.handle()

            self.assertEqual(session_data,
                             deserialize_session_data(req.session[_ELIGIBILITY_DATA_KEY]))

    def test_if_get_and_full_data_from_session_then_delete_unnecessary_data(self):
        only_necessary_data = {'marital_status_eligibility': 'single',
                               'separated_since_last_year_eligibility': 'no',
                               'separated_lived_together_eligibility': 'no',
                               'separated_joint_taxes_eligibility': 'no',
                               'user_a_has_elster_account_eligibility': 'no',
                               'user_b_has_elster_account_eligibility': 'no',
                               'elster_registration_method_eligibility': 'none',
                               'joint_taxes_eligibility': 'no',
                               'alimony_eligibility': 'no',
                               'pension_eligibility': 'yes',
                               'investment_income_eligibility': 'no',
                               'minimal_investment_income_eligibility': 'yes',
                               'taxed_investment_income_eligibility': 'no',
                               'cheaper_check_eligibility': 'no',
                               'employment_income_eligibility': 'no', }
        with self.app.test_request_context(method='GET') as req:
            req.session = SecureCookieSession({_ELIGIBILITY_DATA_KEY: create_session_form_data(FULL_SESSION_DATA)})
            step = EligibilityStepChooser('eligibility').get_correct_step(
                EmploymentDecisionEligibilityInputFormSteuerlotseStep.name)
            step.handle()

            self.assertEqual(only_necessary_data,
                             deserialize_session_data(req.session[_ELIGIBILITY_DATA_KEY]))

    def test_if_multiple_users_then_show_multiple_text(self):
        session_data = {'marital_status_eligibility': 'married',
                        'separated_since_last_year_eligibility': 'no',
                        'joint_taxes_eligibility': 'yes',
                        'user_a_has_elster_account_eligibility': 'no',
                        'user_b_has_elster_account_eligibility': 'no',
                        'alimony_eligibility': 'no',
                        'pension_eligibility': 'yes',
                        'investment_income_eligibility': 'no',
                        'taxed_investment_income_eligibility': 'no',
                        'employment_income_eligibility': 'no'}
        expected_number_of_users = 2
        expected_choices = [('yes', ngettext('form.eligibility.employment_income.yes', 'form.eligibility.employment_income.yes', num=expected_number_of_users)),
                            ('no', ngettext('form.eligibility.employment_income.no', 'form.eligibility.employment_income.no', num=expected_number_of_users))]
        with self.app.test_request_context(method='GET') as req:
            req.session = SecureCookieSession({_ELIGIBILITY_DATA_KEY: create_session_form_data(session_data)})
            step = EligibilityStepChooser('eligibility').get_correct_step(
                EmploymentDecisionEligibilityInputFormSteuerlotseStep.name)
            step._pre_handle()

        self.assertEqual(expected_choices, step.form.employment_income_eligibility.kwargs['choices'])

    def test_if_single_user_then_show_single_text(self):
        session_data = {'marital_status_eligibility': 'single',
                        'separated_since_last_year_eligibility': 'no',
                        'user_a_has_elster_account_eligibility': 'no',
                        'user_b_has_elster_account_eligibility': 'no',
                        'joint_taxes_eligibility': 'no',
                        'alimony_eligibility': 'no',
                        'pension_eligibility': 'yes',
                        'investment_income_eligibility': 'no',
                        'taxed_investment_income_eligibility': 'no',
                        'employment_income_eligibility': 'no'}
        expected_number_of_users = 1
        expected_choices = [('yes', ngettext('form.eligibility.employment_income.yes', 'form.eligibility.employment_income.yes', num=expected_number_of_users)),
                            ('no', ngettext('form.eligibility.employment_income.no', 'form.eligibility.employment_income.no', num=expected_number_of_users))]
        with self.app.test_request_context(method='GET') as req:
            req.session = SecureCookieSession({_ELIGIBILITY_DATA_KEY: create_session_form_data(session_data)})
            step = EligibilityStepChooser('eligibility').get_correct_step(
                EmploymentDecisionEligibilityInputFormSteuerlotseStep.name)
            step._pre_handle()

        self.assertEqual(expected_choices, step.form.employment_income_eligibility.kwargs['choices'])


class TestMarginalEmploymentIncomeEligibilityFailureDisplaySteuerlotseStep(unittest.TestCase):
    @pytest.fixture(autouse=True)
    def attach_fixtures(self, test_request_context):
        self.req = test_request_context

    def test_handle_sets_correct_prev_url(self):
        step = MarginalEmploymentIncomeEligibilityFailureDisplaySteuerlotseStep(endpoint='eligibility')
        expected_url = step.url_for_step(MarginalEmploymentIncomeDecisionEligibilityInputFormSteuerlotseStep.name)
        step.handle()

        self.assertEqual(expected_url, step.render_info.prev_url)


class TestMarginalEmploymentIncomeDecisionEligibilityInputFormSteuerlotseStep(unittest.TestCase):
    @pytest.fixture(autouse=True)
    def attach_fixtures(self, app):
        self.app = app

    def setUp(self):
        self.correct_session_data = {'marital_status_eligibility': 'divorced',
                                     'joint_taxes_eligibility': 'no',
                                     'alimony_eligibility': 'no',
                                     'user_a_has_elster_account_eligibility': 'no',
                                     'pension_eligibility': 'yes',
                                     'investment_income_eligibility': 'yes',
                                     'minimal_investment_income_eligibility': 'no',
                                     'taxed_investment_income_eligibility': 'yes',
                                     'cheaper_check_eligibility': 'no',
                                     'employment_income_eligibility': 'yes'}

    def test_if_post_and_session_data_correct_and_input_data_correct_than_set_next_input_step(self):
        with self.app.test_request_context(method='POST', data={'marginal_employment_eligibility': 'yes'}) as req:
            req.session = SecureCookieSession(
                {_ELIGIBILITY_DATA_KEY: create_session_form_data(self.correct_session_data)})
            step = EligibilityStepChooser('eligibility').get_correct_step(
                MarginalEmploymentIncomeDecisionEligibilityInputFormSteuerlotseStep.name)
            expected_url = step.url_for_step(IncomeOtherDecisionEligibilityInputFormSteuerlotseStep.name)
            step.handle()

        self.assertEqual(expected_url, step.render_info.next_url)

    def test_if_session_data_correct_then_set_prev_input_step_correctly(self):
        with self.app.test_request_context(method='GET') as req:
            req.session = SecureCookieSession(
                {_ELIGIBILITY_DATA_KEY: create_session_form_data(self.correct_session_data)})
            step = EligibilityStepChooser('eligibility').get_correct_step(
                MarginalEmploymentIncomeDecisionEligibilityInputFormSteuerlotseStep.name)
            expected_url = step.url_for_step(EmploymentDecisionEligibilityInputFormSteuerlotseStep.name)
            step.handle()

        self.assertEqual(expected_url, step.render_info.prev_url)

    def test_if_post_and_session_data_correct_and_input_data_incorrect_than_set_next_url_to_alternative_step(self):
        with self.app.test_request_context(method='POST', data={'marginal_employment_eligibility': 'no'}) as req:
            req.session = SecureCookieSession(
                {_ELIGIBILITY_DATA_KEY: create_session_form_data(self.correct_session_data)})
            step = EligibilityStepChooser('eligibility').get_correct_step(
                MarginalEmploymentIncomeDecisionEligibilityInputFormSteuerlotseStep.name)
            expected_url = step.url_for_step(MarginalEmploymentIncomeEligibilityFailureDisplaySteuerlotseStep.name)
            step.handle()

        self.assertEqual(expected_url, step.render_info.next_url)

    def test_if_post_and_data_from_before_invalid_then_raise_incorrect_eligibility_data_error(self):
        with self.app.test_request_context(method='POST', data={'marginal_employment_eligibility': 'yes'}), \
                patch('app.model.recursive_data.RecursiveDataModel.one_previous_field_has_to_be_set',
                      MagicMock(side_effect=PreviousFieldsMissingError)):
            step = EligibilityStepChooser('eligibility').get_correct_step(
                MarginalEmploymentIncomeDecisionEligibilityInputFormSteuerlotseStep.name)

            self.assertRaises(IncorrectEligibilityData, step.handle)

    def test_if_get_and_incorrect_data_from_session_then_delete_incorrect_data(self):
        session_data = {'marital_status_eligibility': 'single',
                        'separated_since_last_year_eligibility': 'no',
                        'user_a_has_elster_account_eligibility': 'no',
                        'user_b_has_elster_account_eligibility': 'no',
                        'joint_taxes_eligibility': 'no',
                        'alimony_eligibility': 'no',
                        'pension_eligibility': 'yes',
                        'investment_income_eligibility': 'no',
                        'minimal_investment_income_eligibility': 'yes',
                        'taxed_investment_income_eligibility': 'no',
                        'cheaper_check_eligibility': 'no',
                        'employment_income_eligibility': 'no',
                        'marginal_employment_eligibility': 'yes', }
        session_data_with_incorrect_key = {**session_data, **{'INCORRECT_KEY': 'UNNECESSARY_VALUE'}}
        with self.app.test_request_context(method='GET') as req:
            req.session = SecureCookieSession(
                {_ELIGIBILITY_DATA_KEY: create_session_form_data(session_data_with_incorrect_key)})
            step = EligibilityStepChooser('eligibility').get_correct_step(
                MarginalEmploymentIncomeDecisionEligibilityInputFormSteuerlotseStep.name)
            step.handle()

            self.assertEqual(session_data,
                             deserialize_session_data(req.session[_ELIGIBILITY_DATA_KEY]))

    def test_if_get_and_correct_data_from_session_then_do_not_delete_any_data(self):
        session_data = {'marital_status_eligibility': 'single',
                        'separated_since_last_year_eligibility': 'no',
                        'user_a_has_elster_account_eligibility': 'no',
                        'user_b_has_elster_account_eligibility': 'no',
                        'joint_taxes_eligibility': 'no',
                        'alimony_eligibility': 'no',
                        'pension_eligibility': 'yes',
                        'investment_income_eligibility': 'no',
                        'minimal_investment_income_eligibility': 'yes',
                        'taxed_investment_income_eligibility': 'no',
                        'cheaper_check_eligibility': 'no',
                        'employment_income_eligibility': 'no',
                        'marginal_employment_eligibility': 'yes', }
        with self.app.test_request_context(method='GET') as req:
            req.session = SecureCookieSession({_ELIGIBILITY_DATA_KEY: create_session_form_data(session_data)})
            step = EligibilityStepChooser('eligibility').get_correct_step(
                MarginalEmploymentIncomeDecisionEligibilityInputFormSteuerlotseStep.name)
            step.handle()

            self.assertEqual(session_data,
                             deserialize_session_data(req.session[_ELIGIBILITY_DATA_KEY]))

    def test_if_get_and_full_data_from_session_then_delete_unnecessary_data(self):
        only_necessary_data = {'marital_status_eligibility': 'single',
                               'separated_since_last_year_eligibility': 'no',
                               'separated_lived_together_eligibility': 'no',
                               'separated_joint_taxes_eligibility': 'no',
                               'user_a_has_elster_account_eligibility': 'no',
                               'user_b_has_elster_account_eligibility': 'no',
                               'elster_registration_method_eligibility': 'none',
                               'joint_taxes_eligibility': 'no',
                               'alimony_eligibility': 'no',
                               'pension_eligibility': 'yes',
                               'investment_income_eligibility': 'no',
                               'minimal_investment_income_eligibility': 'yes',
                               'taxed_investment_income_eligibility': 'no',
                               'cheaper_check_eligibility': 'no',
                               'employment_income_eligibility': 'no',
                               'marginal_employment_eligibility': 'yes', }
        with self.app.test_request_context(method='GET') as req:
            req.session = SecureCookieSession({_ELIGIBILITY_DATA_KEY: create_session_form_data(FULL_SESSION_DATA)})
            step = EligibilityStepChooser('eligibility').get_correct_step(
                MarginalEmploymentIncomeDecisionEligibilityInputFormSteuerlotseStep.name)
            step.handle()

            self.assertEqual(only_necessary_data,
                             deserialize_session_data(req.session[_ELIGIBILITY_DATA_KEY]))


class TestIncomeOtherEligibilityFailureDisplaySteuerlotseStep(unittest.TestCase):
    @pytest.fixture(autouse=True)
    def attach_fixtures(self, test_request_context):
        self.req = test_request_context

    def test_handle_sets_correct_prev_url(self):
        step = IncomeOtherEligibilityFailureDisplaySteuerlotseStep(endpoint='eligibility')
        expected_url = step.url_for_step(IncomeOtherDecisionEligibilityInputFormSteuerlotseStep.name)
        step.handle()

        self.assertEqual(expected_url, step.render_info.prev_url)


class TestIncomeOtherDecisionEligibilityInputFormSteuerlotseStep(unittest.TestCase):
    @pytest.fixture(autouse=True)
    def attach_fixtures(self, app):
        self.app = app

    def setUp(self):
        self.correct_session_data = {'marital_status_eligibility': 'single',
                                     'separated_since_last_year_eligibility': 'no',
                                     'user_a_has_elster_account_eligibility': 'no',
                                     'user_b_has_elster_account_eligibility': 'no',
                                     'joint_taxes_eligibility': 'no',
                                     'alimony_eligibility': 'no',
                                     'pension_eligibility': 'yes',
                                     'investment_income_eligibility': 'no',
                                     'minimal_investment_income_eligibility': 'yes',
                                     'taxed_investment_income_eligibility': 'no',
                                     'cheaper_check_eligibility': 'no',
                                     'employment_income_eligibility': 'no',
                                     'other_income_eligibility': 'no'}

    def test_if_post_and_session_data_correct_and_input_data_correct_than_set_next_input_step(self):
        with self.app.test_request_context(method='POST', data={'other_income_eligibility': 'no'}) as req:
            req.session = SecureCookieSession(
                {_ELIGIBILITY_DATA_KEY: create_session_form_data(self.correct_session_data)})
            step = EligibilityStepChooser('eligibility').get_correct_step(
                IncomeOtherDecisionEligibilityInputFormSteuerlotseStep.name)
            expected_url = step.url_for_step(ForeignCountriesDecisionEligibilityInputFormSteuerlotseStep.name)
            step.handle()

        self.assertEqual(expected_url, step.render_info.next_url)

    def test_if_post_and_session_data_correct_and_input_data_incorrect_than_set_next_url_to_alternative_step(self):
        with self.app.test_request_context(method='POST', data={'other_income_eligibility': 'yes'}) as req:
            req.session = SecureCookieSession(
                {_ELIGIBILITY_DATA_KEY: create_session_form_data(self.correct_session_data)})
            step = EligibilityStepChooser('eligibility').get_correct_step(
                IncomeOtherDecisionEligibilityInputFormSteuerlotseStep.name)
            expected_url = step.url_for_step(IncomeOtherEligibilityFailureDisplaySteuerlotseStep.name)
            step.handle()

        self.assertEqual(expected_url, step.render_info.next_url)

    def test_if_no_employment_income_session_data_correct_then_set_prev_url_correct(self):
        with self.app.test_request_context(method='GET') as req:
            req.session = SecureCookieSession(
                {_ELIGIBILITY_DATA_KEY: create_session_form_data(self.correct_session_data)})
            step = EligibilityStepChooser('eligibility').get_correct_step(
                IncomeOtherDecisionEligibilityInputFormSteuerlotseStep.name)
            expected_url = step.url_for_step(EmploymentDecisionEligibilityInputFormSteuerlotseStep.name)
            step.handle()

        self.assertEqual(expected_url, step.render_info.prev_url)

    def test_if_employment_income_but_marginal_session_data_correct_then_set_prev_url_correct(self):
        alternative_data = {**self.correct_session_data.copy(),
                            **{'employment_income_eligibility': 'yes',
                               'marginal_employment_eligibility': 'yes'}}

        with self.app.test_request_context(method='GET') as req:
            req.session = SecureCookieSession({_ELIGIBILITY_DATA_KEY: create_session_form_data(alternative_data)})
            step = EligibilityStepChooser('eligibility').get_correct_step(
                IncomeOtherDecisionEligibilityInputFormSteuerlotseStep.name)
            expected_url = step.url_for_step(MarginalEmploymentIncomeDecisionEligibilityInputFormSteuerlotseStep.name)
            step.handle()

        self.assertEqual(expected_url, step.render_info.prev_url)

    def test_if_post_and_data_from_before_invalid_then_raise_incorrect_eligibility_data_error(self):
        with self.app.test_request_context(method='POST', data={'other_income_eligibility': 'no'}), \
                patch('app.model.recursive_data.RecursiveDataModel.one_previous_field_has_to_be_set',
                      MagicMock(side_effect=PreviousFieldsMissingError)):
            step = EligibilityStepChooser('eligibility').get_correct_step(
                IncomeOtherDecisionEligibilityInputFormSteuerlotseStep.name)

            self.assertRaises(IncorrectEligibilityData, step.handle)

    def test_if_get_and_incorrect_data_from_session_then_delete_incorrect_data(self):
        session_data = {'marital_status_eligibility': 'single',
                        'separated_since_last_year_eligibility': 'no',
                        'user_a_has_elster_account_eligibility': 'no',
                        'user_b_has_elster_account_eligibility': 'no',
                        'joint_taxes_eligibility': 'no',
                        'alimony_eligibility': 'no',
                        'pension_eligibility': 'yes',
                        'investment_income_eligibility': 'no',
                        'minimal_investment_income_eligibility': 'yes',
                        'taxed_investment_income_eligibility': 'no',
                        'cheaper_check_eligibility': 'no',
                        'employment_income_eligibility': 'no',
                        'marginal_employment_eligibility': 'yes',
                        'other_income_eligibility': 'no'}
        session_data_with_incorrect_key = {**session_data, **{'INCORRECT_KEY': 'UNNECESSARY_VALUE'}}
        with self.app.test_request_context(method='GET') as req:
            req.session = SecureCookieSession(
                {_ELIGIBILITY_DATA_KEY: create_session_form_data(session_data_with_incorrect_key)})
            step = EligibilityStepChooser('eligibility').get_correct_step(
                IncomeOtherDecisionEligibilityInputFormSteuerlotseStep.name)
            step.handle()

            self.assertEqual(session_data,
                             deserialize_session_data(req.session[_ELIGIBILITY_DATA_KEY]))

    def test_if_get_and_correct_data_from_session_then_do_not_delete_any_data(self):
        with self.app.test_request_context(method='GET') as req:
            req.session = SecureCookieSession(
                {_ELIGIBILITY_DATA_KEY: create_session_form_data(self.correct_session_data)})
            step = EligibilityStepChooser('eligibility').get_correct_step(
                IncomeOtherDecisionEligibilityInputFormSteuerlotseStep.name)
            step.handle()

            self.assertEqual(self.correct_session_data,
                             deserialize_session_data(req.session[_ELIGIBILITY_DATA_KEY]))

    def test_if_get_and_full_data_from_session_then_delete_unnecessary_data(self):
        only_necessary_data = {'marital_status_eligibility': 'single',
                               'separated_since_last_year_eligibility': 'no',
                               'separated_lived_together_eligibility': 'no',
                               'separated_joint_taxes_eligibility': 'no',
                               'user_a_has_elster_account_eligibility': 'no',
                               'user_b_has_elster_account_eligibility': 'no',
                               'elster_registration_method_eligibility': 'none',
                               'joint_taxes_eligibility': 'no',
                               'alimony_eligibility': 'no',
                               'pension_eligibility': 'yes',
                               'investment_income_eligibility': 'no',
                               'minimal_investment_income_eligibility': 'yes',
                               'taxed_investment_income_eligibility': 'no',
                               'cheaper_check_eligibility': 'no',
                               'employment_income_eligibility': 'no',
                               'marginal_employment_eligibility': 'yes',
                               'other_income_eligibility': 'no'}
        with self.app.test_request_context(method='GET') as req:
            req.session = SecureCookieSession({_ELIGIBILITY_DATA_KEY: create_session_form_data(FULL_SESSION_DATA)})
            step = EligibilityStepChooser('eligibility').get_correct_step(
                IncomeOtherDecisionEligibilityInputFormSteuerlotseStep.name)
            step.handle()

            self.assertEqual(only_necessary_data,
                             deserialize_session_data(req.session[_ELIGIBILITY_DATA_KEY]))

    def test_if_multiple_users_then_show_multiple_text(self):
        session_data = {'marital_status_eligibility': 'married',
                        'separated_since_last_year_eligibility': 'no',
                        'joint_taxes_eligibility': 'yes',
                        'user_a_has_elster_account_eligibility': 'no',
                        'user_b_has_elster_account_eligibility': 'no',
                        'alimony_eligibility': 'no',
                        'pension_eligibility': 'yes',
                        'investment_income_eligibility': 'no',
                        'taxed_investment_income_eligibility': 'no',
                        'employment_income_eligibility': 'no',
                        'marginal_employment_eligibility': 'yes'}
        expected_number_of_users = 2
        expected_choices = [('yes', ngettext('form.eligibility.income_other.yes', 'form.eligibility.income_other.yes', num=expected_number_of_users)),
                            ('no', ngettext('form.eligibility.income_other.no', 'form.eligibility.income_other.no', num=expected_number_of_users))]
        with self.app.test_request_context(method='GET') as req:
            req.session = SecureCookieSession({_ELIGIBILITY_DATA_KEY: create_session_form_data(session_data)})
            step = EligibilityStepChooser('eligibility').get_correct_step(
                IncomeOtherDecisionEligibilityInputFormSteuerlotseStep.name)
            step._pre_handle()

        self.assertEqual(expected_choices, step.form.other_income_eligibility.kwargs['choices'])

    def test_if_single_user_then_show_single_text(self):
        session_data = {'marital_status_eligibility': 'single',
                        'separated_since_last_year_eligibility': 'no',
                        'user_a_has_elster_account_eligibility': 'no',
                        'user_b_has_elster_account_eligibility': 'no',
                        'joint_taxes_eligibility': 'no',
                        'alimony_eligibility': 'no',
                        'pension_eligibility': 'yes',
                        'investment_income_eligibility': 'no',
                        'taxed_investment_income_eligibility': 'no',
                        'employment_income_eligibility': 'no',
                        'marginal_employment_eligibility': 'yes'}
        expected_number_of_users = 1
        expected_choices = [('yes', ngettext('form.eligibility.income_other.yes', 'form.eligibility.income_other.yes', num=expected_number_of_users)),
                            ('no', ngettext('form.eligibility.income_other.no', 'form.eligibility.income_other.no', num=expected_number_of_users))]
        with self.app.test_request_context(method='GET') as req:
            req.session = SecureCookieSession({_ELIGIBILITY_DATA_KEY: create_session_form_data(session_data)})
            step = EligibilityStepChooser('eligibility').get_correct_step(
                IncomeOtherDecisionEligibilityInputFormSteuerlotseStep.name)
            step._pre_handle()

        self.assertEqual(expected_choices, step.form.other_income_eligibility.kwargs['choices'])


class TestForeignCountriesEligibilityFailureDisplaySteuerlotseStep(unittest.TestCase):
    @pytest.fixture(autouse=True)
    def attach_fixtures(self, test_request_context):
        self.req = test_request_context

    def test_handle_sets_correct_prev_url(self):
        step = ForeignCountriesEligibilityFailureDisplaySteuerlotseStep(endpoint='eligibility')
        expected_url = step.url_for_step(ForeignCountriesDecisionEligibilityInputFormSteuerlotseStep.name)
        step.handle()

        self.assertEqual(expected_url, step.render_info.prev_url)


class TestForeignCountriesDecisionEligibilityInputFormSteuerlotseStep(unittest.TestCase):
    @pytest.fixture(autouse=True)
    def attach_fixtures(self, app):
        self.app = app

    def setUp(self):
        self.correct_session_data = {'marital_status_eligibility': 'divorced',
                                     'joint_taxes_eligibility': 'no',
                                     'alimony_eligibility': 'no',
                                     'user_a_has_elster_account_eligibility': 'no',
                                     'pension_eligibility': 'yes',
                                     'investment_income_eligibility': 'yes',
                                     'minimal_investment_income_eligibility': 'no',
                                     'taxed_investment_income_eligibility': 'yes',
                                     'cheaper_check_eligibility': 'no',
                                     'employment_income_eligibility': 'yes',
                                     'marginal_employment_eligibility': 'yes',
                                     'other_income_eligibility': 'no'}

    def test_if_post_and_session_data_correct_and_input_data_correct_than_set_next_input_step(self):
        with self.app.test_request_context(method='POST', data={'foreign_country_eligibility': 'no'}) as req:
            req.session = SecureCookieSession(
                {_ELIGIBILITY_DATA_KEY: create_session_form_data(self.correct_session_data)})
            step = EligibilityStepChooser('eligibility').get_correct_step(
                ForeignCountriesDecisionEligibilityInputFormSteuerlotseStep.name)
            expected_url = step.url_for_step(EligibilitySuccessDisplaySteuerlotseStep.name)
            step.handle()

        self.assertEqual(expected_url, step.render_info.next_url)

    def test_if_post_and_session_data_correct_and_input_data_incorrect_than_set_next_url_to_alternative_step(self):
        with self.app.test_request_context(method='POST', data={'foreign_country_eligibility': 'yes'}) as req:
            req.session = SecureCookieSession(
                {_ELIGIBILITY_DATA_KEY: create_session_form_data(self.correct_session_data)})
            step = EligibilityStepChooser('eligibility').get_correct_step(
                ForeignCountriesDecisionEligibilityInputFormSteuerlotseStep.name)
            expected_url = step.url_for_step(ForeignCountriesEligibilityFailureDisplaySteuerlotseStep.name)
            step.handle()

        self.assertEqual(expected_url, step.render_info.next_url)

    def test_if_session_data_correct_then_set_prev_input_step_correctly(self):
        with self.app.test_request_context(method='GET') as req:
            req.session = SecureCookieSession(
                {_ELIGIBILITY_DATA_KEY: create_session_form_data(self.correct_session_data)})
            step = EligibilityStepChooser('eligibility').get_correct_step(
                ForeignCountriesDecisionEligibilityInputFormSteuerlotseStep.name)
            expected_url = step.url_for_step(IncomeOtherDecisionEligibilityInputFormSteuerlotseStep.name)
            step.handle()

        self.assertEqual(expected_url, step.render_info.prev_url)

    def test_if_post_and_data_from_before_invalid_then_raise_incorrect_eligibility_data_error(self):
        with self.app.test_request_context(method='POST', data={'other_income_eligibility': 'no',
                                                                'foreign_country_eligibility': 'no'}), \
                patch('app.model.recursive_data.RecursiveDataModel.one_previous_field_has_to_be_set',
                      MagicMock(side_effect=PreviousFieldsMissingError)):
            step = EligibilityStepChooser('eligibility').get_correct_step(
                ForeignCountriesDecisionEligibilityInputFormSteuerlotseStep.name)

            self.assertRaises(IncorrectEligibilityData, step.handle)

    def test_if_get_and_incorrect_data_from_session_then_delete_incorrect_data(self):
        session_data = {'marital_status_eligibility': 'single',
                        'separated_since_last_year_eligibility': 'no',
                        'user_a_has_elster_account_eligibility': 'no',
                        'user_b_has_elster_account_eligibility': 'no',
                        'joint_taxes_eligibility': 'no',
                        'alimony_eligibility': 'no',
                        'pension_eligibility': 'yes',
                        'investment_income_eligibility': 'no',
                        'minimal_investment_income_eligibility': 'yes',
                        'taxed_investment_income_eligibility': 'no',
                        'cheaper_check_eligibility': 'no',
                        'employment_income_eligibility': 'no',
                        'marginal_employment_eligibility': 'yes',
                        'other_income_eligibility': 'no',
                        'foreign_country_eligibility': 'no'}
        session_data_with_incorrect_key = {**session_data, **{'INCORRECT_KEY': 'UNNECESSARY_VALUE'}}
        with self.app.test_request_context(method='GET') as req:
            req.session = SecureCookieSession(
                {_ELIGIBILITY_DATA_KEY: create_session_form_data(session_data_with_incorrect_key)})
            step = EligibilityStepChooser('eligibility').get_correct_step(
                ForeignCountriesDecisionEligibilityInputFormSteuerlotseStep.name)
            step.handle()

            self.assertEqual(session_data,
                             deserialize_session_data(req.session[_ELIGIBILITY_DATA_KEY]))

    def test_if_get_and_correct_data_from_session_then_do_not_delete_any_data(self):
        with self.app.test_request_context(method='GET') as req:
            req.session = SecureCookieSession(
                {_ELIGIBILITY_DATA_KEY: create_session_form_data(self.correct_session_data)})
            step = EligibilityStepChooser('eligibility').get_correct_step(
                ForeignCountriesDecisionEligibilityInputFormSteuerlotseStep.name)
            step.handle()

            self.assertEqual(self.correct_session_data,
                             deserialize_session_data(req.session[_ELIGIBILITY_DATA_KEY]))

    def test_if_get_and_full_data_from_session_then_delete_no_data(self):
        with self.app.test_request_context(method='GET') as req:
            req.session = SecureCookieSession({_ELIGIBILITY_DATA_KEY: create_session_form_data(FULL_SESSION_DATA)})
            step = EligibilityStepChooser('eligibility').get_correct_step(
                ForeignCountriesDecisionEligibilityInputFormSteuerlotseStep.name)
            step.handle()

            self.assertEqual(FULL_SESSION_DATA,
                             deserialize_session_data(req.session[_ELIGIBILITY_DATA_KEY]))

    def test_if_multiple_users_then_show_multiple_text(self):
        session_data = {'marital_status_eligibility': 'married',
                        'separated_since_last_year_eligibility': 'no',
                        'joint_taxes_eligibility': 'yes',
                        'user_a_has_elster_account_eligibility': 'no',
                        'user_b_has_elster_account_eligibility': 'no',
                        'alimony_eligibility': 'no',
                        'pension_eligibility': 'yes',
                        'investment_income_eligibility': 'no',
                        'taxed_investment_income_eligibility': 'no',
                        'employment_income_eligibility': 'no',
                        'marginal_employment_eligibility': 'yes',
                        'other_income_eligibility': 'no'}
        expected_number_of_users = 2
        expected_choices = [('yes', ngettext('form.eligibility.foreign_country.yes', 'form.eligibility.foreign_country.yes', num=expected_number_of_users)),
                            ('no', ngettext('form.eligibility.foreign_country.no', 'form.eligibility.foreign_country.no', num=expected_number_of_users))]
        with self.app.test_request_context(method='GET') as req:
            req.session = SecureCookieSession({_ELIGIBILITY_DATA_KEY: create_session_form_data(session_data)})
            step = EligibilityStepChooser('eligibility').get_correct_step(
                ForeignCountriesDecisionEligibilityInputFormSteuerlotseStep.name)
            step._pre_handle()

        self.assertEqual(expected_choices, step.form.foreign_country_eligibility.kwargs['choices'])

    def test_if_single_user_then_show_single_text(self):
        session_data = {'marital_status_eligibility': 'single',
                        'separated_since_last_year_eligibility': 'no',
                        'user_a_has_elster_account_eligibility': 'no',
                        'user_b_has_elster_account_eligibility': 'no',
                        'joint_taxes_eligibility': 'no',
                        'alimony_eligibility': 'no',
                        'pension_eligibility': 'yes',
                        'investment_income_eligibility': 'no',
                        'taxed_investment_income_eligibility': 'no',
                        'employment_income_eligibility': 'no',
                        'marginal_employment_eligibility': 'yes',
                        'other_income_eligibility': 'no'}
        expected_number_of_users = 1
        expected_choices = [('yes', ngettext('form.eligibility.foreign_country.yes', 'form.eligibility.foreign_country.yes', num=expected_number_of_users)),
                            ('no', ngettext('form.eligibility.foreign_country.no', 'form.eligibility.foreign_country.no', num=expected_number_of_users))]
        with self.app.test_request_context(method='GET') as req:
            req.session = SecureCookieSession({_ELIGIBILITY_DATA_KEY: create_session_form_data(session_data)})
            step = EligibilityStepChooser('eligibility').get_correct_step(
                ForeignCountriesDecisionEligibilityInputFormSteuerlotseStep.name)
            step._pre_handle()

        self.assertEqual(expected_choices, step.form.foreign_country_eligibility.kwargs['choices'])


class TestEligibilitySuccessDisplaySteuerlotseStep(unittest.TestCase):
    @pytest.fixture(autouse=True)
    def attach_fixtures(self, test_request_context):
        self.req = test_request_context

    def test_if_user_b_has_no_elster_account_then_set_correct_info(self):
        expected_information = ['form.eligibility.result-note.user_b_elster_account',
                                'form.eligibility.result-note.user_b_elster_account-registration']
        session_data = {'marital_status_eligibility': 'married',
                        'separated_since_last_year_eligibility': 'no',
                        'user_a_has_elster_account_eligibility': 'yes',
                        'user_b_has_elster_account_eligibility': 'no',
                        'joint_taxes_eligibility': 'yes',
                        'alimony_eligibility': 'no', }
        with patch('app.forms.steps.eligibility_steps._', MagicMock(side_effect=lambda text_id: text_id)):
            step = EligibilitySuccessDisplaySteuerlotseStep(endpoint='eligibility', stored_data=session_data)
            step.handle()

        self.assertEqual(expected_information, step.render_info.additional_info['dependent_notes'])

    def test_if_user_wants_no_cheaper_check_then_set_correct_info(self):
        expected_information = ['form.eligibility.result-note.capital_investment']
        session_data = {'marital_status_eligibility': 'single',
                        'user_a_has_elster_account_eligibility': 'no',
                        'alimony_eligibility': 'no',
                        'pension_eligibility': 'yes',
                        'investment_income_eligibility': 'yes',
                        'minimal_investment_income_eligibility': 'no',
                        'taxed_investment_income_eligibility': 'yes',
                        'cheaper_check_eligibility': 'no', }
        with patch('app.forms.steps.eligibility_steps._', MagicMock(side_effect=lambda text_id: text_id)):
            step = EligibilitySuccessDisplaySteuerlotseStep(endpoint='eligibility', stored_data=session_data)
            step.handle()

        self.assertEqual(expected_information, step.render_info.additional_info['dependent_notes'])

    def test_if_user_has_no_minimal_investment_income_then_set_correct_info(self):
        expected_information = ['form.eligibility.result-note.capital_investment']
        session_data = {'marital_status_eligibility': 'single',
                        'user_a_has_elster_account_eligibility': 'no',
                        'alimony_eligibility': 'no',
                        'pension_eligibility': 'yes',
                        'investment_income_eligibility': 'yes',
                        'minimal_investment_income_eligibility': 'yes',
                        'taxed_investment_income_eligibility': 'yes', }
        with patch('app.forms.steps.eligibility_steps._', MagicMock(side_effect=lambda text_id: text_id)):
            step = EligibilitySuccessDisplaySteuerlotseStep(endpoint='eligibility', stored_data=session_data)
            step.handle()

        self.assertEqual(expected_information, step.render_info.additional_info['dependent_notes'])

    def test_if_user_b_has_no_elster_account_and_user_wants_no_cheaper_check_then_set_correct_info(self):
        expected_information = ['form.eligibility.result-note.user_b_elster_account',
                                'form.eligibility.result-note.user_b_elster_account-registration',
                                'form.eligibility.result-note.capital_investment']
        session_data = {'marital_status_eligibility': 'married',
                        'separated_since_last_year_eligibility': 'no',
                        'user_a_has_elster_account_eligibility': 'yes',
                        'user_b_has_elster_account_eligibility': 'no',
                        'joint_taxes_eligibility': 'yes',
                        'alimony_eligibility': 'no',
                        'pension_eligibility': 'yes',
                        'investment_income_eligibility': 'yes',
                        'minimal_investment_income_eligibility': 'no',
                        'taxed_investment_income_eligibility': 'yes',
                        'cheaper_check_eligibility': 'no', }
        with patch('app.forms.steps.eligibility_steps._', MagicMock(side_effect=lambda text_id: text_id)):
            step = EligibilitySuccessDisplaySteuerlotseStep(endpoint='eligibility', stored_data=session_data)
            step.handle()

        self.assertEqual(expected_information, step.render_info.additional_info['dependent_notes'])

    def test_if_user_b_has_no_elster_account_and_user_has_minimal_investment_income_check_then_set_correct_info(self):
        expected_information = ['form.eligibility.result-note.user_b_elster_account',
                                'form.eligibility.result-note.user_b_elster_account-registration',
                                'form.eligibility.result-note.capital_investment']
        session_data = {'marital_status_eligibility': 'married',
                        'separated_since_last_year_eligibility': 'no',
                        'user_a_has_elster_account_eligibility': 'yes',
                        'user_b_has_elster_account_eligibility': 'no',
                        'joint_taxes_eligibility': 'yes',
                        'alimony_eligibility': 'no',
                        'pension_eligibility': 'yes',
                        'investment_income_eligibility': 'yes',
                        'minimal_investment_income_eligibility': 'yes',
                        'taxed_investment_income_eligibility': 'yes', }
        with patch('app.forms.steps.eligibility_steps._', MagicMock(side_effect=lambda text_id: text_id)):
            step = EligibilitySuccessDisplaySteuerlotseStep(endpoint='eligibility', stored_data=session_data)
            step.handle()

        self.assertEqual(expected_information, step.render_info.additional_info['dependent_notes'])

    def test_if_no_user_b_elster_account_and_no_cheaper_check_then_set_no_info(self):
        expected_information = []
        step = EligibilitySuccessDisplaySteuerlotseStep(endpoint='eligibility')
        step.handle()

        self.assertEqual(expected_information, step.render_info.additional_info['dependent_notes'])
