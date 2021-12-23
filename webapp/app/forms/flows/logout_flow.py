from flask import url_for, flash, request
from flask_babel import _
from flask_login import logout_user, current_user

from app.forms.flows.multistep_flow import MultiStepFlow
from app.forms.steps.logout_steps import LogoutInputStep


class LogoutMultiStepFlow(MultiStepFlow):
    # TODO: This uses the outdated MultiStepFlow. We do not need a multi step procedure for logout.
    #  If you adapt the logout, please consider if you can get rid of the MultiStepFlow.

    _DEBUG_DATA = (
        LogoutInputStep,
        {}
    )

    def __init__(self, endpoint):
        super(LogoutMultiStepFlow, self).__init__(
            title=_('form.auth-request.title'),
            steps=[
                LogoutInputStep
            ],
            endpoint=endpoint,
        )

    # TODO: Use inheritance to clean up this method
    def _handle_specifics_for_step(self, step, render_info, stored_data):
        render_info, stored_data = super(LogoutMultiStepFlow, self)._handle_specifics_for_step(step, render_info, stored_data)

        if isinstance(step, LogoutInputStep):
            render_info.additional_info['next_button_label'] = _('form.logout.logout-anyway-button')
            if request.method == 'POST' and render_info.form.validate():
                self._logout_user_and_flash_success()
                stored_data = {}
                render_info.next_url = url_for('unlock_code_activation')

            elif current_user.has_completed_tax_return():
                self._logout_user_and_flash_success()
                stored_data = {}
                render_info.redirect_url = url_for('index')

        return render_info, stored_data

    def _logout_user_and_flash_success(self):
        logout_user()
        flash(_('flash.logout.successful'), 'success')
