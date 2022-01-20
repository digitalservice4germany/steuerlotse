import React from "react";
import PropTypes from "prop-types";
import { IMaskInput } from "react-imask";
import classNames from "classnames";
import FormFieldScaffolding from "./FormFieldScaffolding";
import FieldLabel from "./FieldLabel";
import FormFieldSeparatedField from "./FormFieldSeparatedField";

function FormFieldEuroInput({
  fieldName,
  fieldId,
  value,
  required,
  autofocus,
  label,
  currency,
  fieldWidth,
  maxLength,
  details,
  errors,
}) {
  // To adapt for the thousandsSeparator sign increase the maxLength
  const calculatedMaxLength =
    maxLength !== undefined ? maxLength + Math.floor(maxLength / 3) : undefined;
  return (
    <FormFieldScaffolding
      {...{
        fieldName,
        errors,
      }}
      labelComponent={<FieldLabel {...{ label, fieldId, details }} />}
      render={() => (
        <div
          className={classNames(
            "input-group",
            "euro-field",
            `input-width-${fieldWidth}`
          )}
        >
          <IMaskInput
            id={fieldId}
            name={fieldName}
            defaultValue={value}
            scale={2}
            type="text"
            inputMode="numeric"
            pattern="[0-9]*"
            mask={Number}
            thousandsSeparator="."
            radix=","
            mapToRadix={[]} // Overwrite to prevent that the thousandsSeparator '.' is mapped to radix
            maxLength={calculatedMaxLength}
            // TODO: autofocus is under review.
            // eslint-disable-next-line
            autoFocus={autofocus || Boolean(errors.length)}
            required={required}
            className={classNames("form-control", "euro_field")}
          />
          <div
            className={classNames("input-group-text", "euro-field-appendix")}
          >
            {currency}
          </div>
        </div>
      )}
    />
  );
}

FormFieldEuroInput.propTypes = {
  fieldId: PropTypes.string.isRequired,
  fieldName: PropTypes.string.isRequired,
  errors: PropTypes.arrayOf(PropTypes.string).isRequired,
  autofocus: PropTypes.bool,
  required: PropTypes.bool,
  value: PropTypes.string.isRequired,
  label: FieldLabel.propTypes.label,
  fieldWidth: PropTypes.number,
  maxLength: PropTypes.number,
  currency: PropTypes.string,
  details: FieldLabel.propTypes.details,
};

FormFieldEuroInput.defaultProps = {
  autofocus: FormFieldSeparatedField.defaultProps.autofocus,
  required: FormFieldSeparatedField.defaultProps.required,
  label: FieldLabel.defaultProps.label,
  fieldWidth: 25,
  maxLength: undefined,
  currency: "€",
  details: FieldLabel.defaultProps.details,
};

export default FormFieldEuroInput;
