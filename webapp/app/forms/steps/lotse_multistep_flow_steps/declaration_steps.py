from flask_wtf.csrf import generate_csrf
from wtforms.validators import InputRequired

from app.forms import SteuerlotseBaseForm
from app.forms.steps.step import FormStep, SectionLink
from app.forms.fields import ConfirmationField

from flask_babel import _
from flask_babel import lazy_gettext as _l

from app.model.components import DeclarationIncomesProps, DeclarationEDatenProps, StepSessionNoteProps
from app.model.components.helpers import form_fields_dict
from app.templates.react_template import render_react_template


class StepDeclarationIncomes(FormStep):
    name = 'decl_incomes'

    label = _l('form.lotse.declaration_incomes.label')
    section_link = SectionLink('mandatory_data', name, _l('form.lotse.mandatory_data.label'))

    class Form(SteuerlotseBaseForm):
        declaration_incomes = ConfirmationField(
            label=_l('form.lotse.field_declaration_incomes.field-confirm-incomes'),
            validators=[InputRequired(message=_l('form.lotse.declaration_incomes.required'))],
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

        return render_react_template(component='DeclarationIncomesPage',
                                     props=props_dict,
                                     # TODO: These are still required by base.html to set the page title.
                                     form=render_info.form,
                                     header_title=_('form.lotse.header-title'),
                                     disable_extended_footer=True)


class StepDeclarationEdaten(FormStep):
    name = 'decl_edaten'

    label = _l('form.lotse.field_declaration_edaten.label')
    section_link = SectionLink('mandatory_data', StepDeclarationIncomes.name, _l('form.lotse.mandatory_data.label'))

    def __init__(self, **kwargs):
        super(StepDeclarationEdaten, self).__init__(
            title=_('form.lotse.declaration-edaten-title'),
            intro=_('form.lotse.declaration-edaten-intro'),
            form=self.Form,
            **kwargs)

    class Form(SteuerlotseBaseForm):
        declaration_edaten = ConfirmationField(
            label=_l('form.lotse.field_declaration_edaten'),
            validators=[InputRequired(message=_l('form.lotse.declaration_edaten.required'))],
            render_kw={'data_label': _l('form.lotse.field_declaration_edaten.data_label')})

    def render(self, data, render_info):
        props_dict = DeclarationEDatenProps(
            step_header={
                'title': _('form.lotse.declaration-edaten-title')
            },
            form={
                'action': render_info.submit_url,
                'csrf_token': generate_csrf(),
                'show_overview_button': bool(render_info.overview_url),
            },
            prev_url=render_info.prev_url,
            fields=form_fields_dict(render_info.form),
        ).camelized_dict()

        return render_react_template(component='DeclarationEDatenPage',
                                     props=props_dict,
                                     # TODO: These are still required by base.html to set the page title.
                                     form=render_info.form,
                                     header_title=_('form.lotse.header-title'),
                                     disable_extended_footer=True)


class StepSessionNote(FormStep):
    name = 'session_note'

    class Form(SteuerlotseBaseForm):
        pass

    def __init__(self, **kwargs):
        super(StepSessionNote, self).__init__(
            title=_('form.lotse.session-note.title'),
            form=self.Form,
            **kwargs)

    def render(self, data, render_info):
        props_dict = StepSessionNoteProps(
            form={
                'action': render_info.submit_url,
                'csrf_token': generate_csrf(),
                'show_overview_button': bool(render_info.overview_url),
            },
            prev_url=render_info.prev_url,
        ).camelized_dict()

        return render_react_template(component='SessionNotePage',
                                     props=props_dict,
                                     header_title=_('form.lotse.header-title'),
                                     disable_extended_footer=True)
