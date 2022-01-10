import { useState } from "react";
import PropTypes from "prop-types";
import styled from "styled-components";
import FormFieldScaffolding from "./FormFieldScaffolding";
import FieldLabelForSeparatedFields from "./FieldLabelForSeparatedFields";
import { optionsPropType } from "../lib/propTypes";
import FieldError from "./FieldError";
import radioButtonCheckedFocus from "../assets/icons/radio_button_checked_focus.svg";
import radioButtonCheckedHover from "../assets/icons/radio_button_checked_hover.svg";
import radioButtonChecked from "../assets/icons/radio_button_checked.svg";
import radioButtonDefault from "../assets/icons/radio_button_default.svg";
import radioButtonFocus from "../assets/icons/radio_button_focus.svg";
import radioButtonHover from "../assets/icons/radio_button_hover.svg";

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
  }

  input[type="radio"] + label::before {
    content: "";
    display: inline-block;
    vertical-align: bottom;
    width: 30px;
    height: 30px;
    min-width: 30px;
    margin-right: 12px;
    background: url(${radioButtonDefault}) no-repeat center;
  }

  input[type="radio"]:checked + label::before {
    background: url(${radioButtonChecked}) no-repeat center;
  }

  input[type="radio"]:checked + label:hover::before {
    background: url(${radioButtonCheckedHover}) no-repeat center;
  }

  input[type="radio"]:not(:checked):focus + label::before {
    background: url(${radioButtonFocus}) no-repeat center;
  }

  input[type="radio"]:not(:checked):hover + label::before {
    background: url(${radioButtonHover}) no-repeat center;
  }

  input[type="radio"]:checked:focus + label::before {
    background: url(${radioButtonCheckedFocus}) no-repeat center;
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
  const groupShouldHaveAutofocus = autofocus || (errors && errors.length !== 0);

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
      hideErrors
      render={() => (
        <Radio>
          <fieldset id={fieldId} name={fieldId}>
            <FieldLabelForSeparatedFields {...{ label, fieldId, details }} />
            <div className="radio-button-list">
              {options.map((option, i) => [
                <input
                  type="radio"
                  id={`${fieldId}-${option.value}`}
                  key={`${fieldId}-${option.value}`}
                  name={fieldId}
                  required={required}
                  autoFocus={groupShouldHaveAutofocus && i === 0}
                  value={option.value}
                  defaultChecked={selectedValue === option.value}
                  onClick={toggleRadioButton}
                  onChange={onChangeHandler}
                />,
                <label
                  htmlFor={`${fieldId}-${option.value}`}
                  key={`${fieldId}-label-${option.value}`}
                >
                  <span>{option.displayName}</span>
                </label>,
              ])}
            </div>
            {errors.map((error, index) => (
              // There is no natural key and the list is completely static, so using the index is fine.
              // eslint-disable-next-line
              <FieldError key={index} fieldName={fieldName}>
                {error}
              </FieldError>
            ))}
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
