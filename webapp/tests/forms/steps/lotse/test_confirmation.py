from unittest.mock import patch, MagicMock

import pytest
from werkzeug.datastructures import MultiDict, ImmutableMultiDict

from app.forms.flows.lotse_flow import LotseMultiStepFlow
from app.forms.flows.lotse_step_chooser import LotseStepChooser
from app.forms.steps.lotse.confirmation import StepSummary
from app.forms.steps.lotse_multistep_flow_steps.confirmation_steps import StepConfirmation
from app.model.form_data import MandatoryFieldMissingValidationError


@pytest.mark.usefixtures('test_request_context')
class TestStepSummary:
    @pytest.fixture
    def summary_step(self):
        step = LotseStepChooser().get_correct_step(StepSummary.name, False, ImmutableMultiDict({}))
        return step

    def test_if_complete_correct_not_set_then_fail_validation(self, summary_step):
        data = MultiDict({})
        form = summary_step.InputForm(formdata=data)
        assert form.validate() is False

    def test_if_complete_correct_set_then_succ_validation(self, summary_step):
        data = MultiDict({'confirm_complete_correct': True})
        form = summary_step.InputForm(formdata=data)
        assert form.validate() is True

    def test_set_section_steps_in_render_info(self, new_test_request_context, summary_step):
        expected_summary_session_steps = {}
        with new_test_request_context(), \
                patch("app.forms.flows.lotse_flow.LotseMultiStepFlow._get_overview_data",
                      MagicMock(return_value=expected_summary_session_steps)), \
                patch("app.forms.flows.lotse_flow.MandatoryFormData.parse_obj"):
            summary_step.handle()

            assert summary_step.render_info.additional_info['section_steps'] == expected_summary_session_steps

    def test_if_data_missing_then_set_next_url_correct(self, new_test_request_context, summary_step):
        data_with_missing_fields = {'steuernummer': 'C3P0'}

        with new_test_request_context(stored_data=data_with_missing_fields), \
                patch('app.forms.flows.lotse_flow.LotseMultiStepFlow._get_overview_data'):
            summary_step.handle()

            assert summary_step.render_info.next_url == LotseMultiStepFlow(endpoint='lotse').url_for_step(StepSummary.name)

    def test_if_data_missing_then_call_get_overview_data_with_missing_fields(self, new_test_request_context):
        data_with_missing_fields = {'steuernummer': 'C3P0'}
        missing_fields = ['spacecraft', 'droids']

        with new_test_request_context(stored_data=data_with_missing_fields), \
                patch('app.forms.flows.step_chooser.StepChooser.default_data', return_value=False), \
                patch('app.forms.flows.lotse_flow.LotseMultiStepFlow._get_overview_data') as get_overview, \
                patch('app.forms.flows.lotse_flow.LotseMultiStepFlow._validate_mandatory_fields',
                      MagicMock(side_effect=MandatoryFieldMissingValidationError(missing_fields))):
            step = LotseStepChooser().get_correct_step(StepSummary.name, True, ImmutableMultiDict({}))
            step.handle()

            get_overview.assert_called_once_with(data_with_missing_fields, missing_fields)

    def test_if_data_missing_then_flash_message_with_missing_fields_once(self, new_test_request_context):
        data_with_missing_fields = {'steuernummer': 'C3P0'}
        missing_fields = ['spacecraft', 'droids']
        missing_fields_error = MandatoryFieldMissingValidationError(missing_fields)

        with patch('app.forms.steps.lotse.confirmation.flash') as mock_flash, \
            patch('app.model.form_data.ngettext', MagicMock(side_effect=lambda text_id, _, **kwargs: text_id)), \
            patch('app.forms.flows.lotse_flow.LotseMultiStepFlow._validate_mandatory_fields',
                  MagicMock(side_effect=missing_fields_error)):
            with new_test_request_context(stored_data=data_with_missing_fields):
                step = LotseStepChooser().get_correct_step(StepSummary.name, True, ImmutableMultiDict({}))
                step.handle()

            with new_test_request_context(stored_data=data_with_missing_fields):
                step = LotseStepChooser().get_correct_step(StepSummary.name, False, ImmutableMultiDict({}))
                step.handle()

            mock_flash.assert_called_once_with(missing_fields_error.get_message(), 'warn')

    def test_if_data_not_missing_then_set_next_url_correct(self, new_test_request_context):
        data_without_missing_fields = {**LotseStepChooser(endpoint='lotse')._DEBUG_DATA,
                                       **{'idnr': '04452397687'}}

        with new_test_request_context(stored_data=data_without_missing_fields), \
                patch('app.forms.flows.lotse_flow.LotseMultiStepFlow._get_overview_data'), \
                patch('app.forms.steps.lotse.confirmation.create_audit_log_confirmation_entry'):
            step = LotseStepChooser().get_correct_step(StepSummary.name, True,
                                                       form_data=ImmutableMultiDict({'confirm_complete_correct': True}))
            step.handle()

            assert step.render_info.next_url == LotseMultiStepFlow(endpoint='lotse').url_for_step(StepConfirmation.name)

    def test_if_data_not_missing_and_required_fields_set_then_create_audit_log(self, new_test_request_context):
        idnr = '04452397687'
        data_without_missing_fields = {**LotseStepChooser(endpoint='lotse')._DEBUG_DATA,
                                       **{'idnr': idnr}}

        with new_test_request_context(stored_data=data_without_missing_fields), \
                patch('app.forms.flows.lotse_flow.LotseMultiStepFlow._get_overview_data'), \
                patch('app.forms.steps.lotse.confirmation.create_audit_log_confirmation_entry') as audit_log_method:
            step = LotseStepChooser().get_correct_step(StepSummary.name, True,
                                                       ImmutableMultiDict({'confirm_complete_correct': True}))
            step.handle()

            audit_log_method.assert_called_once()
            assert audit_log_method.call_args.args[0] == 'Confirmed complete correct data'
            # IP Address is wild-card
            assert audit_log_method.call_args.args[2] == idnr
            assert audit_log_method.call_args.args[3] == 'confirm_complete_correct'
            assert audit_log_method.call_args.args[4] is True

    def test_if_data_missing_and_required_fields_set_then_do_not_create_audit_log(self, new_test_request_context):
        data_with_missing_fields = {}

        with new_test_request_context(stored_data=data_with_missing_fields,
                                      form_data={'confirm_complete_correct': True}), \
                patch('app.forms.flows.lotse_flow.LotseMultiStepFlow._get_overview_data'), \
                patch('app.forms.steps.lotse.confirmation.create_audit_log_confirmation_entry') as audit_log_method:
            step = LotseStepChooser().get_correct_step(StepSummary.name, True,
                                                       form_data=ImmutableMultiDict({'confirm_complete_correct': True}))
            step.handle()

            audit_log_method.assert_not_called()

    def test_if_data_not_missing_but_required_fields_not_set_then_do_not_create_audit_log(self,
                                                                                          new_test_request_context):
        idnr = '04452397687'
        data_without_missing_fields = {**LotseStepChooser(endpoint='lotse')._DEBUG_DATA,
                                       **{'idnr': idnr}}

        with new_test_request_context(stored_data=data_without_missing_fields), \
                patch('app.forms.flows.lotse_flow.LotseMultiStepFlow._get_overview_data'), \
                patch('app.forms.steps.lotse.confirmation.create_audit_log_confirmation_entry') as audit_log_method:
            step = LotseStepChooser().get_correct_step(StepSummary.name, True, ImmutableMultiDict({}))
            step.handle()

            audit_log_method.assert_not_called()
