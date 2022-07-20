import datetime
import logging
import time

from flask import request, flash, session
from flask_babel import _
from markupsafe import escape
from requests import RequestException

from app.data_access.audit_log_controller import create_audit_log_confirmation_entry
from app.data_access.storage.session_storage import SessionStorage
from app.data_access.user_controller import user_exists, create_user
from app.data_access.user_controller_errors import UserAlreadyExistsError
from app.elster_client import elster_client
from app.elster_client.elster_errors import ElsterProcessNotSuccessful
from app.forms.flows.multistep_flow import MultiStepFlow
from app.forms.steps.unlock_code_request_steps import UnlockCodeRequestInputStep, UnlockCodeRequestSuccessStep, \
    UnlockCodeRequestFailureStep
from app.data_access.storage.cookie_storage import CookieStorage

logger = logging.getLogger(__name__)
flashes_saved = []
saved_data = []


class UnlockCodeRequestMultiStepFlow(MultiStepFlow):
    # TODO: This uses the outdated MultiStepFlow. We do not need a multi step procedure for unlock code request.
    #  If you adapt the unlock code request, please consider if you can get rid of the MultiStepFlow.

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
            form_storage=CookieStorage
        )

    # TODO: Use inheritance to clean up this method
    def _handle_specifics_for_step(self, step, render_info, stored_data):
        render_info, stored_data = super(UnlockCodeRequestMultiStepFlow, self)._handle_specifics_for_step(step,
                                                                                                          render_info,
                                                                                                          stored_data)
        seconds_before = time.time()
        if isinstance(step, UnlockCodeRequestInputStep):
            render_info.additional_info['next_button_label'] = _('form.register')

            if request.method == 'GET' and "location" in SessionStorage.get_data("location",
                                                                                 key_identifier=stored_data["idnr"]):
                # If reload done but the request was already sent to erica (location saved in session) then return page
                # with waiting moment
                render_info.additional_info['waiting_moment_active'] = True

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
                except (ElsterProcessNotSuccessful, UserAlreadyExistsError):
                    logger.info("Could not request unlock code for user", exc_info=True)
                    pass
                except RequestException as e:
                    logger.error(f"Could not send a request to erica: {e}", exc_info=True)
                    render_info.next_url = self.url_for_step(UnlockCodeRequestInputStep.name)
                    flash(_('flash.erica.dataConnectionError'), 'warn')
                    flashes_saved.append((_('flash.erica.dataConnectionError'), 'warn'))
                    pass
                finally:
                    self._delete_reload_cookie(stored_data)
                    self._respect_min_waiting_time(seconds_before)

            if request.method == 'POST' and not render_info.form.validate():
                saved_data.append((render_info, stored_data))

            if request.method == 'GET' and saved_data:
                render_info_and_stored_data = saved_data[0]
                render_info = render_info_and_stored_data[0]
                stored_data = render_info_and_stored_data[1]
                saved_data.clear()

            if flashes_saved and '_flashes' not in session:
                for flash_saved in flashes_saved:
                    flash(flash_saved[0], flash_saved[1])
                flashes_saved.clear()

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
        request_id = escape(response['elsterRequestId'])

        create_user(idnr, request_form['dob'].strftime("%d.%m.%Y"), request_id)
