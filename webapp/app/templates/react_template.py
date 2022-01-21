from flask import render_template

def render_react_template(component, props=None, form=None, header_title=None, **kwargs):
    return render_template('react_component.html',
            component=component,
            props=props,
            form=form,
            header_title=header_title,
            **kwargs)