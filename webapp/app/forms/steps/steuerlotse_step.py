from typing import Optional

from flask import request, session, url_for, render_template
from werkzeug.utils import redirect

from app.forms.flows.multistep_flow import RenderInfo, deserialize_session_data, serialize_session_data


class SteuerlotseStep(object):
    """An abstract step that provides default implementations of the handle functions"""
    name = None
    title = None
    intro = None
    template = None

    def __init__(self, endpoint, header_title, overview_step, default_data, prev_step, next_step):
        self.endpoint = endpoint
        self.header_title = header_title
        self.overview_step = overview_step
        self._prev_step = prev_step
        self._next_step = next_step
        self.render_info = None

        self.default_data = default_data

        self.has_link_overview = request.args.get('link_overview', False) == 'True'

    def handle(self):
        stored_data = self._pre_handle()
        stored_data = self._main_handle(stored_data)
        return self._post_handle(stored_data)

    def _pre_handle(self):
        stored_data = self._get_session_data()
        self.render_info = RenderInfo(step_title=self.title, step_intro=self.intro, form=None,
                                      prev_url=self.url_for_step(self._prev_step.name) if self._prev_step else None,
                                      next_url=self.url_for_step(self._next_step.name) if self._next_step else None,
                                      submit_url=self.url_for_step(self.name), overview_url=self.url_for_step(
                self.overview_step.name) if self.has_link_overview and self.overview_step else None,
                                      header_title=self.header_title)
        return stored_data

    def _main_handle(self, stored_data):
        """ Main method to handle specific behavior of a step. Override this method for specific behavior."""
        return stored_data

    def _post_handle(self, stored_data):
        redirection = self._handle_redirects()
        if redirection:
            return redirection
        return self.render()

    def _get_session_data(self, ttl: Optional[int] = None):
        serialized_session = session.get('form_data', b"")

        if self.default_data:
            stored_data = self.default_data | deserialize_session_data(serialized_session, ttl)  # updates session_data only with non_existent values
        else:
            stored_data = deserialize_session_data(serialized_session, ttl)

        return stored_data

    def _handle_redirects(self):
        if self.render_info.redirect_url:
            return redirect(self.render_info.redirect_url)

    def render(self):
        raise NotImplementedError

    def url_for_step(self, step_name, _has_link_overview=None, **values):
        """Generate URL for given step and current session."""
        if not _has_link_overview:
            _has_link_overview = self.has_link_overview

        # show overview buttons if explicitly requested or if shown for current request
        return url_for(self.endpoint,
                       step=step_name,
                       link_overview=_has_link_overview,
                       **values)


class FormSteuerlotseStep(SteuerlotseStep):
    template = 'basis/form_full_width.html'

    def __init__(self, form, endpoint, header_title, overview_step=None, default_data=None, prev_step=None,
                 next_step=None,):
        super(FormSteuerlotseStep, self).__init__(endpoint, header_title, overview_step, default_data, prev_step, next_step)
        self.form = form

    def _pre_handle(self):
        stored_data = super()._pre_handle()
        form = self.create_form(request, prefilled_data=stored_data)
        if request.method == 'POST' and form.validate():
            stored_data.update(form.data)
        self.render_info.form = form
        return stored_data

    def _post_handle(self, stored_data):
        self._override_session_data(stored_data)

        redirection = self._handle_redirects()
        if redirection:
            return redirection

        if request.method == 'POST' and self.render_info.form.validate():
            return redirect(self.render_info.next_url)
        return self.render()

    def create_form(self, request, prefilled_data):
        # If `form_data` is present it will always override `data` during
        # value binding. For `BooleanFields` an empty/missing value in the `form_data`
        # will lead to an unchecked box.
        form_data = request.form
        if len(form_data) == 0:
            form_data = None

        return self.form(form_data, **prefilled_data)

    def render(self):
        """
        Renders a Form step. Use the render_info to provide all the needed data for rendering.
        """
        return render_template(
            template_name_or_list=self.template,
            form=self.render_info.form,
            render_info=self.render_info
        )

    @staticmethod
    def _delete_dependent_data(data_field_prefixes: list, stored_data: dict):
        for field in list(stored_data.keys()):
            if any([field.startswith(data_field_prefix) for data_field_prefix in data_field_prefixes]):
                stored_data.pop(field)
        return stored_data

    @staticmethod
    def _override_session_data(stored_data):
        session['form_data'] = serialize_session_data(stored_data)


class DisplaySteuerlotseStep(SteuerlotseStep):

    def __init__(self, endpoint, header_title, overview_step=None, default_data=None, prev_step=None, next_step=None):
        super(DisplaySteuerlotseStep, self).__init__(endpoint, header_title, overview_step, default_data, prev_step, next_step)

    def render(self):
        """
        Render a display step. Use the render_info to provide all the needed data for rendering.
        """
        return render_template(template_name_or_list=self.template, render_info=self.render_info)


class RedirectSteuerlotseStep(SteuerlotseStep):
    """
    This step is used only to perform a redirection. It acts a a placeholder step that can be used by the step chooser
    to return a SteuerlotseStep that should only redirect to another step.
    """

    def __init__(self, redirection_step_name, endpoint, header_title=None, overview_step=None, default_data=None, prev_step=None, next_step=None):
        super(RedirectSteuerlotseStep, self).__init__(endpoint, header_title, overview_step, default_data, prev_step, next_step)
        self.redirection_step_name = redirection_step_name

    def handle(self):
        # Override handle because this step should do nothing but redirect.
        # Therefore no _pre_handle or _post_handle are needed.
        return redirect(self.url_for_step(self.redirection_step_name))

    def render(self):
        pass
