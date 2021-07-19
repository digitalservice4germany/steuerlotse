from decimal import Decimal

from flask import request
from flask.templating import render_template
from wtforms import RadioField, Field, StringField
from wtforms.fields.core import BooleanField, DateField, SelectField
from wtforms.utils import unset_value
from wtforms.validators import InputRequired
from wtforms.widgets.core import TextInput, Markup, html_params

from flask_babel import _
from babel.numbers import format_decimal, parse_decimal

from app.forms.validators import ValidElsterCharacterSet


class SteuerlotseStringField(StringField):
    def pre_validate(self, form):
        ValidElsterCharacterSet().__call__(form, self)


class MultipleInputFieldWidget(TextInput):
    """A divided input field."""
    separator = ''
    input_field_lengths = []

    def __call__(self, field, **kwargs):
        if 'required' not in kwargs and 'required' in getattr(field, 'flags', []):
            kwargs['required'] = True
        kwargs['class'] = 'form-control'

        joined_input_fields = Markup()
        for idx, input_field_length in enumerate(self.input_field_lengths):
            kwargs['maxlength'] = input_field_length

            kwargs['value'] = field._value()[idx] if len(field._value()) >= idx + 1 else ''
            kwargs['id'] = f'{field.id}_{idx + 1}'
            joined_input_fields += (super(MultipleInputFieldWidget, self).__call__(field, **kwargs))
            if self.separator and idx < len(self.input_field_lengths) - 1:
                joined_input_fields += Markup(self.separator)

        return Markup(joined_input_fields)


class UnlockCodeWidget(MultipleInputFieldWidget):
    """A divided input field with three text input fields, limited to four chars."""
    separator = '-'
    input_field_lengths = [4, 4, 4]


class UnlockCodeField(SteuerlotseStringField):
    def __init__(self, label='', validators=None, **kwargs):
        super(UnlockCodeField, self).__init__(label, validators, **kwargs)
        self.widget = UnlockCodeWidget()

    def process_formdata(self, valuelist):
        if valuelist:
            self.data = '-'.join(valuelist)
        elif self.data is None:
            self.data = ''

    def _value(self):
        return self.data.split('-') if self.data else ''


class EuroFieldWidget(TextInput):
    """A simple Euro widget that uses Bootstrap features for nice looks."""

    def __call__(self, field, **kwargs):
        kwargs['class'] = 'euro_field form-control'
        kwargs['onwheel'] = 'this.blur()'
        markup_input = super(EuroFieldWidget, self).__call__(field, **kwargs)

        markup = Markup(
            Markup('<div class="input-group euro-field">') +
            markup_input +
            Markup('<div class="input-group-append"><span class="input-group-text euro-field-appendix">€</span></div>') +
            Markup('</div>')
        )
        return markup


class EuroField(Field):
    """The Euro field will use Bootstrap features to display the currency symbol, work with German
    locale and internally handles the entry as a Decimal."""
    widget = EuroFieldWidget()

    def __init__(self, label, locale='de_DE', **kwargs):
        super(EuroField, self).__init__(label, **kwargs)
        self.locale = locale
        self.default_value = ''
        if 'render_kw' not in kwargs:
            kwargs['render_kw'] = {}

        if 'example_input' not in kwargs['render_kw']:
            kwargs['render_kw']['example_input'] = _('fields.euro_field.example_input.text')

    def _value(self):
        if self.data in (None, ''):
            return self.default_value
        else:
            return format_decimal(self.data, locale=self.locale).replace('.', '')

    def process_formdata(self, raw_data):
        if not raw_data or not raw_data[0]:
            self.data = None
        else:
            self.data = Decimal(parse_decimal(raw_data[0], locale=self.locale))


class SteuerlotseSelectField(SelectField):

    def __init__(self, **kwargs):
        if kwargs.get('render_kw'):
            if kwargs['render_kw'].get('class'):
                kwargs['render_kw']['class'] = kwargs['render_kw']['class'] + " custom-select steuerlotse-select"
            else:
                kwargs['render_kw']['class'] = "custom-select steuerlotse-select"
        else:
            kwargs['render_kw'] = {'class': "custom-select steuerlotse-select"}
        super(SteuerlotseSelectField, self).__init__(**kwargs)


