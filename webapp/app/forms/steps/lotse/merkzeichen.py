from flask import render_template
from flask_wtf.csrf import generate_csrf
from flask_babel import lazy_gettext as _l, _, ngettext
from wtforms import validators
from wtforms.validators import InputRequired, ValidationError

from app.forms import SteuerlotseBaseForm
from app.forms.fields import YesNoField, SteuerlotseIntegerField, MerkzeichenBooleanField
from app.forms.steps.lotse.lotse_step import LotseFormSteuerlotseStep
from app.forms.steps.lotse.utils import get_number_of_users
from app.forms.steps.lotse.has_disability import HasDisabilityPersonAPrecondition, \
    HasDisabilityPersonBPrecondition
from app.forms.steps.lotse_multistep_flow_steps.personal_data_steps import StepFamilienstand
from app.forms.steps.step import SectionLink
from app.forms.validations.validators import ValidDisabilityDegree
from app.model.components import MerkzeichenProps
from app.model.components.helpers import form_fields_dict


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
        person_a_has_merkzeichen_g = MerkzeichenBooleanField(
            render_kw={'data_label': _l('form.lotse.merkzeichen.has_merkzeichen_g.data_label')})
        person_a_has_merkzeichen_ag = MerkzeichenBooleanField(
            render_kw={'data_label': _l('form.lotse.merkzeichen.has_merkzeichen_ag.data_label')})
        person_a_has_merkzeichen_bl = MerkzeichenBooleanField(
            render_kw={'data_label': _l('form.lotse.merkzeichen.has_merkzeichen_bl.data_label')})
        person_a_has_merkzeichen_tbl = MerkzeichenBooleanField(
            render_kw={'data_label': _l('form.lotse.merkzeichen.has_merkzeichen_tbl.data_label')})
        person_a_has_merkzeichen_h = MerkzeichenBooleanField(
            render_kw={'data_label': _l('form.lotse.merkzeichen.has_merkzeichen_h.data_label')})

        def validate_person_a_disability_degree(self, field):
            if self.person_a_has_merkzeichen_g.data:
                validators.InputRequired(_l('form.lotse.validation-disability_degree.merkzeichen_g_selected.required'))(self, field)

                if field.data and field.data < 20:
                    raise ValidationError(_l('form.lotse.merkzeichen_g_selected.validation-disability_degree.min20'))
            elif self.person_a_has_merkzeichen_ag.data:
                validators.InputRequired(_l('form.lotse.validation-disability_degree.merkzeichen_ag_selected.required'))(self, field)

                if field.data and field.data < 20:
                    raise ValidationError(_l('form.lotse.merkzeichen_ag_selected.validation-disability_degree.min20'))
            else:
                validators.Optional()(self, field)
                if field.data and 0 < field.data < 20:
                    raise ValidationError(_l('form.lotse.validation-disability_degree.min20'))
                

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

        return render_template('react_component.html',
                               component='MerkzeichenPersonAPage',
                               props=props_dict,
                               form=self.render_info.form,
                               header_title=_('form.lotse.header-title'))


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
            validators=[InputRequired(_l('form.lotse.merkzeichen.has_pflegegrad.required'))],
            render_kw={'data_label': _l('form.lotse.merkzeichen.has_pflegegrad.data_label')})
        person_b_disability_degree = SteuerlotseIntegerField(
            validators=[ValidDisabilityDegree()],
            render_kw={'help': _l('form.lotse.field_person_beh_grad-help'),
                       'data_label': _l('form.lotse.merkzeichen.disability_degree')})
        person_b_has_merkzeichen_g = MerkzeichenBooleanField(
            render_kw={'data_label': _l('form.loMerkzeichenBooleanFieldtse.merkzeichen.has_merkzeichen_g.data_label')})
        person_b_has_merkzeichen_ag = MerkzeichenBooleanField(
            render_kw={'data_label': _l('form.lotse.merkzeichen.has_merkzeichen_ag.data_label')})
        person_b_has_merkzeichen_bl = MerkzeichenBooleanField(
            render_kw={'data_label': _l('form.lotse.merkzeichen.has_merkzeichen_bl.data_label')})
        person_b_has_merkzeichen_tbl = MerkzeichenBooleanField(
            render_kw={'data_label': _l('form.lotse.merkzeichen.has_merkzeichen_tbl.data_label')})
        person_b_has_merkzeichen_h = MerkzeichenBooleanField(
            render_kw={'data_label': _l('form.lotse.merkzeichen.has_merkzeichen_h.data_label')})

        def validate_person_b_disability_degree(self, field):
            if self.person_b_has_merkzeichen_g.data:
                validators.InputRequired(_l('form.lotse.validation-disability_degree.merkzeichen_g_selected.required'))(self, field)

                if field.data and field.data < 20:
                    raise ValidationError(_l('form.lotse.merkzeichen_g_selected.validation-disability_degree.min20'))
            elif self.person_b_has_merkzeichen_ag.data:
                validators.InputRequired(_l('form.lotse.validation-disability_degree.merkzeichen_ag_selected.required'))(self, field)

                if field.data and field.data < 20:
                    raise ValidationError(_l('form.lotse.merkzeichen_ag_selected.validation-disability_degree.min20'))
            else:
                validators.Optional()(self, field)
                if field.data and 0 < field.data < 20:
                    raise ValidationError(_l('form.lotse.validation-disability_degree.min20'))

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

        return render_template('react_component.html',
                               component='MerkzeichenPersonBPage',
                               props=props_dict,
                               form=self.render_info.form,
                               header_title=_('form.lotse.header-title'))
