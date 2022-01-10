

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
from app.model.components import FahrkostenpauschaleProps
from app.model.components.helpers import form_fields_dict
from app.forms import SteuerlotseBaseForm
from app.forms.steps.step import SectionLink
from app.forms.steps.lotse.lotse_step import LotseFormSteuerlotseStep
from app.model.disability_data import DisabilityModel


def calculate_fahrkostenpauschale(has_pflegegrad: str = None, disability_degree: int = None,
                                  has_merkzeichen_bl: bool = False, has_merkzeichen_tbl: bool = False,
                                  has_merkzeichen_h: bool = False, has_merkzeichen_ag: bool = False,
                                  has_merkzeichen_g: bool = False):

    if has_pflegegrad == 'yes' or has_merkzeichen_bl or has_merkzeichen_tbl or has_merkzeichen_tbl \
            or has_merkzeichen_h or has_merkzeichen_ag:
        return 4500
    elif disability_degree is not None and (disability_degree >= 80 or (has_merkzeichen_g and disability_degree >= 70)):
        return 900

    return 0


class HasFahrkostenpauschaleClaimPersonAPrecondition(DisabilityModel):
    _step_to_redirect_to = StepMerkzeichenPersonA.name
    _message_to_flash = _l('form.lotse.skip_reason.has_fahrkostenpauschale_claim')

    @root_validator(skip_on_failure=True)
    def has_to_have_fahrkostenpauschale_not_0(cls, values):
        fahrkostenpauschale_claim = calculate_fahrkostenpauschale(
            has_pflegegrad=values.get('person_a_has_pflegegrad', None),
            disability_degree=values.get('person_a_disability_degree', None),
            has_merkzeichen_bl=values.get('person_a_has_merkzeichen_bl', False),
            has_merkzeichen_tbl=values.get('person_a_has_merkzeichen_bl', False),
            has_merkzeichen_h=values.get('person_a_has_merkzeichen_bl', False),
            has_merkzeichen_ag=values.get('person_a_has_merkzeichen_tbl', False),
            has_merkzeichen_g=values.get('person_a_has_merkzeichen_h', False)
        )

        if fahrkostenpauschale_claim == 0:
            raise ValidationError
        return values


class HasFahrkostenpauschaleClaimPersonBPrecondition(DisabilityModel):
    _step_to_redirect_to = StepMerkzeichenPersonB.name
    _message_to_flash = _l('form.lotse.skip_reason.has_fahrkostenpauschale_claim')

    @root_validator(skip_on_failure=True)
    def has_to_have_fahrkostenpauschale_not_0(cls, values):
        fahrkostenpauschale_claim = calculate_fahrkostenpauschale(
            has_pflegegrad=values.get('person_b_has_pflegegrad', None),
            disability_degree=values.get('person_b_disability_degree', None),
            has_merkzeichen_bl=values.get('person_b_has_merkzeichen_bl', False),
            has_merkzeichen_tbl=values.get('person_b_has_merkzeichen_tbl', False),
            has_merkzeichen_h=values.get('person_b_has_merkzeichen_h', False),
            has_merkzeichen_ag=values.get('person_b_has_merkzeichen_ag', False),
            has_merkzeichen_g=values.get('person_b_has_merkzeichen_g', False)
        )

        if fahrkostenpauschale_claim == 0:
            raise ValidationError
        return values


class StepFahrkostenpauschale(LotseFormSteuerlotseStep):

    def get_overview_value_representation(self, value):
        result = None

        if value == 'yes':
            result = str(self.get_fahrkostenpauschale()) + ' ' + _('currency.euro')
        elif value == 'no':
            result = _('form.lotse.summary.not-requested')

        return result

    def get_fahrkostenpauschale(self):
        """
            Get the amount of Fahrkostenpauschale for this step. Should be implemented for each step.
        """
        pass


