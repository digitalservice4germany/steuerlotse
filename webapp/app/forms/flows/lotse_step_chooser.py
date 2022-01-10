import datetime
from decimal import Decimal

from flask_babel import _

from app.forms.flows.step_chooser import StepChooser
from app.forms.steps.lotse.confirmation import StepSummary
from app.forms.steps.lotse.fahrkostenpauschale import StepFahrkostenpauschalePersonB, StepFahrkostenpauschalePersonA
from app.forms.steps.lotse.merkzeichen import StepMerkzeichenPersonA, StepMerkzeichenPersonB
from app.forms.steps.lotse.steuerminderungen import StepVorsorge, StepAussergBela, StepHaushaltsnaheHandwerker, \
    StepGemeinsamerHaushalt, StepReligion, StepSpenden, StepSelectStmind
from app.forms.steps.lotse.personal_data import StepSteuernummer, StepPersonA, StepPersonB, StepTelephoneNumber
from app.forms.steps.lotse.has_disability import StepDisabilityPersonB, StepDisabilityPersonA
from app.forms.steps.lotse.pauschbetrag import StepPauschbetragPersonA, StepPauschbetragPersonB
from app.forms.steps.lotse.no_pauschbetrag import  StepNoPauschbetragPersonA, StepNoPauschbetragPersonB
_LOTSE_DATA_KEY = 'form_data'


class LotseStepChooser(StepChooser):
    session_data_identifier = _LOTSE_DATA_KEY
    _DEBUG_DATA = {
        'declaration_edaten': True,
        'declaration_incomes': True,

        'steuernummer_exists': 'yes',
        'bundesland': 'BY',
        'steuernummer': '19811310010',
        # 'bufa_nr': '9201',
        # 'request_new_tax_number': True,

        'familienstand': 'married',
        'familienstand_date': datetime.date(2000, 1, 31),
        'familienstand_married_lived_separated': 'no',
        'familienstand_confirm_zusammenveranlagung': True,

        'person_a_idnr': '04452397687',
        'person_a_dob': datetime.date(1950, 8, 16),
        'person_a_first_name': 'Manfred',
        'person_a_last_name': 'Mustername',
        'person_a_street': 'Steuerweg',
        'person_a_street_number': 42,
        'person_a_street_number_ext': 'a',
        'person_a_address_ext': 'Seitenflügel',
        'person_a_plz': '20354',
        'person_a_town': 'Hamburg',
        'person_a_religion': 'none',
        'person_a_has_disability': 'yes',
        'person_a_has_pflegegrad': 'no',
        'person_a_disability_degree': 80,
        'person_a_has_merkzeichen_bl': True,
        'person_a_has_merkzeichen_g': True,
        'person_a_requests_pauschbetrag': 'yes',
        'person_a_requests_fahrkostenpauschale': 'yes',

        'person_b_idnr': '02293417683',
        'person_b_dob': datetime.date(1951, 2, 25),
        'person_b_first_name': 'Gerta',
        'person_b_last_name': 'Mustername',
        'person_b_same_address': 'yes',
        'person_b_religion': 'rk',
        'person_b_has_disability': 'yes',
        'person_b_has_pflegegrad': 'no',
        'person_b_has_merkzeichen_h': True,

        # 'is_user_account_holder': 'yes', use for single user
        'account_holder': 'person_a',
        'iban': 'DE35133713370000012345',

        'stmind_select_vorsorge': True,
        'stmind_select_ausserg_bela': True,
        'stmind_select_handwerker': True,
        'stmind_select_religion': True,
        'stmind_select_spenden': True,

        'stmind_haushaltsnahe_entries': ["Gartenarbeiten"],
        'stmind_haushaltsnahe_summe': Decimal('500.00'),

        'stmind_handwerker_entries': ["Renovierung Badezimmer"],
        'stmind_handwerker_summe': Decimal('200.00'),
        'stmind_handwerker_lohn_etc_summe': Decimal('100.00'),

        'stmind_vorsorge_summe': Decimal('111.11'),
        'stmind_spenden_inland': Decimal('222.22'),
        'stmind_spenden_inland_parteien': Decimal('333.33'),
        'stmind_religion_paid_summe': Decimal('444.44'),
        'stmind_religion_reimbursed_summe': Decimal('555.55'),

        'stmind_krankheitskosten_summe': Decimal('1011.11'),
        'stmind_krankheitskosten_anspruch': Decimal('1011.12'),
        'stmind_pflegekosten_summe': Decimal('2022.21'),
        'stmind_pflegekosten_anspruch': Decimal('2022.22'),
        'stmind_beh_aufw_summe': Decimal('3033.31'),
        'stmind_beh_aufw_anspruch': Decimal('3033.32'),
        'stmind_bestattung_summe': Decimal('5055.51'),
        'stmind_bestattung_anspruch': Decimal('5055.52'),
        'stmind_aussergbela_sonst_summe': Decimal('6066.61'),
        'stmind_aussergbela_sonst_anspruch': Decimal('6066.62'),

        # Only use these fields if person is single
        # 'stmind_gem_haushalt_count': 2,
        # 'stmind_gem_haushalt_entries': ['Mustermensch, Martina, 02.04.2011', 'Beispielperson, Stefan, 01.01.1985'],

        'confirm_complete_correct': True,
        'confirm_data_privacy': True,
        'confirm_terms_of_service': True,
        }

    def __init__(self, endpoint="lotse"):
        super(LotseStepChooser, self).__init__(
            title=_('form.lotse.title'),
            steps=[
                StepSteuernummer,
                StepPersonA,
                StepDisabilityPersonA,
                StepMerkzeichenPersonA,
                StepNoPauschbetragPersonA,
                StepPauschbetragPersonA,
                StepFahrkostenpauschalePersonA,
                StepPersonB,
                StepDisabilityPersonB,
                StepMerkzeichenPersonB,
                StepNoPauschbetragPersonB,
                StepPauschbetragPersonB,
                StepFahrkostenpauschalePersonB,
                StepTelephoneNumber,
                StepSelectStmind,
                StepVorsorge,
                StepAussergBela,
                StepHaushaltsnaheHandwerker,
                StepGemeinsamerHaushalt,
                StepSpenden,
                StepReligion,
                StepSummary,
            ],
            endpoint=endpoint,
            overview_step=StepSummary
        )

    # TODO remove this once all steps are converted to steuerlotse steps
    def determine_prev_step(self, current_step_name, stored_data):
        # As we mix Mutlistepflow Steps and SteuerlotseSteps for the lotse, we need to handle leaving the
        # "steuerlotse-step-context" and therefore directly set the prev_step in the SteuerlotseSteps that are
        # adjacent to Mutlistepflow Steps.
        if hasattr(self.steps[current_step_name], 'prev_step'):
            return self.steps[current_step_name].prev_step
        return super().determine_prev_step(current_step_name, stored_data)

    # TODO remove this once all steps are converted to steuerlotse steps
    def determine_next_step(self, current_step_name, stored_data):
        # As we mix Mutlistepflow Steps and SteuerlotseSteps for the lotse, we need to handle leaving the
        # "steuerlotse-step-context" and therefore directly set the next_step in the SteuerlotseSteps that are
        # adjacent to Mutlistepflow Steps.
        if hasattr(self.steps[current_step_name], 'next_step'):
            return self.steps[current_step_name].next_step
        return super().determine_next_step(current_step_name, stored_data)
