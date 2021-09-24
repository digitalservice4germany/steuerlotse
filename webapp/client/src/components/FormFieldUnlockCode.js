import React from "react";
import PropTypes from "prop-types";
import FormFieldScaffolding from "./FormFieldScaffolding";
import FieldLabelForSeparatedFields from "./FieldLabelForSeparatedFields";
import FormFieldSeparatedField from "./FormFieldSeparatedField";
import { alphanumericInput, baselineBugFix } from "../lib/fieldUtils";

function FormFieldUnlockCode({
  fieldName,
  fieldId,
  values,
  required,
  autofocus,
  label,
  details,
  errors,
}) {
  const labelComponent = (
    <FieldLabelForSeparatedFields {...{ label, fieldId, details }} />
  );

  const extraFieldProps = {
    ...alphanumericInput,
    ...baselineBugFix,
  };

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
          transformUppercase
          autofocus={autofocus || Boolean(errors.length)}
          subFieldSeparator="-"
          inputFieldLengths={[4, 4, 4]}
        />
      )}
    />
  );
}

FormFieldUnlockCode.propTypes = {
  fieldId: PropTypes.string.isRequired,
  fieldName: PropTypes.string.isRequired,
  errors: PropTypes.arrayOf(PropTypes.string).isRequired,
  autofocus: PropTypes.bool,
  required: PropTypes.bool,
  values: PropTypes.arrayOf(PropTypes.string).isRequired,
  label: FieldLabelForSeparatedFields.propTypes.label,
  details: FieldLabelForSeparatedFields.propTypes.details,
};
FormFieldUnlockCode.defaultProps = {
  autofocus: FormFieldSeparatedField.defaultProps.autofocus,
  required: FormFieldSeparatedField.defaultProps.required,
  label: FieldLabelForSeparatedFields.defaultProps.label,
  details: FieldLabelForSeparatedFields.defaultProps.details,
};

export default FormFieldUnlockCode;
