from typing import Optional

from flask import render_template
from flask_babel import lazy_gettext as _l, ngettext, _
from pydantic import validator, root_validator
from pydantic.main import BaseModel
from wtforms.validators import InputRequired, ValidationError
from wtforms import SelectField
from flask_wtf.csrf import generate_csrf

from app.forms.steps.lotse.merkzeichen import StepMerkzeichenPersonA, StepMerkzeichenPersonB
from app.forms.steps.lotse.fahrkostenpauschbetrag import calculate_fahrkostenpauschbetrag
from app.model.components import PauschbetragProps
from app.model.components.helpers import form_fields_dict
from app.forms import SteuerlotseBaseForm
from app.forms.steps.step import SectionLink
from app.forms.steps.lotse.lotse_step import LotseFormSteuerlotseStep
from app.forms.steps.lotse.personal_data import ShowPersonBPrecondition, StepFamilienstand
from app.forms.steps.lotse.merkzeichen import StepMerkzeichenPersonA, StepMerkzeichenPersonB
from app.forms.steps.lotse.utils import get_number_of_users
from app.forms.steps.lotse.has_disability import HasDisabilityPersonAPrecondition, HasDisabilityPersonBPrecondition

from app.model.components import NoPauschbetragProps


def calculate_pauschbetrag(has_pflegegrad=None, disability_degree=None, has_merkzeichen_bl=False, has_merkzeichen_tbl=False, has_merkzeichen_h=False):
    """
    Calculates the pauschbetrag given some information about the user.

    :param has_pflegegrad: A str indicating whether the user has a "Pflegegrad" of 4 or 5 ('yes' or 'no')
    :param disability_degree: An integer indicating the disability degree of the user. Must be between 20 and 100
    :param has_merkzeichen_bl: A boolean indicating whether the user has the Merkzeichen Bl
    :param has_merkzeichen_tbl: A boolean indicating whether the user has the Merkzeichen TBl
    :param has_merkzeichen_h: A boolean indicating whether the user has the Merkzeichen H
    """
    if has_pflegegrad == 'yes' or has_merkzeichen_bl or has_merkzeichen_tbl or has_merkzeichen_h:
        return 7400
    
    if disability_degree is None:
        return 0
    if disability_degree == 100:
        return 2840
    elif disability_degree >= 90:
        return 2460
    elif disability_degree >= 80:
        return 2120
    elif disability_degree >= 70:
        return 1780
    elif disability_degree >= 60:
        return 1440
    elif disability_degree >= 50:
        return 1140
    elif disability_degree >= 40:
        return 860
    elif disability_degree >= 30:
        return 620
    elif disability_degree >= 20:
        return 384

    return 0


class DisabilityModel(BaseModel):
    person_a_has_disability: Optional[str]
    person_a_has_pflegegrad: Optional[str]
    person_a_disability_degree: Optional[int]
    person_a_has_merkzeichen_bl: Optional[bool]
    person_a_has_merkzeichen_tbl: Optional[bool]
    person_a_has_merkzeichen_g: Optional[bool]
    person_a_has_merkzeichen_ag: Optional[bool]
    person_a_has_merkzeichen_h: Optional[bool]

    person_b_has_disability: Optional[str]
    person_b_has_pflegegrad: Optional[str]
    person_b_disability_degree: Optional[int]
    person_b_has_merkzeichen_bl: Optional[bool]
    person_b_has_merkzeichen_tbl: Optional[bool]
    person_b_has_merkzeichen_g: Optional[bool]
    person_b_has_merkzeichen_ag: Optional[bool]
    person_b_has_merkzeichen_h: Optional[bool]

    @root_validator()
    def convert_disability_degree_to_int(cls, values):
        values['person_a_disability_degree'] = int(values['person_a_disability_degree']) \
            if values['person_a_disability_degree'] \
            else None
        values['person_b_disability_degree'] = int(values['person_b_disability_degree']) \
            if values['person_b_disability_degree'] \
            else None
        return values


class HasPauschbetragClaimPersonAPrecondition(DisabilityModel):
    _step_to_redirect_to = StepMerkzeichenPersonA.name
    _message_to_flash = _l('form.lotse.skip_reason.has_no_pauschbetrag_claim')

    @root_validator(skip_on_failure=True)
    def has_to_have_pauschbetrag_not_0(cls, values):
        pauschbetrag_claim = calculate_pauschbetrag(
            has_pflegegrad=values.get('person_a_has_pflegegrad', None),
            disability_degree=values.get('person_a_disability_degree', None),
            has_merkzeichen_bl=values.get('person_a_has_merkzeichen_bl', False),
            has_merkzeichen_tbl=values.get('person_a_has_merkzeichen_tbl', False),
            has_merkzeichen_h=values.get('person_a_has_merkzeichen_h', False)
        )

        if pauschbetrag_claim == 0:
            raise ValidationError
        return values


