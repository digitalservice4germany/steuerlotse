import unittest
from unittest.mock import patch, MagicMock, call

import pytest
from flask.sessions import SecureCookieSession
from flask_babel import ngettext, _
from flask_babel import lazy_gettext as _l
from pydantic import ValidationError
from werkzeug.datastructures import ImmutableMultiDict
from werkzeug.exceptions import NotFound

from app.forms.flows.eligibility_step_chooser import EligibilityStepChooser, _ELIGIBILITY_DATA_KEY
from app.forms.steps.eligibility_steps import MarriedJointTaxesEligibilityFailureDisplaySteuerlotseStep, \
    MarriedJointTaxesDecisionEligibilityInputFormSteuerlotseStep, \
    MarriedAlimonyDecisionEligibilityInputFormSteuerlotseStep, IncorrectEligibilityData, TaxYearEligibilityInputFormSteuerlotseStep, \
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
    data_fits_data_model_from_list, data_fits_data_model
from app.forms.steps.steuerlotse_step import RedirectSteuerlotseStep
from app.model.recursive_data import PreviousFieldsMissingError
from tests.forms.mock_steuerlotse_steps import MockRenderStep, MockStartStep, MockFormStep, MockFinalStep, \
    MockDecisionEligibilityInputFormSteuerlotseStep
from tests.utils import create_session_form_data
from app.data_access.storage.form_storage import FormStorage

