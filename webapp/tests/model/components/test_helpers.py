import pytest
from werkzeug.datastructures import MultiDict
from wtforms import Form, validators
from wtforms.fields.core import BooleanField, StringField

from app.model.components.helpers import form_fields_dict


def _form_factory(form_class):
    def _create_form(**kwargs):
        form = form_class(MultiDict(kwargs))
        form.validate()
        return form

    return _create_form


@pytest.fixture
def basic_form():
    class TestForm(Form):
        first_name = StringField(u'First Name', validators=[validators.input_required()])
        last_name = StringField(u'Last Name', validators=[])

    return _form_factory(TestForm)


@pytest.fixture
def form_with_checkbox():
    class TestForm(Form):
        first_name = StringField(u'First Name', validators=[validators.input_required()])
        i_agree = BooleanField(u'Yes?', validators=[])

    return _form_factory(TestForm)


class TestFormFieldsDict:
    def test_should_return_value_and_errors(self, basic_form):
        form = basic_form(first_name=None, last_name='Musterfrau')

        props = form_fields_dict(form)

        assert props == {
            'first_name': {
                'value': '',
                'errors': ['This field is required.']
            },
            'last_name': {
                'value': 'Musterfrau',
                'errors': []
            }
        }

    @pytest.mark.parametrize('checked', [True, False])
    def test_checkboxes_should_return_checked_and_errors(self, form_with_checkbox, checked):
        form = form_with_checkbox(first_name='Erika', i_agree=checked)

        props = form_fields_dict(form)

        assert props == {
            'first_name': {
                'value': 'Erika',
                'errors': []
            },
            'i_agree': {
                'checked': checked,
                'errors': []
            }
        }
