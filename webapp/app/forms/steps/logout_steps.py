from flask_babel import _
from flask_wtf.csrf import generate_csrf

from app.forms import SteuerlotseBaseForm
from app.forms.steps.step import FormStep

from flask import render_template

from app.model.components import LogoutProps


class LogoutInputStep(FormStep):
    name = 'data_input'

    class Form(SteuerlotseBaseForm):
        pass

    def __init__(self, **kwargs):
        super(LogoutInputStep, self).__init__(
            title=_('form.logout.input-title'),
            intro=_('form.logout.input-intro'),
            form=self.Form,
            **kwargs)

    def render(self, data, render_info):
        props_dict = LogoutProps(
            form={
                'action': render_info.submit_url,
                'csrf_token': generate_csrf(),
            }
        ).camelized_dict()

        return render_template('react_component.html',
                               component='LogoutPage',
                               props=props_dict,
                               # TODO: These are still required by base.html to set the page title.
                               form=render_info.form,
                               header_title=_('form.logout.header-title'))
