import React from "react";
import PropTypes from "prop-types";
import { useTranslation } from "react-i18next";
import FormFieldScaffolding from "./FormFieldScaffolding";
import FieldLabelForSeparatedFields from "./FieldLabelForSeparatedFields";
import FormFieldSeparatedField from "./FormFieldSeparatedField";
import {
  baselineBugFix,
  numericInputMask,
  numericInputMode,
} from "../lib/fieldUtils";

function FormFieldDate({
  fieldName,
  fieldId,
  values,
  required,
  autofocus,
  label,
  details,
  errors,
}) {
  const { t } = useTranslation();

  const labelWithDefaultExample = {
    // Use default example input if none is given
    exampleInput: t("fields.dateField.exampleInput.text"),
    ...label,
  };

  const labelComponent = (
    <FieldLabelForSeparatedFields
      {...{ label: labelWithDefaultExample, fieldId, details }}
    />
  );

  const extraFieldProps = {
    ...numericInputMode,
    ...numericInputMask,
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
          autofocus={autofocus || Boolean(errors.length)}
          inputFieldLengths={[2, 2, 4]}
          inputFieldLabels={[
            t("dateField.day"),
            t("dateField.month"),
            t("dateField.year"),
          ]}
        />
      )}
    />
  );
}

FormFieldDate.propTypes = {
  fieldId: PropTypes.string.isRequired,
  fieldName: PropTypes.string.isRequired,
  errors: PropTypes.arrayOf(PropTypes.string).isRequired,
  autofocus: PropTypes.bool,
  required: PropTypes.bool,
  values: PropTypes.arrayOf(PropTypes.string).isRequired,
  label: FieldLabelForSeparatedFields.propTypes.label,
  details: FieldLabelForSeparatedFields.propTypes.details,
};

FormFieldDate.defaultProps = {
  autofocus: FormFieldSeparatedField.defaultProps.autofocus,
  required: FormFieldSeparatedField.defaultProps.required,
  label: FieldLabelForSeparatedFields.defaultProps.label,
  details: FieldLabelForSeparatedFields.defaultProps.details,
};

export default FormFieldDate;
