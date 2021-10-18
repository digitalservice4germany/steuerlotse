from flask import request

from app.forms.steps.steuerlotse_step import FormSteuerlotseStep
from app.model.form_data import FormDataDependencies


class LotseFormSteuerlotseStep(FormSteuerlotseStep):
    template = 'basis/form_standard.html'
    header_title = None

    def __init__(self, endpoint='lotse', **kwargs):
        super().__init__(endpoint=endpoint, header_title=self.header_title, **kwargs)

    @classmethod
    def update_data(cls, stored_data):
        stored_data = super().update_data(stored_data)

        # Delete unnecessary data
        return FormDataDependencies.parse_obj(stored_data).dict(exclude_none=True)

    def _main_handle(self):
        super()._main_handle()

        # redirect in any case if overview button pressed
        if 'overview_button' in request.form:
            from app.forms.steps.lotse.confirmation import StepSummary
            self.render_info.next_url = self.url_for_step(StepSummary.name)
