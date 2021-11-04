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


class InputFieldProps(ComponentProps):
    value: Union[str, List[str]]
    errors: List[str]


class CheckboxFieldProps(ComponentProps):
    checked: bool
    errors: List[str]


FieldProps = Union[InputFieldProps, CheckboxFieldProps]


class StepFormProps(ComponentProps):
    step_header: StepHeaderProps
    form: FormProps
    fields: Dict[str, FieldProps]


class LoginProps(StepFormProps):
    pass


class RegistrationProps(StepFormProps):
    login_link: str
    eligibility_link: str
    terms_of_service_link: str
    data_privacy_link: str


class DeclarationIncomesProps(StepFormProps):
    pass


class SelectStmindProps(StepFormProps):
    pass


class ConfirmationProps(StepFormProps):
    terms_of_service_link: str
    data_privacy_link: str
