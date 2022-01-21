from flask import flash, Markup
from flask_wtf.csrf import generate_csrf
from pydantic import ValidationError, root_validator
from wtforms import validators, SelectField, RadioField
from wtforms.validators import InputRequired, ValidationError as WTFormsValidationError

from flask_babel import lazy_gettext as _l, ngettext, _

from app.elster_client.elster_client import request_tax_offices
from app.forms import SteuerlotseBaseForm
from app.forms.fields import ConfirmationField, \
    TaxNumberField, YesNoField, LegacyIdNrField, LegacySteuerlotseDateField, SteuerlotseNameStringField, \
    SteuerlotseStringField, SteuerlotseHouseNumberIntegerField, SteuerlotseNumericStringField
from app.forms.steps.lotse.lotse_step import LotseFormSteuerlotseStep
from app.forms.steps.lotse.utils import get_number_of_users
from app.forms.steps.lotse_multistep_flow_steps.personal_data_steps import StepFamilienstand, StepIban, \
    get_religion_field
from app.forms.steps.step import SectionLink
from app.forms.validations.date_validations import ValidDateOfBirth
from app.forms.validations.validators import ValidHessenTaxNumber, ValidTaxNumber, ValidTaxNumberLength, \
    ValidIdNr, MaximumLength
from app.forms.validations.validators import DecimalOnly, IntegerLength
from app.model.components import TaxNumberStepFormProps, TelephoneNumberProps
from app.model.components.helpers import form_fields_dict
from app.model.form_data import show_person_b, FamilienstandModel, JointTaxesModel
from app.templates.react_template import render_react_template


