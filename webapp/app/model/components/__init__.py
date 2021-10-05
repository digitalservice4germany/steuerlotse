from typing import Dict, List, Union
from pydantic import BaseModel


class StepHeaderProps(BaseModel):
    title: str
    intro: str


class FormProps(BaseModel):
    action: str
    csrf_token: str
    show_overview_button: bool


class InputFieldProps(BaseModel):
    value: Union[str, List[str]]
    errors: List[str]


class CheckboxFieldProps(BaseModel):
    checked: bool
    errors: List[str]


FieldProps = Union[InputFieldProps, CheckboxFieldProps]


class LoginProps(BaseModel):
    step_header: StepHeaderProps
    form: FormProps
    fields: Dict[str, FieldProps]
