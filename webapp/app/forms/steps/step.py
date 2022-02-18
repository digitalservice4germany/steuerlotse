from collections import namedtuple
from flask import render_template, request

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

    # Override this function, to manipulate the overview value
    def get_overview_value_representation(self, value, stored_data=None):
        return value


class FormStep(Step):
    """A FormStep owns a wtform and knows how to create and render it. The template
    to use can be overidden and customised.
    """
    disable_extended_footer = True

    def __init__(self, title, form, intro=None, prev_step=None, next_step=None, header_title=None,
                 template='basis/form_full_width.html'):
        super(FormStep, self).__init__(title, intro, prev_step, next_step, header_title)
        self.form = form
        self.template = template

    def create_form(self, form_data=None, prefilled_data=None):
        # Form_data is only present because the FormStep should work similar to the newer SteuerlotseSteps as they will
        # be replaced one by one.

        extracted_form_data = request.form  # Override the form_data because the multistep flow does not set it
        if len(extracted_form_data) == 0:
            extracted_form_data = None

        form = self.form(extracted_form_data, **prefilled_data)
        return form

    def render(self, data, render_info):
        """
        :type data: Any
        :type render_info: RenderInfo

        Renders a Form step. Use the render_info to provide all the needed data for rendering.
        """
        render_info.additional_info['disable_extended_footer'] = self.disable_extended_footer
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
