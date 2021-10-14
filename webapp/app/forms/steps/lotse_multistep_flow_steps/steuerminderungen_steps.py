from app.forms import SteuerlotseBaseForm
from app.forms.steps.lotse.personal_data import show_person_b
from app.forms.steps.lotse_multistep_flow_steps.personal_data_steps import StepFamilienstand
from app.forms.steps.step import FormStep, SectionLink
from app.forms.fields import EntriesField, EuroField, SteuerlotseIntegerField

from flask import render_template
from flask_babel import _
from flask_babel import lazy_gettext as _l
from wtforms import RadioField
from wtforms.validators import InputRequired

from app.forms import SteuerlotseBaseForm
from app.forms.steps.step import FormStep, SectionLink


class StepSteuerminderungYesNo(FormStep):
    name = 'steuerminderung_yesno'
    label = _l('form.lotse.step_steuerminderung.label')
    section_link = SectionLink('section_steuerminderung', name, _l('form.lotse.section_steuerminderung.label'))

    class Form(SteuerlotseBaseForm):
        steuerminderung = RadioField(
            # Field overrides the label with a default value if we don't explicitly set it to an empty string
            label='',
            render_kw={'data_label': _l('form.lotse.field_steuerminderung.data_label'),
                       'hide_label': True},
            choices=[
                ('yes', _l('form.lotse.field_steuerminderung-yes')),
                ('no', _l('form.lotse.field_steuerminderung-no')),
            ],
            validators=[InputRequired()]
        )

    def __init__(self, **kwargs):
        super(StepSteuerminderungYesNo, self).__init__(
            title=_l('form.lotse.steuerminderung-title'),
            intro=_l('form.lotse.steuerminderung-intro'),
            form=self.Form,
            header_title=_('form.lotse.steuerminderungen.header-title'),
            template='basis/form_full_width.html',
            **kwargs,
        )
