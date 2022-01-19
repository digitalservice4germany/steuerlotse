import React from "react";
import PropTypes from "prop-types";
import { IMaskInput } from "react-imask";
import styled from "styled-components";
import classNames from "classnames";
import FormFieldScaffolding from "./FormFieldScaffolding";
import FieldLabel from "./FieldLabel";
import FormFieldSeparatedField from "./FormFieldSeparatedField";

const FormEuroField = styled.div``;
const FormCurrencyField = styled.div``;

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
  return (
    <FormFieldScaffolding
      {...{
        fieldName,
        errors,
        label,
      }}
      labelComponent={<FieldLabel {...{ label, fieldId, details }} />}
      render={() => (
        <FormEuroField
          className={classNames(
            "input-group",
            "euro-field",
            `input-width-${fieldWidth}`
          )}
        >
          <IMaskInput
            mask={Number}
            scale={2}
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
            onWheel={(e) => e.target.blur()}
            className={classNames("form-control", "euro_field")}
          />
          <FormCurrencyField
            className={classNames("input-group-text", "euro-field-appendix")}
          >
            {currency}
          </FormCurrencyField>
        </FormEuroField>
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
