from flask_babel import lazy_gettext as _l, ngettext, _
from pydantic import root_validator
from wtforms.validators import ValidationError

from app.forms.steps.lotse.fahrtkostenpauschale import calculate_fahrtkostenpauschale
from app.forms.steps.lotse.lotse_step import LotseFormSteuerlotseStep
from app.forms.steps.lotse.personal_data import ShowPersonBPrecondition
from app.forms.steps.lotse.merkzeichen import StepMerkzeichenPersonA, StepMerkzeichenPersonB
from app.forms.steps.lotse.utils import get_number_of_users
from app.forms.steps.lotse.has_disability import HasDisabilityPersonAPrecondition, HasDisabilityPersonBPrecondition
from app.forms.steps.lotse.pauschbetrag import DisabilityModel, calculate_pauschbetrag
from app.model.components import NoPauschbetragProps
from app.templates.react_template import render_react_template


class HasNoPauschbetragOrFahrtkostenpauschbetragClaimPersonAPrecondition(DisabilityModel):
    _step_to_redirect_to = StepMerkzeichenPersonA.name
    _message_to_flash = _l('form.lotse.skip_reason.has_pauschbetrag_claim')

    @root_validator(skip_on_failure=True)
    def has_to_have_pauschbetrag_and_fahrtkostenpauschbetrag_not_0(cls, values):
        pauschbetrag_claim = calculate_pauschbetrag(
            has_pflegegrad=values.get('person_a_has_pflegegrad', None),
            disability_degree=values.get('person_a_disability_degree', None),
            has_merkzeichen_bl=values.get('person_a_has_merkzeichen_bl', False),
            has_merkzeichen_tbl=values.get('person_a_has_merkzeichen_tbl', False),
            has_merkzeichen_h=values.get('person_a_has_merkzeichen_h', False)
        )
        fahrtkostenpauschbetrag_claim = calculate_fahrtkostenpauschale(
            has_pflegegrad=values.get('person_a_has_pflegegrad', None),
            disability_degree=values.get('person_a_disability_degree', None),
            has_merkzeichen_bl=values.get('person_a_has_merkzeichen_bl', False),
            has_merkzeichen_tbl=values.get('person_a_has_merkzeichen_tbl', False),
            has_merkzeichen_h=values.get('person_a_has_merkzeichen_h', False),
            has_merkzeichen_ag=values.get('person_a_has_merkzeichen_ag', False),
            has_merkzeichen_g=values.get('person_a_has_merkzeichen_g', False)
        )

        if pauschbetrag_claim != 0 or fahrtkostenpauschbetrag_claim != 0:
            raise ValidationError
        return values


class HasNoPauschbetragOrFahrtkostenpauschbetragClaimPersonBPrecondition(DisabilityModel):
    _step_to_redirect_to = StepMerkzeichenPersonB.name
    _message_to_flash = _l('form.lotse.skip_reason.has_pauschbetrag_claim')

    @root_validator(skip_on_failure=True)
    def has_to_have_pauschbetrag_and_fahrtkostenpauschbetrag_not_0(cls, values):
        pauschbetrag_claim = calculate_pauschbetrag(
            has_pflegegrad=values.get('person_b_has_pflegegrad', None),
            disability_degree=values.get('person_b_disability_degree', None),
            has_merkzeichen_bl=values.get('person_b_has_merkzeichen_bl', False),
            has_merkzeichen_tbl=values.get('person_b_has_merkzeichen_tbl', False),
            has_merkzeichen_h=values.get('person_b_has_merkzeichen_h', False)
        )
        fahrtkostenpauschbetrag_claim = calculate_fahrtkostenpauschale(
            has_pflegegrad=values.get('person_b_has_pflegegrad', None),
            disability_degree=values.get('person_b_disability_degree', None),
            has_merkzeichen_bl=values.get('person_b_has_merkzeichen_bl', False),
            has_merkzeichen_tbl=values.get('person_b_has_merkzeichen_tbl', False),
            has_merkzeichen_h=values.get('person_b_has_merkzeichen_h', False),
            has_merkzeichen_ag=values.get('person_b_has_merkzeichen_ag', False),
            has_merkzeichen_g=values.get('person_b_has_merkzeichen_g', False)
        )

        if pauschbetrag_claim != 0 or fahrtkostenpauschbetrag_claim != 0:
            raise ValidationError
        return values


class StepNoPauschbetragPersonA(LotseFormSteuerlotseStep):
    name = 'person_a_no_pauschbetrag'
    title = _l('form.lotse.no_pauschbetrag.person_a.title')
    header_title = _l('form.lotse.mandatory_data.header-title')
    preconditions = [HasDisabilityPersonAPrecondition,
                     HasNoPauschbetragOrFahrtkostenpauschbetragClaimPersonAPrecondition]

    def _pre_handle(self):
        self._set_multiple_texts()
        super()._pre_handle()

    def _set_multiple_texts(self):
        num_of_users = get_number_of_users(self.render_info.stored_data)
        self.title = ngettext('form.lotse.no_pauschbetrag.person_a.title',
                              'form.lotse.no_pauschbetrag.person_a.title',
                              num=num_of_users)

    def render(self):
        props_dict = NoPauschbetragProps(
            step_header={
                'title': str(self.title),
            },
            showOverviewButton=bool(self.render_info.overview_url),
            overviewUrl=self.url_for_step(self.overview_step.name),
            prev_url=self.render_info.prev_url,
            next_url=self.render_info.next_url,
        ).camelized_dict()

        return render_react_template(component='NoPauschbetragPage',
                                     props=props_dict,
                                     form=self.render_info.form,
                                     header_title=_('form.lotse.header-title'),
                                     disable_extended_footer=self.disable_extended_footer)


class StepNoPauschbetragPersonB(LotseFormSteuerlotseStep):
    name = 'person_b_no_pauschbetrag'
    title = _l('form.lotse.no_pauschbetrag.person_b.title')
    header_title = _l('form.lotse.mandatory_data.header-title')
    preconditions = [ShowPersonBPrecondition, HasDisabilityPersonBPrecondition,
                     HasNoPauschbetragOrFahrtkostenpauschbetragClaimPersonBPrecondition]

    def render(self):
        props_dict = NoPauschbetragProps(
            step_header={
                'title': str(self.title),
            },
            showOverviewButton=bool(self.render_info.overview_url),
            overviewUrl=self.url_for_step(self.overview_step.name),
            prev_url=self.render_info.prev_url,
            next_url=self.render_info.next_url,
        ).camelized_dict()

        return render_react_template(component='NoPauschbetragPage',
                                     props=props_dict,
                                     form=self.render_info.form,
                                     header_title=_('form.lotse.header-title'),
                                     disable_extended_footer=self.disable_extended_footer)
