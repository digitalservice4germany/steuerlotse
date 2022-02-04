from unittest.mock import patch, MagicMock

import pytest

from app.forms.steps.lotse.confirmation import StepSummary
from app.forms.steps.lotse.lotse_step import LotseFormSteuerlotseStep


class TestLotseFormSteuerlotseStepPrepareRenderInfo:
    @pytest.mark.usefixtures('test_request_context')
    def test_returns_models_parse_obj_result(self):
        expected_stored_data = {'vacation': 'Netherlands'}
        return_value = MagicMock(dict=MagicMock(return_value=expected_stored_data))
        with patch('app.model.form_data.FormDataDependencies.parse_obj', MagicMock(return_value=return_value)):
            actual_return_value = LotseFormSteuerlotseStep.prepare_render_info({}, {})
            assert actual_return_value.stored_data == expected_stored_data


class TestLotseFormSteuerlotseStepMainHandle:
    def test_if_overview_button_set_in_request_set_next_url_to_summary_step(self, new_test_request_context_with_data_in_session):
        with new_test_request_context_with_data_in_session(form_data={'overview_button': ''}):
            render_info = LotseFormSteuerlotseStep.prepare_render_info({}, {})
            step = LotseFormSteuerlotseStep(render_info=render_info)
            step._main_handle()
            assert StepSummary.name in step.render_info.next_url
