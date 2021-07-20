from app.forms import SteuerlotseBaseForm
from app.forms.steps.lotse.personal_data_steps import StepFamilienstand
from app.forms.steps.step import FormStep, SectionLink
from app.forms.fields import EntriesField, EuroField

from flask import render_template
from flask_babel import _
from flask_babel import lazy_gettext as _l
from wtforms import RadioField, IntegerField, validators
from wtforms.validators import InputRequired

from app.forms.validators import IntegerLength, EURO_FIELD_MAX_LENGTH


class StepSteuerminderungYesNo(FormStep):
    name = 'steuerminderung_yesno'
    label = _l('form.lotse.step_steuerminderung.label')
    section_link = SectionLink('section_steuerminderung', name, _l('form.lotse.section_steuerminderung.label'))

    class Form(SteuerlotseBaseForm):
        steuerminderung = RadioField(
            # Field overrides the label with a default value if we don't explicitly set it to an empty string
            label='',
            render_kw={'data_label': _l('form.lotse.field_steuerminderung.data_label'),
                       'hide_label': True},
            choices=[
                ('yes', _l('form.lotse.field_steuerminderung-yes')),
                ('no', _l('form.lotse.field_steuerminderung-no')),
            ],
            validators=[InputRequired()]
        )

    def __init__(self, **kwargs):
        super(StepSteuerminderungYesNo, self).__init__(
            title=_l('form.lotse.steuerminderung-title'),
            intro=_l('form.lotse.steuerminderung-intro'),
            form=self.Form,
            header_title=_('form.lotse.steuerminderungen.header-title'),
            template='basis/form_full_width.html',
            **kwargs,
        )


class StepVorsorge(FormStep):
    name = 'vorsorge'
    label = _l('form.lotse.step_vorsorge.label')
    section_link = SectionLink('section_steuerminderung',
                               StepSteuerminderungYesNo.name,
                               _l('form.lotse.section_steuerminderung.label'))
    SKIP_COND = [
        ([('steuerminderung', 'no')], StepSteuerminderungYesNo.name, _l('form.lotse.skip_reason.steuerminderung_is_no')),
        ([('steuerminderung', None)], StepSteuerminderungYesNo.name, _l('form.lotse.skip_reason.steuerminderung_is_no'))
    ]

    class Form(SteuerlotseBaseForm):
        stmind_vorsorge_summe = EuroField(
            label=_l('form.lotse.field_vorsorge_summe'),
            validators=[IntegerLength(max=EURO_FIELD_MAX_LENGTH)],
            render_kw={'help': _l('form.lotse.field_vorsorge_summe-help'),
                       'data_label': _l('form.lotse.field_vorsorge_summe.data_label')})

    def __init__(self, **kwargs):
        super(StepVorsorge, self).__init__(
            title=_('form.lotse.vorsorge-title'),
            intro=_('form.lotse.vorsorge-intro'),
            form=self.Form,
            template='lotse/form_aufwendungen_with_list.html',
            **kwargs,
        )

    def render(self, data, render_info):
        render_info.form.first_field = next(iter(render_info.form))
        return render_template(self.template, form=render_info.form, render_info=render_info,
                               post_list_text=_('form.lotse.vorsorge.post-list-text'),
                               list_items=[
                                        _('form.lotse.vorsorge-list-item-1'),
                                        _('form.lotse.vorsorge-list-item-2'),
                                        _('form.lotse.vorsorge-list-item-3'),
                                    ],
                               header_title=_('form.lotse.steuerminderungen.header-title'),)