class HasPauschbetragClaimPersonBPrecondition(DisabilityModel):
    _step_to_redirect_to = StepMerkzeichenPersonB.name
    _message_to_flash = _l('form.lotse.skip_reason.has_no_pauschbetrag_claim')

    @root_validator(skip_on_failure=True)
    def has_to_have_pauschbetrag_not_0(cls, values):
        pauschbetrag_claim = calculate_pauschbetrag(
            has_pflegegrad=values.get('person_b_has_pflegegrad', None),
            disability_degree=values.get('person_b_disability_degree', None),
            has_merkzeichen_bl=values.get('person_b_has_merkzeichen_bl', False),
            has_merkzeichen_tbl=values.get('person_b_has_merkzeichen_tbl', False),
            has_merkzeichen_h=values.get('person_b_has_merkzeichen_h', False)
        )

        if pauschbetrag_claim == 0:
            raise ValidationError
        return values


class HasNoPauschbetragOrFahrkostenpauschbetragClaimPersonAPrecondition(DisabilityModel):
    _step_to_redirect_to = StepMerkzeichenPersonA.name
    _message_to_flash = _l('form.lotse.skip_reason.has_pauschbetrag_claim')

    @root_validator(skip_on_failure=True)
    def has_to_have_pauschbetrag_and_fahrkostenpauschbetrag_not_0(cls, values):
        pauschbetrag_claim = calculate_pauschbetrag(
            has_pflegegrad=values.get('person_a_has_pflegegrad', None),
            disability_degree=values.get('person_a_disability_degree', None),
            has_merkzeichen_bl=values.get('person_a_has_merkzeichen_bl', False),
            has_merkzeichen_tbl=values.get('person_a_has_merkzeichen_tbl', False),
            has_merkzeichen_h=values.get('person_a_has_merkzeichen_h', False)
        )
        fahrkostenpauschbetrag_claim = calculate_fahrkostenpauschbetrag(
            has_pflegegrad=values.get('person_a_has_pflegegrad', None),
            disability_degree=values.get('person_a_disability_degree', None),
            has_merkzeichen_bl=values.get('person_a_has_merkzeichen_bl', False),
            has_merkzeichen_tbl=values.get('person_a_has_merkzeichen_bl', False),
            has_merkzeichen_h=values.get('person_a_has_merkzeichen_bl', False),
            has_merkzeichen_ag=values.get('person_a_has_merkzeichen_tbl', False),
            has_merkzeichen_g=values.get('person_a_has_merkzeichen_h', False)
        )

        if pauschbetrag_claim != 0 or fahrkostenpauschbetrag_claim != 0:
            raise ValidationError
        return values


class HasNoPauschbetragOrFahrkostenpauschbetragClaimPersonBPrecondition(DisabilityModel):
    _step_to_redirect_to = StepMerkzeichenPersonB.name
    _message_to_flash = _l('form.lotse.skip_reason.has_pauschbetrag_claim')

    @root_validator(skip_on_failure=True)
    def has_to_have_pauschbetrag_and_fahrkostenpauschbetrag_not_0(cls, values):
        pauschbetrag_claim = calculate_pauschbetrag(
            has_pflegegrad=values.get('person_b_has_pflegegrad', None),
            disability_degree=values.get('person_b_disability_degree', None),
            has_merkzeichen_bl=values.get('person_b_has_merkzeichen_bl', False),
            has_merkzeichen_tbl=values.get('person_b_has_merkzeichen_tbl', False),
            has_merkzeichen_h=values.get('person_b_has_merkzeichen_h', False)
        )
        fahrkostenpauschbetrag_claim = calculate_fahrkostenpauschbetrag(
            has_pflegegrad=values.get('person_b_has_pflegegrad', None),
            disability_degree=values.get('person_b_disability_degree', None),
            has_merkzeichen_bl=values.get('person_b_has_merkzeichen_bl', False),
            has_merkzeichen_tbl=values.get('person_b_has_merkzeichen_tbl', False),
            has_merkzeichen_h=values.get('person_b_has_merkzeichen_h', False)
        )

        if pauschbetrag_claim != 0 or fahrkostenpauschbetrag_claim != 0:
            raise ValidationError
        return values


