from flask import render_template

REACT_COMPONENT = 'react_component.html'

def render_react_template(component, props=None, form=None, header_title=None):                          
    return render_template(REACT_COMPONENT,
            component=component,
            props=props,
            form=form,
            header_title=header_title)