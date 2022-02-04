import logging
from collections import namedtuple
from typing import Optional

from flask import redirect, request, url_for, abort
from wtforms import Form

# The RenderInfo is provided to all templates
from app.config import Config
from app.forms.session_data import deserialize_session_data, override_session_data, get_session_data
from app.forms.steps.step import FormStep

logger = logging.getLogger(__name__)


class RenderInfo(object):
    def __init__(self, step_title, step_intro, form, prev_url, next_url, submit_url, overview_url, header_title=None, stored_data=None, data_is_valid=False):
        self.step_title = step_title
        self.step_intro = step_intro
        self.header_title = None
        self.form: Form = form
        self.prev_url = prev_url
        self.next_url = next_url
        self.submit_url = submit_url
        self.overview_url = overview_url
        self.header_title = header_title
        self.back_link_text = None
        self.redirect_url = None
        self.additional_info = {}
        self.stored_data = stored_data
        self.data_is_valid = data_is_valid

    def __eq__(self, other):
        if isinstance(other, RenderInfo):
            return self.step_title == other.step_title and \
                   self.step_intro == other.step_intro and \
                   self.form == other.form and \
                   self.prev_url == other.prev_url and \
                   self.next_url == other.next_url and \
                   self.submit_url == other.submit_url and \
                   self.overview_url == other.overview_url and \
                   self.additional_info == other.additional_info and \
                   self.redirect_url == other.redirect_url
        return False


# Used for the header step overview of the main form
FlowNavItem = namedtuple(
    typename='FlowNavItem',
    field_names=['number', 'text', 'active'],
    defaults=[False]
)


class MultiStepFlow:
    # TODO: The MultiStepFlow is outdated and will only be used for unlock code request/activation/revocation and logout
    #  We do want to change that. If you adapt any of the mentioned flows, consider if you can remove the MultiStepFlow.

    """A MultiStepFlow represents a form with individual screens. The current
    context is maintained through a `session` URL parameter that is passed along.
    This allows it to gracefully handle forced refreshs and back/forward navigation
    in the browser. The current state is maintained via a `SessionManager`.
    """
    _DEBUG_DATA = None

    def __init__(self, title, steps, endpoint, overview_step=None):
        """Creates a new MultistepFlow for the given configuration.

        The steps are a list of `FormStep` subclasses.
        This allows to initialise only the steps necessary and to use the
        the declared ordering for initializing `prev_step` and `next_step`.
        """
        self.title = title
        self.steps = {s.name: s for s in steps}
        self.first_step = next(iter(self.steps.values()))
        self.overview_step = overview_step

        self.endpoint = endpoint

        self.has_link_overview = request.args.get('link_overview', False) == 'True'

    def handle(self, step_name):
        if not step_name == "start" and step_name not in self.steps:
            abort(404)
        stored_data = self._get_session_data()
        redirected_step = self._check_step_needs_to_be_skipped(step_name, stored_data)
        if redirected_step:
            return redirect(redirected_step)

        prev_step, step, next_step = self._generate_steps(step_name)

        render_info = RenderInfo(step_title=step.title, step_intro=step.intro, form=None,
                                 prev_url=self.url_for_step(prev_step.name) if prev_step else None,
                                 next_url=self.url_for_step(next_step.name) if next_step else None,
                                 submit_url=self.url_for_step(step.name), overview_url=self.url_for_step(
                self.overview_step.name) if self.has_link_overview and self.overview_step else None)

        render_info, stored_data = self._handle_specifics_for_step(step, render_info, stored_data)
        override_session_data(stored_data)

        if render_info.redirect_url:
            logger.info(f"Redirect to {render_info.redirect_url}")
            return redirect(render_info.redirect_url)
        elif isinstance(step, FormStep) and request.method == 'POST' and render_info.form.validate():
            logger.info(f"Redirect to next Step {render_info.next_url}")
            return redirect(render_info.next_url)
        else:
            return step.render(stored_data, render_info)

    def _check_step_needs_to_be_skipped(self, step_name, input_data):
        """Check whether a step has to be blocked and if so then do provide the correct link"""
        # Find the correct start step
        if step_name == 'start':
            dbg = self.default_data()
            if dbg:
                return self.url_for_step(dbg[0].name)
            else:
                return self.url_for_step(self.first_step.name)
        else:
            return None

    def url_for_step(self, step_name, _has_link_overview=None, **values):
        """Generate URL for given step and current session."""
        if not _has_link_overview:
            _has_link_overview = self.has_link_overview

        # show overview buttons if explicitly requested or if shown for current request
        return url_for(self.endpoint,
                       step=step_name,
                       link_overview=_has_link_overview,
                       **values)

    def _get_session_data(self, ttl: Optional[int] = None):
        form_data = get_session_data('form_data', ttl)
        if self.default_data():
            form_data = self.default_data()[1] | form_data  # updates form_data only with non_existent values
        return form_data

    def _load_step(self, step_name):
        step_names, step_types = list(self.steps.keys()), list(self.steps.values())
        idx = step_names.index(step_name)

        # By default set `prev_step` and `next_step` in order of definition
        return self.steps[step_name](
            prev_step=step_types[idx - 1] if idx > 0 else '',
            next_step=step_types[idx + 1] if idx < len(step_types) - 1 else ''
        )

    def _generate_steps(self, step_name):
        step = self._load_step(step_name)
        prev_step = step.prev_step()
        next_step = step.next_step()

        return prev_step, step, next_step

    # TODO: Use inheritance to clean up this method
    def _handle_specifics_for_step(self, step, render_info, stored_data):
        if isinstance(step, FormStep):
            form = step.create_form(request, prefilled_data=stored_data)
            if request.method == 'POST' and form.validate():
                stored_data.update(form.data)
            render_info.form = form
        return render_info, stored_data

    def default_data(self):
        if Config.PREFILL_SAMPLE_FORM_DATA:
            return self._DEBUG_DATA
        else:
            return {}

    @staticmethod
    def _delete_dependent_data(data_field_prefixes: list, stored_data: dict):
        for field in list(stored_data.keys()):
            if any([field.startswith(data_field_prefix) for data_field_prefix in data_field_prefixes]):
                stored_data.pop(field)
        return stored_data


