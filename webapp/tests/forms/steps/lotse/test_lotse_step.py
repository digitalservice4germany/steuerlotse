from unittest.mock import patch

import pytest

from app.forms.steps.lotse.lotse_step import LotseFormSteuerlotseStep


class TestLotseFormSteuerlotseStepPrepareRenderInfo:
    @pytest.mark.usefixtures('test_request_context')
    def test_calls_correct_models_parse_obj(self):
        with patch('app.model.form_data.FormDataDependencies.parse_obj') as parse_obj_method:
            LotseFormSteuerlotseStep.prepare_render_info({}, {})
            parse_obj_method.assert_called_once()
