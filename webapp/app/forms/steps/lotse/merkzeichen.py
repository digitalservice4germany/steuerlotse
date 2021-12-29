from flask import render_template
from flask_wtf.csrf import generate_csrf
from flask_babel import lazy_gettext as _l, _, ngettext
from pydantic import BaseModel, validator
from wtforms import validators, BooleanField
from wtforms.validators import InputRequired, ValidationError

from app.forms import SteuerlotseBaseForm
from app.forms.fields import YesNoField, SteuerlotseIntegerField
from app.forms.steps.lotse.lotse_step import LotseFormSteuerlotseStep
from app.forms.steps.lotse.personal_data import get_number_of_users, StepDisabilityPersonA, StepDisabilityPersonB
from app.forms.steps.lotse_multistep_flow_steps.personal_data_steps import StepFamilienstand
from app.forms.steps.step import SectionLink
from app.forms.validations.validators import ValidDisabilityDegree
from app.model.components import MerkzeichenProps
from app.model.components.helpers import form_fields_dict


class HasDisabilityPersonAPrecondition(BaseModel):
    _step_to_redirect_to = StepDisabilityPersonA.name
    _message_to_flash = _l('form.lotse.skip_reason.has_no_disability')

    person_a_has_disability: bool

    @validator('person_a_has_disability', always=True)
    def has_to_be_set_true(cls, v):
        if not v:
            raise ValidationError
        return v


class StepMerkzeichenPersonA(LotseFormSteuerlotseStep):
    name = 'merkzeichen_person_a'
    title = _l('form.lotse.merkzeichen_person_a.title')
    intro = _l('form.lotse.merkzeichen.intro')
    header_title = _l('form.lotse.mandatory_data.header-title')
    preconditions = [HasDisabilityPersonAPrecondition]

    label = _l('form.lotse.merkzeichen.label')
    section_link = SectionLink('mandatory_data', StepFamilienstand.name, _l('form.lotse.mandatory_data.label'))

    class InputForm(SteuerlotseBaseForm):
        person_a_has_pflegegrad = YesNoField(
            validators=[InputRequired(_l('form.lotse.merkzeichen.has_pflegegrad.required'))],
            render_kw={'data_label': _l('form.lotse.merkzeichen.has_pflegegrad.data_label')})
        person_a_disability_degree = SteuerlotseIntegerField(
            validators=[ValidDisabilityDegree()],
            render_kw={'help': _l('form.lotse.field_person_beh_grad-help'),
                       'data_label': _l('form.lotse.merkzeichen.disability_degree')})
        person_a_has_merkzeichen_g = BooleanField(
            render_kw={'data_label': _l('form.lotse.merkzeichen.has_merkzeichen_g.data_label')},
            name='person_a_has_merkzeichen_g')
        person_a_has_merkzeichen_ag = BooleanField(
            render_kw={'data_label': _l('form.lotse.merkzeichen.has_merkzeichen_ag.data_label')},
            name='person_a_has_merkzeichen_ag')
        person_a_has_merkzeichen_bl = BooleanField(
            render_kw={'data_label': _l('form.lotse.merkzeichen.has_merkzeichen_bl.data_label')},
            name='person_a_has_merkzeichen_bl')
        person_a_has_merkzeichen_tbl = BooleanField(
            render_kw={'data_label': _l('form.lotse.merkzeichen.has_merkzeichen_tbl.data_label')},
            name='person_a_has_merkzeichen_tbl')
        person_a_has_merkzeichen_h = BooleanField(
            render_kw={'data_label': _l('form.lotse.merkzeichen.has_merkzeichen_h.data_label')},
            name='person_a_has_merkzeichen_h')

        def validate_person_a_disability_degree(self, field):
            if self.person_a_has_merkzeichen_g.data or self.person_a_has_merkzeichen_ag.data:
                if self.person_a_has_merkzeichen_g.data:
                    input_required_message = _l('form.lotse.validation-disability_degree.merkzeichen_g_selected.required')
                else:
                    input_required_message = _l('form.lotse.validation-disability_degree.merkzeichen_ag_selected.required')
                validators.InputRequired(input_required_message)(self, field)
                if field.data and field.data < 20:
                    raise ValidationError(_l('form.lotse.validation-disability_degree.min20'))
            else:
                validators.Optional()(self, field)

    @classmethod
    def get_label(cls, data):
        return cls.label

    def _pre_handle(self):
        self._set_multiple_texts()
        super()._pre_handle()

    def _set_multiple_texts(self):
        number_of_users = get_number_of_users(self.stored_data)
        self.title = ngettext('form.lotse.merkzeichen_person_a.title',
                                               'form.lotse.merkzeichen_person_a.title',
                                               num=number_of_users)
        self.label = ngettext('form.lotse.merkzeichen_person_a.label',
                                               'form.lotse.merkzeichen_person_a.label',
                                               num=number_of_users)

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


