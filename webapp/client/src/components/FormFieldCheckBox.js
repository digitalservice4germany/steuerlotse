import PropTypes from "prop-types";
import styled from "styled-components";
import FormFieldScaffolding from "./FormFieldScaffolding";
import checkedIcon from "../assets/icons/checked.svg";

const CheckBox = styled.div`
  & {
    padding: 0;
    margin-top: var(--spacing-02);
    flex-wrap: inherit;
  }

  input {
    width: 30px;
    height: 30px;
    opacity: 0;
  }

  input:focus + label {
    box-shadow: 0 0 0 3px var(--focus-color);
    background-color: var(--focus-color);
  }

  input:checked + label {
    background-color: var(--link-color);
    background-image: url(${checkedIcon});
    background-repeat: no-repeat;
    background-size: 22px;
    background-position: center;
  }

  label.checkmark {
    display: block;
    width: 30px;
    height: 30px;
    cursor: pointer;
    background: white;
    position: absolute;
    border: 2px solid var(--text-color);
  }
`;

function FormFieldCheckBox({
  fieldName,
  fieldId,
  checked,
  required,
  autofocus,
  labelText,
  errors,
}) {
  return (
    <FormFieldScaffolding
      {...{
        fieldName,
        errors,
      }}
      hideLabel
      render={() => (
        <CheckBox className="form-row col-lg-10">
          <input
            type="checkbox"
            id={fieldId}
            name={fieldName}
            required={required}
            defaultChecked={checked}
            // TODO: autofocus is under review.
            // eslint-disable-next-line
            autoFocus={autofocus}
          />
          {/* TODO: there should be only one label for an input */}
          {/* eslint-disable-next-line */}
          <label htmlFor={fieldId} className="checkmark" />
          <label
            htmlFor={fieldId}
            className="field-label col-sm-10 col-form-label ml-3 pt-0"
          >
            {labelText}
          </label>
        </CheckBox>
      )}
    />
  );
}

FormFieldCheckBox.propTypes = {
  fieldName: PropTypes.string.isRequired,
  fieldId: PropTypes.string.isRequired,
  labelText: PropTypes.oneOfType([PropTypes.string, PropTypes.element])
    .isRequired,
  errors: PropTypes.arrayOf(PropTypes.string).isRequired,
  checked: PropTypes.bool,
  required: PropTypes.bool,
  autofocus: PropTypes.bool,
};

FormFieldCheckBox.defaultProps = {
  checked: false,
  required: false,
  autofocus: false,
};

export default FormFieldCheckBox;
