from collections import namedtuple
from flask import render_template

SectionLink = namedtuple(
    typename='SectionLink',
    field_names=['name', 'beginning_step', 'label']
)

Section = namedtuple(
    typename='Section',
    field_names=['label', 'url', 'data']
)


class Step(object):
    """An abstract step that provides default `prev_step` and `next_step`
    implementations if these are provided during construction.
    """
    label: str = None
    section_link: SectionLink = None
    SKIP_COND = None

    def __init__(self, title, intro, prev_step=None, next_step=None, header_title=None):
        self.title = title
        self.intro = intro
        self._prev_step = prev_step
        self._next_step = next_step
        self.header_title = header_title

    def prev_step(self):
        if self._prev_step is None:
            raise NotImplementedError()
        else:
            return self._prev_step

    def next_step(self):
        if self.next_step is None:
            raise NotImplementedError()
        else:
            return self._next_step

    @classmethod
    def get_label(cls, data=None):
        return cls.label

    @classmethod
    def get_redirection_info_if_skipped(cls, input_data):
        if cls.SKIP_COND is None:
            return None, None

        for (skip_cond, fork_step_name, skip_reason) in cls.SKIP_COND:
            if all([input_data.get(field_key) == field_value_to_skip for field_key, field_value_to_skip in skip_cond]):
                return fork_step_name, skip_reason

        return None, None


class FormStep(Step):
    """A FormStep owns a wtform and knows how to create and render it. The template
    to use can be overidden and customised.
    """

    def __init__(self, title, form, intro=None, prev_step=None, next_step=None, header_title=None,
                 template='basis/form_full_width.html'):
        super(FormStep, self).__init__(title, intro, prev_step, next_step, header_title)
        self.form = form
        self.template = template

    def create_form(self, request, prefilled_data):
        # If `form_data` is present it will always override `data` during
        # value binding. For `BooleanFields` an empty/missing value in the `form_data`
        # will lead to an unchecked box.
        form_data = request.form
        if len(form_data) == 0:
            form_data = None

        form = self.form(form_data, **prefilled_data)
        return form

    def render(self, data, render_info):
        """
        :type data: Any
        :type render_info: RenderInfo

        Renders a Form step. Use the render_info to provide all the needed data for rendering.
        """
        render_info.form.first_field = next(iter(render_info.form))
        return render_template(
            template_name_or_list=self.template,
            form=render_info.form,
            render_info=render_info,
            header_title=self.header_title
        )


class DisplayStep(Step):
    """The DisplayStep usually shows data that is not interactive (except from links)."""

    def __init__(self, title, intro=None, prev_step=None, next_step=None):
        super(DisplayStep, self).__init__(title, intro, prev_step, next_step)

    def render(self, data, render_info):
        """
        Renders a display step. Use the render_info to provide all the needed data for rendering.

        :type data: Any
        :type render_info: RenderInfo
        """
        raise NotImplementedError()
