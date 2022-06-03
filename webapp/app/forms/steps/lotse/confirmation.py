import logging
import json

from flask import request, flash
from flask_wtf.csrf import generate_csrf
from wtforms.validators import InputRequired

from app.data_access.audit_log_controller import create_audit_log_confirmation_entry
from app.forms import SteuerlotseBaseForm
from app.forms.fields import ConfirmationField
from app.forms.steps.lotse.lotse_step import LotseFormSteuerlotseStep

from flask_babel import lazy_gettext as _l, _

from app.forms.steps.lotse_multistep_flow_steps.confirmation_steps import StepConfirmation
from app.model.form_data import MandatoryFieldMissingValidationError
from app.model.components import SummaryDataSectionProps, SummaryPageProps
from app.model.components.helpers import form_fields_dict
from app.templates.react_template import render_react_template

logger = logging.getLogger(__name__)


class StepSummary(LotseFormSteuerlotseStep):
    name = 'summary'
    title = _l('form.lotse.summary-title')
    header_title = _l('form.lotse.summary.header-title')
    next_step = StepConfirmation

    summary_data = {}

    class InputForm(SteuerlotseBaseForm):
        confirm_complete_correct = ConfirmationField(label=_l('form.lotse.field_confirm_complete_correct'),
                                                     validators=[InputRequired(message=_l('form.lotse.confirm_complete_correct.required'))])

    def _main_handle(self):
        super()._main_handle()
        from app.forms.flows.lotse_flow import LotseMultiStepFlow
        missing_fields = None
        try:
            LotseMultiStepFlow._validate_mandatory_fields(self.stored_data)
        except MandatoryFieldMissingValidationError as e:
            logger.info(f"Mandatory est fields missing: {e.missing_fields}", exc_info=True)
            # prevent flashing the same message two times
            if not self.should_update_data:
                flash(e.get_message(), 'warn')
            missing_fields = e.missing_fields
            self.render_info.next_url = self.url_for_step(StepSummary.name)
        # TODO move this to a more sensible location!
        multistep_flow = LotseMultiStepFlow(endpoint='lotse')
       
        self.summary_data = multistep_flow._get_overview_data(self.stored_data, missing_fields)
        self.render_info.overview_url = None


        if not missing_fields and self.should_update_data and self.render_info.data_is_valid:
            create_audit_log_confirmation_entry('Confirmed complete correct data', request.remote_addr,
                                                self.stored_data['idnr'], 'confirm_complete_correct',
                                                self.stored_data['confirm_complete_correct'])

    def render(self):
        props_dict = SummaryPageProps(
            summary_data=SummaryDataSectionProps(mandatory_data=self.summary_data[0]["data"], section_steuerminderung=self.summary_data[1]["data"]),
            form={
                'action': self.render_info.submit_url,
                'csrf_token': generate_csrf(),
                'show_overview_button': bool(self.render_info.overview_url),
            },
            fields=form_fields_dict(self.render_info.form),
            prev_url=self.render_info.prev_url
        ).camelized_dict()

        return render_react_template(component='SummaryPage',
                                     props=props_dict,
                                     form=self.render_info.form,
                                     header_title=_('form.lotse.header-title'),
                                     disable_extended_footer=True)