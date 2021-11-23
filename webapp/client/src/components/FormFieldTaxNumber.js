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
  splitType,
}) {
  const { t } = useTranslation();

  const label = {
    text: t("lotseFlow.taxNumber.taxNumberInput.label.labelText"),
  };

  let concatValues = values.join("");
  let inputFieldLengths;
  switch (splitType) {
    case "0":
      inputFieldLengths = [2, 3, 5];
      concatValues = [
        concatValues.slice(0, 2),
        concatValues.slice(2, 5),
        concatValues.slice(5, 10),
      ];
      break;
    case "1":
      inputFieldLengths = [3, 3, 5];
      concatValues = [
        concatValues.slice(0, 3),
        concatValues.slice(3, 6),
        concatValues.slice(6, 11),
      ];
      break;
    case "2":
      inputFieldLengths = [3, 4, 4];
      concatValues = [
        concatValues.slice(0, 3),
        concatValues.slice(3, 7),
        concatValues.slice(7, 11),
      ];
      break;
    default:
      inputFieldLengths = [11];
      concatValues = [concatValues];
      label.exampleInput = t(
        "lotseFlow.taxNumber.taxNumberInput.label.exampleInput"
      );
      break;
  }

  const fieldLabelProps = { label, fieldId, details };

  const labelComponent = <FieldLabelForSeparatedFields {...fieldLabelProps} />;

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
            values: concatValues,
            required,
          }}
          key={`steuernummerField-${splitType}`} // Enforce re-rendering if other splitType is used
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
  splitType: PropTypes.oneOf(["0", "1", "2", "3"]).isRequired,
};

FormFieldTaxNumber.defaultProps = {
  autofocus: FormFieldSeparatedField.defaultProps.autofocus,
  required: FormFieldSeparatedField.defaultProps.required,
  details: FieldLabelForSeparatedFields.defaultProps.details,
};

export default FormFieldTaxNumber;
