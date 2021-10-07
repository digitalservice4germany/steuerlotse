from wtforms import BooleanField


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
        else:
            field_dict['value'] = field._value()

        fields[field.name] = field_dict

    return fields
