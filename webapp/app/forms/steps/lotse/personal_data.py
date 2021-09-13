from flask import request
from pydantic import ValidationError
from wtforms import validators
from wtforms.validators import InputRequired

from flask_babel import lazy_gettext as _l, _, ngettext

from app.elster_client.elster_client import request_tax_offices
from app.forms import SteuerlotseBaseForm
from app.forms.fields import SteuerlotseSelectField, SteuerlotseNumericStringField, YesNoField, ConfirmationField
from app.forms.steps.lotse_multistep_flow_steps.confirmation_steps import StepSummary
from app.forms.steps.lotse_multistep_flow_steps.personal_data_steps import StepFamilienstand, StepPersonA
from app.forms.steps.step import SectionLink
from app.forms.steps.steuerlotse_step import FormSteuerlotseStep
from app.forms.validators import DecimalOnly, IntegerLength
from app.model.form_data import FamilienstandModel


class LotseFormSteuerlotseStep(FormSteuerlotseStep):
    template = 'basis/form_standard.html'
    header_title = None
    InputForm = None
    prev_step_name = None
    next_step_name = None

    def __init__(self, endpoint, **kwargs):
        super().__init__(
            form=self.InputForm,
            endpoint=endpoint,
            header_title=self.header_title,
            **kwargs,
        )

    def _main_handle(self):
        super()._main_handle()
        self.render_info.prev_url = self.url_for_step(self.prev_step_name)
        self.render_info.next_url = self.url_for_step(self.next_step_name)

        # redirect in any case if overview button pressed
        if 'overview_button' in request.form:
            self.render_info.next_url = self.url_for_step(StepSummary.name)


class StepSteuernummer(LotseFormSteuerlotseStep):
    name = 'steuernummer'
    title = _l('form.lotse.steuernummer-title')
    intro = _l('form.lotse.steuernummer-intro')
    header_title = _l('form.lotse.mandatory_data.header-title')
    template = 'lotse/form_steuernummer.html'
    prev_step_name = StepFamilienstand.name
    next_step_name = StepPersonA.name

    label = _l('form.lotse.step_steuernummer.label')
    section_link = SectionLink('mandatory_data', StepFamilienstand.name, _l('form.lotse.mandatory_data.label'))

    @classmethod
    def get_label(cls, data):
        return cls.label

    def __init__(self, endpoint="lotse", **kwargs):
        super().__init__(endpoint=endpoint, **kwargs)

    class InputForm(SteuerlotseBaseForm):

        steuernummer_exists = YesNoField(
            label=_l('form.lotse.steuernummer_exists'),
            render_kw={'data_label': _l('form.lotse.steuernummer_exists.data_label'),
                       'detail': {'title': _l('form.lotse.steuernummer_exists.detail.title'),
                                  'text': _l('form.lotse.steuernummer_exists.detail.text')}},
            validators=[InputRequired()],)
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
                                                          IntegerLength(min=10, max=11)],
                                              render_kw={'data_label': _l('form.lotse.steuernummer.data_label'),
                                                         'example_input': _l('form.lotse.steuernummer.example_input')})
        request_new_tax_number = ConfirmationField(
            input_required=False,
            label=_l('form.lotse.steuernummer.request_new_tax_number'),
            render_kw={'data_label': _l('form.lotse.steuernummer.request_new_tax_number.data_label')})

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

    def _pre_handle(self):
        tax_offices = request_tax_offices()

        # Set bufa choices here because WTForms will otherwise not accept choices because they are invalid
        self._set_bufa_choices(tax_offices)
        self._set_multiple_texts()
        super()._pre_handle()
        self.render_info.additional_info['tax_offices'] = tax_offices

    def _set_bufa_choices(self, tax_offices):
        choices = []
        for county in tax_offices:
            choices += [(tax_office.get('bufa_nr'), tax_office.get('name')) for tax_office in county.get('tax_offices')]
        self.InputForm.bufa_nr.kwargs['choices'] = choices

    def _set_multiple_texts(self):
        num_of_users = 2 if show_person_b(self.stored_data) else 1
        self.form.steuernummer_exists.kwargs['label'] = ngettext('form.lotse.steuernummer_exists',
                                                                     'form.lotse.steuernummer_exists',
                                                                     num=num_of_users)
        self.form.request_new_tax_number.kwargs['label'] = ngettext('form.lotse.steuernummer.request_new_tax_number',
                                                                     'form.lotse.steuernummer.request_new_tax_number',
                                                                     num=num_of_users)


def show_person_b(personal_data):
    try:
        familienstand_model = FamilienstandModel.parse_obj(personal_data)
        return familienstand_model.show_person_b()
    except ValidationError:
        return False