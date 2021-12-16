import React from "react";
import PropTypes from "prop-types";
import classNames from "classnames";
import FormFieldScaffolding from "./FormFieldScaffolding";
import FieldLabel from "./FieldLabel";
import FormFieldSeparatedField from "./FormFieldSeparatedField";

function FormFieldTextInput({
  fieldName,
  fieldId,
  value,
  required,
  autofocus,
  label,
  maxWidth,
  maxLength,
  details,
  errors,
}) {
  return (
    <FormFieldScaffolding
      {...{
        fieldName,
        errors,
      }}
      labelComponent={<FieldLabel {...{ label, fieldId, details }} />}
      render={() => (
        <input
          type="number"
          id={fieldId}
          name={fieldName}
          defaultValue={value}
          inputMode="numeric"
          maxLength={maxLength}
          // TODO: autofocus is under review.
          // eslint-disable-next-line
          autoFocus={autofocus || Boolean(errors.length)}
          required={required}
          className={classNames("form-control", `input-width-${maxWidth}`)}
        />
      )}
    />
  );
}

FormFieldTextInput.propTypes = {
  fieldId: PropTypes.string.isRequired,
  fieldName: PropTypes.string.isRequired,
  errors: PropTypes.arrayOf(PropTypes.string).isRequired,
  autofocus: PropTypes.bool,
  required: PropTypes.bool,
  setMask: PropTypes.bool,
  value: PropTypes.string.isRequired,
  label: FieldLabel.propTypes.label,
  maxWidth: PropTypes.number,
  maxLength: PropTypes.number,
  details: FieldLabel.propTypes.details,
};

FormFieldTextInput.defaultProps = {
  autofocus: FormFieldSeparatedField.defaultProps.autofocus,
  required: FormFieldSeparatedField.defaultProps.required,
  setMask: false,
  label: FieldLabel.defaultProps.label,
  maxWidth: 25,
  maxLength: undefined,
  details: FieldLabel.defaultProps.details,
};

export default FormFieldTextInput;