FULL_SESSION_DATA = {'marital_status_eligibility': 'single',
                     'separated_since_last_year_eligibility': 'no',
                     'separated_lived_together_eligibility': 'no',
                     'separated_joint_taxes_eligibility': 'no',
                     'joint_taxes_eligibility': 'no',
                     'alimony_eligibility': 'no',
                     'user_a_has_elster_account_eligibility': 'no',
                     'user_b_has_elster_account_eligibility': 'no',
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
        response_step = self.step_chooser.get_correct_step(MockRenderStep.name, False, ImmutableMultiDict({}))

        self.assertIsInstance(response_step, MockRenderStep)

    def test_if_incorrect_step_name_then_raise_404_exception(self):
        self.assertRaises(NotFound, self.step_chooser.get_correct_step, "Incorrect Step Name", False, ImmutableMultiDict({}))

    def test_if_start_step_then_return_redirect_step(self):
        self.step_chooser.default_data = lambda: None
        response_step = self.step_chooser.get_correct_step("start", False, ImmutableMultiDict({}))

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


class TestEligibilityInputFormSteuerlotseStepOverrideSessionData:

    @pytest.mark.usefixtures('test_request_context')
    def test_if_override_storage_data_called_then_cookie_override_function_called_with_same_params(self):
        with patch('app.data_access.storage.cookie_storage.CookieStorage.override_data') as patched_override:
            MockDecisionEligibilityInputFormSteuerlotseStep(endpoint='eligibility')._override_storage_data(stored_data={'name': 'Ash'}, data_identifier='catch_em_all')

        assert patched_override.call_args == call({'name': 'Ash'}, 'catch_em_all')


class TestEligibilityStartDisplaySteuerlotseStep:

    def test_sets_correct_session_data_to_empty_dict(self, new_test_request_context):
        session_data = {
            _ELIGIBILITY_DATA_KEY: create_session_form_data({'marital_status_eligibility': 'single'})
        }
        with new_test_request_context(method='GET') as req:
            req.session = SecureCookieSession(session_data)
            step = EligibilityStepChooser('eligibility').get_correct_step(EligibilityStartDisplaySteuerlotseStep.name,
                                                                          False, ImmutableMultiDict({}))
            step.handle()

            assert {} == FormStorage.deserialize_data(req.session[_ELIGIBILITY_DATA_KEY])

    def test_does_not_change_other_session_data(self, new_test_request_context):
        other_session_key = 'OTHER_SESSION_KEY'
        other_session_data = {'Galileo': 'Figaro - magnificoo'}
        another_session_key = 'ANOTHER_SESSION_KEY'
        another_session_data = {'Scaramouch': 'Fandango'}
        session_data = {
            _ELIGIBILITY_DATA_KEY: create_session_form_data({'marital_status_eligibility': 'single'}),
            other_session_key: create_session_form_data(other_session_data),
            another_session_key: create_session_form_data(another_session_data)
        }

        with new_test_request_context(method='GET') as req:
            req.session = SecureCookieSession(session_data)
            step = EligibilityStepChooser('eligibility').get_correct_step(EligibilityStartDisplaySteuerlotseStep.name,
                                                                          False, ImmutableMultiDict({}))
            step.handle()

            assert other_session_data == FormStorage.deserialize_data(req.session[other_session_key])
            assert another_session_data == FormStorage.deserialize_data(req.session[another_session_key])

    def test_does_not_add_data_to_empty_session_data(self, new_test_request_context):
        session_data = {}
        with new_test_request_context(method='GET') as req:
            req.session = SecureCookieSession(session_data)
            step = EligibilityStepChooser('eligibility').get_correct_step(EligibilityStartDisplaySteuerlotseStep.name,
                                                                          False, ImmutableMultiDict({}))
            step.handle()

            assert {} == FormStorage.deserialize_data(req.session[_ELIGIBILITY_DATA_KEY])

    def test_leaves_session_data_without_correct_key_untouched(self, new_test_request_context):
        other_session_key = 'OTHER_SESSION_KEY'
        other_session_data = {'Galileo': 'Figaro - magnificoo'}
        session_data = {
            other_session_key: create_session_form_data(other_session_data)
        }
        with new_test_request_context(method='GET') as req:
            req.session = SecureCookieSession(session_data)
            step = EligibilityStepChooser('eligibility').get_correct_step(EligibilityStartDisplaySteuerlotseStep.name,
                                                                          False, ImmutableMultiDict({}))
            step.handle()

            assert other_session_data == FormStorage.deserialize_data(req.session[other_session_key])


@pytest.fixture
def eligibility_start_step():
    return EligibilityStepChooser('eligibility').get_correct_step(EligibilityStartDisplaySteuerlotseStep.name,
                                                                          False, ImmutableMultiDict({}))


class TestEligibilityStartDisplaySteuerlotseStepOverrideSessionData:

    @pytest.mark.usefixtures('test_request_context')
    def test_if_override_storage_data_called_then_cookie_override_function_called_with_same_params(self, eligibility_start_step):

        with patch('app.data_access.storage.cookie_storage.CookieStorage.override_data') as patched_override:
            eligibility_start_step._override_storage_data(stored_data={'name': 'Ash'}, data_identifier='catch_em_all')

        assert patched_override.call_args == call({'name': 'Ash'}, 'catch_em_all')


class TestMaritalStatusInputFormSteuerlotseStep:

    def test_if_post_and_married_then_set_next_step_correct(self, new_test_request_context):
        with new_test_request_context(method='POST'):
            step = EligibilityStepChooser('eligibility').get_correct_step(MaritalStatusInputFormSteuerlotseStep.name,
                                                                          True, form_data=ImmutableMultiDict(
                    {'marital_status_eligibility': 'married'}))
            expected_url = step.url_for_step(SeparatedEligibilityInputFormSteuerlotseStep.name)
            step.handle()

        assert expected_url == step.render_info.next_url

    @pytest.mark.usefixtures('test_request_context')
    def test_if_post_and_widowed_then_set_next_step_correct(self):
        step = EligibilityStepChooser('eligibility').get_correct_step(MaritalStatusInputFormSteuerlotseStep.name, True,
                                                                      form_data=ImmutableMultiDict(
                                                                          {'marital_status_eligibility': 'widowed'}))
        expected_url = step.url_for_step(SingleAlimonyDecisionEligibilityInputFormSteuerlotseStep.name)
        step.handle()

        assert expected_url == step.render_info.next_url

    @pytest.mark.usefixtures('test_request_context')
    def test_if_post_and_single_then_set_next_step_correct(self):
        step = EligibilityStepChooser('eligibility').get_correct_step(MaritalStatusInputFormSteuerlotseStep.name, True,
                                                                      form_data=ImmutableMultiDict(
                                                                          {'marital_status_eligibility': 'single'}))
        expected_url = step.url_for_step(SingleAlimonyDecisionEligibilityInputFormSteuerlotseStep.name)
        step.handle()

        assert expected_url, step.render_info.next_url

    @pytest.mark.usefixtures('test_request_context')
    def test_if_post_and_divorced_then_set_next_step_correct(self):
        step = EligibilityStepChooser('eligibility').get_correct_step(MaritalStatusInputFormSteuerlotseStep.name, True,
                                                                      form_data=ImmutableMultiDict(
                                                                          {'marital_status_eligibility': 'divorced'}))
        expected_url = step.url_for_step(DivorcedJointTaxesDecisionEligibilityInputFormSteuerlotseStep.name)
        step.handle()

        assert expected_url == step.render_info.next_url

    @pytest.mark.usefixtures('test_request_context')
    def test_set_prev_input_step_to_none(self, new_test_request_context):
        with new_test_request_context(method='GET'):
            step = EligibilityStepChooser('eligibility').get_correct_step(TaxYearEligibilityInputFormSteuerlotseStep.name,
                                                                          False, ImmutableMultiDict({}))
            step.handle()
        assert step.render_info.prev_url is None

    def test_if_get_and_incorrect_data_from_session_then_delete_incorrect_data(self, new_test_request_context):
        session_data = {'marital_status_eligibility': 'single', }
        session_data_with_incorrect_key = {**session_data, **{'INCORRECT_KEY': 'UNNECESSARY_VALUE'}}
        with new_test_request_context(method='GET') as req:
            req.session = SecureCookieSession(
                {_ELIGIBILITY_DATA_KEY: create_session_form_data(session_data_with_incorrect_key)})
            step = EligibilityStepChooser('eligibility').get_correct_step(MaritalStatusInputFormSteuerlotseStep.name,
                                                                          False, ImmutableMultiDict({}))
            step.handle()

            assert session_data == FormStorage.deserialize_data(req.session[_ELIGIBILITY_DATA_KEY])

    def test_if_get_and_correct_data_from_session_then_do_not_delete_any_data(self, new_test_request_context):
        session_data = {'marital_status_eligibility': 'single', }
        with new_test_request_context(method='GET') as req:
            req.session = SecureCookieSession({_ELIGIBILITY_DATA_KEY: create_session_form_data(session_data)})
            step = EligibilityStepChooser('eligibility').get_correct_step(MaritalStatusInputFormSteuerlotseStep.name,
                                                                          False, ImmutableMultiDict({}))
            step.handle()

            assert session_data == FormStorage.deserialize_data(req.session[_ELIGIBILITY_DATA_KEY])

    def test_if_get_and_full_data_from_session_then_delete_unnecessary_data(self, new_test_request_context):
        only_necessary_data = {'marital_status_eligibility': 'single', }
        with new_test_request_context(method='GET') as req:
            req.session = SecureCookieSession({_ELIGIBILITY_DATA_KEY: create_session_form_data(FULL_SESSION_DATA)})
            step = EligibilityStepChooser('eligibility').get_correct_step(MaritalStatusInputFormSteuerlotseStep.name,
                                                                          False, ImmutableMultiDict({}))
            step.handle()

            assert only_necessary_data == FormStorage.deserialize_data(req.session[_ELIGIBILITY_DATA_KEY])


class TestSeparatedEligibilityInputFormSteuerlotseStep(unittest.TestCase):
    @pytest.fixture(autouse=True)
    def attach_fixtures(self, app):
        self.app = app

    def setUp(self):
        self.correct_session_data = {'marital_status_eligibility': 'married'}

    def test_if_post_and_session_data_correct_and_input_data_correct_than_set_next_input_step(self):
        with self.app.test_request_context(method='POST') as req:
            req.session = SecureCookieSession(
                {_ELIGIBILITY_DATA_KEY: create_session_form_data(self.correct_session_data)})
            step = EligibilityStepChooser('eligibility').get_correct_step(
                SeparatedEligibilityInputFormSteuerlotseStep.name, True,
                form_data=ImmutableMultiDict({'separated_since_last_year_eligibility': 'yes'}))
            expected_url = step.url_for_step(SeparatedLivedTogetherEligibilityInputFormSteuerlotseStep.name)
            step.handle()

        self.assertEqual(expected_url, step.render_info.next_url)

    def test_if_post_and_session_data_correct_and_input_data_incorrect_than_set_next_url_to_alternative_step(self):
        with self.app.test_request_context(method='POST') as req:
            req.session = SecureCookieSession(
                {_ELIGIBILITY_DATA_KEY: create_session_form_data(self.correct_session_data)})
            step = EligibilityStepChooser('eligibility').get_correct_step(
                SeparatedEligibilityInputFormSteuerlotseStep.name, True,
                form_data=ImmutableMultiDict({'separated_since_last_year_eligibility': 'no'}))
            expected_url = step.url_for_step(MarriedJointTaxesDecisionEligibilityInputFormSteuerlotseStep.name)
            step.handle()

        self.assertEqual(expected_url, step.render_info.next_url)

    def test_if_session_data_correct_then_set_prev_input_step_correctly(self):
        with self.app.test_request_context(method='GET') as req:
            req.session = SecureCookieSession(
                {_ELIGIBILITY_DATA_KEY: create_session_form_data(self.correct_session_data)})
            step = EligibilityStepChooser('eligibility').get_correct_step(
                SeparatedEligibilityInputFormSteuerlotseStep.name, False, ImmutableMultiDict({}))
            expected_url = step.url_for_step(MaritalStatusInputFormSteuerlotseStep.name)
            step.handle()
        self.assertEqual(expected_url, step.render_info.prev_url)

    @pytest.mark.usefixtures('test_request_context')
    def test_if_post_and_data_from_before_invalid_then_raise_incorrect_eligibility_data_error(self):
        with patch('app.model.recursive_data.RecursiveDataModel.one_previous_field_has_to_be_set',
                      MagicMock(side_effect=PreviousFieldsMissingError)):
            step = EligibilityStepChooser('eligibility').get_correct_step(
                SeparatedEligibilityInputFormSteuerlotseStep.name, True,
                form_data=ImmutableMultiDict({'separated_since_last_year_eligibility': 'yes'}))

            self.assertRaises(IncorrectEligibilityData, step.handle)

    def test_if_get_and_incorrect_data_from_session_then_delete_incorrect_data(self):
        session_data = {'marital_status_eligibility': 'single',
                        'separated_since_last_year_eligibility': 'no', }
        session_data_with_incorrect_key = {**session_data, **{'INCORRECT_KEY': 'UNNECESSARY_VALUE'}}
        with self.app.test_request_context(method='GET') as req:
            req.session = SecureCookieSession(
                {_ELIGIBILITY_DATA_KEY: create_session_form_data(session_data_with_incorrect_key)})
            step = EligibilityStepChooser('eligibility').get_correct_step(
                SeparatedEligibilityInputFormSteuerlotseStep.name, False, ImmutableMultiDict({}))
            step.handle()

            self.assertEqual(session_data,
                             FormStorage.deserialize_data(req.session[_ELIGIBILITY_DATA_KEY]))

    def test_if_get_and_correct_data_from_session_then_do_not_delete_any_data(self):
        session_data = {'marital_status_eligibility': 'single',
                        'separated_since_last_year_eligibility': 'no', }
        with self.app.test_request_context(method='GET') as req:
            req.session = SecureCookieSession({_ELIGIBILITY_DATA_KEY: create_session_form_data(session_data)})
            step = EligibilityStepChooser('eligibility').get_correct_step(
                SeparatedEligibilityInputFormSteuerlotseStep.name, False, ImmutableMultiDict({}))
            step.handle()

            self.assertEqual(session_data,
                             FormStorage.deserialize_data(req.session[_ELIGIBILITY_DATA_KEY]))

    def test_if_get_and_full_data_from_session_then_delete_unnecessary_data(self):
        only_necessary_data = {'marital_status_eligibility': 'single',
                               'separated_since_last_year_eligibility': 'no', }
        with self.app.test_request_context(method='GET') as req:
            req.session = SecureCookieSession({_ELIGIBILITY_DATA_KEY: create_session_form_data(FULL_SESSION_DATA)})
            step = EligibilityStepChooser('eligibility').get_correct_step(
                SeparatedEligibilityInputFormSteuerlotseStep.name, False, ImmutableMultiDict({}))
            step.handle()

            self.assertEqual(only_necessary_data,
                             FormStorage.deserialize_data(req.session[_ELIGIBILITY_DATA_KEY]))


class TestSeparatedLivedTogetherEligibilityInputFormSteuerlotseStep(unittest.TestCase):
    @pytest.fixture(autouse=True)
    def attach_fixtures(self, app):
        self.app = app

    def setUp(self):
        self.correct_session_data = {'marital_status_eligibility': 'married',
                                     'separated_since_last_year_eligibility': 'yes'}

    def test_if_post_and_session_data_correct_and_input_data_correct_then_set_next_input_step(self):
        with self.app.test_request_context(method='POST') as req:
            req.session = SecureCookieSession(
                {_ELIGIBILITY_DATA_KEY: create_session_form_data(self.correct_session_data)})
            step = EligibilityStepChooser('eligibility').get_correct_step(
                SeparatedLivedTogetherEligibilityInputFormSteuerlotseStep.name, True,
                form_data=ImmutableMultiDict({'separated_lived_together_eligibility': 'yes'}))
            expected_url = step.url_for_step(SeparatedJointTaxesEligibilityInputFormSteuerlotseStep.name)
            step.handle()

        self.assertEqual(expected_url, step.render_info.next_url)

    def test_if_post_and_session_data_correct_and_input_data_incorrect_than_set_next_url_to_alternative_step(self):
        with self.app.test_request_context(method='POST') as req:
            req.session = SecureCookieSession(
                {_ELIGIBILITY_DATA_KEY: create_session_form_data(self.correct_session_data)})
            step = EligibilityStepChooser('eligibility').get_correct_step(
                SeparatedLivedTogetherEligibilityInputFormSteuerlotseStep.name, True,
                form_data=ImmutableMultiDict({'separated_lived_together_eligibility': 'no'}))
            expected_url = step.url_for_step(SingleAlimonyDecisionEligibilityInputFormSteuerlotseStep.name)
            step.handle()

        self.assertEqual(expected_url, step.render_info.next_url)

    def test_if_session_data_correct_then_set_prev_input_step_correctly(self):
        with self.app.test_request_context(method='GET') as req:
            req.session = SecureCookieSession(
                {_ELIGIBILITY_DATA_KEY: create_session_form_data(self.correct_session_data)})
            step = EligibilityStepChooser('eligibility').get_correct_step(
                SeparatedLivedTogetherEligibilityInputFormSteuerlotseStep.name, False, ImmutableMultiDict({}))
            expected_url = step.url_for_step(SeparatedEligibilityInputFormSteuerlotseStep.name)
            step.handle()
        self.assertEqual(expected_url, step.render_info.prev_url)

    def test_if_post_and_data_from_before_invalid_then_raise_incorrect_eligibility_data_error(self):
        with self.app.test_request_context(method='POST'), \
                patch('app.model.recursive_data.RecursiveDataModel.one_previous_field_has_to_be_set',
                      MagicMock(side_effect=PreviousFieldsMissingError)):
            step = EligibilityStepChooser('eligibility').get_correct_step(
                SeparatedLivedTogetherEligibilityInputFormSteuerlotseStep.name, True,
                form_data=ImmutableMultiDict({'separated_lived_together_eligibility': 'yes'}))

            self.assertRaises(IncorrectEligibilityData, step.handle)

    def test_if_get_and_incorrect_data_from_session_then_delete_incorrect_data(self):
        session_data = {'marital_status_eligibility': 'married',
                        'separated_since_last_year_eligibility': 'yes', }
        session_data_with_incorrect_key = {**session_data, **{'INCORRECT_KEY': 'UNNECESSARY_VALUE'}}
        with self.app.test_request_context(method='GET') as req:
            req.session = SecureCookieSession(
                {_ELIGIBILITY_DATA_KEY: create_session_form_data(session_data_with_incorrect_key)})
            step = EligibilityStepChooser('eligibility').get_correct_step(
                SeparatedLivedTogetherEligibilityInputFormSteuerlotseStep.name, False, ImmutableMultiDict({}))
            step.handle()

            self.assertEqual(session_data,
                             FormStorage.deserialize_data(req.session[_ELIGIBILITY_DATA_KEY]))

    def test_if_get_and_correct_data_from_session_then_do_not_delete_any_data(self):
        with self.app.test_request_context(method='GET') as req:
            req.session = SecureCookieSession(
                {_ELIGIBILITY_DATA_KEY: create_session_form_data(self.correct_session_data)})
            step = EligibilityStepChooser('eligibility').get_correct_step(
                SeparatedLivedTogetherEligibilityInputFormSteuerlotseStep.name, False, ImmutableMultiDict({}))
            step.handle()

            self.assertEqual(self.correct_session_data,
                             FormStorage.deserialize_data(req.session[_ELIGIBILITY_DATA_KEY]))

    def test_if_get_and_full_data_from_session_then_delete_unnecessary_data(self):
        only_necessary_data = {'marital_status_eligibility': 'single',
                               'separated_since_last_year_eligibility': 'no',
                               'separated_lived_together_eligibility': 'no', }
        with self.app.test_request_context(method='GET') as req:
            req.session = SecureCookieSession({_ELIGIBILITY_DATA_KEY: create_session_form_data(FULL_SESSION_DATA)})
            step = EligibilityStepChooser('eligibility').get_correct_step(
                SeparatedLivedTogetherEligibilityInputFormSteuerlotseStep.name, False, ImmutableMultiDict({}))
            step.handle()

            self.assertEqual(only_necessary_data,
                             FormStorage.deserialize_data(req.session[_ELIGIBILITY_DATA_KEY]))


class TestSeparatedJointTaxesEligibilityInputFormSteuerlotseStep(unittest.TestCase):
    @pytest.fixture(autouse=True)
    def attach_fixtures(self, app):
        self.app = app

    def setUp(self):
        self.correct_session_data = {'marital_status_eligibility': 'married',
                                     'separated_since_last_year_eligibility': 'yes',
                                     'separated_lived_together_eligibility': 'yes'}

    def test_if_post_and_session_data_correct_and_input_data_correct_then_set_next_input_step(self):
        with self.app.test_request_context(method='POST') as req:
            req.session = SecureCookieSession(
                {_ELIGIBILITY_DATA_KEY: create_session_form_data(self.correct_session_data)})
            step = EligibilityStepChooser('eligibility').get_correct_step(
                SeparatedJointTaxesEligibilityInputFormSteuerlotseStep.name, True,
                form_data=ImmutableMultiDict({'separated_joint_taxes_eligibility': 'yes'}))
            expected_url = step.url_for_step(MarriedAlimonyDecisionEligibilityInputFormSteuerlotseStep.name)
            step.handle()

        self.assertEqual(expected_url, step.render_info.next_url)

    def test_if_post_and_session_data_correct_and_input_data_incorrect_than_set_next_url_to_alternative_step(self):
        with self.app.test_request_context(method='POST') as req:
            req.session = SecureCookieSession(
                {_ELIGIBILITY_DATA_KEY: create_session_form_data(self.correct_session_data)})
            step = EligibilityStepChooser('eligibility').get_correct_step(
                SeparatedJointTaxesEligibilityInputFormSteuerlotseStep.name, True,
                form_data=ImmutableMultiDict({'separated_joint_taxes_eligibility': 'no'}))
            expected_url = step.url_for_step(SingleAlimonyDecisionEligibilityInputFormSteuerlotseStep.name)
            step.handle()

        self.assertEqual(expected_url, step.render_info.next_url)

    def test_if_session_data_correct_then_set_prev_input_step_correctly(self):
        with self.app.test_request_context(method='GET') as req:
            req.session = SecureCookieSession(
                {_ELIGIBILITY_DATA_KEY: create_session_form_data(self.correct_session_data)})
            step = EligibilityStepChooser('eligibility').get_correct_step(
                SeparatedJointTaxesEligibilityInputFormSteuerlotseStep.name, False, ImmutableMultiDict({}))
            expected_url = step.url_for_step(SeparatedLivedTogetherEligibilityInputFormSteuerlotseStep.name)
            step.handle()
        self.assertEqual(expected_url, step.render_info.prev_url)

    def test_if_post_and_data_from_before_invalid_then_raise_incorrect_eligibility_data_error(self):
        with self.app.test_request_context(method='POST'), \
                patch('app.model.recursive_data.RecursiveDataModel.one_previous_field_has_to_be_set',
                      MagicMock(side_effect=PreviousFieldsMissingError)):
            step = EligibilityStepChooser('eligibility').get_correct_step(
                SeparatedJointTaxesEligibilityInputFormSteuerlotseStep.name, True,
                form_data=ImmutableMultiDict({'separated_joint_taxes_eligibility': 'yes'}))

            self.assertRaises(IncorrectEligibilityData, step.handle)

    def test_if_get_and_incorrect_data_from_session_then_delete_incorrect_data(self):
        session_data_with_incorrect_key = {**self.correct_session_data, **{'INCORRECT_KEY': 'UNNECESSARY_VALUE'}}
        with self.app.test_request_context(method='GET') as req:
            req.session = SecureCookieSession(
                {_ELIGIBILITY_DATA_KEY: create_session_form_data(session_data_with_incorrect_key)})
            step = EligibilityStepChooser('eligibility').get_correct_step(
                SeparatedJointTaxesEligibilityInputFormSteuerlotseStep.name, False, ImmutableMultiDict({}))
            step.handle()

            self.assertEqual(self.correct_session_data,
                             FormStorage.deserialize_data(req.session[_ELIGIBILITY_DATA_KEY]))

    def test_if_get_and_correct_data_from_session_then_do_not_delete_any_data(self):
        with self.app.test_request_context(method='GET') as req:
            req.session = SecureCookieSession(
                {_ELIGIBILITY_DATA_KEY: create_session_form_data(self.correct_session_data)})
            step = EligibilityStepChooser('eligibility').get_correct_step(
                SeparatedJointTaxesEligibilityInputFormSteuerlotseStep.name, False, ImmutableMultiDict({}))
            step.handle()

            self.assertEqual(self.correct_session_data,
                             FormStorage.deserialize_data(req.session[_ELIGIBILITY_DATA_KEY]))

    def test_if_get_and_full_data_from_session_then_delete_unnecessary_data(self):
        only_necessary_data = {'marital_status_eligibility': 'single',
                               'separated_since_last_year_eligibility': 'no',
                               'separated_lived_together_eligibility': 'no',
                               'separated_joint_taxes_eligibility': 'no', }
        with self.app.test_request_context(method='GET') as req:
            req.session = SecureCookieSession({_ELIGIBILITY_DATA_KEY: create_session_form_data(FULL_SESSION_DATA)})
            step = EligibilityStepChooser('eligibility').get_correct_step(
                SeparatedJointTaxesEligibilityInputFormSteuerlotseStep.name, False, ImmutableMultiDict({}))
            step.handle()

            self.assertEqual(only_necessary_data,
                             FormStorage.deserialize_data(req.session[_ELIGIBILITY_DATA_KEY]))


class TestMarriedJointTaxesEligibilityFailureDisplaySteuerlotseStep(unittest.TestCase):
    @pytest.fixture(autouse=True)
    def attach_fixtures(self, app):
        self.app = app

    def test_handle_sets_correct_prev_url(self):
        with self.app.test_request_context():
            step = MarriedJointTaxesEligibilityFailureDisplaySteuerlotseStep(
                endpoint='eligibility',
                render_info=MarriedJointTaxesEligibilityFailureDisplaySteuerlotseStep.prepare_render_info(
                    {}))
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
        with self.app.test_request_context(method='POST') as req:
            req.session = SecureCookieSession(
                {_ELIGIBILITY_DATA_KEY: create_session_form_data(self.correct_session_data)})
            step = EligibilityStepChooser('eligibility').get_correct_step(
                MarriedJointTaxesDecisionEligibilityInputFormSteuerlotseStep.name, True,
                form_data=ImmutableMultiDict({'joint_taxes_eligibility': 'yes'}))
            expected_url = step.url_for_step(MarriedAlimonyDecisionEligibilityInputFormSteuerlotseStep.name)
            step.handle()

        self.assertEqual(expected_url, step.render_info.next_url)

    def test_if_post_and_session_data_correct_and_input_data_incorrect_than_set_next_url_to_failure_step(self):
        with self.app.test_request_context(method='POST') as req:
            req.session = SecureCookieSession(
                {_ELIGIBILITY_DATA_KEY: create_session_form_data(self.correct_session_data)})
            step = EligibilityStepChooser('eligibility').get_correct_step(
                MarriedJointTaxesDecisionEligibilityInputFormSteuerlotseStep.name, True,
                form_data=ImmutableMultiDict({'joint_taxes_eligibility': 'no'}))
            expected_url = step.url_for_step(MarriedJointTaxesEligibilityFailureDisplaySteuerlotseStep.name)
            step.handle()

        self.assertEqual(expected_url, step.render_info.next_url)

    def test_if_session_data_correct_then_set_prev_input_step_correctly(self):
        with self.app.test_request_context(method='GET') as req:
            req.session = SecureCookieSession(
                {_ELIGIBILITY_DATA_KEY: create_session_form_data(self.correct_session_data)})
            step = EligibilityStepChooser('eligibility').get_correct_step(
                MarriedJointTaxesDecisionEligibilityInputFormSteuerlotseStep.name, False, ImmutableMultiDict({}))
            expected_url = step.url_for_step(SeparatedEligibilityInputFormSteuerlotseStep.name)
            step.handle()
        self.assertEqual(expected_url, step.render_info.prev_url)

    def test_if_post_and_data_from_before_invalid_then_raise_incorrect_eligibility_data_error(self):
        with self.app.test_request_context(method='POST'), \
                patch('app.model.recursive_data.RecursiveDataModel.one_previous_field_has_to_be_set',
                      MagicMock(side_effect=PreviousFieldsMissingError)):
            step = EligibilityStepChooser('eligibility').get_correct_step(
                MarriedJointTaxesDecisionEligibilityInputFormSteuerlotseStep.name, True,
                form_data=ImmutableMultiDict({'joint_taxes_eligibility': 'yes'}))

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
                MarriedJointTaxesDecisionEligibilityInputFormSteuerlotseStep.name, False, ImmutableMultiDict({}))
            step.handle()

            self.assertEqual(session_data,
                             FormStorage.deserialize_data(req.session[_ELIGIBILITY_DATA_KEY]))

    def test_if_get_and_correct_data_from_session_then_do_not_delete_any_data(self):
        session_data = {'marital_status_eligibility': 'single',
                        'separated_since_last_year_eligibility': 'no',
                        'joint_taxes_eligibility': 'no', }
        with self.app.test_request_context(method='GET') as req:
            req.session = SecureCookieSession({_ELIGIBILITY_DATA_KEY: create_session_form_data(session_data)})
            step = EligibilityStepChooser('eligibility').get_correct_step(
                MarriedJointTaxesDecisionEligibilityInputFormSteuerlotseStep.name, False, ImmutableMultiDict({}))
            step.handle()

            self.assertEqual(session_data,
                             FormStorage.deserialize_data(req.session[_ELIGIBILITY_DATA_KEY]))

    def test_if_get_and_full_data_from_session_then_delete_unnecessary_data(self):
        only_necessary_data = {'marital_status_eligibility': 'single',
                               'separated_since_last_year_eligibility': 'no',
                               'joint_taxes_eligibility': 'no', }
        with self.app.test_request_context(method='GET') as req:
            req.session = SecureCookieSession({_ELIGIBILITY_DATA_KEY: create_session_form_data(FULL_SESSION_DATA)})
            step = EligibilityStepChooser('eligibility').get_correct_step(
                MarriedJointTaxesDecisionEligibilityInputFormSteuerlotseStep.name, False, ImmutableMultiDict({}))
            step.handle()

            self.assertEqual(only_necessary_data,
                             FormStorage.deserialize_data(req.session[_ELIGIBILITY_DATA_KEY]))


