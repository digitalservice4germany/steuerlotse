from unittest.mock import patch, MagicMock

import pytest

from app.forms.flows.lotse_flow import LotseMultiStepFlow
from app.forms.flows.lotse_step_chooser import LotseStepChooser
from app.forms.steps.lotse.confirmation import StepSummary
from app.forms.steps.lotse_multistep_flow_steps.confirmation_steps import StepConfirmation
from app.model.form_data import MandatoryFieldMissingValidationError


@pytest.mark.usefixtures('test_request_context')
class TestStepSummary:
    @pytest.fixture
    def step(self):
        step = StepSummary(endpoint='lotse')
        return step

    def test_set_section_steps_in_render_info(self, make_test_request_context, step):
        expected_summary_session_steps = {}
        with make_test_request_context(), \
                patch("app.forms.flows.lotse_flow.LotseMultiStepFlow._get_overview_data",
                      MagicMock(return_value=expected_summary_session_steps)), \
                patch("app.forms.flows.lotse_flow.MandatoryFormData.parse_obj"):
            step.handle()

            assert step.render_info.additional_info['section_steps'] == expected_summary_session_steps

    def test_if_data_missing_then_set_next_url_correct(self, make_test_request_context, step):
        data_with_missing_fields = {'steuernummer': 'C3P0'}

        with make_test_request_context(method='POST', stored_data=data_with_missing_fields), \
                patch('app.forms.flows.lotse_flow.LotseMultiStepFlow._get_overview_data'):
            step.handle()

            assert step.render_info.next_url == LotseMultiStepFlow(endpoint='lotse').url_for_step(StepSummary.name)

    def test_if_data_missing_then_call_get_overview_data_with_missing_fields(self, make_test_request_context):
        data_with_missing_fields = {'steuernummer': 'C3P0'}
        missing_fields = ['spacecraft', 'droids']

        with make_test_request_context(method='POST', stored_data=data_with_missing_fields), \
                patch('app.forms.flows.step_chooser.StepChooser.default_data', return_value=False), \
                patch('app.forms.flows.lotse_flow.LotseMultiStepFlow._get_overview_data') as get_overview, \
                patch('app.forms.flows.lotse_flow.LotseMultiStepFlow._validate_mandatory_fields',
                      MagicMock(side_effect=MandatoryFieldMissingValidationError(missing_fields))):
            step = LotseStepChooser().get_correct_step(StepSummary.name, update_data=True)
            step.handle()

            get_overview.assert_called_once_with(data_with_missing_fields, missing_fields)

    def test_if_data_missing_then_flash_message_with_missing_fields_once(self, make_test_request_context, step):
        data_with_missing_fields = {'steuernummer': 'C3P0'}
        missing_fields = ['spacecraft', 'droids']
        missing_fields_error = MandatoryFieldMissingValidationError(missing_fields)

        with patch('app.forms.steps.lotse.confirmation.flash') as mock_flash, \
            patch('app.model.form_data.ngettext', MagicMock(side_effect=lambda text_id, _, **kwargs: text_id)), \
            patch('app.forms.flows.lotse_flow.LotseMultiStepFlow._validate_mandatory_fields',
                  MagicMock(side_effect=missing_fields_error)):
            with make_test_request_context(method='POST', stored_data=data_with_missing_fields):
                step = LotseStepChooser().get_correct_step(StepSummary.name, update_data=True)
                step.handle()

            with make_test_request_context(method='GET', stored_data=data_with_missing_fields):
                step = LotseStepChooser().get_correct_step(StepSummary.name, update_data=True)
                step.handle()

            mock_flash.assert_called_once_with(missing_fields_error.get_message(), 'warn')

    def test_if_data_not_missing_then_set_next_url_correct(self, make_test_request_context):
        data_without_missing_fields = {**LotseMultiStepFlow(endpoint='lotse').default_data()[1],
                                       **{'idnr': '04452397687'}}

        with make_test_request_context(method='POST', stored_data=data_without_missing_fields,
                                       form_data={'confirm_complete_correct': True}), \
                patch('app.forms.flows.lotse_flow.LotseMultiStepFlow._get_overview_data'), \
                patch('app.forms.steps.lotse.confirmation.create_audit_log_confirmation_entry'):
            step = LotseStepChooser().get_correct_step(StepSummary.name, update_data=True)
            step.handle()

            assert step.render_info.next_url == LotseMultiStepFlow(endpoint='lotse').url_for_step(StepConfirmation.name)

    # TODO test that audit log
    # TODO test that not valid if complete_correct not set
