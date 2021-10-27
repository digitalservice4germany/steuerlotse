from flask import render_template
from flask_wtf.csrf import generate_csrf

from app.forms import SteuerlotseBaseForm
from app.forms.steps.step import FormStep, SectionLink, DisplayStep
from app.forms.fields import ConfirmationField

from flask_babel import _
from flask_babel import lazy_gettext as _l

from app.model.components import DeclarationIncomesProps
from app.model.components.helpers import form_fields_dict


class StepDeclarationIncomes(FormStep):
    name = 'decl_incomes'

    label = _l('form.lotse.declaration_incomes.label')
    section_link = SectionLink('mandatory_data', name, _l('form.lotse.mandatory_data.label'))

    class Form(SteuerlotseBaseForm):
        declaration_incomes = ConfirmationField(
            label=_l('form.lotse.field_declaration_incomes.field-confirm-incomes'),
            render_kw={'data_label': _l('form.lotse.field_declaration_incomes.data_label')})

    def __init__(self, **kwargs):
        super(StepDeclarationIncomes, self).__init__(
            title=_('form.lotse.declaration_incomes.title'),
            intro=_('form.lotse.declaration_incomes.intro'),
            form=self.Form,
            **kwargs)

    def render(self, data, render_info):
        props_dict = DeclarationIncomesProps(
            step_header={
                'title': render_info.step_title,
                'intro': render_info.step_intro,
            },
            form={
                'action': render_info.submit_url,
                'csrf_token': generate_csrf(),
                'show_overview_button': bool(render_info.overview_url),
            },
            fields=form_fields_dict(render_info.form),
        ).camelized_dict()

        return render_template('react_component.html',
                               component='DeclarationIncomesPage',
                               props=props_dict,
                               # TODO: These are still required by base.html to set the page title.
                               form=render_info.form,
                               header_title=_('form.lotse.header-title'))


class StepDeclarationEdaten(FormStep):
    name = 'decl_edaten'

    label = _l('form.lotse.field_declaration_edaten.label')
    section_link = SectionLink('mandatory_data', StepDeclarationIncomes.name, _l('form.lotse.mandatory_data.label'))

    class Form(SteuerlotseBaseForm):
        declaration_edaten = ConfirmationField(
            label=_l('form.lotse.field_declaration_edaten'),
            render_kw={'data_label': _l('form.lotse.field_declaration_edaten.data_label')})

    def __init__(self, **kwargs):
        super(StepDeclarationEdaten, self).__init__(
            title=_('form.lotse.declaration-edaten-title'),
            intro=_l('form.lotse.declaration-edaten-intro'),
            form=self.Form,
            header_title=_('form.lotse.header-title'),
            template='basis/form_standard_with_list.html',
            **kwargs,
        )


class StepSessionNote(DisplayStep):
    name = 'session_note'

    def __init__(self, **kwargs):
        super(StepSessionNote, self).__init__(
            title=_('form.lotse.session-note.title'), **kwargs)

    def render(self, data, render_info):
        return render_template('basis/display_standard_with_list.html', render_info=render_info, list_items=[
            _l('form.lotse.session-note.list-item-1'),
            _l('form.lotse.session-note.list-item-2'),
            _l('form.lotse.session-note.list-item-3'),
            _l('form.lotse.session-note.list-item-4'),
        ], header_title=_('form.lotse.header-title'))