class HasMerkzeichenPersonAPrecondition(BaseModel):
    _step_to_redirect_to = StepMerkzeichenPersonA.name
    _message_to_flash = _l('form.lotse.skip_reason.has_no_merkzeichen')

    person_a_has_pflegegrad: Optional[str]
    person_a_disability_degree: Optional[int]
    person_a_has_merkzeichen_g: Optional[bool]
    person_a_has_merkzeichen_ag: Optional[bool]
    person_a_has_merkzeichen_bl: Optional[bool]
    person_a_has_merkzeichen_tbl: Optional[bool]
    person_a_has_merkzeichen_h: Optional[bool]

    @validator('person_a_has_merkzeichen_h', always=True)
    def any_merkzeichen_has_to_be_set(cls, v, values):
        merkzeichen_keys = ['person_a_has_pflegegrad',
                            'person_a_disability_degree',
                            'person_a_has_merkzeichen_g',
                            'person_a_has_merkzeichen_ag',
                            'person_a_has_merkzeichen_bl',
                            'person_a_has_merkzeichen_tbl',
                            'person_a_has_merkzeichen_h']
        if not v and not any([values.get(merkzeichen_key) for merkzeichen_key in merkzeichen_keys]):
            raise ValueError
        return v


class StepPauschbetragPersonA(LotseFormSteuerlotseStep):
    name = 'person_a_requests_pauschbetrag'
    section_link = SectionLink('mandatory_data', StepFamilienstand.name, _l('form.lotse.mandatory_data.label'))
    preconditions = [HasDisabilityPersonAPrecondition, HasMerkzeichenPersonAPrecondition, HasPauschbetragClaimPersonAPrecondition]

    class InputForm(SteuerlotseBaseForm):
        person_a_requests_pauschbetrag = SelectField(
            # This mapping is for _generate_value_representation & get_overview_value_representation
            choices=[('yes', 'yes'),('no', 'no')],
            render_kw={'data_label':  _l('form.lotse.request_pauschbetrag.data_label')},
            validators=[InputRequired(_l('validate.input-required'))])

    @classmethod
    def get_label(cls, data=None):
        return ngettext('form.lotse.person_a.request_pauschbetrag.label', 'form.lotse.person_a.request_pauschbetrag.label',
                        num=get_number_of_users(data))

    def get_overview_value_representation(self, value):
        result = None

        if value == 'yes':
            result = str(self.get_pauschbetrag()) + ' ' + _('currency.euro')

        elif not value and self.stored_data.get('person_a_has_disability') == 'yes':
            result = _('form.lotse.no_answer')

        return result

    def render(self):
        props_dict = PauschbetragProps(
            step_header={
                'title': ngettext('form.lotse.person_a.request_pauschbetrag.title', 'form.lotse.person_a.request_pauschbetrag.title',
                        num=get_number_of_users(self.stored_data))
            },
            form={
                'action': self.render_info.submit_url,
                'csrf_token': generate_csrf(),
                'show_overview_button': bool(self.render_info.overview_url),
            },
            pauschbetrag=self.get_pauschbetrag(),
            fields=form_fields_dict(self.render_info.form),
            prev_url=self.render_info.prev_url
        ).camelized_dict()

        return render_template('react_component.html',
                               component='PauschbetragPersonAPage',
                               props=props_dict,
                               form=self.render_info.form,
                               header_title=_('form.lotse.header-title'))

    def get_pauschbetrag(self):
        return calculate_pauschbetrag(
            has_pflegegrad=self.stored_data.get('person_a_has_pflegegrad', None),
            disability_degree=self.stored_data.get('person_a_disability_degree', None),
            has_merkzeichen_bl=self.stored_data.get('person_a_has_merkzeichen_bl', False),
            has_merkzeichen_tbl=self.stored_data.get('person_a_has_merkzeichen_tbl', False),
            has_merkzeichen_h=self.stored_data.get('person_a_has_merkzeichen_h', False)
        )


class HasMerkzeichenPersonBPrecondition(BaseModel):
    _step_to_redirect_to = StepMerkzeichenPersonB.name
    _message_to_flash = _l('form.lotse.skip_reason.has_no_merkzeichen')

    person_b_has_pflegegrad: Optional[str]
    person_b_disability_degree: Optional[int]
    person_b_has_merkzeichen_g: Optional[bool]
    person_b_has_merkzeichen_ag: Optional[bool]
    person_b_has_merkzeichen_bl: Optional[bool]
    person_b_has_merkzeichen_tbl: Optional[bool]
    person_b_has_merkzeichen_h: Optional[bool]

    @validator('person_b_has_merkzeichen_h', always=True)
    def any_merkzeichen_has_to_be_set(cls, v, values):
        merkzeichen_keys = ['person_b_has_pflegegrad',
                            'person_b_disability_degree',
                            'person_b_has_merkzeichen_g',
                            'person_b_has_merkzeichen_ag',
                            'person_b_has_merkzeichen_bl',
                            'person_b_has_merkzeichen_tbl',
                            'person_b_has_merkzeichen_h']
        if not v and not any([values.get(merkzeichen_key) for merkzeichen_key in merkzeichen_keys]):
            raise ValueError
        return v

        
