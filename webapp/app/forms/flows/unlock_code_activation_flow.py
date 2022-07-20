import logging
import time

from app.data_access.user_controller import verify_and_login, activate_user, find_user
from app.data_access.user_controller_errors import UserNotActivatedError, WrongUnlockCodeError, \
    UserNotExistingError
from app.elster_client import elster_client
from app.elster_client.elster_errors import ElsterProcessNotSuccessful
from app.forms.flows.multistep_flow import MultiStepFlow
from flask_babel import _
from flask import request, url_for, flash, session
from requests import RequestException

from app.forms.steps.unlock_code_activation_steps import UnlockCodeActivationInputStep, \
    UnlockCodeActivationFailureStep
from app.data_access.storage.session_storage import SessionStorage
from app.data_access.storage.cookie_storage import CookieStorage

logger = logging.getLogger(__name__)
flashes_saved = []
saved_data = []


def _store_id_in_server_session(idnr):
    SessionStorage.override_data({'idnr': idnr}, 'form_data')


class UnlockCodeActivationMultiStepFlow(MultiStepFlow):
    # TODO: This uses the outdated MultiStepFlow. We do not need a multi step procedure for unlock code activation.
    #  If you adapt the unlock code activation, please consider if you can get rid of the MultiStepFlow.

    _DEBUG_DATA = (
        UnlockCodeActivationInputStep,
        {
            'idnr': '04452397687',
            'unlock_code': 'DBNH-B8JS-9JE7'
        }
    )

    def __init__(self, endpoint):
        super(UnlockCodeActivationMultiStepFlow, self).__init__(
            title=_('form.unlock-code-activation.title'),
            steps=[
                UnlockCodeActivationInputStep,
                UnlockCodeActivationFailureStep
            ],
            endpoint=endpoint,
            form_storage=CookieStorage
        )

    # TODO: Use inheritance to clean up this method
    def _handle_specifics_for_step(self, step, render_info, stored_data):
        render_info, stored_data = super(UnlockCodeActivationMultiStepFlow,
                                         self)._handle_specifics_for_step(step, render_info, stored_data)
        seconds_before = time.time()
        if isinstance(step, UnlockCodeActivationInputStep):

            if request.method == 'GET' and "location" in SessionStorage.get_data("location",
                                                                                 key_identifier=stored_data["idnr"]):
                render_info.additional_info['waiting_moment_active'] = True

            if request.method == 'POST' and render_info.form.validate():
                try:
                    self._login_or_activate_user(stored_data)
                    # prevent going to failure page as in normal flow
                    render_info.next_url = url_for('lotse', step='start')

                    # set idnr also in session
                    _store_id_in_server_session(stored_data['idnr'])
                except (UserNotExistingError, WrongUnlockCodeError, ElsterProcessNotSuccessful):
                    logger.info("Could not activate unlock code for user", exc_info=True)
                    pass  # go to failure step
                except RequestException as e:
                    render_info.next_url = self.url_for_step(UnlockCodeActivationInputStep.name)
                    flash(_('flash.erica.dataConnectionError'), 'warn')
                    flashes_saved.append((_('flash.erica.dataConnectionError'), 'warn'))
                    logger.error(f"Could not send a request to erica: {e}", exc_info=True)
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

        elif isinstance(step, UnlockCodeActivationFailureStep):
            render_info.next_url = None

        return render_info, stored_data

    @staticmethod
    def _login_or_activate_user(request_form):
        """
        This will either log in an active user or activate an inactive user if the fsc code is correct

        :param request_form: The form attribute of the request. It should contain an idnr and an unlock_code"""
        idnr = request_form['idnr']
        unlock_code = request_form['unlock_code']
        try:
            verify_and_login(idnr, unlock_code)
        except UserNotActivatedError:
            request_id = find_user(idnr).elster_request_id
            elster_client.send_unlock_code_activation_with_elster(request_form, request_id, request.remote_addr)
            activate_user(idnr, unlock_code)    # If no error is thrown, this result in a problem
            verify_and_login(idnr, unlock_code)