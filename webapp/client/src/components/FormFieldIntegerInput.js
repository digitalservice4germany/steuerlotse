import React from "react";
import PropTypes from "prop-types";
import { IMaskInput } from "react-imask";
import classNames from "classnames";
import FormFieldScaffolding from "./FormFieldScaffolding";
import FieldLabel from "./FieldLabel";
import FormFieldSeparatedField from "./FormFieldSeparatedField";

function FormFieldIntegerInput({
  fieldName,
  fieldId,
  value,
  required,
  autofocus,
  label,
  fieldWidth,
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
        <IMaskInput
          mask={Number}
          scale={0}
          type="text"
          id={fieldId}
          name={fieldName}
          defaultValue={value}
          inputMode="numeric"
          pattern="[0-9]*"
          maxLength={maxLength}
          // TODO: autofocus is under review.
          // eslint-disable-next-line
          autoFocus={autofocus || Boolean(errors.length)}
          required={required}
          className={classNames("form-control", `input-width-${fieldWidth}`)}
        />
      )}
    />
  );
}

FormFieldIntegerInput.propTypes = {
  fieldId: PropTypes.string.isRequired,
  fieldName: PropTypes.string.isRequired,
  errors: PropTypes.arrayOf(PropTypes.string).isRequired,
  autofocus: PropTypes.bool,
  required: PropTypes.bool,
  setMask: PropTypes.bool,
  value: PropTypes.string.isRequired,
  label: FieldLabel.propTypes.label,
  fieldWidth: PropTypes.number,
  maxLength: PropTypes.number,
  details: FieldLabel.propTypes.details,
};

FormFieldIntegerInput.defaultProps = {
  autofocus: FormFieldSeparatedField.defaultProps.autofocus,
  required: FormFieldSeparatedField.defaultProps.required,
  setMask: false,
  label: FieldLabel.defaultProps.label,
  fieldWidth: 25,
  maxLength: undefined,
  details: FieldLabel.defaultProps.details,
};

export default FormFieldIntegerInput;
