import React from "react";
import PropTypes from "prop-types";
import classNames from "classnames";
import styled from "styled-components";
import Details from "./Details";
import FieldError from "./FieldError";
import FormRowCentered from "./FormRowCentered";
import FieldLabelScaffolding from "./FieldLabelScaffolding";

const SeparatedField = styled(FormRowCentered)`
  flex-wrap: nowrap;
  margin-top: 0;
`;

function FormFieldSeparatedField({
  fieldName,
  fieldId,
  values,
  required,
  autofocus,
  details,
  errors,
  labelComponent,
  subFieldSeparator,
  inputFieldLengths,
  inputFieldLabels,
  extraFieldProps,
  transformUppercase,
}) {
  // TODO: add behaviour from multiple_input_field

  return (
    <fieldset id={fieldId}>
      {labelComponent}
      {
        // TODO styled-components
      }
      <SeparatedField className="separated-field">
        {inputFieldLengths.map((length, index) => {
          const subFieldId = `${fieldId}_${index + 1}`;
          const inputElement = (
            <input
              type="text"
              id={subFieldId}
              name={fieldName}
              defaultValue={values.length > index ? values[index] : ""}
              maxLength={length}
              data-field-length={length}
              // TODO: autofocus is under review.
              // eslint-disable-next-line
              autoFocus={autofocus && index === 0}
              required={required}
              className={classNames("form-control", `input-width-${length}`)}
              style={transformUppercase ? { textTransform: "uppercase" } : {}}
              {...extraFieldProps}
            />
          );

          return (
            // There is no natural key and the list is completely static, so using the index is fine.
            // eslint-disable-next-line
            <React.Fragment key={index}>
              {inputFieldLabels.length > index ? (
                <div>
                  <label htmlFor={subFieldId} className="sub-field-label">
                    {inputFieldLabels[index]}
                  </label>
                  {inputElement}
                </div>
              ) : (
                inputElement
              )}
              {subFieldSeparator &&
                index < inputFieldLengths.length - 1 &&
                subFieldSeparator}
            </React.Fragment>
          );
        })}
      </SeparatedField>
      {details && details.positionAfterField && (
        <Details title={details.title} detailsId={fieldId}>
          {{
            paragraphs: [details.text],
          }}
        </Details>
      )}
      {errors.map((error, index) => (
        // There is no natural key and the list is completely static, so using the index is fine.
        // eslint-disable-next-line
        <FieldError key={index} fieldName={fieldName}>
          {error}
        </FieldError>
      ))}
    </fieldset>
  );
}

FormFieldSeparatedField.propTypes = {
  fieldName: PropTypes.string.isRequired,
  fieldId: PropTypes.string.isRequired,
  values: PropTypes.arrayOf(PropTypes.string).isRequired,
  errors: PropTypes.arrayOf(PropTypes.string).isRequired,
  details: FieldLabelScaffolding.propTypes.details,
  labelComponent: PropTypes.element.isRequired,
  subFieldSeparator: PropTypes.string,
  inputFieldLengths: PropTypes.arrayOf(PropTypes.number),
  inputFieldLabels: PropTypes.arrayOf(PropTypes.string),
  // TODO: This is used for what used to be wtforms widget mixins, mostly to do with input masking.
  // Revisit when reimplementing input masking in React.
  // eslint-disable-next-line
  extraFieldProps: PropTypes.object,
  transformUppercase: PropTypes.bool,
  required: PropTypes.bool,
  autofocus: PropTypes.bool,
};

FormFieldSeparatedField.defaultProps = {
  details: undefined,
  subFieldSeparator: "",
  inputFieldLengths: [],
  inputFieldLabels: [],
  extraFieldProps: {},
  transformUppercase: false,
  required: false,
  autofocus: false,
};

export default FormFieldSeparatedField;