class StepAussergBela(FormStep):
    name = 'ausserg_bela'
    label = _l('form.lotse.step_ausserg_bela.label')
    section_link = SectionLink('section_steuerminderung',
                               StepSteuerminderungYesNo.name, _l('form.lotse.section_steuerminderung.label'))
    SKIP_COND = [
        ([('steuerminderung', 'no')], StepSteuerminderungYesNo.name, _l('form.lotse.skip_reason.steuerminderung_is_no')),
        ([('steuerminderung', None)], StepSteuerminderungYesNo.name, _l('form.lotse.skip_reason.steuerminderung_is_no'))
    ]

    class Form(SteuerlotseBaseForm):
        stmind_krankheitskosten_summe = EuroField(
            label=_l('form.lotse.field_krankheitskosten_summe'),
            render_kw={'help': _l('form.lotse.field_krankheitskosten-help'),
                       'data_label': _l('form.lotse.field_krankheitskosten_summe.data_label')},
            validators=[IntegerLength(max=EURO_FIELD_MAX_LENGTH)])
        stmind_krankheitskosten_anspruch = EuroField(
            label=_l('form.lotse.field_krankheitskosten_anspruch'),
            render_kw={'data_label': _l('form.lotse.field_krankheitskosten_anspruch.data_label')},
            validators=[IntegerLength(max=EURO_FIELD_MAX_LENGTH)])
        stmind_pflegekosten_summe = EuroField(
            label=_l('form.lotse.field_pflegekosten_summe'),
            render_kw={'help': _l('form.lotse.field_pflegekosten-help'),
                       'data_label': _l('form.lotse.field_pflegekosten_summe.data_label')},
            validators=[IntegerLength(max=EURO_FIELD_MAX_LENGTH)])
        stmind_pflegekosten_anspruch = EuroField(
            label=_l('form.lotse.field_pflegekosten_anspruch'),
            render_kw={'data_label': _l('form.lotse.field_pflegekosten_anspruch.data_label')},
            validators=[IntegerLength(max=EURO_FIELD_MAX_LENGTH)])
        stmind_beh_aufw_summe = EuroField(
            label=_l('form.lotse.field_beh_aufw_summe'),
            render_kw={'help': _l('form.lotse.field_beh_aufw-help'),
                       'data_label': _l('form.lotse.field_beh_aufw_summe.data_label')},
            validators=[IntegerLength(max=EURO_FIELD_MAX_LENGTH)])
        stmind_beh_aufw_anspruch = EuroField(
            label=_l('form.lotse.field_beh_aufw_anspruch'),
            render_kw={'data_label': _l('form.lotse.field_beh_aufw_anspruch.data_label')},
            validators=[IntegerLength(max=EURO_FIELD_MAX_LENGTH)])
        stmind_beh_kfz_summe = EuroField(
            label=_l('form.lotse.field_beh_kfz_summe'),
            render_kw={'help': _l('form.lotse.field_beh_kfz-help'),
                       'data_label': _l('form.lotse.field_beh_kfz_summe.data_label')},
            validators=[IntegerLength(max=EURO_FIELD_MAX_LENGTH)])
        stmind_beh_kfz_anspruch = EuroField(
            label=_l('form.lotse.field_beh_kfz_anspruch'),
            render_kw={'data_label': _l('form.lotse.field_beh_kfz_anspruch.data_label')},
            validators=[IntegerLength(max=EURO_FIELD_MAX_LENGTH)])
        stmind_bestattung_summe = EuroField(
            label=_l('form.lotse.bestattung_summe'),
            render_kw={'help': _l('form.lotse.bestattung-help'),
                       'data_label': _l('form.lotse.bestattung_summe.data_label')},
            validators=[IntegerLength(max=EURO_FIELD_MAX_LENGTH)])
        stmind_bestattung_anspruch = EuroField(
            label=_l('form.lotse.bestattung_anspruch'),
            render_kw={'data_label': _l('form.lotse.bestattung_anspruch.data_label')},
            validators=[IntegerLength(max=EURO_FIELD_MAX_LENGTH)])
        stmind_aussergbela_sonst_summe = EuroField(
            label=_l('form.lotse.aussergbela_sonst_summe'),
            render_kw={'help': _l('form.lotse.aussergbela_sonst-help'),
                       'data_label': _l('form.lotse.aussergbela_sonst_summe.data_label')},
            validators=[IntegerLength(max=EURO_FIELD_MAX_LENGTH)])
        stmind_aussergbela_sonst_anspruch = EuroField(
            label=_l('form.lotse.aussergbela_sonst_anspruch'),
            render_kw={'data_label': _l('form.lotse.aussergbela_sonst_anspruch.data_label')},
            validators=[IntegerLength(max=EURO_FIELD_MAX_LENGTH)])

    def __init__(self, **kwargs):
        super(StepAussergBela, self).__init__(
            title=_('form.lotse.ausserg_bela-title'),
            intro=_l('form.lotse.ausserg_bela-intro'),
            form=self.Form,
            header_title=_('form.lotse.steuerminderungen.header-title'),
            template='lotse/form_aufwendungen_with_list.html',
            **kwargs,
        )