class TestMarriedAlimonyEligibilityFailureDisplaySteuerlotseStep(unittest.TestCase):
    @pytest.fixture(autouse=True)
    def attach_fixtures(self, test_request_context):
        self.test_request_context = test_request_context

    def test_handle_sets_correct_prev_url(self):
        step = MarriedAlimonyEligibilityFailureDisplaySteuerlotseStep(
                endpoint='eligibility',
                render_info=MarriedAlimonyEligibilityFailureDisplaySteuerlotseStep.prepare_render_info(
                    {}))
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
        with self.app.test_request_context(method='POST') as req:
            req.session = SecureCookieSession(
                {_ELIGIBILITY_DATA_KEY: create_session_form_data(self.correct_session_data)})
            step = EligibilityStepChooser('eligibility').get_correct_step(
                MarriedAlimonyDecisionEligibilityInputFormSteuerlotseStep.name, True,
                form_data=ImmutableMultiDict({'alimony_eligibility': 'no'}))
            expected_url = step.url_for_step(UserAElsterAccountEligibilityInputFormSteuerlotseStep.name)
            step.handle()

        self.assertEqual(expected_url, step.render_info.next_url)

    def test_if_post_and_session_data_correct_and_input_data_incorrect_than_set_next_url_to_failure_step(self):
        with self.app.test_request_context(method='POST') as req:
            req.session = SecureCookieSession(
                {_ELIGIBILITY_DATA_KEY: create_session_form_data(self.correct_session_data)})
            step = EligibilityStepChooser('eligibility').get_correct_step(
                MarriedAlimonyDecisionEligibilityInputFormSteuerlotseStep.name, True,
                form_data=ImmutableMultiDict({'alimony_eligibility': 'yes'}))
            expected_url = step.url_for_step(MarriedAlimonyEligibilityFailureDisplaySteuerlotseStep.name)
            step.handle()

        self.assertEqual(expected_url, step.render_info.next_url)

    def test_if_not_separated_then_set_prev_input_step_correctly(self):
        with self.app.test_request_context(method='GET') as req:
            req.session = SecureCookieSession(
                {_ELIGIBILITY_DATA_KEY: create_session_form_data(self.correct_session_data)})
            step = EligibilityStepChooser('eligibility').get_correct_step(
                MarriedAlimonyDecisionEligibilityInputFormSteuerlotseStep.name, False, ImmutableMultiDict({}))
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
                MarriedAlimonyDecisionEligibilityInputFormSteuerlotseStep.name, False, ImmutableMultiDict({}))
            expected_url = step.url_for_step(SeparatedJointTaxesEligibilityInputFormSteuerlotseStep.name)
            step.handle()
        self.assertEqual(expected_url, step.render_info.prev_url)

    def test_if_post_and_data_from_before_invalid_then_raise_incorrect_eligibility_data_error(self):
        with self.app.test_request_context(method='POST'), \
                patch('app.model.recursive_data.RecursiveDataModel.one_previous_field_has_to_be_set',
                      MagicMock(side_effect=PreviousFieldsMissingError)):
            step = EligibilityStepChooser('eligibility').get_correct_step(
                MarriedAlimonyDecisionEligibilityInputFormSteuerlotseStep.name, True,
                form_data=ImmutableMultiDict({'alimony_eligibility': 'no'}))

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
                MarriedAlimonyDecisionEligibilityInputFormSteuerlotseStep.name, False, ImmutableMultiDict({}))
            step.handle()

            self.assertEqual(session_data,
                             FormStorage.deserialize_data(req.session[_ELIGIBILITY_DATA_KEY]))

    def test_if_get_and_correct_data_from_session_then_do_not_delete_any_data(self):
        session_data = {'marital_status_eligibility': 'single',
                        'separated_since_last_year_eligibility': 'no',
                        'joint_taxes_eligibility': 'no',
                        'alimony_eligibility': 'no', }
        with self.app.test_request_context(method='GET') as req:
            req.session = SecureCookieSession({_ELIGIBILITY_DATA_KEY: create_session_form_data(session_data)})
            step = EligibilityStepChooser('eligibility').get_correct_step(
                MarriedAlimonyDecisionEligibilityInputFormSteuerlotseStep.name, False, ImmutableMultiDict({}))
            step.handle()

            self.assertEqual(session_data,
                             FormStorage.deserialize_data(req.session[_ELIGIBILITY_DATA_KEY]))

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
                MarriedAlimonyDecisionEligibilityInputFormSteuerlotseStep.name, False, ImmutableMultiDict({}))
            step.handle()

            self.assertEqual(only_necessary_data,
                             FormStorage.deserialize_data(req.session[_ELIGIBILITY_DATA_KEY]))

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
                MarriedAlimonyDecisionEligibilityInputFormSteuerlotseStep.name, False, ImmutableMultiDict({}))
            step._pre_handle()

        self.assertEqual(expected_choices, step.render_info.form.alimony_eligibility.choices)

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
                MarriedAlimonyDecisionEligibilityInputFormSteuerlotseStep.name, False, ImmutableMultiDict({}))
            step._pre_handle()

        self.assertEqual(expected_choices, step.render_info.form.alimony_eligibility.choices)


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
        with self.app.test_request_context(method='POST') as req:
            req.session = SecureCookieSession(
                {_ELIGIBILITY_DATA_KEY: create_session_form_data(self.correct_session_data)})
            step = EligibilityStepChooser('eligibility').get_correct_step(
                UserAElsterAccountEligibilityInputFormSteuerlotseStep.name, True,
                form_data=ImmutableMultiDict({'user_a_has_elster_account_eligibility': 'no'}))
            expected_url = step.url_for_step(PensionDecisionEligibilityInputFormSteuerlotseStep.name)
            step.handle()

        self.assertEqual(expected_url, step.render_info.next_url)

    def test_if_post_and_session_data_correct_and_input_data_incorrect_than_set_next_url_to_alternative_step(self):
        with self.app.test_request_context(method='POST') as req:
            req.session = SecureCookieSession(
                {_ELIGIBILITY_DATA_KEY: create_session_form_data(self.correct_session_data)})
            step = EligibilityStepChooser('eligibility').get_correct_step(
                UserAElsterAccountEligibilityInputFormSteuerlotseStep.name, True,
                form_data=ImmutableMultiDict({'user_a_has_elster_account_eligibility': 'yes'}))
            expected_url = step.url_for_step(UserBElsterAccountDecisionEligibilityInputFormSteuerlotseStep.name)
            step.handle()

        self.assertEqual(expected_url, step.render_info.next_url)

    def test_if_session_data_correct_then_set_prev_input_step_correctly(self):
        with self.app.test_request_context(method='GET') as req:
            req.session = SecureCookieSession(
                {_ELIGIBILITY_DATA_KEY: create_session_form_data(self.correct_session_data)})
            step = EligibilityStepChooser('eligibility').get_correct_step(
                UserAElsterAccountEligibilityInputFormSteuerlotseStep.name, False, ImmutableMultiDict({}))
            expected_url = step.url_for_step(MarriedAlimonyDecisionEligibilityInputFormSteuerlotseStep.name)
            step.handle()
        self.assertEqual(expected_url, step.render_info.prev_url)

    @pytest.mark.usefixtures('test_request_context')
    def test_if_post_and_data_from_before_invalid_then_raise_incorrect_eligibility_data_error(self):
        with patch('app.model.recursive_data.RecursiveDataModel.one_previous_field_has_to_be_set',
                      MagicMock(side_effect=PreviousFieldsMissingError)):
            step = EligibilityStepChooser('eligibility').get_correct_step(
                UserAElsterAccountEligibilityInputFormSteuerlotseStep.name, True,
                form_data=ImmutableMultiDict({'user_a_has_elster_account_eligibility': 'no'}))

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
                UserAElsterAccountEligibilityInputFormSteuerlotseStep.name, False, ImmutableMultiDict({}))
            step.handle()

            self.assertEqual(session_data,
                             FormStorage.deserialize_data(req.session[_ELIGIBILITY_DATA_KEY]))

    def test_if_get_and_correct_data_from_session_then_do_not_delete_any_data(self):
        session_data = {'marital_status_eligibility': 'single',
                        'separated_since_last_year_eligibility': 'no',
                        'user_a_has_elster_account_eligibility': 'no',
                        'joint_taxes_eligibility': 'no',
                        'alimony_eligibility': 'no', }
        with self.app.test_request_context(method='GET') as req:
            req.session = SecureCookieSession({_ELIGIBILITY_DATA_KEY: create_session_form_data(session_data)})
            step = EligibilityStepChooser('eligibility').get_correct_step(
                UserAElsterAccountEligibilityInputFormSteuerlotseStep.name, False, ImmutableMultiDict({}))
            step.handle()

            self.assertEqual(session_data,
                             FormStorage.deserialize_data(req.session[_ELIGIBILITY_DATA_KEY]))

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
                UserAElsterAccountEligibilityInputFormSteuerlotseStep.name, False, ImmutableMultiDict({}))
            step.handle()

            self.assertEqual(only_necessary_data,
                             FormStorage.deserialize_data(req.session[_ELIGIBILITY_DATA_KEY]))


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
        with self.app.test_request_context(method='POST') as req:
            req.session = SecureCookieSession(
                {_ELIGIBILITY_DATA_KEY: create_session_form_data(self.correct_session_data)})
            step = EligibilityStepChooser('eligibility').get_correct_step(
                UserBElsterAccountDecisionEligibilityInputFormSteuerlotseStep.name, True,
                form_data=ImmutableMultiDict({'user_b_has_elster_account_eligibility': 'no'}))
            expected_url = step.url_for_step(PensionDecisionEligibilityInputFormSteuerlotseStep.name)
            step.handle()

        self.assertEqual(expected_url, step.render_info.next_url)

    def test_if_post_and_session_data_correct_and_input_data_incorrect_than_set_next_url_to_alternative_step(self):
        with self.app.test_request_context(method='POST') as req:
            req.session = SecureCookieSession(
                {_ELIGIBILITY_DATA_KEY: create_session_form_data(self.correct_session_data)})
            step = EligibilityStepChooser('eligibility').get_correct_step(
                UserBElsterAccountDecisionEligibilityInputFormSteuerlotseStep.name, True,
                form_data=ImmutableMultiDict({'user_b_has_elster_account_eligibility': 'yes'}))
            expected_url = step.url_for_step(PensionDecisionEligibilityInputFormSteuerlotseStep.name)
            step.handle()

        self.assertEqual(expected_url, step.render_info.next_url)

    def test_if_session_data_correct_then_set_prev_input_step_correctly(self):
        with self.app.test_request_context(method='GET') as req:
            req.session = SecureCookieSession(
                {_ELIGIBILITY_DATA_KEY: create_session_form_data(self.correct_session_data)})
            step = EligibilityStepChooser('eligibility').get_correct_step(
                UserBElsterAccountDecisionEligibilityInputFormSteuerlotseStep.name, False, ImmutableMultiDict({}))
            expected_url = step.url_for_step(UserAElsterAccountEligibilityInputFormSteuerlotseStep.name)
            step.handle()
        self.assertEqual(expected_url, step.render_info.prev_url)

    @pytest.mark.usefixtures('test_request_context')
    def test_if_post_and_data_from_before_invalid_then_raise_incorrect_eligibility_data_error(self):
        with patch('app.model.recursive_data.RecursiveDataModel.one_previous_field_has_to_be_set',
                      MagicMock(side_effect=PreviousFieldsMissingError)):
            step = EligibilityStepChooser('eligibility').get_correct_step(
                UserBElsterAccountDecisionEligibilityInputFormSteuerlotseStep.name, True,
                form_data=ImmutableMultiDict({'user_b_has_elster_account_eligibility': 'no'}))

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
                UserBElsterAccountDecisionEligibilityInputFormSteuerlotseStep.name, False, ImmutableMultiDict({}))
            step.handle()

            self.assertEqual(session_data,
                             FormStorage.deserialize_data(req.session[_ELIGIBILITY_DATA_KEY]))

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
                UserBElsterAccountDecisionEligibilityInputFormSteuerlotseStep.name, False, ImmutableMultiDict({}))
            step.handle()

            self.assertEqual(session_data,
                             FormStorage.deserialize_data(req.session[_ELIGIBILITY_DATA_KEY]))

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
                UserBElsterAccountDecisionEligibilityInputFormSteuerlotseStep.name, False, ImmutableMultiDict({}))
            step.handle()

            self.assertEqual(only_necessary_data,
                             FormStorage.deserialize_data(req.session[_ELIGIBILITY_DATA_KEY]))


