from pydantic import ValidationError

from app.forms import SteuerlotseBaseForm
from app.forms.steps.step import FormStep, SectionLink
from app.forms.fields import YesNoField, SteuerlotseDateField, SteuerlotseSelectField, ConfirmationField, \
    SteuerlotseStringField

from flask_babel import _
from flask_babel import lazy_gettext as _l
from wtforms import IntegerField, RadioField, validators, BooleanField
from wtforms.validators import InputRequired

from app.forms.validators import IntegerLength, ValidIban, ValidIdNr, DecimalOnly
from app.model.form_data import FamilienstandModel
from app.utils import get_first_day_of_tax_period


class StepFamilienstand(FormStep):
    name = 'familienstand'

    label = _l('form.lotse.step_familienstand.label')
    section_link = SectionLink('mandatory_data', name, _l('form.lotse.mandatory_data.label'))

    class Form(SteuerlotseBaseForm):
        familienstand = RadioField(
            label=_l('form.lotse.field_familienstand'),
            render_kw={'data_label': _l('form.lotse.field_familienstand.data_label')},
            choices=[
                ('single', _l('form.lotse.familienstand-single')),
                ('married', _l('form.lotse.familienstand-married')),
                ('widowed', _l('form.lotse.familienstand-widowed')),
                ('divorced', _l('form.lotse.familienstand-divorced')),
            ],
            validators=[InputRequired()]
        )
        familienstand_date = SteuerlotseDateField(
            label=_l('form.lotse.familienstand_date'),
            render_kw={'data_label': _l('form.lotse.familienstand_date.data_label')},
            validators=())
        familienstand_married_lived_separated = YesNoField(
            label=_l('form.lotse.familienstand_married_lived_separated'),
            render_kw={'data_label': _l('form.lotse.familienstand_married_lived_separated.data_label')})
        familienstand_married_lived_separated_since = SteuerlotseDateField(
            label=_l('form.lotse.familienstand_married_lived_separated_since'),
            render_kw={'data_label': _l('form.lotse.familienstand_married_lived_separated_since.data_label')},
            validators=())
        familienstand_widowed_lived_separated = YesNoField(
            label=_l('form.lotse.familienstand_widowed_lived_separated'),
            render_kw={'data_label': _l('form.lotse.familienstand_widowed_lived_separated.data_label')})
        familienstand_widowed_lived_separated_since = SteuerlotseDateField(
            label=_l('form.lotse.familienstand_widowed_lived_separated_since'),
            render_kw={'data_label': _l('form.lotse.familienstand_widowed_lived_separated_since.data_label')},
            validators=())
        familienstand_zusammenveranlagung = YesNoField(
            label=_l('form.lotse.field_familienstand_zusammenveranlagung'),
            render_kw={'data_label': _l('form.lotse.familienstand_zusammenveranlagung.data_label')})
        familienstand_confirm_zusammenveranlagung = ConfirmationField(
            input_required=False,
            label=_l('form.lotse.familienstand_confirm_zusammenveranlagung'),
            render_kw={'data_label': _l('form.lotse.familienstand_confirm_zusammenveranlagung.data_label')})

        def validate_familienstand_date(self, field):
            if self.familienstand.data == 'single':
                validators.Optional()(self, field)
            else:
                validators.InputRequired(_l('form.lotse.validation-familienstand-date'))(self, field)

        def validate_familienstand_married_lived_separated(self, field):
            if self.familienstand.data == 'married':
                validators.InputRequired(_l('form.lotse.validation-familienstand-married-lived-separated'))(self, field)
            else:
                validators.Optional()(self, field)

        def validate_familienstand_married_lived_separated_since(self, field):
            if self.familienstand.data == 'married' and self.familienstand_married_lived_separated.data == 'yes':
                validators.InputRequired(_l('form.lotse.validation-familienstand-married-lived-separated-since'))(self,
                                                                                                                  field)
            else:
                validators.Optional()(self, field)
            if field.data < self.familienstand_date.data:
                from wtforms.validators import ValidationError
                raise ValidationError(_('form.lotse.validation.married-after-separated'))

        def validate_familienstand_widowed_lived_separated(self, field):
            if self.familienstand.data == 'widowed' and \
                    self.familienstand_date.data and \
                    self.familienstand_date.data >= get_first_day_of_tax_period():
                validators.InputRequired(_l('form.lotse.validation-familienstand-widowed-lived-separated'))(self, field)
            else:
                validators.Optional()(self, field)

        def validate_familienstand_widowed_lived_separated_since(self, field):
            if self.familienstand.data == 'widowed' and self.familienstand_widowed_lived_separated.data == 'yes':
                validators.InputRequired(_l('form.lotse.validation-familienstand-widowed-lived-separated-since'))(self,
                                                                                                                  field)
            else:
                validators.Optional()(self, field)
            if field.data >= self.familienstand_date.data:
                from wtforms.validators import ValidationError
                raise ValidationError(_('form.lotse.validation.widowed-before-separated'))

        def validate_familienstand_zusammenveranlagung(self, field):
            married_separated_recently = self.familienstand.data == 'married' and \
                                         self.familienstand_married_lived_separated.data == 'yes' and \
                                         self.familienstand_married_lived_separated_since.data and \
                                         self.familienstand_married_lived_separated_since.data > get_first_day_of_tax_period()
            widowed_separated_recently = self.familienstand.data == 'widowed' and \
                                         self.familienstand_widowed_lived_separated.data == 'yes' and \
                                         self.familienstand_widowed_lived_separated_since.data and \
                                         self.familienstand_widowed_lived_separated_since.data > get_first_day_of_tax_period()

            if married_separated_recently or widowed_separated_recently:
                validators.InputRequired(_l('form.lotse.validation-familienstand-zusammenveranlagung'))(self, field)
            else:
                validators.Optional()(self, field)

        def validate_familienstand_confirm_zusammenveranlagung(self, field):
            married_not_separated = self.familienstand.data == 'married' and \
                                    self.familienstand_married_lived_separated.data == 'no'
            widowed_recently_not_separated = self.familienstand.data == 'widowed' and \
                                             self.familienstand_date.data and \
                                             self.familienstand_date.data >= get_first_day_of_tax_period() and \
                                             self.familienstand_widowed_lived_separated.data == 'no'

            if married_not_separated or widowed_recently_not_separated:
                validators.InputRequired(_l('form.lotse.validation-familienstand-confirm-zusammenveranlagung'))(self,
                                                                                                                field)
            else:
                validators.Optional()(self, field)

    def __init__(self, **kwargs):
        super(StepFamilienstand, self).__init__(
            title=_l('form.lotse.familienstand-title'),
            form=self.Form,
            **kwargs,
            header_title=_('form.lotse.mandatory_data.header-title'),
            template='lotse/form_familienstand.html'
        )


