from typing import Optional

from flask import session
from werkzeug.exceptions import abort

from app import app
from app.forms.flows.multistep_flow import deserialize_session_data
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

    def _get_possible_redirect(self, step_name):
        """
        Check whether the step name is an actual step or a redirect to the first step has to take place.
        """
        if not self._is_step_name_valid(step_name):
            abort(404)
        if step_name == 'start':
            dbg = self.default_data()
            if dbg:
                return dbg[0].name
            else:
                return self.first_step.name
        else:
            return None

    def _get_session_data(self, session_data_identifier=None, ttl: Optional[int] = None):
        if session_data_identifier is None:
            session_data_identifier = self.session_data_identifier
        serialized_session = session.get(session_data_identifier, b"")

        if self.default_data():
            stored_data = self.default_data() | deserialize_session_data(serialized_session,
                                                                         ttl)  # updates session_data only with non_existent values
        else:
            stored_data = deserialize_session_data(serialized_session, ttl)

        return stored_data

    def get_correct_step(self, step_name) -> SteuerlotseStep:
        if self._get_possible_redirect(step_name):
            return RedirectSteuerlotseStep(self._get_possible_redirect(step_name), endpoint=self.endpoint)

        # By default set `prev_step` and `next_step` in order of definition
        return self.steps[step_name](
            endpoint=self.endpoint,
            overview_step=self.overview_step,
            prev_step=self.determine_prev_step(step_name),
            next_step=self.determine_next_step(step_name)
        )

    def determine_prev_step(self, step_name):
        idx = self.step_order.index(step_name)
        return self.steps[self.step_order[idx - 1]] if idx > 0 else None

    def determine_next_step(self, step_name):
        idx = self.step_order.index(step_name)
        return self.steps[self.step_order[idx + 1]] if idx < len(self.step_order) - 1 else None

    def default_data(self):
        if app.config['DEBUG_DATA']:
            return self._DEBUG_DATA
        else:
            return {}
