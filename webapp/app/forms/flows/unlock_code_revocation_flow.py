import datetime
import logging

from app.data_access.db_model.user import User

from app.data_access.user_controller import user_exists, check_dob, delete_user
from app.data_access.user_controller_errors import UserNotExistingError, WrongDateOfBirthError
from app.elster_client import elster_client

from app.forms.flows.multistep_flow import MultiStepFlow
from flask_babel import _
from flask import request, url_for

from app.elster_client.elster_errors import ElsterProcessNotSuccessful, ElsterRequestIdUnkownError, \
    ElsterRequestAlreadyRevoked
from app.forms.steps.unlock_code_revocation_steps import UnlockCodeRevocationInputStep, UnlockCodeRevocationSuccessStep, \
    UnlockCodeRevocationFailureStep


logger = logging.getLogger(__name__)


class UnlockCodeRevocationMultiStepFlow(MultiStepFlow):

    _DEBUG_DATA = (
        UnlockCodeRevocationInputStep,
        {
            'idnr': '04452397687',
            'dob': datetime.date(1985, 1, 1)
        }
    )

    def __init__(self, endpoint):
        super(UnlockCodeRevocationMultiStepFlow, self).__init__(
            title=_('form.auth-revocation.title'),
            steps=[
                UnlockCodeRevocationInputStep,
                UnlockCodeRevocationFailureStep,
                UnlockCodeRevocationSuccessStep
            ],
            endpoint=endpoint,
        )

    # TODO: Use inheritance to clean up this method
    def _handle_specifics_for_step(self, step, render_info, stored_data):
        render_info, stored_data = super(UnlockCodeRevocationMultiStepFlow, self)._handle_specifics_for_step(step, render_info, stored_data)

        if isinstance(step, UnlockCodeRevocationInputStep):
            if request.method == 'POST' and render_info.form.validate():
                try:
                    self._cancel_user(stored_data)
                    # prevent going to failure page as in normal flow
                    render_info.next_url = self.url_for_step(UnlockCodeRevocationSuccessStep.name)
                except (UserNotExistingError, WrongDateOfBirthError, ElsterProcessNotSuccessful):
                    logger.info("Could not revoke unlock code for user", exc_info=True)
                    pass  # go to failure step
        elif isinstance(step, UnlockCodeRevocationFailureStep):
            render_info.next_url = None
        elif isinstance(step, UnlockCodeRevocationSuccessStep):
            render_info.prev_url = self.url_for_step(UnlockCodeRevocationInputStep.name)
            render_info.next_url = url_for('unlock_code_request', step='data_input')

        return render_info, stored_data

    @staticmethod
    def _cancel_user(request_form):
        """
        This method deletes the user and cancels the current unlock code at Elster.
        This is also allowed for non-activated users.

        :param request_form: The form attribute of the request. It should contain an idnr.
        """
        idnr = request_form['idnr']

        if not user_exists(idnr):
            raise UserNotExistingError(idnr)  # break here to not query Elster unnecessarily

        user = User.get(idnr)

        if not check_dob(user, request_form['dob'].strftime("%d.%m.%Y")):
            raise WrongDateOfBirthError(idnr)

        form_data = {'idnr': idnr, 'elster_request_id': user.elster_request_id}
        try:
            elster_client.send_unlock_code_revocation_with_elster(form_data, request.remote_addr)
        except (ElsterRequestIdUnkownError, ElsterRequestAlreadyRevoked):
            # In case we have the user stored and elster does not have a request (anymore)
            # we want to delete the user in our db anyways.
            logger.info("Could not revoke unlock code for user", exc_info=True)
            pass
        delete_user(idnr)
