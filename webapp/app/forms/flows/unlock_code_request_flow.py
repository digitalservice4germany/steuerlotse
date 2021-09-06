import datetime
import logging

from flask import request
from flask_babel import _
from markupsafe import escape

from app.data_access.audit_log_controller import create_audit_log_confirmation_entry
from app.data_access.user_controller import user_exists, create_user
from app.data_access.user_controller_errors import UserAlreadyExistsError
from app.elster_client import elster_client
from app.elster_client.elster_errors import ElsterProcessNotSuccessful
from app.forms.flows.multistep_flow import MultiStepFlow
from app.forms.steps.unlock_code_request_steps import UnlockCodeRequestInputStep, UnlockCodeRequestSuccessStep, \
    UnlockCodeRequestFailureStep


logger = logging.getLogger(__name__)


class UnlockCodeRequestMultiStepFlow(MultiStepFlow):

    _DEBUG_DATA = (
        UnlockCodeRequestInputStep,
        {
            'idnr': '04452397687',
            'dob': datetime.date(1985, 1, 1),
            'registration_confirm_data_privacy': True,
            'registration_confirm_terms_of_service': True,
            'registration_confirm_incomes': True,
            'registration_confirm_e_data': True,
        }
    )

    def __init__(self, endpoint):
        super(UnlockCodeRequestMultiStepFlow, self).__init__(
            title=_('form.auth-request.title'),
            steps=[
                UnlockCodeRequestInputStep,
                UnlockCodeRequestFailureStep,
                UnlockCodeRequestSuccessStep
            ],
            endpoint=endpoint,
        )

    # TODO: Use inheritance to clean up this method
    def _handle_specifics_for_step(self, step, render_info, stored_data):
        render_info, stored_data = super(UnlockCodeRequestMultiStepFlow, self)._handle_specifics_for_step(step, render_info, stored_data)

        if isinstance(step, UnlockCodeRequestInputStep):
            render_info.additional_info['next_button_label'] = _('form.register')
            if request.method == 'POST' and render_info.form.validate():
                create_audit_log_confirmation_entry('Confirmed registration data privacy', request.remote_addr,
                                                    stored_data['idnr'], 'registration_confirm_data_privacy',
                                                    stored_data['registration_confirm_data_privacy'])
                create_audit_log_confirmation_entry('Confirmed registration terms of service', request.remote_addr,
                                                    stored_data['idnr'], 'registration_confirm_terms_of_service',
                                                    stored_data['registration_confirm_terms_of_service'])
                create_audit_log_confirmation_entry('Confirmed registration incomes', request.remote_addr,
                                                    stored_data['idnr'], 'registration_confirm_incomes',
                                                    stored_data['registration_confirm_incomes'])
                create_audit_log_confirmation_entry('Confirmed registration edata', request.remote_addr,
                                                    stored_data['idnr'], 'registration_confirm_e_data',
                                                    stored_data['registration_confirm_e_data'])
                try:
                    self._register_user(stored_data)
                    # prevent going to failure page as in normal flow
                    render_info.next_url = self.url_for_step(UnlockCodeRequestSuccessStep.name)
                except (UserAlreadyExistsError, ElsterProcessNotSuccessful):
                    logger.info("Could not request unlock code for user", exc_info=True)
                    pass  # go to failure step
        elif isinstance(step, UnlockCodeRequestFailureStep):
            render_info.next_url = None
        elif isinstance(step, UnlockCodeRequestSuccessStep):
            render_info.prev_url = self.url_for_step(UnlockCodeRequestInputStep.name)

        return render_info, stored_data

    @staticmethod
    def _register_user(request_form):
        """
        This method requests an unlock code with Elster for not registered users. If successful
        the users will be registered.

        :param request_form: The form attribute of the request. It should contain an idnr and a dob element.
        """
        idnr = request_form['idnr']

        if user_exists(idnr):
            raise UserAlreadyExistsError(idnr)

        response = elster_client.send_unlock_code_request_with_elster(request_form, request.remote_addr)
        request_id = escape(response['elster_request_id'])

        create_user(idnr, request_form['dob'].strftime("%d.%m.%Y"), request_id)