class StepSteuernummer(LotseFormSteuerlotseStep):
    name = 'steuernummer'
    title = _l('form.lotse.steuernummer-title')
    intro = _l('form.lotse.steuernummer-intro')
    header_title = _l('form.lotse.mandatory_data.header-title')
    # TODO remove this once all steps are converted to steuerlotse steps
    prev_step = StepFamilienstand

    label = _l('form.lotse.step_steuernummer.label')
    section_link = SectionLink('mandatory_data', StepFamilienstand.name, _l('form.lotse.mandatory_data.label'))

    @classmethod
    def get_label(cls, data):
        return cls.label

    class InputForm(SteuerlotseBaseForm):
        steuernummer_exists = YesNoField(
            label=_l('form.lotse.steuernummer_exists'),
            render_kw={'data_label': _l('form.lotse.steuernummer_exists.data_label'),
                       'data-detail': {'title': _l('form.lotse.steuernummer_exists.detail.title'),
                        'text': _l('form.lotse.steuernummer_exists.detail.text')}},
            validators=[InputRequired(_l('form.lotse.steuernummer.selection_input_required'))])
        bundesland = SelectField(
            label=_l('form.lotse.field_bundesland'),
            choices=[
                ('BW', _l('form.lotse.field_bundesland_bw')),
                ('BY', _l('form.lotse.field_bundesland_by')),
                ('BE', _l('form.lotse.field_bundesland_be')),
                ('BB', _l('form.lotse.field_bundesland_bb')),
                ('HB', _l('form.lotse.field_bundesland_hb')),
                ('HH', _l('form.lotse.field_bundesland_hh')),
                ('HE', _l('form.lotse.field_bundesland_he')),
                ('MV', _l('form.lotse.field_bundesland_mv')),
                ('ND', _l('form.lotse.field_bundesland_nd')),
                ('NW', _l('form.lotse.field_bundesland_nw')),
                ('RP', _l('form.lotse.field_bundesland_rp')),
                ('SL', _l('form.lotse.field_bundesland_sl')),
                ('SN', _l('form.lotse.field_bundesland_sn')),
                ('ST', _l('form.lotse.field_bundesland_st')),
                ('SH', _l('form.lotse.field_bundesland_sh')),
                ('TH', _l('form.lotse.field_bundesland_th'))
            ],
            render_kw={'data_label': _l('form.lotse.field_bundesland.data_label')},
            validators=[InputRequired(_l('form.lotse.steuernummer.input_required'))], 
        )
        bufa_nr = SelectField(
            label=_l('form.lotse.bufa_nr'),
            choices=[
                ('', '---'),
            ],
            render_kw={'data_label': _l('form.lotse.bufa_nr.data_label')}
        )
        steuernummer = TaxNumberField(label=_l('form.lotse.steuernummer'),
                                      validators=[ValidTaxNumberLength(), ValidHessenTaxNumber()],
                                      render_kw={'data_label': _l('form.lotse.steuernummer.data_label'),
                                                 'data-example-input': _l('form.lotse.steuernummer.example_input')})
        request_new_tax_number = ConfirmationField(
            input_required=False,
            label=_l('form.lotse.steuernummer.request_new_tax_number'),
            render_kw={'data_label': _l('form.lotse.steuernummer.request_new_tax_number.data_label')})

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            tax_offices = request_tax_offices()
            self.tax_offices = tax_offices
            choices = []
            for county in tax_offices:
                choices += [(tax_office.get('bufa_nr'), tax_office.get('name')) for tax_office in
                            county.get('tax_offices')]
            self.bufa_nr.choices = choices

        def validate_bundesland(form, field):
            if form.steuernummer_exists.data == 'yes' or form.steuernummer_exists.data == 'no':
                validators.InputRequired()(form, field)
            else:
                validators.Optional()(form, field)

        def validate_steuernummer(form, field):
            if form.steuernummer_exists.data == 'yes' and form.bundesland:
                validators.InputRequired()(form, field)
            else:
                validators.Optional()(form, field)

        def validate_bufa_nr(form, field):
            if form.steuernummer_exists.data == 'no' and form.bundesland:
                validators.InputRequired()(form, field)
            else:
                validators.Optional()(form, field)

        def validate_request_new_tax_number(form, field):
            if form.steuernummer_exists.data == 'no' and form.bufa_nr:
                validators.InputRequired()(form, field)
            else:
                validators.Optional()(form, field)

        def validate(self, extra_validators=None):
            all_fields_are_valid = super().validate(extra_validators)

            if not all_fields_are_valid and (self.steuernummer.errors or self.bundesland.errors):
                return False  # Only validate tax number if all other validations of tax number are correct

            try:
                ValidTaxNumber()(self, self.steuernummer)
            except WTFormsValidationError:
                flash(Markup(_('form.lotse.tax-number.invalid-tax-number-error')), 'warn')
                return False

            return all_fields_are_valid

    def _pre_handle(self):
        self._set_multiple_texts()
        super()._pre_handle()

    def _set_multiple_texts(self):
        num_of_users = 2 if show_person_b(self.stored_data) else 1
        self.render_info.form.steuernummer_exists.label.text = ngettext('form.lotse.steuernummer_exists',
                                                                             'form.lotse.steuernummer_exists',
                                                                             num=num_of_users)
        self.render_info.form.request_new_tax_number.label.text = ngettext(
            'form.lotse.steuernummer.request_new_tax_number',
            'form.lotse.steuernummer.request_new_tax_number',
            num=num_of_users)

    def render(self, **kwargs):
        props_dict = TaxNumberStepFormProps(
            step_header={
                'title': str(self.render_info.step_title),
                'intro': str(self.render_info.step_intro),
            },
            form={
                'action': self.render_info.submit_url,
                'csrf_token': generate_csrf(),
                'show_overview_button': bool(self.render_info.overview_url),
            },
            fields=form_fields_dict(self.render_info.form),
            prev_url=self.render_info.prev_url,
            tax_office_list=self.render_info.form.tax_offices,
            number_of_users=2 if show_person_b(self.stored_data) else 1
        ).camelized_dict()

        return render_react_template(component='TaxNumberPage',
                               props=props_dict,
                               # TODO: These are still required by base.html to set the page title.
                               form=self.render_info.form,
                               header_title=self.header_title)