class TestDivorcedJointTaxesEligibilityFailureDisplaySteuerlotseStep(unittest.TestCase):
    @pytest.fixture(autouse=True)
    def attach_fixtures(self, test_request_context):
        self.req = test_request_context

    def test_handle_sets_correct_prev_url(self):
        step = DivorcedJointTaxesEligibilityFailureDisplaySteuerlotseStep(
                endpoint='eligibility',
                render_info=DivorcedJointTaxesEligibilityFailureDisplaySteuerlotseStep.prepare_render_info(
                    {}))
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
        with self.app.test_request_context(method='POST') as req:
            req.session = SecureCookieSession(
                {_ELIGIBILITY_DATA_KEY: create_session_form_data(self.correct_session_data)})
            step = EligibilityStepChooser('eligibility').get_correct_step(
                DivorcedJointTaxesDecisionEligibilityInputFormSteuerlotseStep.name, True,
                form_data=ImmutableMultiDict({'joint_taxes_eligibility': 'no'}))
            expected_url = step.url_for_step(SingleAlimonyDecisionEligibilityInputFormSteuerlotseStep.name)
            step.handle()

        self.assertEqual(expected_url, step.render_info.next_url)

    def test_if_post_and_session_data_correct_and_input_data_incorrect_than_set_next_url_to_alternative_step(self):
        with self.app.test_request_context(method='POST') as req:
            req.session = SecureCookieSession(
                {_ELIGIBILITY_DATA_KEY: create_session_form_data(self.correct_session_data)})
            step = EligibilityStepChooser('eligibility').get_correct_step(
                DivorcedJointTaxesDecisionEligibilityInputFormSteuerlotseStep.name, True,
                form_data=ImmutableMultiDict({'joint_taxes_eligibility': 'yes'}))
            expected_url = step.url_for_step(DivorcedJointTaxesEligibilityFailureDisplaySteuerlotseStep.name)
            step.handle()

        self.assertEqual(expected_url, step.render_info.next_url)

    def test_if_session_data_correct_then_set_prev_input_step_correctly(self):
        with self.app.test_request_context(method='GET') as req:
            req.session = SecureCookieSession(
                {_ELIGIBILITY_DATA_KEY: create_session_form_data(self.correct_session_data)})
            step = EligibilityStepChooser('eligibility').get_correct_step(
                DivorcedJointTaxesDecisionEligibilityInputFormSteuerlotseStep.name, False, ImmutableMultiDict({}))
            expected_url = step.url_for_step(MaritalStatusInputFormSteuerlotseStep.name)
            step.handle()
        self.assertEqual(expected_url, step.render_info.prev_url)

    @pytest.mark.usefixtures('test_request_context')
    def test_if_post_and_data_from_before_invalid_then_raise_incorrect_eligibility_data_error(self):
        with patch('app.model.recursive_data.RecursiveDataModel.one_previous_field_has_to_be_set',
                      MagicMock(side_effect=PreviousFieldsMissingError)):
            step = EligibilityStepChooser('eligibility').get_correct_step(
                DivorcedJointTaxesDecisionEligibilityInputFormSteuerlotseStep.name, True,
                form_data=ImmutableMultiDict({'joint_taxes_eligibility': 'no'}))

            with pytest.raises(IncorrectEligibilityData):
                step.handle()

    def test_if_get_and_incorrect_data_from_session_then_delete_incorrect_data(self):
        session_data = {'marital_status_eligibility': 'single',
                        'joint_taxes_eligibility': 'no', }
        session_data_with_incorrect_key = {**session_data, **{'INCORRECT_KEY': 'UNNECESSARY_VALUE'}}
        with self.app.test_request_context(method='GET') as req:
            req.session = SecureCookieSession(
                {_ELIGIBILITY_DATA_KEY: create_session_form_data(session_data_with_incorrect_key)})
            step = EligibilityStepChooser('eligibility').get_correct_step(
                DivorcedJointTaxesDecisionEligibilityInputFormSteuerlotseStep.name, False, ImmutableMultiDict({}))
            step.handle()

            self.assertEqual(session_data,
                             FormStorage.deserialize_data(req.session[_ELIGIBILITY_DATA_KEY]))

    def test_if_get_and_correct_data_from_session_then_do_not_delete_any_data(self):
        session_data = {'marital_status_eligibility': 'single',
                        'joint_taxes_eligibility': 'no', }
        with self.app.test_request_context(method='GET') as req:
            req.session = SecureCookieSession({_ELIGIBILITY_DATA_KEY: create_session_form_data(session_data)})
            step = EligibilityStepChooser('eligibility').get_correct_step(
                DivorcedJointTaxesDecisionEligibilityInputFormSteuerlotseStep.name, False, ImmutableMultiDict({}))
            step.handle()

            self.assertEqual(session_data,
                             FormStorage.deserialize_data(req.session[_ELIGIBILITY_DATA_KEY]))

    def test_if_get_and_full_data_from_session_then_delete_unnecessary_data(self):
        only_necessary_data = {'marital_status_eligibility': 'single',
                               'joint_taxes_eligibility': 'no', }
        with self.app.test_request_context(method='GET') as req:
            req.session = SecureCookieSession({_ELIGIBILITY_DATA_KEY: create_session_form_data(FULL_SESSION_DATA)})
            step = EligibilityStepChooser('eligibility').get_correct_step(
                DivorcedJointTaxesDecisionEligibilityInputFormSteuerlotseStep.name, False, ImmutableMultiDict({}))
            step.handle()

            self.assertEqual(only_necessary_data,
                             FormStorage.deserialize_data(req.session[_ELIGIBILITY_DATA_KEY]))


class TestSingleAlimonyEligibilityFailureDisplaySteuerlotseStep(unittest.TestCase):
    @pytest.fixture(autouse=True)
    def attach_fixtures(self, test_request_context):
        self.req = test_request_context

    def test_handle_sets_correct_prev_url(self):
        step = SingleAlimonyEligibilityFailureDisplaySteuerlotseStep(
                endpoint='eligibility',
                render_info=SingleAlimonyEligibilityFailureDisplaySteuerlotseStep.prepare_render_info(
                    {}))
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
        with self.app.test_request_context(method='POST') as req:
            req.session = SecureCookieSession(
                {_ELIGIBILITY_DATA_KEY: create_session_form_data(self.correct_session_data)})
            step = EligibilityStepChooser('eligibility').get_correct_step(
                SingleAlimonyDecisionEligibilityInputFormSteuerlotseStep.name, True,
                form_data=ImmutableMultiDict({'alimony_eligibility': 'no'}))
            expected_url = step.url_for_step(SingleElsterAccountDecisionEligibilityInputFormSteuerlotseStep.name)
            step.handle()

        self.assertEqual(expected_url, step.render_info.next_url)

    def test_if_post_and_session_data_correct_and_input_data_incorrect_than_set_next_url_to_alternative_step(self):
        with self.app.test_request_context(method='POST') as req:
            req.session = SecureCookieSession(
                {_ELIGIBILITY_DATA_KEY: create_session_form_data(self.correct_session_data)})
            step = EligibilityStepChooser('eligibility').get_correct_step(
                SingleAlimonyDecisionEligibilityInputFormSteuerlotseStep.name, True,
                form_data=ImmutableMultiDict({'alimony_eligibility': 'yes'}))
            expected_url = step.url_for_step(SingleAlimonyEligibilityFailureDisplaySteuerlotseStep.name)
            step.handle()

        self.assertEqual(expected_url, step.render_info.next_url)

    def test_if_divorced_session_data_correct_then_set_prev_input_step_correctly(self):
        with self.app.test_request_context(method='GET') as req:
            req.session = SecureCookieSession(
                {_ELIGIBILITY_DATA_KEY: create_session_form_data(self.correct_session_data)})
            step = EligibilityStepChooser('eligibility').get_correct_step(
                SingleAlimonyDecisionEligibilityInputFormSteuerlotseStep.name, False, ImmutableMultiDict({}))
            expected_url = step.url_for_step(DivorcedJointTaxesDecisionEligibilityInputFormSteuerlotseStep.name)
            step.handle()
        self.assertEqual(expected_url, step.render_info.prev_url)

    def test_if_single_session_data_correct_then_set_prev_input_step_correctly(self):
        alternative_data = {'marital_status_eligibility': 'single'}
        with self.app.test_request_context(method='GET') as req:
            req.session = SecureCookieSession({_ELIGIBILITY_DATA_KEY: create_session_form_data(alternative_data)})
            step = EligibilityStepChooser('eligibility').get_correct_step(
                SingleAlimonyDecisionEligibilityInputFormSteuerlotseStep.name, False, ImmutableMultiDict({}))
            expected_url = step.url_for_step(MaritalStatusInputFormSteuerlotseStep.name)
            step.handle()
        self.assertEqual(expected_url, step.render_info.prev_url)

    def test_if_widowed_session_data_correct_then_set_prev_input_step_correctly(self):
        alternative_data = {'marital_status_eligibility': 'widowed'}
        with self.app.test_request_context(method='GET') as req:
            req.session = SecureCookieSession({_ELIGIBILITY_DATA_KEY: create_session_form_data(alternative_data)})
            step = EligibilityStepChooser('eligibility').get_correct_step(
                SingleAlimonyDecisionEligibilityInputFormSteuerlotseStep.name, False, ImmutableMultiDict({}))
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
                SingleAlimonyDecisionEligibilityInputFormSteuerlotseStep.name, False, ImmutableMultiDict({}))
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
                SingleAlimonyDecisionEligibilityInputFormSteuerlotseStep.name, False, ImmutableMultiDict({}))
            expected_url = step.url_for_step(SeparatedJointTaxesEligibilityInputFormSteuerlotseStep.name)
            step.handle()
        self.assertEqual(expected_url, step.render_info.prev_url)

    @pytest.mark.usefixtures('test_request_context')
    def test_if_post_and_data_from_before_invalid_then_raise_incorrect_eligibility_data_error(self):
        with patch('app.model.recursive_data.RecursiveDataModel.one_previous_field_has_to_be_set',
                      MagicMock(side_effect=PreviousFieldsMissingError)):
            step = EligibilityStepChooser('eligibility').get_correct_step(
                SingleAlimonyDecisionEligibilityInputFormSteuerlotseStep.name, True,
                form_data=ImmutableMultiDict({'alimony_eligibility': 'no'}))

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
                SingleAlimonyDecisionEligibilityInputFormSteuerlotseStep.name, False, ImmutableMultiDict({}))
            step.handle()

            self.assertEqual(session_data,
                             FormStorage.deserialize_data(req.session[_ELIGIBILITY_DATA_KEY]))

    def test_if_get_and_correct_data_from_session_then_do_not_delete_any_data(self):
        session_data = {'marital_status_eligibility': 'single',
                        'joint_taxes_eligibility': 'no',
                        'alimony_eligibility': 'no', }
        with self.app.test_request_context(method='GET') as req:
            req.session = SecureCookieSession({_ELIGIBILITY_DATA_KEY: create_session_form_data(session_data)})
            step = EligibilityStepChooser('eligibility').get_correct_step(
                SingleAlimonyDecisionEligibilityInputFormSteuerlotseStep.name, False, ImmutableMultiDict({}))
            step.handle()

            self.assertEqual(session_data,
                             FormStorage.deserialize_data(req.session[_ELIGIBILITY_DATA_KEY]))

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
                SingleAlimonyDecisionEligibilityInputFormSteuerlotseStep.name, False, ImmutableMultiDict({}))
            step.handle()

            self.assertEqual(only_necessary_data,
                             FormStorage.deserialize_data(req.session[_ELIGIBILITY_DATA_KEY]))


class TestSingleElsterAccountDecisionEligibilityInputFormSteuerlotseStep(unittest.TestCase):
    @pytest.fixture(autouse=True)
    def attach_fixtures(self, app):
        self.app = app

    def setUp(self):
        self.correct_session_data = {'marital_status_eligibility': 'divorced',
                                     'joint_taxes_eligibility': 'no',
                                     'alimony_eligibility': 'no'}

    def test_if_post_and_session_data_correct_and_input_data_correct_than_set_next_input_step(self):
        with self.app.test_request_context(method='POST') as req:
            req.session = SecureCookieSession(
                {_ELIGIBILITY_DATA_KEY: create_session_form_data(self.correct_session_data)})
            step = EligibilityStepChooser('eligibility').get_correct_step(
                SingleElsterAccountDecisionEligibilityInputFormSteuerlotseStep.name, True,
                form_data=ImmutableMultiDict({'user_a_has_elster_account_eligibility': 'no'}))
            expected_url = step.url_for_step(PensionDecisionEligibilityInputFormSteuerlotseStep.name)
            step.handle()

        self.assertEqual(expected_url, step.render_info.next_url)

    def test_if_post_and_session_data_correct_and_input_data_incorrect_than_set_next_url_to_alternative_step(self):
        with self.app.test_request_context(method='POST') as req:
            req.session = SecureCookieSession(
                {_ELIGIBILITY_DATA_KEY: create_session_form_data(self.correct_session_data)})
            step = EligibilityStepChooser('eligibility').get_correct_step(
                SingleElsterAccountDecisionEligibilityInputFormSteuerlotseStep.name, True,
                form_data=ImmutableMultiDict({'user_a_has_elster_account_eligibility': 'yes'}))
            expected_url = step.url_for_step(PensionDecisionEligibilityInputFormSteuerlotseStep.name)
            step.handle()

        self.assertEqual(expected_url, step.render_info.next_url)

    def test_if_session_data_correct_then_set_prev_input_step_correctly(self):
        with self.app.test_request_context(method='GET') as req:
            req.session = SecureCookieSession(
                {_ELIGIBILITY_DATA_KEY: create_session_form_data(self.correct_session_data)})
            step = EligibilityStepChooser('eligibility').get_correct_step(
                SingleElsterAccountDecisionEligibilityInputFormSteuerlotseStep.name, False, ImmutableMultiDict({}))
            expected_url = step.url_for_step(SingleAlimonyDecisionEligibilityInputFormSteuerlotseStep.name)
            step.handle()
        self.assertEqual(expected_url, step.render_info.prev_url)

    @pytest.mark.usefixtures('test_request_context')
    def test_if_post_and_data_from_before_invalid_then_raise_incorrect_eligibility_data_error(self):
        with patch('app.model.recursive_data.RecursiveDataModel.one_previous_field_has_to_be_set',
                      MagicMock(side_effect=PreviousFieldsMissingError)):
            step = EligibilityStepChooser('eligibility').get_correct_step(
                SingleElsterAccountDecisionEligibilityInputFormSteuerlotseStep.name, True,
                form_data=ImmutableMultiDict({'user_a_has_elster_account_eligibility': 'no'}))

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
                SingleElsterAccountDecisionEligibilityInputFormSteuerlotseStep.name, False, ImmutableMultiDict({}))
            step.handle()

            self.assertEqual(session_data,
                             FormStorage.deserialize_data(req.session[_ELIGIBILITY_DATA_KEY]))

    def test_if_get_and_correct_data_from_session_then_do_not_delete_any_data(self):
        session_data = {'marital_status_eligibility': 'single',
                        'user_a_has_elster_account_eligibility': 'no',
                        'joint_taxes_eligibility': 'no',
                        'alimony_eligibility': 'no', }
        with self.app.test_request_context(method='GET') as req:
            req.session = SecureCookieSession({_ELIGIBILITY_DATA_KEY: create_session_form_data(session_data)})
            step = EligibilityStepChooser('eligibility').get_correct_step(
                SingleElsterAccountDecisionEligibilityInputFormSteuerlotseStep.name, False, ImmutableMultiDict({}))
            step.handle()

            self.assertEqual(session_data,
                             FormStorage.deserialize_data(req.session[_ELIGIBILITY_DATA_KEY]))

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
                SingleElsterAccountDecisionEligibilityInputFormSteuerlotseStep.name, False, ImmutableMultiDict({}))
            step.handle()

            self.assertEqual(only_necessary_data,
                             FormStorage.deserialize_data(req.session[_ELIGIBILITY_DATA_KEY]))


