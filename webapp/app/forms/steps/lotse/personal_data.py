from flask import request, flash, Markup
from flask import request
from pydantic import ValidationError
from wtforms import validators
from wtforms.validators import InputRequired, ValidationError as WTFormsValidationError

from flask_babel import lazy_gettext as _l, ngettext, _

from app.elster_client.elster_client import request_tax_offices
from app.forms import SteuerlotseBaseForm
from app.forms.fields import SteuerlotseSelectField, SteuerlotseNumericStringField, YesNoField, ConfirmationField
from app.forms.steps.lotse.lotse_step import LotseFormSteuerlotseStep
from app.forms.steps.lotse_multistep_flow_steps.personal_data_steps import StepFamilienstand, StepPersonA
from app.forms.steps.step import SectionLink
from app.forms.validators import DecimalOnly, IntegerLength, ValidHessenTaxNumber, ValidTaxNumber
from app.forms.validators import DecimalOnly, IntegerLength
from app.model.form_data import show_person_b


class StepSteuernummer(LotseFormSteuerlotseStep):
    name = 'steuernummer'
    title = _l('form.lotse.steuernummer-title')
    intro = _l('form.lotse.steuernummer-intro')
    header_title = _l('form.lotse.mandatory_data.header-title')
    template = 'lotse/form_steuernummer.html'
    # TODO remove this once all steps are converted to steuerlotse steps
    prev_step = StepFamilienstand
    next_step = StepPersonA

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
            validators=[InputRequired()], )
        bundesland = SteuerlotseSelectField(
            label=_l('form.lotse.field_bundesland'),
            choices=[
                ('', _l('form.select_input.default_selection')),
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
            render_kw={'data_label': _l('form.lotse.field_bundesland.data_label'),
                       'input_req_err_msg': _l('form.lotse.field_bundesland_required')}
        )
        bufa_nr = SteuerlotseSelectField(
            label=_l('form.lotse.bufa_nr'),
            choices=[
                ('', '---'),
            ],
            render_kw={'data_label': _l('form.lotse.bufa_nr.data_label')}
        )
        steuernummer = SteuerlotseNumericStringField(label=_l('form.lotse.steuernummer'),
                                                     validators=[DecimalOnly(),
                                                                 IntegerLength(min=10, max=11), ValidHessenTaxNumber()],
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