class SteuerlotseDateField(DateField):

    def __init__(self, **kwargs):
        if not kwargs.get('format'):
            kwargs['format'] = "%d.%m.%Y"

        if kwargs.get('render_kw'):
            if kwargs['render_kw'].get('class'):
                kwargs['render_kw']['class'] = kwargs['render_kw']['class'] + " date_input form-control"
            else:
                kwargs['render_kw']['class'] = "date_input form-control"
            if 'example_input' not in kwargs['render_kw']:
                kwargs['render_kw']['example_input'] = _('fields.date_field.example_input.text')
        else:
            kwargs['render_kw'] = {'class': "date_input form-control",
                                   'example_input': _('fields.date_field.example_input.text')}
        super(SteuerlotseDateField, self).__init__(**kwargs)


class ConfirmationField(BooleanField):
    """A CheckBox that will not validate unless checked."""

    def __init__(self, label=None, false_values=None, input_required=True, **kwargs):
        validators = [InputRequired(message=_('confirmation_field_must_be_set'))] if input_required else []
        super(BooleanField, self).__init__(
            label,
            validators=validators,
            **kwargs
        )


class JqueryEntriesWidget(object):
    """A custom multi-entry widget that is based on jquery."""
    html_params = staticmethod(html_params)

    def __init__(self):
        self.input_type = None

    def __call__(self, field, **kwargs):
        kwargs.setdefault('id', field.id)
        kwargs.setdefault('data', field.data)
        kwargs.setdefault('split_chars', field.split_chars)
        kwargs.setdefault('add_button_text', _('jquery_entries.add'))
        if 'value' not in kwargs:
            kwargs['value'] = field._value()
        if 'required' not in kwargs and 'required' in getattr(field, 'flags', []):
            kwargs['required'] = True
        return Markup(render_template('fields/jquery_entries.html', kwargs=kwargs))


class EntriesField(Field):
    """The entries field will display its internal `list` data through multiple
    input text boxes where the user can add and remove items."""
    widget = JqueryEntriesWidget()
    split_chars = '~~~'

    def _value(self):
        if self.data:
            return self.split_chars.join(self.data)
        else:
            return ''

    def _split(self, string):
        return [x.strip() for x in string.split(self.split_chars) if x]

    def process_formdata(self, valuelist):
        if valuelist:
            self.data = self._split(valuelist[0])
        else:
            self.data = []

    def pre_validate(self, form):
        ValidElsterCharacterSet().__call__(form, self)


class YesNoWidget(object):
    """A simple switch-box that allows to choose between yes and no."""

    def __call__(self, field, **kwargs):
        if 'required' not in kwargs and 'required' in getattr(field, 'flags', []):
            kwargs['required'] = True

        html = ""
        html += f'<fieldset class="btn-group btn-group-toggle" id="{field.id}" name="{field.name}" data-toggle="buttons">\n'

        for choice in field.choices:
            value, desc = choice
            html += f'<label for="{field.id}-{value}" class="btn btn-secondary switch-{value}">'
            html += f'<input type="radio" %s>' % html_params(
                id=f'{field.id}-{value}',
                name=field.name,
                value=value,
                checked=(field.data == value),
                **kwargs
            )
            html += desc
            html += '</label>\n'

        html += '</fieldset>\n'

        return Markup(html)


class YesNoField(RadioField):
    def __init__(self, label='', validators=None, **kwargs):
        kwargs['choices'] = [('yes', _('switch.yes')), ('no', _('switch.no'))]
        super(YesNoField, self).__init__(label, validators, **kwargs)
        self.widget = YesNoWidget()

    def process(self, formdata, data=unset_value):
        # In a POST-request, `formdata` is all data posted by the user (MultiDict).
        # In contrast, `data` is the value previously stored for the field ('yes' or 'no').
        # In case the user does not select yes or no for this specific YesNoField instance (example: yes_no_field),
        # the `formdata` does not include 'yes_no_field' as a key.
        #
        # Default behaviour of WTForms:
        # If yes_no_field was previously filled - thus is present in `data` (as 'yes' or 'no') -
        # it overrides the nonexistent value 'yes_no_field' in `formdata`.
        # input: `data` = 'yes'; `formdata` = {}
        # result: {'yes_no_field': 'yes'}
        #
        # Wanted behaviour:
        # If no option is selected we want to store that no option is selected.
        # We therefore disregard the `data` in case `formdata` is POSTed without this field and `data` is set.
        # input: `data` = 'yes'; `formdata` = {}
        # result: {}
        if request and request.method == 'POST' and data != unset_value and \
                (not formdata or self.name not in formdata):
            super(YesNoField, self).process(formdata)
        else:
            super(YesNoField, self).process(formdata, data)
