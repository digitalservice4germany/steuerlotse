from flask_wtf.csrf import generate_csrf
from wtforms.validators import InputRequired

from app.config import Config
from app.forms import SteuerlotseBaseForm
from app.forms.steps.step import FormStep, DisplayStep
from app.forms.fields import ConfirmationField

from flask import request, url_for, flash
from flask_babel import _
from flask_babel import lazy_gettext as _l

from app.model.components import ConfirmationProps, FilingSuccessProps, FilingFailureProps, StepSubmitAcknowledgeProps
from app.model.components.helpers import form_fields_dict
from app.templates.react_template import render_react_template


class StepConfirmation(FormStep):
    name = 'confirmation'

    class Form(SteuerlotseBaseForm):
        confirm_data_privacy = ConfirmationField(
            validators=[InputRequired(message=_l('form.lotse.confirm_data_privacy.required'))])
        confirm_terms_of_service = ConfirmationField(
            validators=[InputRequired(message=_l('form.lotse.confirm_terms_of_service.required'))])

    def __init__(self, **kwargs):
        super(StepConfirmation, self).__init__(
            title=_('form.lotse.confirmation-title'),
            intro=_('form.lotse.confirmation-intro'),
            form=self.Form,
            **kwargs,
        )

    def render(self, data, render_info):
        props_dict = ConfirmationProps(
            step_header={
                'title': _('form.lotse.confirmation-title'),
                'intro': _('form.lotse.confirmation-intro'),
            },
            form={
                'action': render_info.submit_url,
                'csrf_token': generate_csrf(),
                'show_overview_button': bool(render_info.overview_url),
            },
            fields=form_fields_dict(render_info.form),
            terms_of_service_link=url_for('agb'),
            data_privacy_link=url_for('data_privacy'),
            prev_url=render_info.prev_url,
        ).camelized_dict()

        elster_error = request.args.get('elster_error')
        if elster_error:
            flash(elster_error)

        return render_react_template(component='ConfirmationPage',
                                     props=props_dict,
                                     # TODO: These are still required by base.html to set the page title.
                                     form=render_info.form,
                                     header_title=_('form.lotse.confirmation.header-title'))


class StepFiling(DisplayStep):
    name = 'filing'

    def __init__(self, **kwargs):
        super(StepFiling, self).__init__(title=_('form.lotse.filing.success.header-title'),
                                         **kwargs)

    def render(self, data, render_info):
        if render_info.additional_info['elster_data']['was_successful']:
            props_dict = FilingSuccessProps(
                next_url=render_info.next_url,
                transfer_ticket=render_info.additional_info['elster_data']['transfer_ticket'],
                download_url=url_for("download_pdf"),
                # This ternary operator is needed so that we catch the case of users going directly to the filing page with incorrent data and not going through the actual flow.
                taxNumber_provided=data.get('steuernummer_exists') == 'yes' if data.get('steuernummer_exists') else None,
                plausible_domain=Config.PLAUSIBLE_DOMAIN
            ).camelized_dict()
            component = 'FilingSuccessPage'
            header_title = _('form.lotse.filing.success.header-title')
        else:
            props_dict = FilingFailureProps(
                error_details=render_info.additional_info['elster_data'][
                    'validation_problems'] if 'validation_problems' in render_info.additional_info[
                    'elster_data'] else []
            ).camelized_dict()
            component = 'FilingFailurePage'
            header_title = _('form.lotse.filing.failure.header-title')
        return render_react_template(component=component,
                                     props=props_dict,
                                     # TODO: These are still required by base.html to set the page title.
                                     form=render_info.form,
                                     header_title=header_title)


class StepAck(DisplayStep):
    name = 'ack'

    def __init__(self, **kwargs):
        super(StepAck, self).__init__(title=_('form.lotse.ack.alert.title'), **kwargs)

    def render(self, data, render_info):
        prop_dicts = StepSubmitAcknowledgeProps(
            prev_url=render_info.prev_url,
            logout_url=render_info.next_url,
            plausible_domain=Config.PLAUSIBLE_DOMAIN
        ).camelized_dict()
        return render_react_template(component='SubmitAcknowledgePage',
                                     props=prop_dicts,
                                     header_title=_('form.lotse.filing.success.header-title'))
