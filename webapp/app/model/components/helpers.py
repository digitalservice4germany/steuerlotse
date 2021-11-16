from wtforms import BooleanField, SelectField

from app.forms.fields import YesNoField


def form_fields_dict(form):
    fields = {}

    for field in form:
        field_dict = {
            # Need to convert to str because some errors use lazy babel strings, which pydantic's doesn't accept as str.
            'errors': list(map(str, field.errors)),
        }
        if isinstance(field, BooleanField):
            # Checkboxes don't need a 'value': WTForms is happy with any non-"False" value, browsers default to "on".
            # They do need to know whether the box should initially be checked or not, though.
            field_dict['checked'] = field.data
        elif isinstance(field, YesNoField):
            field_dict['value'] = field.data
        elif isinstance(field, SelectField):
            field_dict['selected_value'] = field.data
            if hasattr(field, 'choices'):
                # Need to convert to str because some choices use lazy babel strings, which pydantic's doesn't accept as str.
                field_dict['options'] = list(map(lambda field_choice: {"value": str(field_choice[0]), "display_name": str(field_choice[1])}, field.choices))
        elif hasattr(field, "_value"):
            field_dict['value'] = field._value()


        fields[field.name] = field_dict

    return fields
