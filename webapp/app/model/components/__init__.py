from typing import Dict, List, Optional, Union, Tuple

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
    pass


class LoginFailureProps(StepDisplayProps):
    registration_link: str
    revocation_link: str


class RegistrationProps(StepFormProps):
    login_link: str
    eligibility_link: str
    terms_of_service_link: str
    data_privacy_link: str


class UnlockCodeSuccessProps(ComponentProps):
    prev_url: Optional[str]
    steuer_erklaerung_link: str
    vorbereitungs_hilfe_link: str


class UnlockCodeFailureProps(ComponentProps):
    prev_url: Optional[str]


class RevocationProps(StepFormProps):
    pass


class RevocationSuccessProps(StepDisplayProps):
    pass


class DeclarationIncomesProps(StepFormProps):
    pass

class DeclarationEDatenProps(StepFormProps):
    prev_url: str

class ConfirmationProps(StepFormProps):
    terms_of_service_link: str
    data_privacy_link: str


class TaxNumberStepFormProps(StepFormProps):
    tax_office_list: List[Dict]
    number_of_users: int


class HasDisabilityPersonAProps(StepFormProps):
    num_users: int


class HasDisabilityPersonBProps(StepFormProps):
    pass


class MerkzeichenProps(StepFormProps):
    pass


class PauschbetragProps(StepFormProps):
    pauschbetrag: str


class NoPauschbetragProps(StepDisplayProps):
    showOverviewButton: bool
    overviewUrl: str


class FahrtkostenpauschaleProps(StepFormProps):
    fahrtkostenpauschale_amount: int


class TelephoneNumberProps(StepFormProps):
    pass


class SelectStMindProps(StepFormProps):
    pass
