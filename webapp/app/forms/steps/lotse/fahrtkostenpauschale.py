

from flask import render_template
from flask_babel import lazy_gettext as _l, ngettext, _
from pydantic import root_validator
from wtforms.validators import InputRequired, ValidationError
from wtforms import SelectField
from flask_wtf.csrf import generate_csrf

from app.forms.steps.lotse.has_disability import HasDisabilityPersonAPrecondition, HasDisabilityPersonBPrecondition
from app.forms.steps.lotse.merkzeichen import HasMerkzeichenPersonAPrecondition, HasMerkzeichenPersonBPrecondition, \
    StepMerkzeichenPersonA, StepMerkzeichenPersonB
from app.forms.steps.lotse.personal_data import ShowPersonBPrecondition
from app.forms.steps.lotse.utils import get_number_of_users
from app.forms.steps.lotse_multistep_flow_steps.personal_data_steps import StepFamilienstand
from app.model.components import FahrtkostenpauschaleProps
from app.model.components.helpers import form_fields_dict
from app.forms import SteuerlotseBaseForm
from app.forms.steps.step import SectionLink
from app.forms.steps.lotse.lotse_step import LotseFormSteuerlotseStep
from app.model.disability_data import DisabilityModel


def calculate_fahrtkostenpauschale(has_pflegegrad: str = None, disability_degree: int = None,
                                  has_merkzeichen_bl: bool = False, has_merkzeichen_tbl: bool = False,
                                  has_merkzeichen_h: bool = False, has_merkzeichen_ag: bool = False,
                                  has_merkzeichen_g: bool = False):

    if has_pflegegrad == 'yes' or has_merkzeichen_bl or has_merkzeichen_tbl or has_merkzeichen_tbl \
            or has_merkzeichen_h or has_merkzeichen_ag:
        return 4500
    elif disability_degree is not None and (disability_degree >= 80 or (has_merkzeichen_g and disability_degree >= 70)):
        return 900

    return 0


class HasFahrtkostenpauschaleClaimPersonAPrecondition(DisabilityModel):
    _step_to_redirect_to = StepMerkzeichenPersonA.name
    _message_to_flash = _l('form.lotse.skip_reason.has_fahrtkostenpauschale_claim')

    @root_validator(skip_on_failure=True)
    def has_to_have_fahrtkostenpauschale_not_0(cls, values):
        fahrtkostenpauschale_claim = calculate_fahrtkostenpauschale(
            has_pflegegrad=values.get('person_a_has_pflegegrad', None),
            disability_degree=values.get('person_a_disability_degree', None),
            has_merkzeichen_bl=values.get('person_a_has_merkzeichen_bl', False),
            has_merkzeichen_tbl=values.get('person_a_has_merkzeichen_tbl', False),
            has_merkzeichen_h=values.get('person_a_has_merkzeichen_h', False),
            has_merkzeichen_ag=values.get('person_a_has_merkzeichen_ag', False),
            has_merkzeichen_g=values.get('person_a_has_merkzeichen_g', False)
        )

        if fahrtkostenpauschale_claim == 0:
            raise ValidationError
        return values


class HasFahrtkostenpauschaleClaimPersonBPrecondition(DisabilityModel):
    _step_to_redirect_to = StepMerkzeichenPersonB.name
    _message_to_flash = _l('form.lotse.skip_reason.has_fahrtkostenpauschale_claim')

    @root_validator(skip_on_failure=True)
    def has_to_have_fahrtkostenpauschale_not_0(cls, values):
        fahrtkostenpauschale_claim = calculate_fahrtkostenpauschale(
            has_pflegegrad=values.get('person_b_has_pflegegrad', None),
            disability_degree=values.get('person_b_disability_degree', None),
            has_merkzeichen_bl=values.get('person_b_has_merkzeichen_bl', False),
            has_merkzeichen_tbl=values.get('person_b_has_merkzeichen_tbl', False),
            has_merkzeichen_h=values.get('person_b_has_merkzeichen_h', False),
            has_merkzeichen_ag=values.get('person_b_has_merkzeichen_ag', False),
            has_merkzeichen_g=values.get('person_b_has_merkzeichen_g', False)
        )

        if fahrtkostenpauschale_claim == 0:
            raise ValidationError
        return values


class StepFahrtkostenpauschale(LotseFormSteuerlotseStep):

    def get_overview_value_representation(self, value, stored_data=None):
        result = None

        if value == 'yes':
            result = str(self.get_fahrtkostenpauschale(stored_data)) + ' ' + _('currency.euro')
        elif value == 'no':
            result = _('form.lotse.summary.not-requested')

        return result

    def get_fahrtkostenpauschale(self, form_data):
        """
            Get the amount of Fahrtkostenpauschale for this step. Should be implemented for each step.
        """
        pass