class TestPensionEligibilityFailureDisplaySteuerlotseStep:
    def test_handle_sets_correct_prev_url(self, test_request_context):
        step = PensionEligibilityFailureDisplaySteuerlotseStep(
                endpoint='eligibility',
                render_info=PensionEligibilityFailureDisplaySteuerlotseStep.prepare_render_info(
                    {}))
        expected_url = step.url_for_step(PensionDecisionEligibilityInputFormSteuerlotseStep.name)
        step.handle()

        assert step.render_info.prev_url == expected_url


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
        with self.app.test_request_context(method='POST') as req:
            req.session = SecureCookieSession(
                {_ELIGIBILITY_DATA_KEY: create_session_form_data(self.correct_session_data)})
            step = EligibilityStepChooser('eligibility').get_correct_step(
                PensionDecisionEligibilityInputFormSteuerlotseStep.name, True,
                form_data=ImmutableMultiDict({'pension_eligibility': 'yes'}))
            expected_url = step.url_for_step(InvestmentIncomeDecisionEligibilityInputFormSteuerlotseStep.name)
            step.handle()

        self.assertEqual(expected_url, step.render_info.next_url)

    def test_if_post_and_session_data_correct_and_input_data_incorrect_than_set_next_url_to_alternative_step(self):
        with self.app.test_request_context(method='POST') as req:
            req.session = SecureCookieSession(
                {_ELIGIBILITY_DATA_KEY: create_session_form_data(self.correct_session_data)})
            step = EligibilityStepChooser('eligibility').get_correct_step(
                PensionDecisionEligibilityInputFormSteuerlotseStep.name, True,
                form_data=ImmutableMultiDict({'pension_eligibility': 'no'}))
            expected_url = step.url_for_step(PensionEligibilityFailureDisplaySteuerlotseStep.name)
            step.handle()

        self.assertEqual(expected_url, step.render_info.next_url)

    def test_if_no_joint_taxes_session_data_correct_then_set_prev_input_step_correctly(self):
        with self.app.test_request_context(method='GET') as req:
            req.session = SecureCookieSession(
                {_ELIGIBILITY_DATA_KEY: create_session_form_data(self.correct_session_data)})
            step = EligibilityStepChooser('eligibility').get_correct_step(
                PensionDecisionEligibilityInputFormSteuerlotseStep.name, False, ImmutableMultiDict({}))
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
                PensionDecisionEligibilityInputFormSteuerlotseStep.name, False, ImmutableMultiDict({}))
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
                PensionDecisionEligibilityInputFormSteuerlotseStep.name, False, ImmutableMultiDict({}))
            expected_url = step.url_for_step(UserBElsterAccountDecisionEligibilityInputFormSteuerlotseStep.name)
            step.handle()
        self.assertEqual(expected_url, step.render_info.prev_url)

    @pytest.mark.usefixtures('test_request_context')
    def test_if_post_and_data_from_before_invalid_then_raise_incorrect_eligibility_data_error(self):
        with patch('app.model.recursive_data.RecursiveDataModel.one_previous_field_has_to_be_set',
                      MagicMock(side_effect=PreviousFieldsMissingError)):
            step = EligibilityStepChooser('eligibility').get_correct_step(
                PensionDecisionEligibilityInputFormSteuerlotseStep.name, True,
                form_data=ImmutableMultiDict({'pension_eligibility': 'yes'}))

            self.assertRaises(IncorrectEligibilityData, step.handle)

    def test_if_get_and_incorrect_data_from_session_then_delete_incorrect_data(self):
        session_data = {'marital_status_eligibility': 'single',
                        'separated_since_last_year_eligibility': 'no',
                        'joint_taxes_eligibility': 'no',
                        'alimony_eligibility': 'no',
                        'pension_eligibility': 'yes', }
        session_data_with_incorrect_key = {**session_data, **{'INCORRECT_KEY': 'UNNECESSARY_VALUE'}}
        with self.app.test_request_context(method='GET') as req:
            req.session = SecureCookieSession(
                {_ELIGIBILITY_DATA_KEY: create_session_form_data(session_data_with_incorrect_key)})
            step = EligibilityStepChooser('eligibility').get_correct_step(
                PensionDecisionEligibilityInputFormSteuerlotseStep.name, False, ImmutableMultiDict({}))
            step.handle()

            self.assertEqual(session_data,
                             FormStorage.deserialize_data(req.session[_ELIGIBILITY_DATA_KEY]))

    def test_if_get_and_correct_data_from_session_then_do_not_delete_any_data(self):
        session_data = {'marital_status_eligibility': 'single',
                        'separated_since_last_year_eligibility': 'no',
                        'joint_taxes_eligibility': 'no',
                        'alimony_eligibility': 'no',
                        'pension_eligibility': 'yes', }
        with self.app.test_request_context(method='GET') as req:
            req.session = SecureCookieSession({_ELIGIBILITY_DATA_KEY: create_session_form_data(session_data)})
            step = EligibilityStepChooser('eligibility').get_correct_step(
                PensionDecisionEligibilityInputFormSteuerlotseStep.name, False, ImmutableMultiDict({}))
            step.handle()

            self.assertEqual(session_data,
                             FormStorage.deserialize_data(req.session[_ELIGIBILITY_DATA_KEY]))

    def test_if_get_and_full_data_from_session_then_delete_unnecessary_data(self):
        only_necessary_data = {'marital_status_eligibility': 'single',
                               'separated_since_last_year_eligibility': 'no',
                               'separated_joint_taxes_eligibility': 'no',
                               'separated_lived_together_eligibility': 'no',
                               'joint_taxes_eligibility': 'no',
                               'alimony_eligibility': 'no',
                               'pension_eligibility': 'yes', }
        with self.app.test_request_context(method='GET') as req:
            req.session = SecureCookieSession({_ELIGIBILITY_DATA_KEY: create_session_form_data(FULL_SESSION_DATA)})
            step = EligibilityStepChooser('eligibility').get_correct_step(
                PensionDecisionEligibilityInputFormSteuerlotseStep.name, False, ImmutableMultiDict({}))
            step.handle()

            self.assertEqual(only_necessary_data,
                             FormStorage.deserialize_data(req.session[_ELIGIBILITY_DATA_KEY]))

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
                PensionDecisionEligibilityInputFormSteuerlotseStep.name, False, ImmutableMultiDict({}))
            step._pre_handle()

        self.assertEqual(expected_choices, step.render_info.form.pension_eligibility.choices)

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
                PensionDecisionEligibilityInputFormSteuerlotseStep.name, False, ImmutableMultiDict({}))
            step._pre_handle()

        self.assertEqual(expected_choices, step.render_info.form.pension_eligibility.choices)


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
        with self.app.test_request_context(method='POST') as req:
            req.session = SecureCookieSession(
                {_ELIGIBILITY_DATA_KEY: create_session_form_data(self.correct_session_data)})
            step = EligibilityStepChooser('eligibility').get_correct_step(
                InvestmentIncomeDecisionEligibilityInputFormSteuerlotseStep.name, True,
                form_data=ImmutableMultiDict({'investment_income_eligibility': 'yes'}))
            expected_url = step.url_for_step(MinimalInvestmentIncomeDecisionEligibilityInputFormSteuerlotseStep.name)
            step.handle()

        self.assertEqual(expected_url, step.render_info.next_url)

    def test_if_post_and_session_data_correct_and_input_data_incorrect_than_set_next_url_to_alternative_step(self):
        with self.app.test_request_context(method='POST') as req:
            req.session = SecureCookieSession(
                {_ELIGIBILITY_DATA_KEY: create_session_form_data(self.correct_session_data)})
            step = EligibilityStepChooser('eligibility').get_correct_step(
                InvestmentIncomeDecisionEligibilityInputFormSteuerlotseStep.name, True,
                form_data=ImmutableMultiDict({'investment_income_eligibility': 'no'}))
            expected_url = step.url_for_step(EmploymentDecisionEligibilityInputFormSteuerlotseStep.name)
            step.handle()

        self.assertEqual(expected_url, step.render_info.next_url)

    def test_if_session_data_correct_then_set_prev_input_step_correctly(self):
        with self.app.test_request_context(method='GET') as req:
            req.session = SecureCookieSession(
                {_ELIGIBILITY_DATA_KEY: create_session_form_data(self.correct_session_data)})
            step = EligibilityStepChooser('eligibility').get_correct_step(
                InvestmentIncomeDecisionEligibilityInputFormSteuerlotseStep.name, False, ImmutableMultiDict({}))
            expected_url = step.url_for_step(PensionDecisionEligibilityInputFormSteuerlotseStep.name)
            step.handle()
        self.assertEqual(expected_url, step.render_info.prev_url)

    @pytest.mark.usefixtures('test_request_context')
    def test_if_post_and_data_from_before_invalid_then_raise_incorrect_eligibility_data_error(self):
        with patch('app.model.recursive_data.RecursiveDataModel.one_previous_field_has_to_be_set',
                      MagicMock(side_effect=PreviousFieldsMissingError)):
            step = EligibilityStepChooser('eligibility').get_correct_step(
                InvestmentIncomeDecisionEligibilityInputFormSteuerlotseStep.name, True,
                form_data=ImmutableMultiDict({'investment_income_eligibility': 'yes'}))

            self.assertRaises(IncorrectEligibilityData, step.handle)

    def test_if_get_and_incorrect_data_from_session_then_delete_incorrect_data(self):
        session_data = {'marital_status_eligibility': 'single',
                        'separated_since_last_year_eligibility': 'no',
                        'joint_taxes_eligibility': 'no',
                        'alimony_eligibility': 'no',
                        'pension_eligibility': 'yes',
                        'investment_income_eligibility': 'no', }
        session_data_with_incorrect_key = {**session_data, **{'INCORRECT_KEY': 'UNNECESSARY_VALUE'}}
        with self.app.test_request_context(method='GET') as req:
            req.session = SecureCookieSession(
                {_ELIGIBILITY_DATA_KEY: create_session_form_data(session_data_with_incorrect_key)})
            step = EligibilityStepChooser('eligibility').get_correct_step(
                InvestmentIncomeDecisionEligibilityInputFormSteuerlotseStep.name, False, ImmutableMultiDict({}))
            step.handle()

            self.assertEqual(session_data,
                             FormStorage.deserialize_data(req.session[_ELIGIBILITY_DATA_KEY]))

    def test_if_get_and_correct_data_from_session_then_do_not_delete_any_data(self):
        session_data = {'marital_status_eligibility': 'single',
                        'separated_since_last_year_eligibility': 'no',
                        'joint_taxes_eligibility': 'no',
                        'alimony_eligibility': 'no',
                        'pension_eligibility': 'yes',
                        'investment_income_eligibility': 'no', }
        with self.app.test_request_context(method='GET') as req:
            req.session = SecureCookieSession({_ELIGIBILITY_DATA_KEY: create_session_form_data(session_data)})
            step = EligibilityStepChooser('eligibility').get_correct_step(
                InvestmentIncomeDecisionEligibilityInputFormSteuerlotseStep.name, False, ImmutableMultiDict({}))
            step.handle()

            self.assertEqual(session_data,
                             FormStorage.deserialize_data(req.session[_ELIGIBILITY_DATA_KEY]))

    def test_if_get_and_full_data_from_session_then_delete_unnecessary_data(self):
        only_necessary_data = {'marital_status_eligibility': 'single',
                               'separated_since_last_year_eligibility': 'no',
                               'separated_joint_taxes_eligibility': 'no',
                               'separated_lived_together_eligibility': 'no',
                               'joint_taxes_eligibility': 'no',
                               'alimony_eligibility': 'no',
                               'pension_eligibility': 'yes',
                               'investment_income_eligibility': 'no', }
        with self.app.test_request_context(method='GET') as req:
            req.session = SecureCookieSession({_ELIGIBILITY_DATA_KEY: create_session_form_data(FULL_SESSION_DATA)})
            step = EligibilityStepChooser('eligibility').get_correct_step(
                InvestmentIncomeDecisionEligibilityInputFormSteuerlotseStep.name, False, ImmutableMultiDict({}))
            step.handle()

            self.assertEqual(only_necessary_data,
                             FormStorage.deserialize_data(req.session[_ELIGIBILITY_DATA_KEY]))

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
                InvestmentIncomeDecisionEligibilityInputFormSteuerlotseStep.name, False, ImmutableMultiDict({}))
            step._pre_handle()

        self.assertEqual(expected_choices, step.render_info.form.investment_income_eligibility.choices)

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
                InvestmentIncomeDecisionEligibilityInputFormSteuerlotseStep.name, False, ImmutableMultiDict({}))
            step._pre_handle()

        self.assertEqual(expected_choices, step.render_info.form.investment_income_eligibility.choices)


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
        with self.app.test_request_context(method='POST') as req:
            req.session = SecureCookieSession(
                {_ELIGIBILITY_DATA_KEY: create_session_form_data(self.correct_session_data)})
            step = EligibilityStepChooser('eligibility').get_correct_step(
                MinimalInvestmentIncomeDecisionEligibilityInputFormSteuerlotseStep.name, True,
                form_data=ImmutableMultiDict({'minimal_investment_income_eligibility': 'yes'}))
            expected_url = step.url_for_step(EmploymentDecisionEligibilityInputFormSteuerlotseStep.name)
            step.handle()

        self.assertEqual(expected_url, step.render_info.next_url)

    def test_if_post_and_session_data_correct_and_input_data_incorrect_than_set_next_url_to_alternative_step(self):
        with self.app.test_request_context(method='POST') as req:
            req.session = SecureCookieSession(
                {_ELIGIBILITY_DATA_KEY: create_session_form_data(self.correct_session_data)})
            step = EligibilityStepChooser('eligibility').get_correct_step(
                MinimalInvestmentIncomeDecisionEligibilityInputFormSteuerlotseStep.name, True,
                form_data=ImmutableMultiDict({'minimal_investment_income_eligibility': 'no'}))
            expected_url = step.url_for_step(TaxedInvestmentIncomeDecisionEligibilityInputFormSteuerlotseStep.name)
            step.handle()

        self.assertEqual(expected_url, step.render_info.next_url)

    def test_if_session_data_correct_then_set_prev_input_step_correctly(self):
        with self.app.test_request_context(method='GET') as req:
            req.session = SecureCookieSession(
                {_ELIGIBILITY_DATA_KEY: create_session_form_data(self.correct_session_data)})
            step = EligibilityStepChooser('eligibility').get_correct_step(
                MinimalInvestmentIncomeDecisionEligibilityInputFormSteuerlotseStep.name, False, ImmutableMultiDict({}))
            expected_url = step.url_for_step(InvestmentIncomeDecisionEligibilityInputFormSteuerlotseStep.name)
            step.handle()
        self.assertEqual(expected_url, step.render_info.prev_url)

    @pytest.mark.usefixtures('test_request_context')
    def test_if_post_and_data_from_before_invalid_then_raise_incorrect_eligibility_data_error(self):
        with patch('app.model.recursive_data.RecursiveDataModel.one_previous_field_has_to_be_set',
                      MagicMock(side_effect=PreviousFieldsMissingError)):
            step = EligibilityStepChooser('eligibility').get_correct_step(
                MinimalInvestmentIncomeDecisionEligibilityInputFormSteuerlotseStep.name, True,
                form_data=ImmutableMultiDict({'investment_income_eligibility': 'yes',
                                              'minimal_investment_income_eligibility': 'no'}))

            self.assertRaises(IncorrectEligibilityData, step.handle)

    def test_if_get_and_incorrect_data_from_session_then_delete_incorrect_data(self):
        session_data = {'marital_status_eligibility': 'single',
                        'separated_since_last_year_eligibility': 'no',
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
                MinimalInvestmentIncomeDecisionEligibilityInputFormSteuerlotseStep.name, False, ImmutableMultiDict({}))
            step.handle()

            self.assertEqual(session_data,
                             FormStorage.deserialize_data(req.session[_ELIGIBILITY_DATA_KEY]))

    def test_if_get_and_correct_data_from_session_then_do_not_delete_any_data(self):
        session_data = {'marital_status_eligibility': 'single',
                        'separated_since_last_year_eligibility': 'no',
                        'joint_taxes_eligibility': 'no',
                        'alimony_eligibility': 'no',
                        'pension_eligibility': 'yes',
                        'investment_income_eligibility': 'no',
                        'minimal_investment_income_eligibility': 'yes'}
        with self.app.test_request_context(method='GET') as req:
            req.session = SecureCookieSession({_ELIGIBILITY_DATA_KEY: create_session_form_data(session_data)})
            step = EligibilityStepChooser('eligibility').get_correct_step(
                MinimalInvestmentIncomeDecisionEligibilityInputFormSteuerlotseStep.name, False, ImmutableMultiDict({}))
            step.handle()

            self.assertEqual(session_data,
                             FormStorage.deserialize_data(req.session[_ELIGIBILITY_DATA_KEY]))

    def test_if_get_and_full_data_from_session_then_delete_unnecessary_data(self):
        only_necessary_data = {'marital_status_eligibility': 'single',
                               'separated_since_last_year_eligibility': 'no',
                               'separated_lived_together_eligibility': 'no',
                               'separated_joint_taxes_eligibility': 'no',
                               'joint_taxes_eligibility': 'no',
                               'alimony_eligibility': 'no',
                               'pension_eligibility': 'yes',
                               'investment_income_eligibility': 'no',
                               'minimal_investment_income_eligibility': 'yes'}
        with self.app.test_request_context(method='GET') as req:
            req.session = SecureCookieSession({_ELIGIBILITY_DATA_KEY: create_session_form_data(FULL_SESSION_DATA)})
            step = EligibilityStepChooser('eligibility').get_correct_step(
                MinimalInvestmentIncomeDecisionEligibilityInputFormSteuerlotseStep.name, False, ImmutableMultiDict({}))
            step.handle()

            self.assertEqual(only_necessary_data,
                             FormStorage.deserialize_data(req.session[_ELIGIBILITY_DATA_KEY]))

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
                MinimalInvestmentIncomeDecisionEligibilityInputFormSteuerlotseStep.name, False, ImmutableMultiDict({}))
            step._pre_handle()

        self.assertEqual(expected_choices, step.render_info.form.minimal_investment_income_eligibility.choices)

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
                MinimalInvestmentIncomeDecisionEligibilityInputFormSteuerlotseStep.name, False, ImmutableMultiDict({}))
            step._pre_handle()

        self.assertEqual(expected_choices, step.render_info.form.minimal_investment_income_eligibility.choices)


