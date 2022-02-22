from flask import request

from app.forms.steps.steuerlotse_step import FormSteuerlotseStep
from app.model.form_data import FormDataDependencies


class LotseFormSteuerlotseStep(FormSteuerlotseStep):
    template = 'basis/form_standard.html'
    header_title = None
    disable_extended_footer = True

    def __init__(self, endpoint='lotse', **kwargs):
        super().__init__(endpoint=endpoint, header_title=self.header_title, **kwargs)

    @classmethod
    def prepare_render_info(cls, stored_data, input_data=None, should_update_data=False, *args, **kwargs):
        render_info = super().prepare_render_info(stored_data, input_data, should_update_data, *args, **kwargs)

        stored_data_without_unnecessary_fields = FormDataDependencies.parse_obj(render_info.stored_data).dict(exclude_none=True)
        render_info.stored_data = stored_data_without_unnecessary_fields
        return render_info

    def _main_handle(self):
        super()._main_handle()
        self.render_info.additional_info['disable_extended_footer'] = self.disable_extended_footer
        # redirect in any case if overview button pressed
        if 'overview_button' in request.form:
            from app.forms.steps.lotse.confirmation import StepSummary
            self.render_info.next_url = self.url_for_step(StepSummary.name)