class HasDisabilityPersonBPrecondition(BaseModel):
    _step_to_redirect_to = StepDisabilityPersonB.name
    _message_to_flash = _l('form.lotse.skip_reason.has_no_disability')

    person_b_has_disability: bool

    @validator('person_b_has_disability', always=True)
    def has_to_be_set_true(cls, v):
        if not v:
            raise ValidationError
        return v


class StepMerkzeichenPersonB(LotseFormSteuerlotseStep):
    name = 'merkzeichen_person_b'
    title = _l('form.lotse.merkzeichen_person_b.title')
    intro = _l('form.lotse.merkzeichen.intro')
    header_title = _l('form.lotse.mandatory_data.header-title')
    preconditions = [HasDisabilityPersonBPrecondition]

    label = _l('form.lotse.merkzeichen_person_b.label')
    section_link = SectionLink('mandatory_data', StepFamilienstand.name, _l('form.lotse.mandatory_data.label'))

    class InputForm(SteuerlotseBaseForm):
        person_b_has_pflegegrad = YesNoField(
            validators=[InputRequired(_('form.lotse.merkzeichen.has_pflegegrad.required'))],
            render_kw={'data_label': _l('form.lotse.merkzeichen.has_pflegegrad.data_label')})
        person_b_disability_degree = SteuerlotseIntegerField(
            validators=[ValidDisabilityDegree()],
            render_kw={'help': _l('form.lotse.field_person_beh_grad-help'),
                       'data_label': _l('form.lotse.merkzeichen.disability_degree')})
        person_b_has_merkzeichen_g = BooleanField(
            render_kw={'data_label': _l('form.lotse.merkzeichen.has_merkzeichen_g.data_label')},
            name='person_b_has_merkzeichen_g')
        person_b_has_merkzeichen_ag = BooleanField(
            render_kw={'data_label': _l('form.lotse.merkzeichen.has_merkzeichen_ag.data_label')},
            name='person_b_has_merkzeichen_ag')
        person_b_has_merkzeichen_bl = BooleanField(
            render_kw={'data_label': _l('form.lotse.merkzeichen.has_merkzeichen_bl.data_label')},
            name='person_b_has_merkzeichen_bl')
        person_b_has_merkzeichen_tbl = BooleanField(
            render_kw={'data_label': _l('form.lotse.merkzeichen.has_merkzeichen_tbl.data_label')},
            name='person_b_has_merkzeichen_tbl')
        person_b_has_merkzeichen_h = BooleanField(
            render_kw={'data_label': _l('form.lotse.merkzeichen.has_merkzeichen_h.data_label')},
            name='person_b_has_merkzeichen_h')

        def validate_person_b_disability_degree(self, field):
            if self.person_b_has_merkzeichen_g.data or self.person_b_has_merkzeichen_ag.data:
                input_required_message = _l('form.lotse.validation-disability_degree.merkzeichen_g_selected.required') if self.person_b_has_merkzeichen_g.data else _l('form.lotse.validation-disability_degree.merkzeichen_ag_selected.required')
                validators.InputRequired(input_required_message)(self, field)
                if field.data and field.data < 20:
                    raise ValidationError(_l('form.lotse.validation-disability_degree.min20'))
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
        props_dict['fields']['personBHasPflegegrad'] = props_dict['fields'].pop('personB_hasPflegegrad')
        props_dict['fields']['personBDisabilityDegree'] = props_dict['fields'].pop('personB_disabilityDegree')
        props_dict['fields']['personBHasMerkzeichenG'] = props_dict['fields'].pop('personB_hasMerkzeichenG')
        props_dict['fields']['personBHasMerkzeichenAg'] = props_dict['fields'].pop('personB_hasMerkzeichenAg')
        props_dict['fields']['personBHasMerkzeichenBl'] = props_dict['fields'].pop('personB_hasMerkzeichenBl')
        props_dict['fields']['personBHasMerkzeichenTbl'] = props_dict['fields'].pop('personB_hasMerkzeichenTbl')
        props_dict['fields']['personBHasMerkzeichenH'] = props_dict['fields'].pop('personB_hasMerkzeichenH')

        return render_template('react_component.html',
                               component='MerkzeichenPersonBPage',
                               props=props_dict,
                               form=self.render_info.form,
                               header_title=_('form.lotse.header-title'))
