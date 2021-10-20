import React from "react";
import PropTypes from "prop-types";
import FormFieldScaffolding from "./FormFieldScaffolding";
import FieldLabelForSeparatedFields from "./FieldLabelForSeparatedFields";
import FormFieldSeparatedField from "./FormFieldSeparatedField";
import {
  baselineBugFix,
  numericInputMask,
  numericInputMode,
} from "../lib/fieldUtils";

function FormFieldTaxNumber({
  fieldName,
  fieldId,
  values,
  required,
  autofocus,
  label,
  details,
  errors,
  isSplit,
}) {
  const labelComponent = (
    <FieldLabelForSeparatedFields {...{ label, fieldId, details }} />
  );

  const extraFieldProps = {
    ...numericInputMode,
    ...numericInputMask,
    ...baselineBugFix,
  };

  const inputFieldLengths = isSplit ? [3, 4, 4] : [11];

  return (
    <FormFieldScaffolding
      {...{
        fieldName,
        errors,
        labelComponent,
      }}
      hideLabel
      hideErrors
      render={() => (
        // Separated fields ignore field class names
        <FormFieldSeparatedField
          {...{
            fieldName,
            labelComponent,
            errors,
            details,
            extraFieldProps,
            fieldId,
            values,
            required,
          }}
          autoFocus={autofocus || Boolean(errors.length)}
          inputFieldLengths={inputFieldLengths}
        />
      )}
    />
  );
}

FormFieldTaxNumber.propTypes = {
  fieldId: PropTypes.string.isRequired,
  fieldName: PropTypes.string.isRequired,
  errors: PropTypes.arrayOf(PropTypes.string).isRequired,
  autofocus: PropTypes.bool,
  required: PropTypes.bool,
  values: PropTypes.arrayOf(PropTypes.string).isRequired,
  label: FieldLabelForSeparatedFields.propTypes.label,
  details: FieldLabelForSeparatedFields.propTypes.details,
  isSplit: PropTypes.bool.isRequired,
};

FormFieldTaxNumber.defaultProps = {
  autofocus: FormFieldSeparatedField.defaultProps.autofocus,
  required: FormFieldSeparatedField.defaultProps.required,
  label: FieldLabelForSeparatedFields.defaultProps.label,
  details: FieldLabelForSeparatedFields.defaultProps.details,
};

export default FormFieldTaxNumber;
