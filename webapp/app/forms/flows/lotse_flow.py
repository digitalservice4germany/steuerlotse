import datetime
import logging
from decimal import Decimal

from flask import request, flash, url_for
from flask_babel import _, lazy_gettext as _l
from flask_login import current_user
from pydantic import ValidationError, MissingError
from wtforms import SelectField, BooleanField, RadioField
from wtforms.fields.core import UnboundField
from requests import RequestException

from app.config import Config
from app.data_access.audit_log_controller import create_audit_log_confirmation_entry
from app.data_access.user_controller import store_pdf_and_transfer_ticket, check_idnr
from app.elster_client.elster_errors import ElsterGlobalValidationError, ElsterTransferError, EricaIsMissingFieldError, \
    ElsterInvalidBufaNumberError
from app.forms.fields import SteuerlotseDateField, LegacySteuerlotseSelectField, LegacyYesNoField, \
    LegacySteuerlotseDateField, SteuerlotseStringField, \
    ConfirmationField, EntriesField, EuroField, YesNoField, MerkzeichenBooleanField
from wtforms.fields import IntegerField
from app.forms.flows.multistep_flow import MultiStepFlow
from app.forms.steps.lotse.confirmation import StepSummary
from app.forms.steps.lotse.merkzeichen import StepMerkzeichenPersonA, StepMerkzeichenPersonB
from app.forms.steps.lotse.steuerminderungen import StepVorsorge, StepAussergBela, StepHaushaltsnaheHandwerker, \
    StepGemeinsamerHaushalt, StepReligion, StepSpenden, StepSelectStmind
from app.forms.steps.lotse_multistep_flow_steps.confirmation_steps import StepConfirmation, StepAck, StepFiling
from app.forms.steps.lotse_multistep_flow_steps.declaration_steps import StepDeclarationIncomes, StepDeclarationEdaten, StepSessionNote
from app.forms.steps.lotse.personal_data import StepSteuernummer, StepPersonB, StepTelephoneNumber, StepPersonA
from app.forms.steps.lotse.has_disability import StepDisabilityPersonB, StepDisabilityPersonA
from app.forms.steps.lotse.pauschbetrag import StepPauschbetragPersonA, StepPauschbetragPersonB
from app.forms.steps.lotse.fahrtkostenpauschale import StepFahrtkostenpauschalePersonA, StepFahrtkostenpauschalePersonB
from app.forms.steps.lotse_multistep_flow_steps.personal_data_steps import StepIban, StepFamilienstand
from app.forms.steps.step import Section
from app.model.form_data import MandatoryFormData, MandatoryConfirmations, \
    ConfirmationMissingInputValidationError, MandatoryFieldMissingValidationError, InputDataInvalidError, \
    IdNrMismatchInputValidationError, show_person_b

SPECIAL_RESEND_TEST_IDNRS = ['04452397687', '02259674819']


logger = logging.getLogger(__name__)


