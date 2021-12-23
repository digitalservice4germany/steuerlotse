import { useState } from "react";
import PropTypes from "prop-types";
import styled from "styled-components";
import { Trans } from "react-i18next";
import FormFieldScaffolding from "./FormFieldScaffolding";
import FieldLabelForSeparatedFields from "./FieldLabelForSeparatedFields";
import { optionsPropType } from "../lib/propTypes";

const Radio = styled.div`
  input[type="radio"] {
    opacity: 0;
    position: absolute;
  }

  input[type="radio"] + label {
    display: flex;
    padding-left: 0;
    padding-top: 0;
    font-size: var(--text-medium);
    white-space: pre;
  }

  input[type="radio"] + label::before {
    content: "";
    display: inline-block;
    vertical-align: bottom;
    width: 30px;
    height: 30px;
    min-width: 30px;
    margin-right: 12px;
    background: url("/icons/radio_button_default.svg") no-repeat center;
  }

  input[type="radio"]:checked + label::before {
    background: url("/icons/radio_button_checked.svg") no-repeat center;
  }

  input[type="radio"]:checked + label:hover::before {
    background: url("/icons/radio_button_checked_hover.svg") no-repeat center;
  }

  input[type="radio"]:not(:checked):focus + label::before {
    background: url("/icons/radio_button_focus.svg") no-repeat center;
  }

  input[type="radio"]:checked:focus + label::before {
    background: url("/icons/radio_button_checked_focus.svg") no-repeat center;
  }

  .radio-button-list {
    padding-top: var(--spacing-02);
  }
`;

function FormFieldRadioGroup({
  fieldName,
  fieldId,
  options,
  value,
  required,
  autofocus,
  label,
  details,
  errors,
  onChangeHandler,
}) {
  const [selectedValue, setSelectedValue] = useState(value);

  const toggleRadioButton = (event) => {
    setSelectedValue(event.target.value);
  };

  return (
    <FormFieldScaffolding
      {...{
        fieldName,
        errors,
      }}
      hideLabel
      render={() => (
        <Radio>
          <fieldset id={fieldId} name={fieldId}>
            <FieldLabelForSeparatedFields {...{ label, fieldId, details }} />
            <div className="radio-button-list">
              {options.map((option, i) => [
                <input
                  type="radio"
                  id={fieldId + option.value}
                  key={`${fieldId}-${option.value}`}
                  name={fieldId}
                  required={required}
                  autoFocus={autofocus && i === 0}
                  value={option.value}
                  defaultChecked={selectedValue === option.value}
                  onClick={toggleRadioButton}
                  onChange={onChangeHandler}
                />,
                <label
                  htmlFor={fieldId + option.value}
                  key={`${fieldId}-label-${option.value}`}
                >
                  {option.displayName}
                </label>,
              ])}
            </div>
          </fieldset>
        </Radio>
      )}
    />
  );
}

FormFieldRadioGroup.propTypes = {
  fieldName: PropTypes.string.isRequired,
  fieldId: PropTypes.string.isRequired,
  options: optionsPropType.isRequired,
  value: PropTypes.string,
  label: PropTypes.oneOfType([PropTypes.string, PropTypes.object]),
  details: FieldLabelForSeparatedFields.propTypes.details,
  errors: PropTypes.arrayOf(PropTypes.string).isRequired,
  required: PropTypes.bool,
  autofocus: PropTypes.bool,
  onChangeHandler: PropTypes.func,
};

FormFieldRadioGroup.defaultProps = {
  value: undefined,
  label: undefined,
  required: false,
  autofocus: false,
  details: FieldLabelForSeparatedFields.defaultProps.details,
  onChangeHandler: undefined,
};

export default FormFieldRadioGroup;

export function boldifyChoices(oldChoices) {
  return oldChoices.map((choice) => ({
    value: choice.value,
    displayName: (
      <Trans
        components={{
          bold: <b />,
        }}
      >
        {choice.displayName}
      </Trans>
    ),
  }));
}