class StepHaushaltsnahe(FormStep):
    name = 'haushaltsnahe'
    label = _l('form.lotse.step_haushaltsnahe.label')
    section_link = SectionLink('section_steuerminderung',
                               StepSteuerminderungYesNo.name, _l('form.lotse.section_steuerminderung.label'))
    SKIP_COND = [
        ([('steuerminderung', 'no')], StepSteuerminderungYesNo.name, _l('form.lotse.skip_reason.steuerminderung_is_no')),
        ([('steuerminderung', None)], StepSteuerminderungYesNo.name, _l('form.lotse.skip_reason.steuerminderung_is_no'))
    ]

    class Form(SteuerlotseBaseForm):
        stmind_haushaltsnahe_entries = EntriesField(
            label=_l('form.lotse.field_haushaltsnahe_entries'), default=[''],
            validators=[validators.Length(max=999)],
            render_kw={'help': _l('form.lotse.field_haushaltsnahe_entries-help'),
                       'data_label': _l('form.lotse.field_haushaltsnahe_entries.data_label')})
        stmind_haushaltsnahe_summe = EuroField(
            label=_l('form.lotse.field_haushaltsnahe_summe'),
            render_kw={'help': _l('form.lotse.field_haushaltsnahe_summe-help'),
                       'data_label': _l('form.lotse.field_haushaltsnahe_summe.data_label')},
            validators=[IntegerLength(max=EURO_FIELD_MAX_LENGTH)])

        def validate_stmind_haushaltsnahe_summe(self, field):
            if SteuerlotseBaseForm._list_has_entries(self.stmind_haushaltsnahe_entries):
                validators.InputRequired(_l('form.lotse.validation-haushaltsnahe-summe'))(self, field)
            else:
                validators.Optional()(self, field)

        def validate_stmind_haushaltsnahe_entries(self, field):
            if self.stmind_haushaltsnahe_summe.data:
                validators.InputRequired(_l('form.lotse.validation-haushaltsnahe-entries'))(self, field)
            else:
                validators.Optional()(self, field)

    def __init__(self, **kwargs):
        super(StepHaushaltsnahe, self).__init__(
            title=_('form.lotse.haushaltsnahe-title'),
            intro=_('form.lotse.haushaltsnahe-intro'),
            form=self.Form,
            template='lotse/form_aufwendungen_with_list.html',
            **kwargs,
        )

    def render(self, data, render_info):
        render_info.form.first_field = next(iter(render_info.form))
        return render_template(self.template, form=render_info.form, render_info=render_info, list_items=[
            _('form.lotse.haushaltsnahe-list-item-1'),
            _('form.lotse.haushaltsnahe-list-item-2'),
            _('form.lotse.haushaltsnahe-list-item-3'),
            _('form.lotse.haushaltsnahe-list-item-4'),
            _('form.lotse.haushaltsnahe-list-item-5'),
        ], header_title=_('form.lotse.steuerminderungen.header-title'))


