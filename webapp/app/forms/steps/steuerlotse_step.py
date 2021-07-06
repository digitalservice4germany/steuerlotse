from typing import Optional

from flask import request, session, url_for, render_template
from werkzeug.utils import redirect

from app.forms.flows.multistep_flow import RenderInfo, deserialize_session_data, override_session_data, serialize_session_data


class SteuerlotseStep(object):
    """An abstract step that provides default implementations of the handle functions"""
    name = None

    def __init__(self, title, intro, endpoint, overview_step=None, default_data=None, prev_step=None, next_step=None, header_title=None):
        self.title = title
        self.intro = intro
        self.endpoint = endpoint
        self.overview_step = overview_step
        self._prev_step = prev_step
        self._next_step = next_step
        self.header_title = header_title
        self.render_info = None

        self.default_data = default_data

        self.has_link_overview = request.args.get('link_overview', False) == 'True'

    def handle(self):
        stored_data = self._get_session_data()
        stored_data = self._pre_handle(stored_data)
        stored_data = self._main_handle(stored_data)
        return self._post_handle(stored_data)

    def _pre_handle(self, stored_data):
        self.render_info = RenderInfo(step_title=self.title, step_intro=self.intro, form=None,
                                      prev_url=self.url_for_step(self._prev_step.name) if self._prev_step else None,
                                      next_url=self.url_for_step(self._next_step.name) if self._next_step else None,
                                      submit_url=self.url_for_step(self.name), overview_url=self.url_for_step(
                self.overview_step.name) if self.has_link_overview and self.overview_step else None)
        return stored_data

    def _handle_redirects(self):
        if self.render_info.redirect_url:
            return redirect(self.render_info.redirect_url)

    def _post_handle(self, stored_data):
        redirection = self._handle_redirects()
        if redirection:
            return redirection
        return self.render()

    def _main_handle(self, stored_data):
        return stored_data

    def render(self):
        raise NotImplementedError

    def _get_session_data(self, ttl: Optional[int] = None):
        serialized_session = session.get('form_data', b"")

        if self.default_data:
            stored_data = self.default_data | deserialize_session_data(serialized_session, ttl)  # updates session_data only with non_existent values
        else:
            stored_data = deserialize_session_data(serialized_session, ttl)

        return stored_data

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

    def __init__(self, title, form, intro=None, endpoint=None, overview_step=None, default_data=None, prev_step=None, next_step=None, header_title=None,
                 template='basis/form_full_width.html'):
        super(FormSteuerlotseStep, self).__init__(title, intro, endpoint, overview_step, default_data, prev_step, next_step, header_title)
        self.form = form
        self.template = template

    def _pre_handle(self, stored_data):
        super()._pre_handle(stored_data)
        form = self.create_form(request, prefilled_data=stored_data)
        if request.method == 'POST' and form.validate():
            stored_data.update(form.data)
        self.render_info.form = form
        return stored_data

    def _post_handle(self, stored_data):
        override_session_data(stored_data)

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

        form = self.form(form_data, **prefilled_data)
        return form

    def render(self):
        """
        Renders a Form step. Use the render_info to provide all the needed data for rendering.
        """
        self.render_info.form.first_field = next(iter(self.render_info.form))
        return render_template(
            template_name_or_list=self.template,
            form=self.render_info.form,
            render_info=self.render_info,
            header_title=self.header_title
        )

    @staticmethod
    def _delete_dependent_data(data_field_prefixes: list, stored_data: dict):
        for field in list(stored_data.keys()):
            if any([field.startswith(data_field_prefix) for data_field_prefix in data_field_prefixes]):
                stored_data.pop(field)
        return stored_data


class DisplaySteuerlotseStep(SteuerlotseStep):

    def __init__(self, title, intro=None, endpoint=None, overview_step=None, default_data=None, prev_step=None, next_step=None):
        super(DisplaySteuerlotseStep, self).__init__(title, intro, endpoint, overview_step, default_data, prev_step, next_step)

    def render(self):
        """
        Renders a display step. Use the render_info to provide all the needed data for rendering.
        """
        raise NotImplementedError()


class RedirectSteuerlotseStep(SteuerlotseStep):

    def __init__(self, redirection_step_name, endpoint, title=None, intro=None, overview_step=None, default_data=None, prev_step=None, next_step=None):
        super(RedirectSteuerlotseStep, self).__init__(title, intro, endpoint, overview_step, default_data, prev_step, next_step)
        self.redirection_step_name = redirection_step_name

    def handle(self):
        return redirect(self.url_for_step(self.redirection_step_name))

    def render(self):
        pass
