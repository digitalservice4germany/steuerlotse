def form_fields_dict(form):
    return {
        field.name: {
            'value': field._value(),
            'errors': field.errors,
        }
        for field in form
    }