class TestTaxedInvestmentIncomeEligibilityFailureDisplaySteuerlotseStep(unittest.TestCase):
    @pytest.fixture(autouse=True)
    def attach_fixtures(self, test_request_context):
        self.req = test_request_context

    def test_handle_sets_correct_prev_url(self):
        step = TaxedInvestmentIncomeEligibilityFailureDisplaySteuerlotseStep(
                endpoint='eligibility',
                render_info=TaxedInvestmentIncomeEligibilityFailureDisplaySteuerlotseStep.prepare_render_info(
                    {}))
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
        with self.app.test_request_context(method='POST') as req:
            req.session = SecureCookieSession(
                {_ELIGIBILITY_DATA_KEY: create_session_form_data(self.correct_session_data)})
            step = EligibilityStepChooser('eligibility').get_correct_step(
                TaxedInvestmentIncomeDecisionEligibilityInputFormSteuerlotseStep.name, True,
                form_data=ImmutableMultiDict({'taxed_investment_income_eligibility': 'yes'}))
            expected_url = step.url_for_step(CheaperCheckDecisionEligibilityInputFormSteuerlotseStep.name)
            step.handle()

        self.assertEqual(expected_url, step.render_info.next_url)

    def test_if_post_and_session_data_correct_and_input_data_incorrect_than_set_next_url_to_alternative_step(self):
        with self.app.test_request_context(method='POST') as req:
            req.session = SecureCookieSession(
                {_ELIGIBILITY_DATA_KEY: create_session_form_data(self.correct_session_data)})
            step = EligibilityStepChooser('eligibility').get_correct_step(
                TaxedInvestmentIncomeDecisionEligibilityInputFormSteuerlotseStep.name, True,
                form_data=ImmutableMultiDict({'taxed_investment_income_eligibility': 'no'}))
            expected_url = step.url_for_step(TaxedInvestmentIncomeEligibilityFailureDisplaySteuerlotseStep.name)
            step.handle()

        self.assertEqual(expected_url, step.render_info.next_url)

    def test_if_session_data_correct_then_set_prev_input_step_correctly(self):
        with self.app.test_request_context(method='GET') as req:
            req.session = SecureCookieSession(
                {_ELIGIBILITY_DATA_KEY: create_session_form_data(self.correct_session_data)})
            step = EligibilityStepChooser('eligibility').get_correct_step(
                TaxedInvestmentIncomeDecisionEligibilityInputFormSteuerlotseStep.name, False, ImmutableMultiDict({}))
            expected_url = step.url_for_step(MinimalInvestmentIncomeDecisionEligibilityInputFormSteuerlotseStep.name)
            step.handle()
        self.assertEqual(expected_url, step.render_info.prev_url)

    @pytest.mark.usefixtures('test_request_context')
    def test_if_post_and_data_from_before_invalid_then_raise_incorrect_eligibility_data_error(self):
        with patch('app.model.recursive_data.RecursiveDataModel.one_previous_field_has_to_be_set',
                      MagicMock(side_effect=PreviousFieldsMissingError)):
            step = EligibilityStepChooser('eligibility').get_correct_step(
                TaxedInvestmentIncomeDecisionEligibilityInputFormSteuerlotseStep.name, True,
                form_data=ImmutableMultiDict({'taxed_investment_income_eligibility': 'yes'}))

            self.assertRaises(IncorrectEligibilityData, step.handle)

    def test_if_get_and_incorrect_data_from_session_then_delete_incorrect_data(self):
        session_data = {'marital_status_eligibility': 'single',
                        'separated_since_last_year_eligibility': 'no',
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
                TaxedInvestmentIncomeDecisionEligibilityInputFormSteuerlotseStep.name, False, ImmutableMultiDict({}))
            step.handle()

            self.assertEqual(session_data,
                             FormStorage.deserialize_data(req.session[_ELIGIBILITY_DATA_KEY]))

    def test_if_get_and_correct_data_from_session_then_do_not_delete_any_data(self):
        session_data = {'marital_status_eligibility': 'single',
                        'separated_since_last_year_eligibility': 'no',
                        'joint_taxes_eligibility': 'no',
                        'alimony_eligibility': 'no',
                        'pension_eligibility': 'yes',
                        'investment_income_eligibility': 'no',
                        'minimal_investment_income_eligibility': 'yes',
                        'taxed_investment_income_eligibility': 'no'}
        with self.app.test_request_context(method='GET') as req:
            req.session = SecureCookieSession({_ELIGIBILITY_DATA_KEY: create_session_form_data(session_data)})
            step = EligibilityStepChooser('eligibility').get_correct_step(
                TaxedInvestmentIncomeDecisionEligibilityInputFormSteuerlotseStep.name, False, ImmutableMultiDict({}))
            step.handle()

            self.assertEqual(session_data,
                             FormStorage.deserialize_data(req.session[_ELIGIBILITY_DATA_KEY]))

    def test_if_get_and_full_data_from_session_then_delete_unnecessary_data(self):
        only_necessary_data = {'marital_status_eligibility': 'single',
                               'separated_since_last_year_eligibility': 'no',
                               'separated_lived_together_eligibility': 'no',
                               'separated_joint_taxes_eligibility': 'no',
                               'joint_taxes_eligibility': 'no',
                               'alimony_eligibility': 'no',
                               'pension_eligibility': 'yes',
                               'investment_income_eligibility': 'no',
                               'minimal_investment_income_eligibility': 'yes',
                               'taxed_investment_income_eligibility': 'no'}
        with self.app.test_request_context(method='GET') as req:
            req.session = SecureCookieSession({_ELIGIBILITY_DATA_KEY: create_session_form_data(FULL_SESSION_DATA)})
            step = EligibilityStepChooser('eligibility').get_correct_step(
                TaxedInvestmentIncomeDecisionEligibilityInputFormSteuerlotseStep.name, False, ImmutableMultiDict({}))
            step.handle()

            self.assertEqual(only_necessary_data,
                             FormStorage.deserialize_data(req.session[_ELIGIBILITY_DATA_KEY]))


class TestCheaperCheckEligibilityFailureDisplaySteuerlotseStep(unittest.TestCase):
    @pytest.fixture(autouse=True)
    def attach_fixtures(self, test_request_context):
        self.req = test_request_context

    def test_handle_sets_correct_prev_url(self):
        step = CheaperCheckEligibilityFailureDisplaySteuerlotseStep(
                endpoint='eligibility',
                render_info=CheaperCheckEligibilityFailureDisplaySteuerlotseStep.prepare_render_info(
                    {}))
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
        with self.app.test_request_context(method='POST') as req:
            req.session = SecureCookieSession(
                {_ELIGIBILITY_DATA_KEY: create_session_form_data(self.correct_session_data)})
            step = EligibilityStepChooser('eligibility').get_correct_step(
                CheaperCheckDecisionEligibilityInputFormSteuerlotseStep.name, True,
                form_data=ImmutableMultiDict({'cheaper_check_eligibility': 'no'}))
            expected_url = step.url_for_step(EmploymentDecisionEligibilityInputFormSteuerlotseStep.name)
            step.handle()

        self.assertEqual(expected_url, step.render_info.next_url)

    def test_if_post_and_session_data_correct_and_input_data_incorrect_than_set_next_url_to_alternative_step(self):
        with self.app.test_request_context(method='POST') as req:
            req.session = SecureCookieSession(
                {_ELIGIBILITY_DATA_KEY: create_session_form_data(self.correct_session_data)})
            step = EligibilityStepChooser('eligibility').get_correct_step(
                CheaperCheckDecisionEligibilityInputFormSteuerlotseStep.name, True,
                form_data=ImmutableMultiDict({'cheaper_check_eligibility': 'yes'}))
            expected_url = step.url_for_step(CheaperCheckEligibilityFailureDisplaySteuerlotseStep.name)
            step.handle()

        self.assertEqual(expected_url, step.render_info.next_url)

    def test_if_session_data_correct_then_set_prev_input_step_correctly(self):
        with self.app.test_request_context(method='GET') as req:
            req.session = SecureCookieSession(
                {_ELIGIBILITY_DATA_KEY: create_session_form_data(self.correct_session_data)})
            step = EligibilityStepChooser('eligibility').get_correct_step(
                CheaperCheckDecisionEligibilityInputFormSteuerlotseStep.name, False, ImmutableMultiDict({}))
            expected_url = step.url_for_step(TaxedInvestmentIncomeDecisionEligibilityInputFormSteuerlotseStep.name)
            step.handle()
        self.assertEqual(expected_url, step.render_info.prev_url)

    @pytest.mark.usefixtures('test_request_context')
    def test_if_post_and_data_from_before_invalid_then_raise_incorrect_eligibility_data_error(self):
        with patch('app.model.recursive_data.RecursiveDataModel.one_previous_field_has_to_be_set',
                      MagicMock(side_effect=PreviousFieldsMissingError)):
            step = EligibilityStepChooser('eligibility').get_correct_step(
                CheaperCheckDecisionEligibilityInputFormSteuerlotseStep.name, True,
                form_data=ImmutableMultiDict({'cheaper_check_eligibility': 'no'}))

            self.assertRaises(IncorrectEligibilityData, step.handle)

    def test_if_get_and_incorrect_data_from_session_then_delete_incorrect_data(self):
        session_data = {'alimony_eligibility': 'no',
                        'cheaper_check_eligibility': 'no',
                        'investment_income_eligibility': 'no',
                        'joint_taxes_eligibility': 'no',
                        'marital_status_eligibility': 'single',
                        'minimal_investment_income_eligibility': 'yes',
                        'pension_eligibility': 'yes',
                        'separated_since_last_year_eligibility': 'no',
                        'taxed_investment_income_eligibility': 'no',}
        session_data_with_incorrect_key = {**session_data, **{'INCORRECT_KEY': 'UNNECESSARY_VALUE'}}
        with self.app.test_request_context(method='GET') as req:
            req.session = SecureCookieSession(
                {_ELIGIBILITY_DATA_KEY: create_session_form_data(session_data_with_incorrect_key)})
            step = EligibilityStepChooser('eligibility').get_correct_step(
                CheaperCheckDecisionEligibilityInputFormSteuerlotseStep.name, False, ImmutableMultiDict({}))
            step.handle()

            self.assertEqual(session_data,
                             FormStorage.deserialize_data(req.session[_ELIGIBILITY_DATA_KEY]))

    def test_if_get_and_correct_data_from_session_then_do_not_delete_any_data(self):
        session_data = {'alimony_eligibility': 'no',
                        'cheaper_check_eligibility': 'no', 
                        'investment_income_eligibility': 'no',
                        'joint_taxes_eligibility': 'no',
                        'marital_status_eligibility': 'single',
                        'minimal_investment_income_eligibility': 'yes',
                        'pension_eligibility': 'yes',
                        'separated_since_last_year_eligibility': 'no',
                        'taxed_investment_income_eligibility': 'no',
                        }
        with self.app.test_request_context(method='GET') as req:
            req.session = SecureCookieSession({_ELIGIBILITY_DATA_KEY: create_session_form_data(session_data)})
            step = EligibilityStepChooser('eligibility').get_correct_step(
                CheaperCheckDecisionEligibilityInputFormSteuerlotseStep.name, False, ImmutableMultiDict({}))
            step.handle()

            self.assertEqual(session_data,
                             FormStorage.deserialize_data(req.session[_ELIGIBILITY_DATA_KEY]))

    def test_if_get_and_full_data_from_session_then_delete_unnecessary_data(self):
        only_necessary_data = {'marital_status_eligibility': 'single',
                               'separated_since_last_year_eligibility': 'no',
                               'separated_lived_together_eligibility': 'no',
                               'separated_joint_taxes_eligibility': 'no',
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
                CheaperCheckDecisionEligibilityInputFormSteuerlotseStep.name, False, ImmutableMultiDict({}))
            step.handle()

            self.assertEqual(only_necessary_data,
                             FormStorage.deserialize_data(req.session[_ELIGIBILITY_DATA_KEY]))

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
                CheaperCheckDecisionEligibilityInputFormSteuerlotseStep.name, False, ImmutableMultiDict({}))
            step._pre_handle()

        self.assertEqual(expected_choices, step.render_info.form.cheaper_check_eligibility.choices)

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
                CheaperCheckDecisionEligibilityInputFormSteuerlotseStep.name, False, ImmutableMultiDict({}))
            step._pre_handle()

        self.assertEqual(expected_choices, step.render_info.form.cheaper_check_eligibility.choices)


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
        with self.app.test_request_context(method='POST') as req:
            req.session = SecureCookieSession(
                {_ELIGIBILITY_DATA_KEY: create_session_form_data(self.correct_session_data)})
            step = EligibilityStepChooser('eligibility').get_correct_step(
                EmploymentDecisionEligibilityInputFormSteuerlotseStep.name, True,
                form_data=ImmutableMultiDict({'employment_income_eligibility': 'no'}))
            expected_url = step.url_for_step(IncomeOtherDecisionEligibilityInputFormSteuerlotseStep.name)
            step.handle()

        self.assertEqual(expected_url, step.render_info.next_url)

    def test_if_post_and_session_data_correct_and_input_data_incorrect_than_set_next_url_to_alternative_step(self):
        with self.app.test_request_context(method='POST') as req:
            req.session = SecureCookieSession(
                {_ELIGIBILITY_DATA_KEY: create_session_form_data(self.correct_session_data)})
            step = EligibilityStepChooser('eligibility').get_correct_step(
                EmploymentDecisionEligibilityInputFormSteuerlotseStep.name, True,
                form_data=ImmutableMultiDict({'employment_income_eligibility': 'yes'}))
            expected_url = step.url_for_step(MarginalEmploymentIncomeDecisionEligibilityInputFormSteuerlotseStep.name)
            step.handle()

        self.assertEqual(expected_url, step.render_info.next_url)

    def test_if_incomes_but_no_cheaper_check_session_data_correct_then_set_prev_input_step_correctly(self):
        with self.app.test_request_context(method='GET') as req:
            req.session = SecureCookieSession(
                {_ELIGIBILITY_DATA_KEY: create_session_form_data(self.correct_session_data)})
            step = EligibilityStepChooser('eligibility').get_correct_step(
                EmploymentDecisionEligibilityInputFormSteuerlotseStep.name, False, ImmutableMultiDict({}))
            expected_url = step.url_for_step(CheaperCheckDecisionEligibilityInputFormSteuerlotseStep.name)
            step.handle()
        self.assertEqual(expected_url, step.render_info.prev_url)

    def test_if_incomes_but_minimal_investment_session_data_correct_then_set_prev_input_step_correctly(self):
        alternative_data = {**self.correct_session_data.copy(), **{'minimal_investment_income_eligibility': 'yes'}}
        with self.app.test_request_context(method='GET') as req:
            req.session = SecureCookieSession({_ELIGIBILITY_DATA_KEY: create_session_form_data(alternative_data)})
            step = EligibilityStepChooser('eligibility').get_correct_step(
                EmploymentDecisionEligibilityInputFormSteuerlotseStep.name, False, ImmutableMultiDict({}))
            expected_url = step.url_for_step(MinimalInvestmentIncomeDecisionEligibilityInputFormSteuerlotseStep.name)
            step.handle()
        self.assertEqual(expected_url, step.render_info.prev_url)

    def test_if_no_incomes_session_data_correct_then_set_prev_input_step_correctly(self):
        alternative_data = {**self.correct_session_data.copy(), **{'investment_income_eligibility': 'no'}}
        with self.app.test_request_context(method='GET') as req:
            req.session = SecureCookieSession({_ELIGIBILITY_DATA_KEY: create_session_form_data(alternative_data)})
            step = EligibilityStepChooser('eligibility').get_correct_step(
                EmploymentDecisionEligibilityInputFormSteuerlotseStep.name, False, ImmutableMultiDict({}))
            expected_url = step.url_for_step(InvestmentIncomeDecisionEligibilityInputFormSteuerlotseStep.name)
            step.handle()
        self.assertEqual(expected_url, step.render_info.prev_url)

    @pytest.mark.usefixtures('test_request_context')
    def test_if_post_and_data_from_before_invalid_then_raise_incorrect_eligibility_data_error(self):
        with patch('app.model.recursive_data.RecursiveDataModel.one_previous_field_has_to_be_set',
                      MagicMock(side_effect=PreviousFieldsMissingError)):
            step = EligibilityStepChooser('eligibility').get_correct_step(
                EmploymentDecisionEligibilityInputFormSteuerlotseStep.name, True,
                form_data=ImmutableMultiDict({'employment_income_eligibility': 'no'}))

            self.assertRaises(IncorrectEligibilityData, step.handle)

    def test_if_get_and_incorrect_data_from_session_then_delete_incorrect_data(self):
        session_data = {'marital_status_eligibility': 'single',
                        'separated_since_last_year_eligibility': 'no',
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
                EmploymentDecisionEligibilityInputFormSteuerlotseStep.name, False, ImmutableMultiDict({}))
            step.handle()

            self.assertEqual(session_data,
                             FormStorage.deserialize_data(req.session[_ELIGIBILITY_DATA_KEY]))

    def test_if_get_and_correct_data_from_session_then_do_not_delete_any_data(self):
        session_data = {'marital_status_eligibility': 'single',
                        'separated_since_last_year_eligibility': 'no',
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
                EmploymentDecisionEligibilityInputFormSteuerlotseStep.name, False, ImmutableMultiDict({}))
            step.handle()

            self.assertEqual(session_data,
                             FormStorage.deserialize_data(req.session[_ELIGIBILITY_DATA_KEY]))

    def test_if_get_and_full_data_from_session_then_delete_unnecessary_data(self):
        only_necessary_data = {'marital_status_eligibility': 'single',
                               'separated_since_last_year_eligibility': 'no',
                               'separated_lived_together_eligibility': 'no',
                               'separated_joint_taxes_eligibility': 'no',
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
                EmploymentDecisionEligibilityInputFormSteuerlotseStep.name, False, ImmutableMultiDict({}))
            step.handle()

            self.assertEqual(only_necessary_data,
                             FormStorage.deserialize_data(req.session[_ELIGIBILITY_DATA_KEY]))

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
                EmploymentDecisionEligibilityInputFormSteuerlotseStep.name, False, ImmutableMultiDict({}))
            step._pre_handle()

        self.assertEqual(expected_choices, step.render_info.form.employment_income_eligibility.choices)

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
                EmploymentDecisionEligibilityInputFormSteuerlotseStep.name, False, ImmutableMultiDict({}))
            step._pre_handle()

        self.assertEqual(expected_choices, step.render_info.form.employment_income_eligibility.choices)


