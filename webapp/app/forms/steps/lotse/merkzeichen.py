from flask import render_template
from flask_wtf.csrf import generate_csrf
from flask_babel import lazy_gettext as _l, _
from wtforms import validators, BooleanField
from wtforms.validators import InputRequired

from app.forms import SteuerlotseBaseForm
from app.forms.fields import YesNoField, SteuerlotseIntegerField
from app.forms.steps.lotse.lotse_step import LotseFormSteuerlotseStep
from app.forms.steps.lotse_multistep_flow_steps.personal_data_steps import StepFamilienstand
from app.forms.steps.step import SectionLink
from app.forms.validations.validators import ValidDisabilityDegree
from app.model.components import MerkzeichenProps
from app.model.components.helpers import form_fields_dict


class StepMerkzeichenPersonA(LotseFormSteuerlotseStep):
    name = 'merkzeichen_person_a'
    title = _l('form.lotse.merkzeichen.title')
    intro = _l('form.lotse.merkzeichen.intro')
    header_title = _l('form.lotse.mandatory_data.header-title')

    label = _l('form.lotse.merkzeichen.label')
    section_link = SectionLink('mandatory_data', StepFamilienstand.name, _l('form.lotse.mandatory_data.label'))

    class InputForm(SteuerlotseBaseForm):
        person_a_has_pflegegrad = YesNoField(
            validators=[InputRequired(_('form.lotse.merkzeichen.person_a_has_pflegegrad.required'))],
            render_kw={'data_label': _l('form.lotse.merkzeichen.person_a_has_pflegegrad.data_label')})
        person_a_disability_degree = SteuerlotseIntegerField(
            validators=[ValidDisabilityDegree()],
            render_kw={'help': _l('form.lotse.field_person_beh_grad-help'),
                       'data_label': _l('form.lotse.merkzeichen.person_a_disability_degree')})
        person_a_has_merkzeichen_g = BooleanField(
            render_kw={'data_label': _l('form.lotse.merkzeichen.person_a_has_merkzeichen_g.data_label')})
        person_a_has_merkzeichen_ag = BooleanField(
            render_kw={'data_label': _l('form.lotse.merkzeichen.person_a_has_merkzeichen_ag.data_label')})
        person_a_has_merkzeichen_bl = BooleanField(
            render_kw={'data_label': _l('form.lotse.merkzeichen.person_a_has_merkzeichen_bl.data_label')})
        person_a_has_merkzeichen_tbl = BooleanField(
            render_kw={'data_label': _l('form.lotse.merkzeichen.person_a_has_merkzeichen_tbl.data_label')})
        person_a_has_merkzeichen_h = BooleanField(
            render_kw={'data_label': _l('form.lotse.merkzeichen.person_a_has_merkzeichen_h.data_label')})

        def validate_person_a_disability_degree(self, field):
            if self.person_a_has_merkzeichen_g.data or self.person_a_has_merkzeichen_ag.data:
                validators.InputRequired(_l('form.lotse.validation-disability_degree'))(self, field)
            else:
                validators.Optional()(self, field)

    @classmethod
    def get_label(cls, data):
        return cls.label

    def render(self):
        props_dict = MerkzeichenProps(
            step_header={
                'title': str(self.title),
                'intro': str(self.intro),
            },
            form={
                'action': self.render_info.submit_url,
                'csrf_token': generate_csrf(),
                'show_overview_button': bool(self.render_info.overview_url),
            },
            fields=form_fields_dict(self.render_info.form),
            prev_url=self.render_info.prev_url,
        ).camelized_dict()

        # Manually fix Humps error to camelize individual letters correctly.
        props_dict['fields']['personAHasPflegegrad'] = props_dict['fields'].pop('personA_hasPflegegrad')
        props_dict['fields']['personADisabilityDegree'] = props_dict['fields'].pop('personA_disabilityDegree')
        props_dict['fields']['personAHasMerkzeichenG'] = props_dict['fields'].pop('personA_hasMerkzeichenG')
        props_dict['fields']['personAHasMerkzeichenAg'] = props_dict['fields'].pop('personA_hasMerkzeichenAg')
        props_dict['fields']['personAHasMerkzeichenBl'] = props_dict['fields'].pop('personA_hasMerkzeichenBl')
        props_dict['fields']['personAHasMerkzeichenTbl'] = props_dict['fields'].pop('personA_hasMerkzeichenTbl')
        props_dict['fields']['personAHasMerkzeichenH'] = props_dict['fields'].pop('personA_hasMerkzeichenH')

        return render_template('react_component.html',
                               component='MerkzeichenPersonAPage',
                               props=props_dict,
                               form=self.render_info.form,
                               header_title=_('form.lotse.header-title'))
