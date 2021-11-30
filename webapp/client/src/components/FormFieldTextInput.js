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
  maxLength,
  setMaxLength,
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
          type="text"
          id={fieldId}
          name={fieldName}
          defaultValue={value}
          maxLength={setMaxLength ? maxLength : null}
          data-field-length={maxLength}
          // TODO: autofocus is under review.
          // eslint-disable-next-line
          autoFocus={autofocus || Boolean(errors.length)}
          required={required}
          className={classNames("form-control", `input-width-${maxLength}`)}
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
  value: PropTypes.string.isRequired,
  label: FieldLabel.propTypes.label,
  maxLength: PropTypes.number,
  setMaxLength: PropTypes.bool,
  details: FieldLabel.propTypes.details,
};

FormFieldTextInput.defaultProps = {
  autofocus: FormFieldSeparatedField.defaultProps.autofocus,
  required: FormFieldSeparatedField.defaultProps.required,
  label: FieldLabel.defaultProps.label,
  maxLength: 25,
  setMaxLength: false,
  details: FieldLabel.defaultProps.details,
};

export default FormFieldTextInput;
