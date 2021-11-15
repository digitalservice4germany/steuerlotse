import React from "react";
import { useTranslation } from "react-i18next";
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
  details,
  errors,
  isSplit,
}) {
  const { t } = useTranslation();

  const label = {
    text: t("lotseFlow.taxNumber.taxNumberInput.label.labelText"),
  };

  if (isSplit) {
    label.exampleInput = t(
      "lotseFlow.taxNumber.taxNumberInput.label.exampleInput"
    );
  }

  const fieldLabelProps = { label, fieldId, details };

  const labelComponent = <FieldLabelForSeparatedFields {...fieldLabelProps} />;

  const extraFieldProps = {
    ...numericInputMode,
    ...numericInputMask,
    ...baselineBugFix,
  };

  const inputFieldLengths = isSplit ? [3, 4, 4] : [11];
  const concatValues = isSplit ? values : [values.join()];

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
            values: concatValues,
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
  details: FieldLabelForSeparatedFields.propTypes.details,
  isSplit: PropTypes.bool.isRequired,
};

FormFieldTaxNumber.defaultProps = {
  autofocus: FormFieldSeparatedField.defaultProps.autofocus,
  required: FormFieldSeparatedField.defaultProps.required,
  details: FieldLabelForSeparatedFields.defaultProps.details,
};

export default FormFieldTaxNumber;