class StepPersonA(LotseFormSteuerlotseStep):
    name = 'person_a'
    title = None  # set below
    intro = None  # set below
    header_title = _l('form.lotse.mandatory_data.header-title')

    label = None  # set below
    section_link = SectionLink('mandatory_data', StepFamilienstand.name, _l('form.lotse.mandatory_data.label'))

    template = 'lotse/form_person_a.html'

    class InputForm(SteuerlotseBaseForm):
        person_a_idnr = LegacyIdNrField(
            label=_l('form.lotse.field_person_idnr'),
            validators=[InputRequired(message=_l('validate.missing-idnr')), ValidIdNr()],
            render_kw={'data_label': _l('form.lotse.field_person_idnr.data_label')})
        person_a_dob = LegacySteuerlotseDateField(
            label=_l('form.lotse.field_person_dob'),
            render_kw={'data_label': _l('form.lotse.field_person_dob.data_label')},
            validators=[InputRequired(message=_l('form.lotse.validation-dob-missing')), ValidDateOfBirth()],
            prevent_validation_error=True)
        person_a_first_name = SteuerlotseNameStringField(
            label=_l('form.lotse.field_person_first_name'),
            render_kw={'data_label': _l('form.lotse.field_person_first_name.data_label'),
                       'max_characters': 25},
            validators=[InputRequired(), validators.length(max=25)])
        person_a_last_name = SteuerlotseNameStringField(
            label=_l('form.lotse.field_person_last_name'),
            render_kw={'data_label': _l('form.lotse.field_person_last_name.data_label'),
                       'max_characters': 25},
            validators=[InputRequired(), validators.length(max=25)])
        person_a_street = SteuerlotseStringField(
            label=_l('form.lotse.field_person_street'),
            render_kw={'data_label': _l('form.lotse.field_person_street.data_label'),
                       'max_characters': 25},
            validators=[InputRequired(), validators.length(max=25)])
        person_a_street_number = SteuerlotseHouseNumberIntegerField(
            label=_l('form.lotse.field_person_street_number'),
            render_kw={'data_label': _l('form.lotse.field_person_street_number.data_label'),
                       'max_characters': 4},
            validators=[InputRequired(), IntegerLength(max=4)])
        person_a_street_number_ext = SteuerlotseStringField(
            label=_l('form.lotse.field_person_street_number_ext'),
            render_kw={'data_label': _l('form.lotse.field_person_street_number_ext.data_label'),
                       'max_characters': 6},
            validators=[validators.length(max=6)])
        person_a_address_ext = SteuerlotseStringField(
            label=_l('form.lotse.field_person_address_ext'),
            render_kw={'data_label': _l('form.lotse.field_person_address_ext.data_label'),
                       'max_characters': 25},
            validators=[validators.length(max=25)])
        person_a_plz = SteuerlotseNumericStringField(
            label=_l('form.lotse.field_person_plz'),
            render_kw={'data_label': _l('form.lotse.field_person_plz.data_label'),
                       'max_characters': 5},
            validators=[InputRequired(), DecimalOnly(),
                        validators.length(min=5, max=5, message=_l('validator-length-exactly', minmax=5))])
        person_a_town = SteuerlotseStringField(
            label=_l('form.lotse.field_person_town'),
            render_kw={'data_label': _l('form.lotse.field_person_town.data_label'),
                       'max_characters': 25},
            validators=[InputRequired(), validators.length(max=20)])
        person_a_religion = get_religion_field()

    @classmethod
    def get_label(cls, data=None):
        return ngettext('form.lotse.step_person_a.label', 'form.lotse.step_person_a.label',
                        num=get_number_of_users(data))

    def _pre_handle(self):
        self._set_multiple_texts()
        super()._pre_handle()

    def _set_multiple_texts(self):
        number_of_users = get_number_of_users(self.stored_data)
        self.render_info.step_title = ngettext('form.lotse.person-a-title', 'form.lotse.person-a-title',
                                               num=number_of_users)
        self.render_info.step_intro = _('form.lotse.person-a-intro') if number_of_users > 1 else None


class ShowPersonBPrecondition(FamilienstandModel):
    _step_to_redirect_to = StepFamilienstand.name
    _message_to_flash = _l('form.lotse.skip_reason.familienstand_single')

    @root_validator(skip_on_failure=True)
    def person_b_must_be_shown(cls, values):
        if not JointTaxesModel.show_person_b(values):
            raise ValidationError
        return values