class LotseMultiStepFlow(MultiStepFlow):
    _DEBUG_DATA = (
        StepSummary,
        {
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
            'person_a_has_merkzeichen_g': True,
            'person_a_requests_pauschbetrag': 'yes',
            'person_a_requests_fahrtkostenpauschale': 'yes',

            'person_b_idnr': '02293417683',
            'person_b_dob': datetime.date(1951, 2, 25),
            'person_b_first_name': 'Gerta',
            'person_b_last_name': 'Mustername',
            'person_b_same_address': 'yes',
            'person_b_religion': 'rk',
            'person_b_has_disability': 'yes',
            'person_b_has_pflegegrad': 'no',

            #'is_user_account_holder': 'yes', use for single user
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
    )

    def __init__(self, endpoint):
        super(LotseMultiStepFlow, self).__init__(
            title=_('form.lotse.title'),
            endpoint=endpoint,
            steps=[
                StepDeclarationIncomes,
                StepDeclarationEdaten,
                StepSessionNote,

                StepFamilienstand,
                StepSteuernummer,
                StepPersonA,
                StepDisabilityPersonA,
                StepMerkzeichenPersonA,
                StepPauschbetragPersonA,
                StepFahrtkostenpauschalePersonA,
                StepPersonB,
                StepDisabilityPersonB,
                StepMerkzeichenPersonB,
                StepPauschbetragPersonB,
                StepFahrtkostenpauschalePersonB,
                StepTelephoneNumber,
                StepIban,

                StepSelectStmind,
                StepVorsorge,
                StepAussergBela,
                StepHaushaltsnaheHandwerker,
                StepGemeinsamerHaushalt,
                StepSpenden,
                StepReligion,


                StepSummary,
                StepConfirmation,
                StepFiling,
                StepAck,
            ],
            overview_step=StepSummary,
        )

    def _check_step_needs_to_be_skipped(self, step_name, input_data):
        """Check whether a step has to be blocked and if so then do provide the correct link"""
        redirected_step = super()._check_step_needs_to_be_skipped(step_name, input_data)
        if redirected_step:
            return redirected_step

        redirection_destination, skip_reason = self.steps[step_name].get_redirection_info_if_skipped(input_data)
        if redirection_destination:
            flash(skip_reason, 'warn')
            return self.url_for_step(redirection_destination)

    # TODO: Use inheritance to clean up this method
    def _handle_specifics_for_step(self, step, render_info, stored_data):
        render_info, stored_data = super(LotseMultiStepFlow, self)._handle_specifics_for_step(step, render_info,
                                                                                              stored_data)
        if isinstance(step, StepConfirmation):
            if request.method == 'POST' and render_info.form.validate():
                create_audit_log_confirmation_entry('Confirmed data privacy', request.remote_addr,
                                                    stored_data['idnr'], 'confirm_data_privacy',
                                                    stored_data['confirm_data_privacy'])
                create_audit_log_confirmation_entry('Confirmed terms of service', request.remote_addr,
                                                    stored_data['idnr'], 'confirm_terms_of_service',
                                                    stored_data['confirm_terms_of_service'])
        if isinstance(step, StepAck):
            render_info.overview_url = None
            render_info.next_url = url_for('logout')
            render_info.additional_info['next_button_label'] = _('form.logout')
        if isinstance(step, StepFiling):
            if not current_user.has_completed_tax_return() or is_test_user(current_user):
                try:
                    self._validate_input(stored_data)
                    from app.elster_client.elster_client import send_est_with_elster
                    elster_data = send_est_with_elster(stored_data, request.remote_addr)
                    store_pdf_and_transfer_ticket(current_user,
                                                  elster_data.pop('pdf', None),
                                                  elster_data.get('transfer_ticket'))
                    render_info.additional_info['elster_data'] = elster_data
                    render_info.overview_url = None
                    render_info.prev_url = None
                except ConfirmationMissingInputValidationError as e:
                    flash(e.message, 'warn')
                    render_info.redirect_url = self.url_for_step(StepConfirmation.name)
                except (MandatoryFieldMissingValidationError, InputDataInvalidError, EricaIsMissingFieldError,
                        ElsterInvalidBufaNumberError) as e:
                    logger.info("Fields are missing or incorrect", exc_info=True)
                    flash(e.message, 'warn')
                    render_info.redirect_url = self.url_for_step(StepSummary.name)
                except ElsterGlobalValidationError as e:
                    logger.info("Could not send est", exc_info=True)
                    render_info.additional_info['elster_data'] = {
                        'was_successful': False,
                        'eric_response': e.eric_response,
                        'server_response': '',
                        'validation_problems': e.validation_problems}
                except ElsterTransferError as e:
                    logger.info("Could not send est", exc_info=True)
                    render_info.additional_info['elster_data'] = {
                        'was_successful': False,
                        'eric_response': e.eric_response,
                        'server_response': e.server_response}
                except RequestException:
                    flash(_('flash.erica.dataConnectionError'), 'warn')
                    render_info.redirect_url = self.url_for_step(StepConfirmation.name)
            else:
                render_info.additional_info['elster_data'] = {
                    'was_successful': True,
                    'pdf': current_user.pdf,
                    'transfer_ticket': current_user.transfer_ticket
                }
        elif isinstance(step, StepDeclarationIncomes):
            if request.method == 'POST' and render_info.form.validate():
                create_audit_log_confirmation_entry('Confirmed incomes', request.remote_addr,
                                                    stored_data['idnr'], 'declaration_incomes',
                                                    stored_data['declaration_incomes'])
        elif isinstance(step, StepDeclarationEdaten):
            if request.method == 'POST' and render_info.form.validate():
                create_audit_log_confirmation_entry('Confirmed edata', request.remote_addr,
                                                    stored_data['idnr'], 'declaration_edaten',
                                                    stored_data['declaration_edaten'])
        elif isinstance(step, StepFamilienstand):
            if request.method == 'POST' and render_info.form.validate():
                if not show_person_b(stored_data):
                    stored_data = self._delete_dependent_data(['person_b', 'account_holder'], stored_data)
                else:
                    stored_data = self._delete_dependent_data(['is_user_account_holder', 'stmind_gem_haushalt'], stored_data)
                if stored_data['familienstand'] == 'single':
                    stored_data = self._delete_dependent_data(['familienstand_date'], stored_data)
        elif isinstance(step, StepHaushaltsnaheHandwerker):
            if show_person_b(stored_data) or \
                    not stored_data.get('stmind_handwerker_summe') and \
                    not stored_data.get('stmind_haushaltsnahe_summe'):
                render_info.next_url = self.url_for_step(StepReligion.name)
            if request.method == 'POST' and render_info.form.validate():
                if not stored_data.get('stmind_handwerker_summe') and not stored_data.get('stmind_haushaltsnahe_summe'):
                    stored_data = self._delete_dependent_data(['stmind_gem_haushalt'], stored_data)
        elif isinstance(step, StepReligion):
            if show_person_b(stored_data) or \
                    not stored_data.get('stmind_handwerker_summe') and \
                    not stored_data.get('stmind_haushaltsnahe_summe'):
                render_info.prev_url = self.url_for_step(StepHaushaltsnaheHandwerker.name)

        # redirect in any case if overview button pressed
        if 'overview_button' in request.form:
            render_info.next_url = self.url_for_step(StepSummary.name)
        return render_info, stored_data

    def _get_overview_data(self, stored_data, missing_fields=None) -> {str, Section}:
        """
            Method to structure the data from the form according to the steps, where it was collected.
            To do this, the data is collected for each step's fields and the put into the correct section.


            :param stored_data: The unstructured data from the forms taken out of the cookie.
            :return: A dict of the sections, in which the data is structured.
        """
        _IGNORED_STEPS = [
            StepSessionNote, StepSummary, StepConfirmation,
            StepFiling, StepAck
        ]

        sections = {}
        for curr_step in self.steps.values():
            if curr_step in _IGNORED_STEPS:
                continue  # no need to collect data from ignored section steps

            step_data = self._collect_data_for_step(curr_step(), stored_data, missing_fields)

            if step_data:
                if curr_step.section_link.name not in sections:
                    # Append new section
                    sections[curr_step.section_link.name] = self._create_section_from_section_link(
                        curr_step.section_link, {})
                curr_section = sections[curr_step.section_link.name]

                curr_section.data[curr_step.name] = Section(curr_step.get_label(stored_data),
                                                            self.url_for_step(curr_step.name, _has_link_overview=True),
                                                            step_data, name=curr_step.name)

        return sections

    def _create_section_from_section_link(self, section_link, data=None, _has_link_overview=True):
        return Section(section_link.label,
                       self.url_for_step(section_link.beginning_step,
                                         _has_link_overview=_has_link_overview, name=None),
                       data)

    @staticmethod
    def _generate_value_representation(field: UnboundField, value):
        label = field.kwargs['render_kw']['data_label']
        value_representation = None

        if value is None or value == "" or value == "none" or value == _('form.lotse.no_answer'):
            return label, None

        if field.field_class == RadioField:
            for choice in field.kwargs['choices']:
                if choice[0] == value:
                    value_representation = choice[1]
        elif field.field_class in (SelectField, LegacySteuerlotseSelectField):
            for choice in field.kwargs['choices']:  # choice is a tuple of (value, label)
                if choice[0] == value:
                    value_representation = choice[
                        1]  # Use label because this is also shown to user when making selections
                    break
        elif field.field_class in (LegacyYesNoField, YesNoField):
            value_representation = "Ja" if value == "yes" else "Nein"
        elif field.field_class == MerkzeichenBooleanField:
            value_representation = "Ja" if value else None
        elif field.field_class == BooleanField:
            value_representation = "Ja" if value else "Nein"
        elif field.field_class in (SteuerlotseDateField, LegacySteuerlotseDateField):
            value_representation = value.strftime("%d.%m.%Y")
        elif field.field_class == EntriesField:
            value_representation = ', '.join(value)
        elif field.field_class == EuroField:
            value_representation = str(value) + " €"
        elif issubclass(field.field_class, SteuerlotseStringField):
            value_representation = value
        elif issubclass(field.field_class, IntegerField):
            value_representation = value
        elif field.field_class == ConfirmationField:
            value_representation = "Ja" if value else None
        else:
            raise ValueError

        return label, value_representation

    # TODO: Use a better structure to collect data for the summary page. Potentially use a pydantic data structure
    def _collect_data_for_step(self, step, stored_data, missing_fields=None):
        """
            This function collects all the data from the form_data, which is represented through a field in the step.

            :param step: An instance of the step, of which the data will be collected
            :param stored_data: The form_data from the cookie
        """
        step_data = {}
        for attr in step.create_form(request.form, stored_data).__dict__:
            if missing_fields and attr in missing_fields:
                field = getattr(step.form, attr)
                label = field.kwargs['render_kw']['data_label']
                step_data[label] = _l('form.lotse.missing_mandatory_field')
            elif attr in stored_data or hasattr(step.form, attr):
                field = getattr(step.form, attr)
                # TODO: When the summary page is refactored we should merge _generate_value_representation &
                #  get_overview_value_representation     
                label, value = self._generate_value_representation(field, stored_data.get(attr))
                value = step.get_overview_value_representation(value, stored_data)
                if value is not None:
                    # If get_overview_value_representation() returns None, the value will not be displayed
                    step_data[label] = value

        return step_data

    @staticmethod
    def _validate_input(form_data):
        try:
            MandatoryConfirmations.parse_obj(form_data)
        except ValidationError as e:
            missing_fields = LotseMultiStepFlow._get_missing_fields(e.raw_errors)
            if any([isinstance(raw_e.exc, IdNrMismatchInputValidationError) for raw_e in e.raw_errors]):
                raise IdNrMismatchInputValidationError
            elif missing_fields:
                raise MandatoryFieldMissingValidationError(missing_fields)
            elif any([isinstance(raw_e.exc, ConfirmationMissingInputValidationError) for raw_e in e.raw_errors]):
                missing_confirmations = LotseMultiStepFlow._get_missing_fields(e.raw_errors,
                                                                               ConfirmationMissingInputValidationError)
                raise ConfirmationMissingInputValidationError(missing_confirmations)
            else:
                raise

    @staticmethod
    def _get_missing_fields(raw_errors, expected_error=None):
        if not expected_error:
            expected_error = MissingError
        missing_fields = []
        for raw_e in raw_errors:
            if isinstance(raw_e.exc, expected_error):
                missing_fields.append(raw_e._loc)
            elif isinstance(raw_e.exc, ValidationError):
                missing_fields += LotseMultiStepFlow._get_missing_fields(raw_e.exc.raw_errors, expected_error)

        return missing_fields

    @staticmethod
    def _validate_mandatory_fields(form_data):
        try:
            MandatoryFormData.parse_obj(form_data)
        except ValidationError as e:
            missing_fields = LotseMultiStepFlow._get_missing_fields(e.raw_errors)
            if missing_fields:
                raise MandatoryFieldMissingValidationError(missing_fields)
            else:
                raise


def is_test_user(user):
    if Config.ALLOW_RESEND_FOR_TEST_USER:
        return any([check_idnr(user, special_idnr) for special_idnr in SPECIAL_RESEND_TEST_IDNRS])
    else:
        return False