class TestMarginalEmploymentIncomeEligibilityFailureDisplaySteuerlotseStep(unittest.TestCase):
    @pytest.fixture(autouse=True)
    def attach_fixtures(self, test_request_context):
        self.req = test_request_context

    def test_handle_sets_correct_prev_url(self):
        step = MarginalEmploymentIncomeEligibilityFailureDisplaySteuerlotseStep(
                endpoint='eligibility',
                render_info=MarginalEmploymentIncomeEligibilityFailureDisplaySteuerlotseStep.prepare_render_info(
                    {}))
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
        with self.app.test_request_context(method='POST') as req:
            req.session = SecureCookieSession(
                {_ELIGIBILITY_DATA_KEY: create_session_form_data(self.correct_session_data)})
            step = EligibilityStepChooser('eligibility').get_correct_step(
                MarginalEmploymentIncomeDecisionEligibilityInputFormSteuerlotseStep.name, True,
                form_data=ImmutableMultiDict({'marginal_employment_eligibility': 'yes'}))
            expected_url = step.url_for_step(IncomeOtherDecisionEligibilityInputFormSteuerlotseStep.name)
            step.handle()

        self.assertEqual(expected_url, step.render_info.next_url)

    def test_if_session_data_correct_then_set_prev_input_step_correctly(self):
        with self.app.test_request_context(method='GET') as req:
            req.session = SecureCookieSession(
                {_ELIGIBILITY_DATA_KEY: create_session_form_data(self.correct_session_data)})
            step = EligibilityStepChooser('eligibility').get_correct_step(
                MarginalEmploymentIncomeDecisionEligibilityInputFormSteuerlotseStep.name, False, ImmutableMultiDict({}))
            expected_url = step.url_for_step(EmploymentDecisionEligibilityInputFormSteuerlotseStep.name)
            step.handle()

        self.assertEqual(expected_url, step.render_info.prev_url)

    def test_if_post_and_session_data_correct_and_input_data_incorrect_than_set_next_url_to_alternative_step(self):
        with self.app.test_request_context(method='POST') as req:
            req.session = SecureCookieSession(
                {_ELIGIBILITY_DATA_KEY: create_session_form_data(self.correct_session_data)})
            step = EligibilityStepChooser('eligibility').get_correct_step(
                MarginalEmploymentIncomeDecisionEligibilityInputFormSteuerlotseStep.name, True,
                form_data=ImmutableMultiDict({'marginal_employment_eligibility': 'no'}))
            expected_url = step.url_for_step(MarginalEmploymentIncomeEligibilityFailureDisplaySteuerlotseStep.name)
            step.handle()

        self.assertEqual(expected_url, step.render_info.next_url)

    @pytest.mark.usefixtures('test_request_context')
    def test_if_post_and_data_from_before_invalid_then_raise_incorrect_eligibility_data_error(self):
        with patch('app.model.recursive_data.RecursiveDataModel.one_previous_field_has_to_be_set',
                      MagicMock(side_effect=PreviousFieldsMissingError)):
            step = EligibilityStepChooser('eligibility').get_correct_step(
                MarginalEmploymentIncomeDecisionEligibilityInputFormSteuerlotseStep.name, True,
                form_data=ImmutableMultiDict({'marginal_employment_eligibility': 'yes'}))

            self.assertRaises(IncorrectEligibilityData, step.handle)

    def test_if_get_and_incorrect_data_from_session_then_delete_incorrect_data(self):
        session_data = {'marital_status_eligibility': 'single',
                        'separated_since_last_year_eligibility': 'no',
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
                MarginalEmploymentIncomeDecisionEligibilityInputFormSteuerlotseStep.name, False, ImmutableMultiDict({}))
            step.handle()

            self.assertEqual(session_data,
                             FormStorage.deserialize_data(req.session[_ELIGIBILITY_DATA_KEY]))

    def test_if_get_and_correct_data_from_session_then_do_not_delete_any_data(self):
        session_data = {'marital_status_eligibility': 'single',
                        'separated_since_last_year_eligibility': 'no',
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
                MarginalEmploymentIncomeDecisionEligibilityInputFormSteuerlotseStep.name, False, ImmutableMultiDict({}))
            step.handle()

            self.assertEqual(session_data,
                             FormStorage.deserialize_data(req.session[_ELIGIBILITY_DATA_KEY]))

    def test_if_get_and_full_data_from_session_then_delete_unnecessary_data(self):
        only_necessary_data = {'marital_status_eligibility': 'single',
                               'separated_since_last_year_eligibility': 'no',
                               'separated_lived_together_eligibility': 'no',
                               'separated_joint_taxes_eligibility': 'no',
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
                MarginalEmploymentIncomeDecisionEligibilityInputFormSteuerlotseStep.name, False, ImmutableMultiDict({}))
            step.handle()

            self.assertEqual(only_necessary_data,
                             FormStorage.deserialize_data(req.session[_ELIGIBILITY_DATA_KEY]))


class TestIncomeOtherEligibilityFailureDisplaySteuerlotseStep(unittest.TestCase):
    @pytest.fixture(autouse=True)
    def attach_fixtures(self, test_request_context):
        self.req = test_request_context

    def test_handle_sets_correct_prev_url(self):
        step = IncomeOtherEligibilityFailureDisplaySteuerlotseStep(
                endpoint='eligibility',
                render_info=IncomeOtherEligibilityFailureDisplaySteuerlotseStep.prepare_render_info(
                    {}))
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
        with self.app.test_request_context(method='POST') as req:
            req.session = SecureCookieSession(
                {_ELIGIBILITY_DATA_KEY: create_session_form_data(self.correct_session_data)})
            step = EligibilityStepChooser('eligibility').get_correct_step(
                IncomeOtherDecisionEligibilityInputFormSteuerlotseStep.name, True,
                form_data=ImmutableMultiDict({'other_income_eligibility': 'no'}))
            expected_url = step.url_for_step(ForeignCountriesDecisionEligibilityInputFormSteuerlotseStep.name)
            step.handle()

        self.assertEqual(expected_url, step.render_info.next_url)

    def test_if_post_and_session_data_correct_and_input_data_incorrect_than_set_next_url_to_alternative_step(self):
        with self.app.test_request_context(method='POST') as req:
            req.session = SecureCookieSession(
                {_ELIGIBILITY_DATA_KEY: create_session_form_data(self.correct_session_data)})
            step = EligibilityStepChooser('eligibility').get_correct_step(
                IncomeOtherDecisionEligibilityInputFormSteuerlotseStep.name, True,
                form_data=ImmutableMultiDict({'other_income_eligibility': 'yes'}))
            expected_url = step.url_for_step(IncomeOtherEligibilityFailureDisplaySteuerlotseStep.name)
            step.handle()

        self.assertEqual(expected_url, step.render_info.next_url)

    def test_if_no_employment_income_session_data_correct_then_set_prev_url_correct(self):
        with self.app.test_request_context(method='GET') as req:
            req.session = SecureCookieSession(
                {_ELIGIBILITY_DATA_KEY: create_session_form_data(self.correct_session_data)})
            step = EligibilityStepChooser('eligibility').get_correct_step(
                IncomeOtherDecisionEligibilityInputFormSteuerlotseStep.name, False, ImmutableMultiDict({}))
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
                IncomeOtherDecisionEligibilityInputFormSteuerlotseStep.name, False, ImmutableMultiDict({}))
            expected_url = step.url_for_step(MarginalEmploymentIncomeDecisionEligibilityInputFormSteuerlotseStep.name)
            step.handle()

        self.assertEqual(expected_url, step.render_info.prev_url)

    @pytest.mark.usefixtures('test_request_context')
    def test_if_post_and_data_from_before_invalid_then_raise_incorrect_eligibility_data_error(self):
        with patch('app.model.recursive_data.RecursiveDataModel.one_previous_field_has_to_be_set',
                      MagicMock(side_effect=PreviousFieldsMissingError)):
            step = EligibilityStepChooser('eligibility').get_correct_step(
                IncomeOtherDecisionEligibilityInputFormSteuerlotseStep.name, True,
                form_data=ImmutableMultiDict({'other_income_eligibility': 'no'}))

            self.assertRaises(IncorrectEligibilityData, step.handle)

    def test_if_get_and_incorrect_data_from_session_then_delete_incorrect_data(self):
        session_data = {'marital_status_eligibility': 'single',
                        'separated_since_last_year_eligibility': 'no',
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
                IncomeOtherDecisionEligibilityInputFormSteuerlotseStep.name, False, ImmutableMultiDict({}))
            step.handle()

            self.assertEqual(session_data,
                             FormStorage.deserialize_data(req.session[_ELIGIBILITY_DATA_KEY]))

    def test_if_get_and_correct_data_from_session_then_do_not_delete_any_data(self):
        with self.app.test_request_context(method='GET') as req:
            req.session = SecureCookieSession(
                {_ELIGIBILITY_DATA_KEY: create_session_form_data(self.correct_session_data)})
            step = EligibilityStepChooser('eligibility').get_correct_step(
                IncomeOtherDecisionEligibilityInputFormSteuerlotseStep.name, False, ImmutableMultiDict({}))
            step.handle()

            self.assertEqual(self.correct_session_data,
                             FormStorage.deserialize_data(req.session[_ELIGIBILITY_DATA_KEY]))

    def test_if_get_and_full_data_from_session_then_delete_unnecessary_data(self):
        only_necessary_data = {'marital_status_eligibility': 'single',
                               'separated_since_last_year_eligibility': 'no',
                               'separated_lived_together_eligibility': 'no',
                               'separated_joint_taxes_eligibility': 'no',
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
                IncomeOtherDecisionEligibilityInputFormSteuerlotseStep.name, False, ImmutableMultiDict({}))
            step.handle()

            self.assertEqual(only_necessary_data,
                             FormStorage.deserialize_data(req.session[_ELIGIBILITY_DATA_KEY]))

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
                IncomeOtherDecisionEligibilityInputFormSteuerlotseStep.name, False, ImmutableMultiDict({}))
            step._pre_handle()

        self.assertEqual(expected_choices, step.render_info.form.other_income_eligibility.choices)

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
                IncomeOtherDecisionEligibilityInputFormSteuerlotseStep.name, False, ImmutableMultiDict({}))
            step._pre_handle()

        self.assertEqual(expected_choices, step.render_info.form.other_income_eligibility.choices)


class TestForeignCountriesEligibilityFailureDisplaySteuerlotseStep(unittest.TestCase):
    @pytest.fixture(autouse=True)
    def attach_fixtures(self, test_request_context):
        self.req = test_request_context

    def test_handle_sets_correct_prev_url(self):
        step = ForeignCountriesEligibilityFailureDisplaySteuerlotseStep(
                endpoint='eligibility',
                render_info=ForeignCountriesEligibilityFailureDisplaySteuerlotseStep.prepare_render_info(
                    {}))
        expected_url = step.url_for_step(ForeignCountriesDecisionEligibilityInputFormSteuerlotseStep.name)
        step.handle()

        self.assertEqual(expected_url, step.render_info.prev_url)


