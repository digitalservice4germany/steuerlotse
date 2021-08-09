from decimal import Decimal

from flask import request
from flask.templating import render_template
from wtforms import RadioField, Field, StringField
from wtforms.fields.core import BooleanField, DateField, SelectField, IntegerField
from wtforms.utils import unset_value
from wtforms.validators import InputRequired
from wtforms.widgets.core import TextInput, Markup, html_params

from flask_babel import _
from flask_babel import lazy_gettext as _l
from babel.numbers import format_decimal, parse_decimal

from app.forms.validators import ValidElsterCharacterSet


class BaselineBugFixMixin:
    """ Safari and Firefox have a bug where empty input fields do not align correctly with baseline alignment. The reason is that
    if an input field is empty its bottom border is used as the baseline instead of the baseline of the text input.
    This can be fixed by setting a placeholder text. """

    def __call__(self, field, **kwargs):
        # Safari and Firefox have has a bug where empty input fields do not align correctly with baseline alignment.
        # Thus, we add a placeholder.
        kwargs.setdefault('placeholder', ' ')
        return kwargs


class SteuerlotseStringField(StringField):

    def pre_validate(self, form):
        ValidElsterCharacterSet().__call__(form, self)


class MultipleInputFieldWidget(TextInput, BaselineBugFixMixin):
    """A divided input field."""
    sub_field_separator = ''
    input_field_lengths = []
    input_field_labels = []

    def __call__(self, field, **kwargs):
        kwargs = BaselineBugFixMixin.__call__(self, field, **kwargs)

        if 'required' not in kwargs and 'required' in getattr(field, 'flags', []):
            kwargs['required'] = True
        kwargs['class'] = 'form-control'

        joined_input_fields = Markup()
        for idx, input_field_length in enumerate(self.input_field_lengths):
            kwargs['maxlength'] = input_field_length

            sub_field_id = f'{field.id}_{idx + 1}'
            kwargs['id'] = sub_field_id
            kwargs['value'] = field._value()[idx] if len(field._value()) >= idx + 1 else ''
            kwargs['class'] = kwargs.get('class', '') + f' input-width-{input_field_length}'

            if len(self.input_field_labels) > idx:
                joined_input_fields += Markup(
                    f'<div>'
                    f'<label for="{sub_field_id}" class="sub-field-label">{self.input_field_labels[idx]}</label>')
                joined_input_fields += (super(MultipleInputFieldWidget, self).__call__(field, **kwargs))
                joined_input_fields += Markup('</div>')
            else:
                joined_input_fields += (super(MultipleInputFieldWidget, self).__call__(field, **kwargs))
            if self.sub_field_separator and idx < len(self.input_field_lengths) - 1:
                joined_input_fields += Markup(self.sub_field_separator)

        return Markup(joined_input_fields)


class UnlockCodeWidget(MultipleInputFieldWidget):
    """A divided input field with three text input fields, limited to four chars."""
    sub_field_separator = '-'
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


class SteuerlotseDateWidget(MultipleInputFieldWidget):
    separator = ''
    input_field_lengths = [2, 2, 4]
    input_field_labels = [_l('date-field.day'), _l('date-field.month'), _l('date-field.year')]


class SteuerlotseDateField(DateField):

    def __init__(self, **kwargs):
        kwargs.setdefault('format', "%d %m %Y")

        if kwargs.get('render_kw'):
            kwargs['render_kw']['class'] = kwargs['render_kw'].get('class', '') + " date_input form-control"
            kwargs['render_kw']['example_input'] = kwargs['render_kw'].get('example_input',
                                                                           _('fields.date_field.example_input.text'))
        else:
            kwargs['render_kw'] = {'class': "date_input form-control",
                                   'example_input': _('fields.date_field.example_input.text')}
        super(SteuerlotseDateField, self).__init__(**kwargs)
        self.widget = SteuerlotseDateWidget()

    def _value(self):
        if self.data:
            return [self.data.day, self.data.month, self.data.year]
        else:
            return self.raw_data if self.raw_data else []


class IdNrWidget(MultipleInputFieldWidget):
    """A divided input field with four text input fields, limited to two to three chars."""
    sub_field_separator = ''
    input_field_lengths = [2, 3, 3, 3]


class IdNrField(SteuerlotseStringField):
    """
        Field to store the IdNr in four separate input fields.

        We get the formdata as a list of four strings (e.g. ['04', '452', '397', '687'])
        but want to handle it in the rest of the program as one string (e.g. '04452397687').
        At the same time, in case of a validation error (e.g. for ['04', '452', '3', '687']) we want to keep the order
        of inputs to not confuse the user. Thus, we only concatenate the strings to one string on succeeded validation
        in post_validate().
        Once the input validates, we can be sure to have the complete, valid string in our data and
        can split it into the expected chunks as seen in _value().
    """
    def __init__(self, label='', validators=None, **kwargs):
        super(IdNrField, self).__init__(label, validators, **kwargs)
        self.widget = IdNrWidget()

    def process_formdata(self, valuelist):
        # The formdata (from the request) is written to self.data as is (as a list of inputted strings)
        if valuelist:
            self.data = valuelist
        elif self.data is None:
            self.data = []

    def _value(self):
        """ Returns the representation of data as needed by the widget. In this case: a list of strings. """
        # In case the validation was not successful, we already have the data as a list of strings
        # (as it is not concatenated in post_validate()).
        if isinstance(self.data, list):
            return self.data

        # Once the validation has gone through, post_validate() stores the data as string.
        # As we know that it is correct, we can just separate it in chunks here.
        split_data = []
        chunk_sizes = self.widget.input_field_lengths
        start_idx = 0
        for chunk_size in chunk_sizes:
            end_index = start_idx + chunk_size
            if self.data:
                split_data.append(self.data[start_idx: end_index])
            start_idx = end_index
        return split_data

    def post_validate(self, form, validation_stopped):
        # Once the validation has gone through, we know that the idnr is correct.
        # We can therefore store it as a string and just separate it into chunks in self._value().
        if not validation_stopped and len(self.errors) == 0:
            self.data = ''.join(self.data)


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


class ConfirmationField(BooleanField):
    """A CheckBox that will not validate unless checked."""

    def __init__(self, label=None, false_values=None, input_required=True, **kwargs):
        validators = [InputRequired(message=_('confirmation_field_must_be_set'))] if input_required else []
        super(BooleanField, self).__init__(
            label,
            validators=validators,
            **kwargs
        )


class JqueryEntriesWidget(BaselineBugFixMixin, object):
    """A custom multi-entry widget that is based on jquery."""
    html_params = staticmethod(html_params)

    def __init__(self):
        self.input_type = None

    def __call__(self, field, **kwargs):
        kwargs = super().__call__(field, **kwargs)
        kwargs.setdefault('id', field.id)
        kwargs.setdefault('data', field.data)
        kwargs.setdefault('split_chars', field.split_chars)
        kwargs.setdefault('add_button_text', _('jquery_entries.add'))
        if 'value' not in kwargs:
            kwargs['value'] = field._value()
        if 'required' not in kwargs and 'required' in getattr(field, 'flags', []):
            kwargs['required'] = True
        if 'max_characters' not in kwargs:
            kwargs['max_characters'] = 25
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