class StepHandwerker(FormStep):
    name = 'handwerker'
    label = _l('form.lotse.step_handwerker.label')
    section_link = SectionLink('section_steuerminderung', StepSteuerminderungYesNo.name, _l('form.lotse.section_steuerminderung.label'))
    SKIP_COND = [([('steuerminderung', 'no')], StepSteuerminderungYesNo.name, _l('form.lotse.skip_reason.steuerminderung_is_no')),
                 ([('steuerminderung', None)], StepSteuerminderungYesNo.name, _l('form.lotse.skip_reason.steuerminderung_is_no'))]

    class Form(SteuerlotseBaseForm):
        stmind_handwerker_entries = EntriesField(
            label=_l('form.lotse.field_handwerker_entries'), default=[''],
            validators=[validators.Length(max=999)],
            render_kw={'help': _l('form.lotse.field_handwerker_entries-help'),
                       'data_label': _l('form.lotse.field_handwerker_entries.data_label')})
        stmind_handwerker_summe = EuroField(
            label=_l('form.lotse.field_handwerker_summe'),
            render_kw={'help': _l('form.lotse.field_handwerker_summe-help'),
                       'data_label': _l('form.lotse.field_handwerker_summe.data_label')},
            validators=[IntegerLength(max=EURO_FIELD_MAX_LENGTH)])
        stmind_handwerker_lohn_etc_summe = EuroField(
            label=_l('form.lotse.field_handwerker_lohn_etc_summe'),
            render_kw={'data_label': _l('form.lotse.field_handwerker_lohn_etc_summe.data_label')},
            validators=[IntegerLength(max=EURO_FIELD_MAX_LENGTH)])

        def validate_stmind_handwerker_summe(self, field):
            if SteuerlotseBaseForm._list_has_entries(self.stmind_handwerker_entries) or self.stmind_handwerker_lohn_etc_summe.data:
                validators.InputRequired(_l('form.lotse.validation-handwerker-summe'))(self, field)
            else:
                validators.Optional()(self, field)

        def validate_stmind_handwerker_entries(self, field):
            if self.stmind_handwerker_summe.data or self.stmind_handwerker_lohn_etc_summe.data:
                validators.InputRequired(_l('form.lotse.validation-handwerker-entries'))(self, field)
            else:
                validators.Optional()(self, field)

        def validate_stmind_handwerker_lohn_etc_summe(self, field):
            if self.stmind_handwerker_summe.data or SteuerlotseBaseForm._list_has_entries(self.stmind_handwerker_entries):
                validators.InputRequired(_l('form.lotse.validation-handwerker-lohn-etc-summe'))(self, field)
            else:
                validators.Optional()(self, field)

    def __init__(self, **kwargs):
        super(StepHandwerker, self).__init__(
            title=_('form.lotse.handwerker-title'),
            intro=_('form.lotse.handwerker-intro'),
            form=self.Form,
            template='lotse/form_aufwendungen_with_list.html',
            **kwargs,
        )

    def render(self, data, render_info):
        render_info.form.first_field = next(iter(render_info.form))
        return render_template(self.template, form=render_info.form, render_info=render_info, list_items=[
            _('form.lotse.handwerker-list-item-1'),
            _('form.lotse.handwerker-list-item-2'),
            _('form.lotse.handwerker-list-item-3'),
            _('form.lotse.handwerker-list-item-4'),
            _('form.lotse.handwerker-list-item-5'),
        ], header_title=_('form.lotse.steuerminderungen.header-title'))


class StepGemeinsamerHaushalt(FormStep):
    name = 'gem_haushalt'
    label = _l('form.lotse.step_gem_haushalt.label')
    section_link = SectionLink('section_steuerminderung', StepSteuerminderungYesNo.name, _l('form.lotse.section_steuerminderung.label'))
    SKIP_COND = [
        ([('steuerminderung', 'no')], StepSteuerminderungYesNo.name, _l('form.lotse.skip_reason.steuerminderung_is_no')),
        ([('steuerminderung', None)], StepSteuerminderungYesNo.name, _l('form.lotse.skip_reason.steuerminderung_is_no')),
        ([('familienstand', 'married')], StepFamilienstand.name, _l('form.lotse.skip_reason.stmind_gem_haushalt.married')),
        ([('familienstand', None)], StepFamilienstand.name, _l('form.lotse.skip_reason.stmind_gem_haushalt.married')),
        ([('stmind_handwerker_summe', None), ('stmind_haushaltsnahe_summe', None)], StepHaushaltsnahe.name,
         _l('form.lotse.skip_reason.stmind_gem_haushalt.no_handwerker_haushaltsnahe'))
    ]

    class Form(SteuerlotseBaseForm):
        stmind_gem_haushalt_count = IntegerField(
            label=_l('form.lotse.field_gem_haushalt_count'),
            render_kw={'data_label': _l('form.lotse.field_gem_haushalt_count.data_label')},
            validators=[IntegerLength(max=15)])

        stmind_gem_haushalt_entries = EntriesField(
            label=_l('form.lotse.field_gem_haushalt_entries'),
            render_kw={'help': _l('form.lotse.field_gem_haushalt_entries-help'),
                       'data_label': _l('form.lotse.field_gem_haushalt_entries.data_label')},
            default=[''],
            validators=[validators.Length(max=999)])

        def validate_stmind_gem_haushalt_count(self, field):
            if SteuerlotseBaseForm._list_has_entries(self.stmind_gem_haushalt_entries):
                validators.InputRequired(_l('form.lotse.validation-gem-haushalt-count'))(self, field)
            else:
                validators.Optional()(self, field)

        def validate_stmind_gem_haushalt_entries(self, field):
            if self.stmind_gem_haushalt_count.data and self.stmind_gem_haushalt_count.data != 0:
                validators.InputRequired(_l('form.lotse.validation-gem-haushalt-entries'))(self, field)
            else:
                validators.Optional()(self, field)

    def __init__(self, **kwargs):
        super(StepGemeinsamerHaushalt, self).__init__(
            title=_('form.lotse.gem-haushalt-title'),
            intro=_('form.lotse.gem-haushalt-intro'),
            form=self.Form,
            template='lotse/form_aufwendungen_with_list.html',
            **kwargs,
        )

    def render(self, data, render_info):
        render_info.form.first_field = next(iter(render_info.form))
        return render_template(self.template, form=render_info.form, render_info=render_info, list_items=[
            _('form.lotse.gem_haushalt-list-item-1'),
            _('form.lotse.gem_haushalt-list-item-2')
        ], header_title=_('form.lotse.steuerminderungen.header-title'))


