import pytest
from wtforms import Form, validators
from wtforms.fields.core import StringField

from app.model.components.helpers import form_fields_dict

@pytest.fixture
def basic_form():
    class TestForm(Form):
        first_name = StringField(u'First Name', validators=[validators.input_required()])
        last_name  = StringField(u'Last Name', validators=[])

    form = TestForm(data={
        'first_name': None,
        'last_name': 'Musterfrau'
    })
    form.validate()
    return form

class TestFormFieldsDict:
    def test_basic_conversion(self, basic_form):
        props = form_fields_dict(basic_form)

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