class TestForeignCountriesDecisionEligibilityInputFormSteuerlotseStep:
    @pytest.fixture
    def correct_session_data(self):
        correct_session_data = {
            'marital_status_eligibility': 'divorced', 'joint_taxes_eligibility': 'no', 'alimony_eligibility': 'no',
            'user_a_has_elster_account_eligibility': 'no', 'pension_eligibility': 'yes',
            'investment_income_eligibility': 'yes', 'minimal_investment_income_eligibility': 'no',
            'taxed_investment_income_eligibility': 'yes', 'cheaper_check_eligibility': 'no',
            'employment_income_eligibility': 'yes', 'marginal_employment_eligibility': 'yes',
            'other_income_eligibility': 'no'}
        return correct_session_data
    
    @pytest.fixture
    def correct_session_data_users_have_elster(self):
        correct_session_data = {
            'marital_status_eligibility': 'divorced', 'joint_taxes_eligibility': 'no', 'alimony_eligibility': 'no',
            'user_a_has_elster_account_eligibility': 'yes', 'user_b_has_elster_account_eligibility': 'yes',
            'pension_eligibility': 'yes', 'investment_income_eligibility': 'yes', 'minimal_investment_income_eligibility': 'no',
            'taxed_investment_income_eligibility': 'yes', 'cheaper_check_eligibility': 'no',
            'employment_income_eligibility': 'yes', 'marginal_employment_eligibility': 'yes',
            'other_income_eligibility': 'no'}
        return correct_session_data
        
    @pytest.fixture
    def correct_session_data_user_a_have_elster(self):
        correct_session_data = {
            'marital_status_eligibility': 'divorced', 'joint_taxes_eligibility': 'no', 'alimony_eligibility': 'no',
            'user_a_has_elster_account_eligibility': 'yes', 'user_b_has_elster_account_eligibility': 'no',
            'pension_eligibility': 'yes', 'investment_income_eligibility': 'yes', 'minimal_investment_income_eligibility': 'no',
            'taxed_investment_income_eligibility': 'yes', 'cheaper_check_eligibility': 'no',
            'employment_income_eligibility': 'yes', 'marginal_employment_eligibility': 'yes',
            'other_income_eligibility': 'no'}
        return correct_session_data
    
    @pytest.fixture
    def correct_session_data_single_user_a_have_elster(self):
        correct_session_data = {
            'marital_status_eligibility': 'single', 'joint_taxes_eligibility': 'yes', 'alimony_eligibility': 'no',
            'user_a_has_elster_account_eligibility': 'yes', 'pension_eligibility': 'yes', 
            'investment_income_eligibility': 'yes', 'minimal_investment_income_eligibility': 'no',
            'taxed_investment_income_eligibility': 'yes', 'cheaper_check_eligibility': 'no',
            'employment_income_eligibility': 'yes', 'marginal_employment_eligibility': 'yes',
            'other_income_eligibility': 'no'}
        return correct_session_data
    
    
    def test_if_post_and_session_data_correct_and_input_data_correct_then_set_success_step(self, app, correct_session_data):
        with app.test_request_context(method='POST') as req:
            req.session = SecureCookieSession(
                {_ELIGIBILITY_DATA_KEY: create_session_form_data(correct_session_data)})
            step = EligibilityStepChooser('eligibility').get_correct_step(
                ForeignCountriesDecisionEligibilityInputFormSteuerlotseStep.name, True,
                form_data=ImmutableMultiDict({'foreign_country_eligibility': 'no'}))
            expected_url = step.url_for_step(EligibilitySuccessDisplaySteuerlotseStep.name)
            step.handle()

        assert step.render_info.next_url == expected_url
                
    def test_if_post_and_session_data_correct_and_user_a_has_elster_and_input_data_correct_then_set_success_step(self, app, correct_session_data_user_a_have_elster):
        with app.test_request_context(method='POST') as req:
            req.session = SecureCookieSession(
                {_ELIGIBILITY_DATA_KEY: create_session_form_data(correct_session_data_user_a_have_elster)})
            step = EligibilityStepChooser('eligibility').get_correct_step(
                ForeignCountriesDecisionEligibilityInputFormSteuerlotseStep.name, True,
                form_data=ImmutableMultiDict({'foreign_country_eligibility': 'no'}))
            expected_url = step.url_for_step(EligibilitySuccessDisplaySteuerlotseStep.name)
            step.handle()

        assert step.render_info.next_url == expected_url

    def test_if_post_and_session_data_correct_and_input_data_incorrect_then_set_next_url_to_failure_step(self, app, correct_session_data):
        with app.test_request_context(method='POST') as req:
            req.session = SecureCookieSession(
                {_ELIGIBILITY_DATA_KEY: create_session_form_data(correct_session_data)})
            step = EligibilityStepChooser('eligibility').get_correct_step(
                ForeignCountriesDecisionEligibilityInputFormSteuerlotseStep.name, True,
                ImmutableMultiDict({'foreign_country_eligibility': 'yes'}))
            expected_url = step.url_for_step(ForeignCountriesEligibilityFailureDisplaySteuerlotseStep.name)
            step.handle()

        assert step.render_info.next_url == expected_url

    def test_if_session_data_correct_then_set_prev_input_step_correctly(self, app, correct_session_data):
        with app.test_request_context(method='GET') as req:
            req.session = SecureCookieSession(
                {_ELIGIBILITY_DATA_KEY: create_session_form_data(correct_session_data)})
            step = EligibilityStepChooser('eligibility').get_correct_step(
                ForeignCountriesDecisionEligibilityInputFormSteuerlotseStep.name, False, ImmutableMultiDict({}))
            expected_url = step.url_for_step(IncomeOtherDecisionEligibilityInputFormSteuerlotseStep.name)
            step.handle()

        assert step.render_info.prev_url == expected_url

    def test_if_post_and_data_from_before_invalid_then_raise_incorrect_eligibility_data_error(self, app):
        with app.test_request_context(method='POST'), \
                patch('app.model.recursive_data.RecursiveDataModel.one_previous_field_has_to_be_set',
                      MagicMock(side_effect=PreviousFieldsMissingError)):
            step = EligibilityStepChooser('eligibility').get_correct_step(
                ForeignCountriesDecisionEligibilityInputFormSteuerlotseStep.name, True,
                form_data=ImmutableMultiDict({'other_income_eligibility': 'no',
                                              'foreign_country_eligibility': 'no'}))

            with pytest.raises(IncorrectEligibilityData):
                step.handle()

    def test_if_get_and_incorrect_data_from_session_then_delete_incorrect_data(self, app):
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
        with app.test_request_context(method='GET') as req:
            req.session = SecureCookieSession(
                {_ELIGIBILITY_DATA_KEY: create_session_form_data(session_data_with_incorrect_key)})
            step = EligibilityStepChooser('eligibility').get_correct_step(
                ForeignCountriesDecisionEligibilityInputFormSteuerlotseStep.name, False, ImmutableMultiDict({}))
            step.handle()

            assert FormStorage.deserialize_data(req.session[_ELIGIBILITY_DATA_KEY]) == session_data

    def test_if_get_and_correct_data_from_session_then_do_not_delete_any_data(self, app, correct_session_data):
        with app.test_request_context(method='GET') as req:
            req.session = SecureCookieSession(
                {_ELIGIBILITY_DATA_KEY: create_session_form_data(correct_session_data)})
            step = EligibilityStepChooser('eligibility').get_correct_step(
                ForeignCountriesDecisionEligibilityInputFormSteuerlotseStep.name, False, ImmutableMultiDict({}))
            step.handle()

            assert FormStorage.deserialize_data(req.session[_ELIGIBILITY_DATA_KEY]) == correct_session_data

    def test_if_get_and_full_data_from_session_then_delete_no_data(self, app):
        with app.test_request_context(method='GET') as req:
            req.session = SecureCookieSession({_ELIGIBILITY_DATA_KEY: create_session_form_data(FULL_SESSION_DATA)})
            step = EligibilityStepChooser('eligibility').get_correct_step(
                ForeignCountriesDecisionEligibilityInputFormSteuerlotseStep.name, False, ImmutableMultiDict({}))
            step.handle()

            assert FormStorage.deserialize_data(req.session[_ELIGIBILITY_DATA_KEY]) == FULL_SESSION_DATA

    def test_if_multiple_users_then_show_multiple_text(self, app):
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
        with app.test_request_context(method='GET') as req:
            req.session = SecureCookieSession({_ELIGIBILITY_DATA_KEY: create_session_form_data(session_data)})
            step = EligibilityStepChooser('eligibility').get_correct_step(
                ForeignCountriesDecisionEligibilityInputFormSteuerlotseStep.name, False, ImmutableMultiDict({}))
            step._pre_handle()

        assert step.render_info.form.foreign_country_eligibility.choices == expected_choices

    def test_if_single_user_then_show_single_text(self, app):
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
        with app.test_request_context(method='GET') as req:
            req.session = SecureCookieSession({_ELIGIBILITY_DATA_KEY: create_session_form_data(session_data)})
            step = EligibilityStepChooser('eligibility').get_correct_step(
                ForeignCountriesDecisionEligibilityInputFormSteuerlotseStep.name, False, ImmutableMultiDict({}))
            step._pre_handle()

        assert step.render_info.form.foreign_country_eligibility.choices == expected_choices


class TestEligibilitySuccessDisplaySteuerlotseStep(unittest.TestCase):
    @pytest.fixture(autouse=True)
    def attach_fixtures(self, test_request_context, app):
        self.req = test_request_context
        self.app = app

    def test_if_session_data_correct_then_set_prev_input_step_correctly(self):
        correct_session_data = {'marital_status_eligibility': 'single',
                                'user_a_has_elster_account_eligibility': 'no',
                                'alimony_eligibility': 'no',
                                'pension_eligibility': 'yes',
                                'investment_income_eligibility': 'no',
                                'taxed_investment_income_eligibility': 'no',
                                'employment_income_eligibility': 'no',
                                'other_income_eligibility': 'no',
                                'foreign_country_eligibility': 'no'}
        with self.app.test_request_context(method='GET') as req:
            req.session = SecureCookieSession(
                {_ELIGIBILITY_DATA_KEY: create_session_form_data(correct_session_data)})
            step = EligibilityStepChooser('eligibility').get_correct_step(
                EligibilitySuccessDisplaySteuerlotseStep.name, False, ImmutableMultiDict({}))
            expected_url = step.url_for_step(ForeignCountriesDecisionEligibilityInputFormSteuerlotseStep.name)
            step.handle()
        self.assertEqual(expected_url, step.render_info.prev_url)

    def test_if_user_b_has_no_elster_account_then_set_correct_info(self):
        expected_information = [_('form.eligibility.result-note.user_elster_account-registration-success')]
        session_data = {'marital_status_eligibility': 'married',
                        'separated_since_last_year_eligibility': 'no',
                        'user_a_has_elster_account_eligibility': 'yes',
                        'user_b_has_elster_account_eligibility': 'no',
                        'joint_taxes_eligibility': 'yes',
                        'alimony_eligibility': 'no', }
        with patch('app.forms.steps.eligibility_steps._', MagicMock(side_effect=lambda text_id: text_id)):
            step = EligibilitySuccessDisplaySteuerlotseStep(
                endpoint='eligibility',
                stored_data=session_data,
                render_info=EligibilitySuccessDisplaySteuerlotseStep.prepare_render_info(
                    {})
            )
            step.handle()

        self.assertEqual(expected_information, step.render_info.additional_info['dependent_notes'])

    def test_if_user_wants_no_cheaper_check_then_set_correct_info(self):
        expected_information = [_l('form.eligibility.result-note.user_elster_account-registration-success'), _l('form.eligibility.result-note.capital_investment')]
        session_data = {'marital_status_eligibility': 'single',
                        'user_a_has_elster_account_eligibility': 'no',
                        'alimony_eligibility': 'no',
                        'pension_eligibility': 'yes',
                        'investment_income_eligibility': 'yes',
                        'minimal_investment_income_eligibility': 'no',
                        'taxed_investment_income_eligibility': 'yes',
                        'cheaper_check_eligibility': 'no', }
        with patch('app.forms.steps.eligibility_steps._', MagicMock(side_effect=lambda text_id: text_id)):
            step = EligibilitySuccessDisplaySteuerlotseStep(
                endpoint='eligibility',
                stored_data=session_data,
                render_info=EligibilitySuccessDisplaySteuerlotseStep.prepare_render_info(
                    {})
            )
            step.handle()

        self.assertEqual(expected_information, step.render_info.additional_info['dependent_notes'])

    def test_if_user_has_no_minimal_investment_income_then_set_correct_info(self):
        expected_information = [_l('form.eligibility.result-note.user_elster_account-registration-success'), _l('form.eligibility.result-note.capital_investment')]        
        session_data = {'marital_status_eligibility': 'single',
                        'user_a_has_elster_account_eligibility': 'no',
                        'alimony_eligibility': 'no',
                        'pension_eligibility': 'yes',
                        'investment_income_eligibility': 'yes',
                        'minimal_investment_income_eligibility': 'yes',
                        'taxed_investment_income_eligibility': 'yes', }
        with patch('app.forms.steps.eligibility_steps._', MagicMock(side_effect=lambda text_id: text_id)):
            step = EligibilitySuccessDisplaySteuerlotseStep(
                endpoint='eligibility',
                stored_data=session_data,
                render_info=EligibilitySuccessDisplaySteuerlotseStep.prepare_render_info(
                    {})
            )
            step.handle()

        self.assertEqual(expected_information, step.render_info.additional_info['dependent_notes'])

    def test_if_user_b_has_no_elster_account_and_user_wants_no_cheaper_check_then_set_correct_info(self):
        expected_information = [_('form.eligibility.result-note.user_elster_account-registration-success'),
                                _('form.eligibility.result-note.capital_investment')]
        
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
            step = EligibilitySuccessDisplaySteuerlotseStep(
                endpoint='eligibility',
                stored_data=session_data,
                render_info=EligibilitySuccessDisplaySteuerlotseStep.prepare_render_info(
                    {})
            )
            step.handle()

        self.assertEqual(expected_information, step.render_info.additional_info['dependent_notes'])

    def test_if_user_b_has_no_elster_account_and_user_has_minimal_investment_income_check_then_set_correct_info(self):
        expected_information = [_('form.eligibility.result-note.user_elster_account-registration-success'),
                                _('form.eligibility.result-note.capital_investment')]
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
            step = EligibilitySuccessDisplaySteuerlotseStep(
                endpoint='eligibility',
                stored_data=session_data,
                render_info=EligibilitySuccessDisplaySteuerlotseStep.prepare_render_info(
                    {})
            )
            step.handle()

        self.assertEqual(expected_information, step.render_info.additional_info['dependent_notes'])
        

    def test_if_no_user_b_elster_account_and_no_cheaper_check_then_set_no_info(self):
        expected_information = []
        with patch('app.forms.steps.eligibility_steps._', MagicMock(side_effect=lambda text_id: text_id)):
            step = EligibilitySuccessDisplaySteuerlotseStep(
                    endpoint='eligibility',
                    render_info=EligibilitySuccessDisplaySteuerlotseStep.prepare_render_info(
                        {}))
            step.handle()

        self.assertEqual(expected_information, step.render_info.additional_info['dependent_notes'])