class StepReligion(FormStep):
    name = 'religion'
    label = _l('form.lotse.step_religion.label')
    section_link = SectionLink('section_steuerminderung', StepSteuerminderungYesNo.name, _l('form.lotse.section_steuerminderung.label'))
    SKIP_COND = [([('steuerminderung', 'no')], StepSteuerminderungYesNo.name, _l('form.lotse.skip_reason.steuerminderung_is_no')),
                 ([('steuerminderung', None)], StepSteuerminderungYesNo.name, _l('form.lotse.skip_reason.steuerminderung_is_no'))]

    class Form(SteuerlotseBaseForm):
        stmind_religion_paid_summe = EuroField(
            label=_l('form.lotse.field_religion_paid_summe'),
            validators=[IntegerLength(max=EURO_FIELD_MAX_LENGTH)],
            render_kw={'help': _l('form.lotse.field_religion_paid_summe-help'),
                       'data_label': _l('form.lotse.field_religion_paid_summe.data_label')})
        stmind_religion_reimbursed_summe = EuroField(
            label=_l('form.lotse.field_religion_reimbursed_summe'),
            render_kw={'help': _l('form.lotse.field_religion_reimbursed-help'),
                       'data_label': _l('form.lotse.field_religion_reimbursed_summe.data_label')},
            validators=[IntegerLength(max=EURO_FIELD_MAX_LENGTH)])

    def __init__(self, **kwargs):
        super(StepReligion, self).__init__(
            title=_('form.lotse.religion-title'),
            intro=_l('form.lotse.religion-intro'),
            form=self.Form,
            template='lotse/form_aufwendungen_with_list.html',
            **kwargs,
        )

    def render(self, data, render_info):
        render_info.form.first_field = next(iter(render_info.form))
        return render_template(self.template, form=render_info.form, render_info=render_info, list_items=[],
                               header_title=_('form.lotse.steuerminderungen.header-title'))


class StepSpenden(FormStep):
    name = 'spenden'
    label = _l('form.lotse.step_spenden.label')
    section_link = SectionLink('section_steuerminderung', StepSteuerminderungYesNo.name, _l('form.lotse.section_steuerminderung.label'))
    SKIP_COND = [([('steuerminderung', 'no')], StepSteuerminderungYesNo.name, _l('form.lotse.skip_reason.steuerminderung_is_no')),
                 ([('steuerminderung', None)], StepSteuerminderungYesNo.name, _l('form.lotse.skip_reason.steuerminderung_is_no'))]

    class Form(SteuerlotseBaseForm):
        stmind_spenden_inland = EuroField(
            label=_l('form.lotse.spenden-inland'),
            validators=[IntegerLength(max=EURO_FIELD_MAX_LENGTH)],
            render_kw={'help': _l('form.lotse.spenden-help'),
                       'data_label': _l('form.lotse.spenden-inland.data_label')})
        stmind_spenden_inland_parteien = EuroField(
            label=_l('form.lotse.spenden-inland-parteien'),
            render_kw={'help': _l('form.lotse.spenden-inland-parteien-help'),
                       'data_label': _l('form.lotse.spenden-inland-parteien.data_label}')},
            validators=[IntegerLength(max=EURO_FIELD_MAX_LENGTH)])

    def __init__(self, **kwargs):
        super(StepSpenden, self).__init__(
            title=_('form.lotse.spenden-inland-title'),
            intro=_('form.lotse.spenden-inland-intro'),
            form=self.Form,
            header_title=_('form.lotse.steuerminderungen.header-title'),
            template='basis/form_standard.html',
            **kwargs,
        )