class StepFahrkostenpauschalePersonA(StepFahrkostenpauschale):
    name = 'person_a_requests_fahrkostenpauschale'
    section_link = SectionLink('mandatory_data', StepFamilienstand.name, _l(
        'form.lotse.mandatory_data.label'))

    preconditions = [HasDisabilityPersonAPrecondition, HasMerkzeichenPersonAPrecondition, HasFahrkostenpauschaleClaimPersonAPrecondition]

    class InputForm(SteuerlotseBaseForm):
        person_a_requests_fahrkostenpauschale = SelectField(
            choices=[('yes', 'yes'), ('no', 'no')],
            render_kw={'data_label':  _l(
                'form.lotse.request_fahrkostenpauschale.data_label')},
            validators=[InputRequired(_l('validate.input-required'))])

    @classmethod
    def get_label(cls, data=None):
        return ngettext('form.lotse.person_a.request_fahrkostenpauschale.label', 'form.lotse.person_a.request_fahrkostenpauschale.label',
                        num=get_number_of_users(data))

    def render(self):
        props_dict = FahrkostenpauschaleProps(
            step_header={
                'title': ngettext('form.lotse.person_a.request_fahrkostenpauschale.title', 'form.lotse.person_a.request_fahrkostenpauschale.title',
                                  num=get_number_of_users(self.stored_data))
            },
            form={
                'action': self.render_info.submit_url,
                'csrf_token': generate_csrf(),
                'show_overview_button': bool(self.render_info.overview_url),
            },
            fahrkostenpauschale_amount=self.get_fahrkostenpauschale(),
            fields=form_fields_dict(self.render_info.form),
            prev_url=self.render_info.prev_url
        ).camelized_dict()

        return render_template('react_component.html',
                               component='FahrkostenpauschalePersonAPage',
                               props=props_dict,
                               form=self.render_info.form,
                               header_title=_('form.lotse.header-title'))

    def get_fahrkostenpauschale(self):
        return calculate_fahrkostenpauschale(
            has_pflegegrad=self.stored_data.get('person_a_has_pflegegrad', False),
            disability_degree=self.stored_data.get('person_a_disability_degree', None),
            has_merkzeichen_bl=self.stored_data.get('person_a_has_merkzeichen_bl', False),
            has_merkzeichen_tbl=self.stored_data.get('person_a_has_merkzeichen_tbl', False),
            has_merkzeichen_h=self.stored_data.get('person_a_has_merkzeichen_h', False),
            has_merkzeichen_ag=self.stored_data.get('person_a_has_merkzeichen_ag', False),
            has_merkzeichen_g=self.stored_data.get('person_a_has_merkzeichen_g', False)
        )


class StepFahrkostenpauschalePersonB(StepFahrkostenpauschale):
    name = 'person_b_requests_fahrkostenpauschale'
    section_link = SectionLink('mandatory_data', StepFamilienstand.name, _l(
        'form.lotse.mandatory_data.label'))

    label = _l('form.lotse.person_b.request_fahrkostenpauschale.label')
    preconditions = [ShowPersonBPrecondition, HasDisabilityPersonBPrecondition, HasMerkzeichenPersonBPrecondition, HasFahrkostenpauschaleClaimPersonBPrecondition]

    class InputForm(SteuerlotseBaseForm):
        person_b_requests_fahrkostenpauschale = SelectField(
            choices=[('yes', 'yes'), ('no', 'no')],
            render_kw={'data_label':  _l(
                'form.lotse.request_fahrkostenpauschale.data_label')},
            validators=[InputRequired(_l('validate.input-required'))])

    @classmethod
    def get_label(cls, data):
        return cls.label

    def render(self):
        props_dict = FahrkostenpauschaleProps(
            step_header={
                'title': _('form.lotse.person_b.request_fahrkostenpauschale.title')
            },
            form={
                'action': self.render_info.submit_url,
                'csrf_token': generate_csrf(),
                'show_overview_button': bool(self.render_info.overview_url),
            },
            fahrkostenpauschale_amount=self.get_fahrkostenpauschale(),
            fields=form_fields_dict(self.render_info.form),
            prev_url=self.render_info.prev_url
        ).camelized_dict()

        return render_template('react_component.html',
                               component='FahrkostenpauschalePersonBPage',
                               props=props_dict,
                               form=self.render_info.form,
                               header_title=_('form.lotse.header-title'))

    def get_fahrkostenpauschale(self):
        return calculate_fahrkostenpauschale(
            has_pflegegrad=self.stored_data.get('person_b_has_pflegegrad', False),
            disability_degree=self.stored_data.get('person_b_disability_degree', None),
            has_merkzeichen_bl=self.stored_data.get('person_b_has_merkzeichen_bl', False),
            has_merkzeichen_tbl=self.stored_data.get('person_b_has_merkzeichen_tbl', False),
            has_merkzeichen_h=self.stored_data.get('person_b_has_merkzeichen_h', False),
            has_merkzeichen_ag=self.stored_data.get('person_b_has_merkzeichen_ag', False),
            has_merkzeichen_g=self.stored_data.get('person_b_has_merkzeichen_g', False)
        )