class StepPersonB(LotseFormSteuerlotseStep):
    name = 'person_b'
    title = _l('form.lotse.person-b-title')
    intro = _l('form.lotse.person-b-intro')
    header_title = _l('form.lotse.mandatory_data.header-title')

    label = _l('form.lotse.step_person_b.label')
    section_link = SectionLink('mandatory_data', StepFamilienstand.name, _l('form.lotse.mandatory_data.label'))

    template = 'lotse/form_person_b.html'

    preconditions = [ShowPersonBPrecondition]

    class InputForm(SteuerlotseBaseForm):
        def input_required_if_not_same_address(form, field):
            if form.person_b_same_address.data == 'yes':
                validators.Optional()(form, field)
            else:
                validators.InputRequired()(form, field)

        person_b_idnr = LegacyIdNrField(
            label=_l('form.lotse.field_person_idnr'), validators=[InputRequired(message=_l('validate.missing-idnr')), ValidIdNr()],
            render_kw={'data_label': _l('form.lotse.field_person_idnr.data_label')})
        person_b_dob = LegacySteuerlotseDateField(
            label=_l('form.lotse.field_person_dob'),
            render_kw={'data_label': _l('form.lotse.field_person_dob.data_label')},
            validators=[InputRequired(message=_l('form.lotse.validation-dob-missing')), ValidDateOfBirth()],
            prevent_validation_error=True)
        person_b_first_name = SteuerlotseNameStringField(
            label=_l('form.lotse.field_person_first_name'),
            render_kw={'data_label': _l('form.lotse.field_person_first_name.data_label'),
                       'max_characters': 25},
            validators=[InputRequired(), validators.length(max=25)])
        person_b_last_name = SteuerlotseNameStringField(
            label=_l('form.lotse.field_person_last_name'),
            render_kw={'data_label': _l('form.lotse.field_person_last_name.data_label'),
                       'max_characters': 25},
            validators=[InputRequired(), validators.length(max=25)])

        person_b_same_address = RadioField(
            label="",
            render_kw={'data_label': _l('form.lotse.field_person_b_same_address.data_label'),
                       'hide_label': True},
            choices=[('yes', _l('form.lotse.field_person_b_same_address-yes')),
                     ('no', _l('form.lotse.field_person_b_same_address-no')),
                     ])
        person_b_street = SteuerlotseStringField(
            label=_l('form.lotse.field_person_street'),
            render_kw={'data_label': _l('form.lotse.field_person_street.data_label'),
                       'max_characters': 25,
                       'required_if_shown': True},
            validators=[input_required_if_not_same_address, validators.length(max=25)])
        person_b_street_number = SteuerlotseHouseNumberIntegerField(
            label=_l('form.lotse.field_person_street_number'),
            render_kw={'data_label': _l('form.lotse.field_person_street_number'
                                        '.data_label'),
                       'max_characters': 4,
                       'required_if_shown': True},
            validators=[input_required_if_not_same_address, IntegerLength(max=4)])
        person_b_street_number_ext = SteuerlotseStringField(
            label=_l('form.lotse.field_person_street_number_ext'),
            render_kw={'data_label': _l('form.lotse.field_person_street_number_ext.data_label'),
                       'max_characters': 6},
            validators=[validators.length(max=6)])
        person_b_address_ext = SteuerlotseStringField(
            label=_l('form.lotse.field_person_address_ext'),
            render_kw={'data_label': _l('form.lotse.field_person_address_ext.data_label'),
                       'max_characters': 25},
            validators=[validators.length(max=25)])
        person_b_plz = SteuerlotseNumericStringField(
            label=_l('form.lotse.field_person_plz'),
            render_kw={'data_label': _l('form.lotse.field_person_plz.data_label'),
                       'max_characters': 5,
                       'required_if_shown': True},
            validators=[input_required_if_not_same_address, DecimalOnly(),
                        validators.length(min=5, max=5, message=_l('validator-length-exactly', minmax=5))])
        person_b_town = SteuerlotseStringField(
            label=_l('form.lotse.field_person_town'),
            render_kw={'data_label': _l('form.lotse.field_person_town.data_label'),
                       'max_characters': 25,
                       'required_if_shown': True},
            validators=[input_required_if_not_same_address, validators.length(max=20)])
        person_b_religion = get_religion_field()

    @classmethod
    def get_label(cls, data):
        return cls.label


class StepTelephoneNumber(LotseFormSteuerlotseStep):
    name = 'telephone_number'
    title = _l('form.lotse.telephone-number.title')
    intro = _l('form.lotse.telephone-number.intro')
    header_title = _l('form.lotse.mandatory_data.header-title')
    # TODO remove this once the next steps is converted to steuerlotse step
    next_step = StepIban

    label = _l('form.lotse.step_telephone_number.label')
    section_link = SectionLink('mandatory_data', StepFamilienstand.name, _l('form.lotse.mandatory_data.label'))

    class InputForm(SteuerlotseBaseForm):
        telephone_number = SteuerlotseStringField(
            validators=[MaximumLength(25)],
            render_kw={'data_label': _l('form.lotse.field_telephone_number.data_label')})

    @classmethod
    def get_label(cls, data):
        return cls.label

    def render(self):
        props_dict = TelephoneNumberProps(
            step_header={
                'title': str(self.title),
                'intro': str(self.intro),
            },
            form={
                'action': self.render_info.submit_url,
                'csrf_token': generate_csrf(),
                'show_overview_button': bool(self.render_info.overview_url),
            },
            fields=form_fields_dict(self.render_info.form),
            prev_url=self.render_info.prev_url,
        ).camelized_dict()

        return render_react_template(component='TelephoneNumberPage',
                               props=props_dict,
                               form=self.render_info.form,
                               header_title=_('form.lotse.header-title'))

