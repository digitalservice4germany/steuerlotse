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
    text: t("lotse.taxNumber.taxNumberInput.label.labelText"),
  };

  let reformattedValues = values.join("");
  let inputFieldLengths;
  let setMaxLength = true;
  switch (splitType) {
    case "splitType_0":
      inputFieldLengths = [2, 3, 5];
      reformattedValues = [
        reformattedValues.slice(0, 2),
        reformattedValues.slice(2, 5),
        reformattedValues.slice(5, 10),
      ];
      break;
    case "splitType_1":
      inputFieldLengths = [3, 3, 5];
      reformattedValues = [
        reformattedValues.slice(0, 3),
        reformattedValues.slice(3, 6),
        reformattedValues.slice(6, 11),
      ];
      break;
    case "splitType_2":
      inputFieldLengths = [3, 4, 4];
      reformattedValues = [
        reformattedValues.slice(0, 3),
        reformattedValues.slice(3, 7),
        reformattedValues.slice(7, 11),
      ];
      break;
    default:
      inputFieldLengths = [11];
      setMaxLength = false;
      reformattedValues = [reformattedValues];
      label.exampleInput = t(
        "lotse.taxNumber.taxNumberInput.label.exampleInput"
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
            values: values.every(
              (item, index) => item.length <= inputFieldLengths[index]
            )
              ? values
              : reformattedValues,
            required,
            setMaxLength,
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
  splitType: PropTypes.oneOf([
    "splitType_0",
    "splitType_1",
    "splitType_2",
    "splitType_notSplit",
  ]).isRequired,
};

FormFieldTaxNumber.defaultProps = {
  autofocus: FormFieldSeparatedField.defaultProps.autofocus,
  required: FormFieldSeparatedField.defaultProps.required,
  details: FieldLabelForSeparatedFields.defaultProps.details,
};

export default FormFieldTaxNumber;