class StepPauschbetragPersonB(LotseFormSteuerlotseStep):
    name = 'person_b_requests_pauschbetrag'
    section_link = SectionLink('mandatory_data', StepFamilienstand.name, _l('form.lotse.mandatory_data.label'))

    label = _l('form.lotse.person_b.request_pauschbetrag.label')
    preconditions = [ShowPersonBPrecondition, HasDisabilityPersonBPrecondition, HasPauschbetragClaimPersonBPrecondition, HasMerkzeichenPersonBPrecondition]
        
    class InputForm(SteuerlotseBaseForm):
        person_b_requests_pauschbetrag = SelectField(
            # This mapping is for _generate_value_representation & get_overview_value_representation
            choices=[('yes', 'yes'),('no', 'no')],
            render_kw={'data_label':  _l('form.lotse.request_pauschbetrag.data_label')},
            validators=[InputRequired(_l('validate.input-required'))])

    @classmethod
    def get_label(cls, data):
        return cls.label

    def get_overview_value_representation(self, value):
        result = None

        if value == 'yes':
            result = str(self.get_pauschbetrag()) + ' ' + _('currency.euro')

        elif not value and self.stored_data.get('person_b_has_disability') == 'yes':
            result = _('form.lotse.no_answer')

        return result

    def render(self):
        props_dict = PauschbetragProps(
            step_header={
                'title': _('form.lotse.person_b.request_pauschbetrag.title')
            },
            form={
                'action': self.render_info.submit_url,
                'csrf_token': generate_csrf(),
                'show_overview_button': bool(self.render_info.overview_url),
            },
            pauschbetrag=self.get_pauschbetrag(),
            fields=form_fields_dict(self.render_info.form),
            prev_url=self.render_info.prev_url
        ).camelized_dict()

        return render_template('react_component.html',
                            component='PauschbetragPersonBPage',
                            props=props_dict,
                            form=self.render_info.form,
                            header_title=_('form.lotse.header-title'))

    def get_pauschbetrag(self):
        return calculate_pauschbetrag(
            has_pflegegrad=self.stored_data.get('person_b_has_pflegegrad', None),
            disability_degree=self.stored_data.get('person_b_disability_degree', None),
            has_merkzeichen_bl=self.stored_data.get('person_b_has_merkzeichen_bl', False),
            has_merkzeichen_tbl=self.stored_data.get('person_b_has_merkzeichen_tbl', False),
            has_merkzeichen_h=self.stored_data.get('person_b_has_merkzeichen_h', False)
        )


class StepNoPauschbetragPersonA(LotseFormSteuerlotseStep):
    name = 'person_a_no_pauschbetrag'
    title = _l('form.lotse.no_pauschbetrag.person_a.title')
    header_title = _l('form.lotse.mandatory_data.header-title')
    preconditions = [HasDisabilityPersonAPrecondition,
                     HasNoPauschbetragOrFahrkostenpauschbetragClaimPersonAPrecondition]

    def _pre_handle(self):
        self._set_multiple_texts()
        super()._pre_handle()

    def _set_multiple_texts(self):
        num_of_users = get_number_of_users(self.render_info.stored_data)
        self.render_info.step_title = ngettext('form.lotse.no_pauschbetrag.person_a.title',
                                               'form.lotse.no_pauschbetrag.person_a.title',
                                               num=num_of_users)

    def render(self):
        props_dict = NoPauschbetragProps(
            step_header={
                'title': str(self.title),
            },
            prev_url=self.render_info.prev_url,
            next_url=self.render_info.next_url,
        ).camelized_dict()

        return render_template('react_component.html',
                               component='NoPauschbetragPage',
                               props=props_dict,
                               form=self.render_info.form,
                               header_title=_('form.lotse.header-title'))


class StepNoPauschbetragPersonB(LotseFormSteuerlotseStep):
    name = 'person_b_no_pauschbetrag'
    title = _l('form.lotse.no_pauschbetrag.person_b.title')
    header_title = _l('form.lotse.mandatory_data.header-title')
    preconditions = [ShowPersonBPrecondition, HasDisabilityPersonBPrecondition, HasNoPauschbetragOrFahrkostenpauschbetragClaimPersonBPrecondition]

    def render(self):
        props_dict = NoPauschbetragProps(
            step_header={
                'title': str(self.title),
            },
            prev_url=self.render_info.prev_url,
            next_url=self.render_info.next_url,
        ).camelized_dict()

        return render_template('react_component.html',
                               component='NoPauschbetragPage',
                               props=props_dict,
                               form=self.render_info.form,
                               header_title=_('form.lotse.header-title'))
