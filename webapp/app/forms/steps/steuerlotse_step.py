from typing import Optional

from flask import request, session, url_for, render_template
from flask_babel import ngettext
from werkzeug.utils import redirect

from app.forms.flows.multistep_flow import RenderInfo, deserialize_session_data, serialize_session_data


class SteuerlotseStep(object):
    """An abstract step that provides default implementations of the handle functions"""
    name = None
    title = None
    title_multiple = None
    intro = None
    intro_multiple = None
    template = None
    session_data_identifier = 'form_data'

    def __init__(self, endpoint, header_title, overview_step, default_data, prev_step, next_step):
        self.endpoint = endpoint
        self.header_title = header_title
        self.overview_step = overview_step
        self._prev_step = prev_step
        self._next_step = next_step
        self.render_info: Optional[RenderInfo] = None

        self.default_data = default_data

        self.has_link_overview = request.args.get('link_overview', False) == 'True'

    def handle(self):
        stored_data = self._pre_handle()
        stored_data = self._main_handle(stored_data)
        return self._post_handle(stored_data)

    def _pre_handle(self):
        stored_data = self._get_session_data()
        self.render_info = RenderInfo(step_title=ngettext(self.title, self.title_multiple,
                                                          num=self.number_of_users(stored_data)
                                                          ) if self.title_multiple else self.title,
                                      step_intro=ngettext(self.intro, self.intro_multiple,
                                                          num=self.number_of_users(stored_data)
                                                          ) if self.intro_multiple else self.intro,
                                      form=None,
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

    def _get_session_data(self, session_data_identifier=None, ttl: Optional[int] = None):
        if session_data_identifier is None:
            session_data_identifier = self.session_data_identifier
        serialized_session = session.get(session_data_identifier, b"")

        if self.default_data:
            stored_data = self.default_data | deserialize_session_data(serialized_session,
                                                                       ttl)  # updates session_data only with non_existent values
        else:
            stored_data = deserialize_session_data(serialized_session, ttl)

        return stored_data

    def _override_session_data(self, stored_data, session_data_identifier=None):
        if session_data_identifier is None:
            session_data_identifier = self.session_data_identifier
        session[session_data_identifier] = serialize_session_data(stored_data)

    def _handle_redirects(self):
        if self.render_info.redirect_url:
            return redirect(self.render_info.redirect_url)

    def number_of_users(self, input_data=None):
        return 1

    def render(self, **kwargs):
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

    def __init__(self, form, endpoint, header_title, form_multiple=None, overview_step=None, default_data=None,
                 prev_step=None,
                 next_step=None, ):
        super(FormSteuerlotseStep, self).__init__(endpoint, header_title, overview_step, default_data, prev_step,
                                                  next_step)
        self.form = form
        self.form_multiple = form_multiple

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

        if self.form_multiple and self.number_of_users(prefilled_data) > 1:
            return self.form_multiple(form_data, **prefilled_data)

        return self.form(form_data, **prefilled_data)

    def render(self, **kwargs):
        """
        Renders a Form step. Use the render_info to provide all the needed data for rendering.
        """
        self.render_info.form.first_field = next(iter(self.render_info.form))
        return render_template(
            template_name_or_list=self.template,
            form=self.render_info.form,
            render_info=self.render_info,
            **kwargs
        )

    @staticmethod
    def _delete_dependent_data(stored_data: dict, pre_fixes:list=None, post_fixes:list=None):
        """This method filters the stored data. It deletes all the elements where the key includes the
        data_field_identifier. """
        filtered_data = stored_data
        if pre_fixes:
            filtered_data = dict(filter(lambda elem: not any([elem[0].startswith(data_field_prefix)
                                                              for data_field_prefix in pre_fixes]), filtered_data.items()))
        if post_fixes:
            filtered_data = dict(filter(lambda elem: not any([elem[0].endswith(data_field_postfix)
                                                              for data_field_postfix in post_fixes]), filtered_data.items()))
        return filtered_data


class DisplaySteuerlotseStep(SteuerlotseStep):

    def __init__(self, endpoint, header_title, overview_step=None, default_data=None, prev_step=None, next_step=None):
        super(DisplaySteuerlotseStep, self).__init__(endpoint, header_title, overview_step, default_data, prev_step,
                                                     next_step)

    def render(self, **kwargs):
        """
        Render a display step. Use the render_info to provide all the needed data for rendering.
        """
        return render_template(template_name_or_list=self.template, render_info=self.render_info, **kwargs)


class RedirectSteuerlotseStep(SteuerlotseStep):
    """
    This step is used only to perform a redirection. It acts a a placeholder step that can be used by the step chooser
    to return a SteuerlotseStep that should only redirect to another step.
    """

    def __init__(self, redirection_step_name, endpoint, header_title=None, overview_step=None, default_data=None,
                 prev_step=None, next_step=None):
        super(RedirectSteuerlotseStep, self).__init__(endpoint, header_title, overview_step, default_data, prev_step,
                                                      next_step)
        self.redirection_step_name = redirection_step_name

    def handle(self):
        # Override handle because this step should do nothing but redirect.
        # Therefore no _pre_handle or _post_handle are needed.
        return redirect(self.url_for_step(self.redirection_step_name))

    def render(self):
        pass