class StepFahrtkostenpauschalePersonA(StepFahrtkostenpauschale):
    name = 'person_a_requests_fahrtkostenpauschale'
    section_link = SectionLink('mandatory_data', StepFamilienstand.name, _l(
        'form.lotse.mandatory_data.label'))

    preconditions = [HasDisabilityPersonAPrecondition, HasMerkzeichenPersonAPrecondition, HasFahrtkostenpauschaleClaimPersonAPrecondition]

    class InputForm(SteuerlotseBaseForm):
        person_a_requests_fahrtkostenpauschale = SelectField(
            choices=[('yes', 'yes'), ('no', 'no')],
            render_kw={'data_label':  _l(
                'form.lotse.request_fahrtkostenpauschale.data_label')},
            validators=[InputRequired(_l('validate.input-required'))])

    @classmethod
    def get_label(cls, data=None):
        return ngettext('form.lotse.person_a.request_fahrtkostenpauschale.label', 'form.lotse.person_a.request_fahrtkostenpauschale.label',
                        num=get_number_of_users(data))

    def render(self):
        props_dict = FahrtkostenpauschaleProps(
            step_header={
                'title': ngettext('form.lotse.person_a.request_fahrtkostenpauschale.title', 'form.lotse.person_a.request_fahrtkostenpauschale.title',
                                  num=get_number_of_users(self.stored_data))
            },
            form={
                'action': self.render_info.submit_url,
                'csrf_token': generate_csrf(),
                'show_overview_button': bool(self.render_info.overview_url),
            },
            fahrtkostenpauschale_amount=self.get_fahrtkostenpauschale(self.stored_data),
            fields=form_fields_dict(self.render_info.form),
            prev_url=self.render_info.prev_url
        ).camelized_dict()

        return render_template('react_component.html',
                               component='FahrtkostenpauschalePersonAPage',
                               props=props_dict,
                               form=self.render_info.form,
                               header_title=_('form.lotse.header-title'))

    def get_fahrtkostenpauschale(self, stored_data):
        return calculate_fahrtkostenpauschale(
            has_pflegegrad=stored_data.get('person_a_has_pflegegrad', False),
            disability_degree=stored_data.get('person_a_disability_degree', None),
            has_merkzeichen_bl=stored_data.get('person_a_has_merkzeichen_bl', False),
            has_merkzeichen_tbl=stored_data.get('person_a_has_merkzeichen_tbl', False),
            has_merkzeichen_h=stored_data.get('person_a_has_merkzeichen_h', False),
            has_merkzeichen_ag=stored_data.get('person_a_has_merkzeichen_ag', False),
            has_merkzeichen_g=stored_data.get('person_a_has_merkzeichen_g', False)
        )


class StepFahrtkostenpauschalePersonB(StepFahrtkostenpauschale):
    name = 'person_b_requests_fahrtkostenpauschale'
    section_link = SectionLink('mandatory_data', StepFamilienstand.name, _l(
        'form.lotse.mandatory_data.label'))

    label = _l('form.lotse.person_b.request_fahrtkostenpauschale.label')
    preconditions = [ShowPersonBPrecondition, HasDisabilityPersonBPrecondition, HasMerkzeichenPersonBPrecondition, HasFahrtkostenpauschaleClaimPersonBPrecondition]

    class InputForm(SteuerlotseBaseForm):
        person_b_requests_fahrtkostenpauschale = SelectField(
            choices=[('yes', 'yes'), ('no', 'no')],
            render_kw={'data_label':  _l(
                'form.lotse.request_fahrtkostenpauschale.data_label')},
            validators=[InputRequired(_l('validate.input-required'))])

    @classmethod
    def get_label(cls, data):
        return cls.label

    def render(self):
        props_dict = FahrtkostenpauschaleProps(
            step_header={
                'title': _('form.lotse.person_b.request_fahrtkostenpauschale.title')
            },
            form={
                'action': self.render_info.submit_url,
                'csrf_token': generate_csrf(),
                'show_overview_button': bool(self.render_info.overview_url),
            },
            fahrtkostenpauschale_amount=self.get_fahrtkostenpauschale(self.stored_data),
            fields=form_fields_dict(self.render_info.form),
            prev_url=self.render_info.prev_url
        ).camelized_dict()

        return render_template('react_component.html',
                               component='FahrtkostenpauschalePersonBPage',
                               props=props_dict,
                               form=self.render_info.form,
                               header_title=_('form.lotse.header-title'))

    def get_fahrtkostenpauschale(self, form_data):
        return calculate_fahrtkostenpauschale(
            has_pflegegrad=form_data.get('person_b_has_pflegegrad', False),
            disability_degree=form_data.get('person_b_disability_degree', None),
            has_merkzeichen_bl=form_data.get('person_b_has_merkzeichen_bl', False),
            has_merkzeichen_tbl=form_data.get('person_b_has_merkzeichen_tbl', False),
            has_merkzeichen_h=form_data.get('person_b_has_merkzeichen_h', False),
            has_merkzeichen_ag=form_data.get('person_b_has_merkzeichen_ag', False),
            has_merkzeichen_g=form_data.get('person_b_has_merkzeichen_g', False)
        )