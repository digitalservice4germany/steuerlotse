import React, { useEffect, useRef } from "react";
import PropTypes from "prop-types";
import classNames from "classnames";
import styled from "styled-components";
import jQuery from "jquery";
import "jquery-mask-plugin";
import FieldError from "./FieldError";

const FormField = styled.div`
  &.error-found-line {
    margin-left: var(--spacing-02);
    padding-left: var(--spacing-04) !important;
    border-left: 2px solid var(--error-color);
  }
`;

// TODO: implement concrete fields with this:
// - ConfirmationField: cols="12" hideLabel=True
// - BooleanField, YesNoField: hideLabel=True
// - RadioField, SteuerlotseDateField: hideLabel=True hideErrors=True
export default function FormFieldScaffolding({
  render,
  fieldName,
  labelComponent,
  errors,
  cols,
  displayBlock,
  maxCharacters,
  extraClassNames,
  fieldDivClasses,
  hideLabel,
  hideErrors,
}) {
  const element = useRef();

  // TODO: replace jquery-mask with non-jquery equivalent
  useEffect(() => {
    jQuery(
      element.current.querySelectorAll("input[data-alphanumeric-field=true]")
    ).mask("W", {
      translation: { W: { pattern: /[a-zA-Z0-9]/, recursive: true } },
    });
  }, []);

  const divClassNames = classNames(`col-md-${cols}`, "px-0", fieldDivClasses, {
    "error-found-line": errors.length,
  });

  // TODO: these are not used by separated fields but will need to be included on non-separated fields.
  const fieldClassNames = classNames("form-control", extraClassNames, {
    "field-error-found": errors.length,
    [maxCharacters ? `input-width-${maxCharacters}` : "dummy"]: maxCharacters, // TODO: find a better way
  });

  return (
    <FormField ref={element} className={divClassNames}>
      {!hideLabel && labelComponent}
      <div className={classNames({ "d-block": displayBlock })}>
        {render(fieldClassNames)}
        {/* TODO: this goes into the concrete fields
          {% if field.type == 'ConfirmationField' %}
              {{ components.consent_box(field, classes=classes, position_details_after=position_details_after, first_field=first_field) }}
          {% elif field.type == 'BooleanField' %}
              {{ components.checkbox(field, classes=classes, position_details_after=position_details_after, first_field=first_field) }}
          {% elif field.type == 'RadioField' %}
              {{ components.radio_field(field, position_details_after=position_details_after, first_field=first_field) }}
          {% elif field.type == 'YesNoField' %}
              {{ components.yes_no_field(field, position_details_after=position_details_after, first_field=first_field) }}
          {% elif field.type == 'SteuerlotseDateField' %}
              {{ components.separated_field(field, position_details_after=position_details_after, first_field=first_field) }}
          {% else %}
              {% if first_field or field.errors %}
                  {{ field(class=classes, autofocus=True) }}
              {% else %}
                  {{ field(class=classes) }}
              {% endif %}
          {% endif %}
        */}
        {!hideErrors &&
          errors.map((error, index) => (
            // There is no natural key and the list is completely static, so using the index is fine.
            // eslint-disable-next-line
            <FieldError key={index} fieldName={fieldName}>
              {error}
            </FieldError>
          ))}
      </div>
    </FormField>
  );
}

FormFieldScaffolding.propTypes = {
  render: PropTypes.func.isRequired,
  fieldName: PropTypes.string.isRequired,
  labelComponent: PropTypes.element.isRequired,
  errors: PropTypes.arrayOf(PropTypes.string),
  cols: PropTypes.string,
  extraClassNames: PropTypes.string, // field.render_kw['class']
  maxCharacters: PropTypes.string, // field.render_kw['max_characters']
  fieldDivClasses: PropTypes.string,
  displayBlock: PropTypes.bool,
  hideLabel: PropTypes.bool,
  hideErrors: PropTypes.bool,
};

FormFieldScaffolding.defaultProps = {
  errors: [],
  cols: "6",
  extraClassNames: "",
  fieldDivClasses: "",
  maxCharacters: undefined,
  displayBlock: false,
  hideLabel: false,
  hideErrors: false,
};
