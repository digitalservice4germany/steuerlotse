from typing import Dict, List, Optional, Union

import humps
from pydantic import BaseModel, Extra


class ComponentProps(BaseModel, extra=Extra.forbid):
    def camelized_dict(self):
        return humps.camelize(self.dict())


class StepHeaderProps(ComponentProps):
    title: str
    intro: Optional[str]


class FormProps(ComponentProps):
    action: str
    csrf_token: str
    show_overview_button: bool
    next_button_label: Optional[str]


class ComponentPlausibleProps(ComponentProps):
    plausible_domain: Optional[str]


class FormPropsNoOverview(ComponentProps):
    action: str
    csrf_token: str
    next_button_label: Optional[str]


class InputFieldProps(ComponentProps):
    value: Union[str, List[str]]
    errors: List[str]


class CheckboxFieldProps(ComponentProps):
    checked: bool
    errors: List[str]


class SelectOption(BaseModel, extra=Extra.forbid):
    value: str
    display_name: str


class SelectFieldProps(ComponentProps):
    selected_value: Optional[str]
    options: List[SelectOption]
    errors: List[str]


class YesNoFieldProps(ComponentProps):
    value: Optional[str]
    errors: List[str]


FieldProps = Union[SelectFieldProps, InputFieldProps, CheckboxFieldProps, YesNoFieldProps]


class StepFormProps(ComponentProps):
    step_header: StepHeaderProps
    prev_url: Optional[str]
    form: FormProps
    fields: Dict[str, FieldProps]


class StepDisplayProps(ComponentProps):
    step_header: StepHeaderProps
    prev_url: Optional[str]
    next_url: Optional[str]


class LoginProps(StepFormProps):
    waiting_moment_active: Optional[bool]


class LogoutProps(ComponentProps):
    form: FormPropsNoOverview


class LoginFailureProps(StepDisplayProps):
    registration_link: str
    revocation_link: str


class RegistrationProps(StepFormProps):
    login_link: str
    eligibility_link: str
    terms_of_service_link: str
    data_privacy_link: str
    waiting_moment_active: Optional[bool]


class UnlockCodeSuccessProps(ComponentPlausibleProps):
    prev_url: Optional[str]
    steuer_erklaerung_link: str
    vorbereitungs_hilfe_link: str
    data_privacy_link: str
    csrf_token: str


class UnlockCodeFailureProps(ComponentProps):
    prev_url: Optional[str]


class RevocationProps(StepFormProps):
    waiting_moment_active: Optional[bool]


class RevocationSuccessProps(StepDisplayProps):
    pass


class RevocationFailureProps(ComponentProps):
    prev_url: Optional[str]


class DeclarationIncomesProps(StepFormProps):
    plausible_domain: Optional[str]


class DeclarationEDatenProps(StepFormProps):
    prev_url: str
    plausible_domain: Optional[str]


class ConfirmationProps(StepFormProps):
    terms_of_service_link: str
    data_privacy_link: str


class FilingSuccessProps(ComponentPlausibleProps):
    next_url: str
    transfer_ticket: str
    download_url: str
    taxNumber_provided: bool


class FilingFailureProps(ComponentProps):
    error_details: List[str]


class TaxNumberStepFormProps(StepFormProps):
    tax_office_list: List[Dict]
    number_of_users: int
    plausible_domain: Optional[str]


class HasDisabilityPersonAProps(StepFormProps):
    num_users: int
    plausible_domain: Optional[str]


class HasDisabilityPersonBProps(StepFormProps):
    plausible_domain: Optional[str]


class MerkzeichenProps(StepFormProps):
    plausible_domain: Optional[str]


class PauschbetragProps(StepFormProps):
    pauschbetrag: str
    plausible_domain: Optional[str]


class NoPauschbetragProps(StepDisplayProps):
    showOverviewButton: bool
    overviewUrl: str


class FahrtkostenpauschaleProps(StepFormProps):
    fahrtkostenpauschale_amount: int
    plausible_domain: Optional[str]


class TelephoneNumberProps(StepFormProps):
    plausible_domain: Optional[str]


class SelectStMindProps(StepFormProps):
    plausible_domain: Optional[str]


class StepSessionNoteProps(ComponentProps):
    prev_url: Optional[str]
    form: FormProps


class StepSubmitAcknowledgeProps(ComponentPlausibleProps):
    prev_url: str
    logout_url: str


class InfoTaxReturnForPensionersProps(ComponentPlausibleProps):
    pass


class PensionExpensesProps(ComponentProps):
    pass


class MedicalExpensesInfoPageProps(ComponentProps):
    pass


class CareCostsInfoPageProps(ComponentProps):
    pass


class FuneralExpensesInfoPageProps(ComponentProps):
    pass


class VorbereitenInfoProps(ComponentProps):
    download_preparation_link: str
    vorsorgeaufwendungen_url: str
    krankheitskosten_url: str
    pflegekosten_url: str
    angaben_bei_behinderung_url: str
    bestattungskosten_url: str
    wiederbeschaffungskosten_url: str
    haushaltsnahe_dienstleistungen_url: str
    handwerkerleistungen_url: str
    spenden_und_mitgliedsbeitraege_url: str
    kirchensteuer_url: str

class HouseholdServicesInfoPageProps(ComponentProps):
    pass


class ReplacementCostsInfoPageProps(ComponentProps):
    pass


class DisabilityCostsInfoProps(ComponentProps):
    pass


class DonationInfoPageProps(ComponentProps):
    pass


class ChurchTaxInfoPageProps(ComponentProps):
    pass


class CraftsmanServicesInfoPageProps(ComponentProps):
    pass


class InfoForRelativesPageProps(ComponentProps):
    pass

class SummaryDataSectionProps(ComponentProps):
    mandatory_data: Dict
    section_steuerminderung: Dict

class SummaryPageProps(ComponentProps):
    summary_data: SummaryDataSectionProps
    prev_url: Optional[str]
    form: FormProps
    fields: Dict[str, FieldProps]


class LandingPageProps(ComponentPlausibleProps):
    pass

class NewsletterSuccessPageProps(ComponentProps):
    pass


class FreeTaxDeclarationForPensionersProps(ComponentPlausibleProps):
    pass


class MandateForTaxDeclarationProps(ComponentPlausibleProps):
    pass