class StepSteuernummer(FormStep):
    name = 'steuernummer'

    label = _l('form.lotse.step_steuernummer.label')
    section_link = SectionLink('mandatory_data', StepFamilienstand.name, _l('form.lotse.mandatory_data.label'))

    class Form(SteuerlotseBaseForm):
        bundesland = SteuerlotseSelectField(
            label=_l('form.lotse.field_bundesland'),
            choices=[
                ('', '---'),
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
            validators=[InputRequired(message=_('form.lotse.field_bundesland_required'))],
            render_kw={'data_label': _l('form.lotse.field_bundesland.data_label'),
                       'input_req_err_msg': _l('form.lotse.field_bundesland_required')}
        )
        steuernummer = SteuerlotseStringField(label=_l('form.lotse.steuernummer'),
                                              validators=[InputRequired(), DecimalOnly(),
                                                          IntegerLength(min=10, max=11)],
                                              render_kw={'data_label': _l('form.lotse.steuernummer.data_label'),
                                                         'example_input': _l('form.lotse.steuernummer.example_input')})

    def __init__(self, **kwargs):
        super(StepSteuernummer, self).__init__(
            title=_l('form.lotse.steuernummer-title'),
            intro=_l('form.lotse.steuernummer-intro'),
            form=self.Form,
            **kwargs,
            header_title=_('form.lotse.mandatory_data.header-title'),
            template='basis/form_standard.html'
        )


def get_religion_field():
    return SteuerlotseSelectField(
        label=_l('form.lotse.field_person_religion'),
        choices=[
            ('none', _l('form.lotse.field_person_religion.none')),
            ('ak', _l('form.lotse.field_person_religion.ak')),
            ('ev', _l('form.lotse.field_person_religion.ev')),
            ('er', _l('form.lotse.field_person_religion.er')),
            ('erb', _l('form.lotse.field_person_religion.erb')),
            ('ers', _l('form.lotse.field_person_religion.ers')),
            ('fr', _l('form.lotse.field_person_religion.fr')),
            ('fra', _l('form.lotse.field_person_religion.fra')),
            ('fgm', _l('form.lotse.field_person_religion.fgm')),
            ('fgo', _l('form.lotse.field_person_religion.fgo')),
            ('flb', _l('form.lotse.field_person_religion.flb')),
            ('flp', _l('form.lotse.field_person_religion.flp')),
            ('is', _l('form.lotse.field_person_religion.is')),
            ('irb', _l('form.lotse.field_person_religion.irb')),
            ('iw', _l('form.lotse.field_person_religion.iw')),
            ('ikb', _l('form.lotse.field_person_religion.ikb')),
            ('inw', _l('form.lotse.field_person_religion.inw')),
            ('jgf', _l('form.lotse.field_person_religion.jgf')),
            ('jh', _l('form.lotse.field_person_religion.jh')),
            ('jgh', _l('form.lotse.field_person_religion.jgh')),
            ('jkk', _l('form.lotse.field_person_religion.jkk')),
            ('rk', _l('form.lotse.field_person_religion.rk')),
            ('other', _l('form.lotse.field_person_religion.other'))
        ],
        validators=[InputRequired()],
        render_kw={'help': _l('form.lotse.field_person_religion-help'),
                   'data_label': _l('form.lotse.field_person_religion.data_label')})


class StepPersonA(FormStep):
    name = 'person_a'

    label = _l('form.lotse.step_person_a.label')
    section_link = SectionLink('mandatory_data', StepFamilienstand.name, _l('form.lotse.mandatory_data.label'))

    class Form(SteuerlotseBaseForm):
        person_a_idnr = SteuerlotseStringField(
            label=_l('form.lotse.field_person_idnr'),
            validators=[InputRequired(), ValidIdNr()],
            render_kw={'help': _l('form.lotse.field_person_idnr-help'),
                       'data_label': _l('form.lotse.field_person_idnr.data_label')})
        person_a_dob = SteuerlotseDateField(
            label=_l('form.lotse.field_person_dob'),
            render_kw={'data_label': _l('form.lotse.field_person_dob.data_label')}, validators=[InputRequired()])
        person_a_first_name = SteuerlotseStringField(
            label=_l('form.lotse.field_person_first_name'),
            render_kw={'data_label': _l('form.lotse.field_person_first_name.data_label')},
            validators=[InputRequired(), validators.length(max=25)])
        person_a_last_name = SteuerlotseStringField(
            label=_l('form.lotse.field_person_last_name'),
            render_kw={'data_label': _l('form.lotse.field_person_last_name.data_label')},
            validators=[InputRequired(), validators.length(max=25)])
        person_a_street = SteuerlotseStringField(
            label=_l('form.lotse.field_person_street'),
            render_kw={'data_label': _l('form.lotse.field_person_street.data_label')},
            validators=[InputRequired(), validators.length(max=25)])
        person_a_street_number = IntegerField(
            label=_l('form.lotse.field_person_street_number'),
            render_kw={'data_label': _l('form.lotse.field_person_street_number.data_label')},
            validators=[InputRequired(), IntegerLength(max=4)])
        person_a_street_number_ext = SteuerlotseStringField(
            label=_l('form.lotse.field_person_street_number_ext'),
            render_kw={'data_label': _l('form.lotse.field_person_street_number_ext.data_label')},
            validators=[validators.length(max=6)])
        person_a_address_ext = SteuerlotseStringField(
            label=_l('form.lotse.field_person_address_ext'),
            render_kw={'data_label': _l('form.lotse.field_person_address_ext.data_label')},
            validators=[validators.length(max=25)])
        person_a_plz = SteuerlotseStringField(
            label=_l('form.lotse.field_person_plz'),
            render_kw={'data_label': _l('form.lotse.field_person_plz.data_label')},
            validators=[InputRequired(), DecimalOnly(), validators.length(max=5)])
        person_a_town = SteuerlotseStringField(
            label=_l('form.lotse.field_person_town'),
            render_kw={'data_label': _l('form.lotse.field_person_town.data_label')},
            validators=[InputRequired(), validators.length(max=20)])
        person_a_religion = get_religion_field()

        person_a_beh_grad = IntegerField(
            label=_l('form.lotse.field_person_beh_grad'),
            validators=[
                validators.any_of([25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100])],
            render_kw={'help': _l('form.lotse.field_person_beh_grad-help'),
                       'data_label': _l('form.lotse.field_person_beh_grad.data_label'),
                       'example_input': _l('form.lotse.field_person_beh_grad.example_input')})
        person_a_blind = BooleanField(
            label=_l('form.lotse.field_person_blind'),
            render_kw={'data_label': _l('form.lotse.field_person_blind.data_label')})
        person_a_gehbeh = BooleanField(
            label=_l('form.lotse.field_person_gehbeh'),
            render_kw={'data_label': _l('form.lotse.field_person_gehbeh.data_label')})

        def validate_person_a_beh_grad(self, field):
            if self.person_a_gehbeh.data:
                validators.InputRequired(_l('form.lotse.validation-person-beh-grad'))(self, field)
            else:
                validators.Optional()(self, field)

    def __init__(self, **kwargs):
        super(StepPersonA, self).__init__(
            title=_('form.lotse.person-a-title'),
            intro=_l('form.lotse.person-a-intro'),
            form=self.Form,
            **kwargs,
            header_title=_('form.lotse.mandatory_data.header-title'),
            template='lotse/form_person_a.html'
        )


class StepPersonB(FormStep):
    name = 'person_b'

    label = _l('form.lotse.step_person_b.label')
    section_link = SectionLink('mandatory_data', StepFamilienstand.name, _l('form.lotse.mandatory_data.label'))

    class Form(SteuerlotseBaseForm):
        def input_required_if_not_same_address(form, field):
            if form.person_b_same_address.data == 'yes':
                validators.Optional()(form, field)
            else:
                validators.InputRequired()(form, field)

        def validate_person_b_beh_grad(self, field):
            if self.person_b_gehbeh.data:
                validators.InputRequired(_l('form.lotse.validation-person-beh-grad'))(self, field)
            else:
                validators.Optional()(self, field)

        person_b_idnr = SteuerlotseStringField(
            label=_l('form.lotse.field_person_idnr'), validators=[InputRequired(), ValidIdNr()],
            render_kw={'help': _l('form.lotse.field_person_idnr-help'),
                       'data_label': _l('form.lotse.field_person_idnr.data_label')})
        person_b_dob = SteuerlotseDateField(
            label=_l('form.lotse.field_person_dob'),
            render_kw={'data_label': _l('form.lotse.field_person_dob.data_label')},
            validators=[InputRequired()])
        person_b_first_name = SteuerlotseStringField(
            label=_l('form.lotse.field_person_first_name'),
            render_kw={'data_label': _l('form.lotse.field_person_first_name.data_label')},
            validators=[InputRequired(), validators.length(max=25)])
        person_b_last_name = SteuerlotseStringField(
            label=_l('form.lotse.field_person_last_name'),
            render_kw={'data_label': _l('form.lotse.field_person_last_name.data_label')},
            validators=[InputRequired(), validators.length(max=25)])

        person_b_same_address = RadioField(
            label=_l('form.lotse.field_person_b_same_address'),
            render_kw={'data_label': _l('form.lotse.field_person_b_same_address.data_label'),
                       'hide_label': True},
            choices=[('yes', _l('form.lotse.field_person_b_same_address-yes')),
                     ('no', _l('form.lotse.field_person_b_same_address-no')),
                     ])
        person_b_street = SteuerlotseStringField(
            label=_l('form.lotse.field_person_street'),
            render_kw={'data_label': _l('form.lotse.field_person_street.data_label'),
                       'required_if_shown': True},
            validators=[input_required_if_not_same_address, validators.length(max=25)])
        person_b_street_number = IntegerField(
            label=_l('form.lotse.field_person_street_number'),
            render_kw={'data_label': _l('form.lotse.field_person_street_number'
                                        '.data_label'),
                       'required_if_shown': True},
            validators=[input_required_if_not_same_address, IntegerLength(max=4)])
        person_b_street_number_ext = SteuerlotseStringField(
            label=_l('form.lotse.field_person_street_number_ext'),
            render_kw={'data_label': _l('form.lotse.field_person_street_number_ext.data_label')},
            validators=[validators.length(max=6)])
        person_b_address_ext = SteuerlotseStringField(
            label=_l('form.lotse.field_person_address_ext'),
            render_kw={
                'data_label': _l('form.lotse.field_person_address_ext.data_label')},
            validators=[validators.length(max=25)])
        person_b_plz = SteuerlotseStringField(
            label=_l('form.lotse.field_person_plz'),
            render_kw={'data_label': _l('form.lotse.field_person_plz.data_label'),
                       'required_if_shown': True},
            validators=[input_required_if_not_same_address, DecimalOnly(), validators.length(max=5)])
        person_b_town = SteuerlotseStringField(
            label=_l('form.lotse.field_person_town'),
            render_kw={'data_label': _l('form.lotse.field_person_town.data_label'),
                       'required_if_shown': True},
            validators=[input_required_if_not_same_address, validators.length(max=20)])
        person_b_religion = get_religion_field()

        person_b_beh_grad = IntegerField(
            label=_l('form.lotse.field_person_beh_grad'),
            validators=[validators.any_of([25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100])],
            render_kw={'help': _l('form.lotse.field_person_beh_grad-help'),
                       'data_label': _l('form.lotse.field_person_beh_grad.data_label'),
                       'example_input': _l('form.lotse.field_person_beh_grad.example_input')})
        person_b_blind = BooleanField(
            label=_l('form.lotse.field_person_blind'),
            render_kw={'data_label': _l('form.lotse.field_person_blind.data_label')})
        person_b_gehbeh = BooleanField(
            label=_l('form.lotse.field_person_gehbeh'),
            render_kw={'data_label': _l('form.lotse.field_person_gehbeh.data_label')})

    def __init__(self, **kwargs):
        super(StepPersonB, self).__init__(
            title=_('form.lotse.person-b-title'),
            intro=_('form.lotse.person-b-intro'),
            form=self.Form,
            **kwargs,
            header_title=_('form.lotse.mandatory_data.header-title'),
            template='lotse/form_person_b.html'
        )

    @classmethod
    def get_redirection_info_if_skipped(cls, input_data):
        try:
            familienstand_model = FamilienstandModel.parse_obj(input_data)
            if familienstand_model.show_person_b():
                return None, None
            else:
                return StepFamilienstand.name, _l('form.lotse.skip_reason.familienstand_single')
        except ValidationError:
            return StepFamilienstand.name, _l('form.lotse.skip_reason.familienstand_single')


class StepIban(FormStep):
    name = 'iban'
    label = _l('form.lotse.step_iban.label')
    section_link = SectionLink('mandatory_data', StepFamilienstand.name, _l('form.lotse.mandatory_data.label'))

    class Form(SteuerlotseBaseForm):
        is_person_a_account_holder = RadioField(
            label=_l('form.lotse.field_is_person_a_account_holder'),
            render_kw={'data_label': _l('form.lotse.field_is_person_a_account_holder.data_label')},
            choices=[('yes', _l('form.lotse.field_is_person_a_account_holder-person-a')),
                     ('no', _l('form.lotse.field_is_person_a_account_holder-person-b')),
                     ])
        iban = SteuerlotseStringField(
            label=_l('form.lotse.field_iban'),
            render_kw={'data_label': _l('form.lotse.field_iban.data_label'),
                       'example_input': _l('form.loste.field_iban.example_input')},
            validators=[InputRequired(), ValidIban()],
            filters=[lambda value: value.replace(' ', '') if value else value])

    class FormSingle(SteuerlotseBaseForm):
        is_person_a_account_holder = ConfirmationField(
            label=_l('form.lotse.field_is_person_a_account_holder_single'),
            render_kw={'data_label': _l('form.lotse.field_is_person_a_account_holder_single.data_label')})
        iban = SteuerlotseStringField(
            label=_l('form.lotse.field_iban'),
            render_kw={'data_label': _l('form.lotse.field_iban.data_label'),
                       'example_input': _l('form.loste.field_iban.example_input')},
            validators=[InputRequired(), ValidIban()],
            filters=[lambda value: value.replace(' ', '') if value else value])

    def __init__(self, **kwargs):
        super(StepIban, self).__init__(
            title=_l('form.lotse.iban-title'),
            intro=_l('form.lotse.iban-intro'),
            form=self.Form,
            **kwargs,
            header_title=_('form.lotse.mandatory_data.header-title'),
            template='basis/form_standard.html'
        )

    def create_form(self, request, prefilled_data):
        from app.forms.flows.lotse_flow import show_person_b
        if not show_person_b(prefilled_data):
            self.form = self.FormSingle

        return super().create_form(request, prefilled_data)
