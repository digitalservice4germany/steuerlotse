from werkzeug.exceptions import abort

from app.config import Config
from app.forms.session_data import get_session_data, deserialize_session_data
from app.forms.steps.steuerlotse_step import SteuerlotseStep, RedirectSteuerlotseStep


class StepChooser:
    """A StepChooser represents an arrangement of steps and allows to find the correct step to handle an incoming
    request. The current step is determined by the URL (e.g. 'specific_flow / step / second_step' determines the
    second_step of the specific_flow). Relevant data for the current session (e.g. data from form input) is stored in
    the session cookie.
    """
    _DEBUG_DATA = None
    session_data_identifier = None

    def __init__(self, title, steps, endpoint, overview_step=None):
        self.title = title
        self.steps = {s.name: s for s in steps}
        self.step_order = [s.name for s in steps]
        self.first_step = next(iter(self.steps.values()))
        self.endpoint = endpoint
        self.overview_step = overview_step

    def _is_step_name_valid(self, step_name):
        return step_name == "start" or step_name in self.steps

    def _get_possible_redirect(self, step_name, stored_data):
        """
        Check whether the step name is an actual step or a redirect to the first step has to take place.
        """
        if not self._is_step_name_valid(step_name):
            abort(404)
        elif step_name == 'start':
            dbg = self.default_data()
            if dbg:
                return dbg[0].name
            else:
                return self.first_step.name
        elif step_to_redirect_to := self.steps[step_name].get_redirection_step(stored_data):
            return step_to_redirect_to
        else:
            return None

    def get_correct_step(self, step_name: str, update_data: bool = False) -> SteuerlotseStep:
        stored_data = get_session_data(self.session_data_identifier, default_data=self.default_data())
        if step_name_to_redirect_to := self._get_possible_redirect(step_name, stored_data):
            return RedirectSteuerlotseStep(step_name_to_redirect_to, endpoint=self.endpoint)

        if update_data:
            stored_data = self.steps[step_name].update_data(stored_data)

        # By default set `prev_step` and `next_step` in order of definition
        return self.steps[step_name](
            endpoint=self.endpoint,
            stored_data=stored_data,
            overview_step=self.overview_step,
            prev_step=self.determine_prev_step(step_name, stored_data),
            next_step=self.determine_next_step(step_name, stored_data),
            session_data_identifier=self.session_data_identifier
        )

    def determine_prev_step(self, current_step_name, stored_data):
        """
        This method searches the correct previous step for the given @current_step_name on the basis of the
        @stored_data.
        It loops through the list of steps starting from the current_step (i) upwards. Each step is then asked if they
        could be the previous step (via checking their own precondition). If the answer of i-1 is yes, that step is
        returned. Otherwise, the step i-2 is asked and so on until a fitting step is found.

        :param current_step_name: The name of the step to get the previous step for
        :param stored_data: The data currently in the session
        """
        idx = self.step_order.index(current_step_name)
        for possible_prev_step_idx in range(idx - 1, -1, -1):
            possible_prev_step = self.steps[self.step_order[possible_prev_step_idx]]
            if possible_prev_step.check_precondition(stored_data):
                return possible_prev_step
        return None

    def determine_next_step(self, current_step_name, stored_data):
        """
        This method searches the correct next step for the given @current_step_name on the basis of the
        @stored_data.
        It loops through the list of steps starting from the current_step (i) downwards. Each step is then asked if they
        could be the next step (via checking their own precondition). If the answer of i+1 is yes, that step is
        returned. Otherwise, the step i+2 is asked and so on until a fitting step is found.

        :param current_step_name: The name of the step to get the next step for
        :param stored_data: The data currently in the session
        """
        idx = self.step_order.index(current_step_name)
        for possible_next_step_idx in range(idx + 1, len(self.steps)):
            possible_next_step = self.steps[self.step_order[possible_next_step_idx]]
            if possible_next_step.check_precondition(stored_data):
                return possible_next_step
        return None

    def default_data(self):
        if Config.DEBUG_DATA:
            return self._DEBUG_DATA
        else:
            return {}
