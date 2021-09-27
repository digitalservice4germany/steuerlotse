import PropTypes from "prop-types";
import styled from "styled-components";
import FormFieldScaffolding from "./FormFieldScaffolding";

const ConsentBox = styled.div`
  &.checkbox {
    padding: 0;
    margin-top: var(--spacing-02);
    flex-wrap: inherit;
  }

  &.consent-box {
    background-color: var(--bg-highlight-color);
    padding: var(--spacing-04);
  }

  &.checkbox input {
    width: 30px;
    height: 30px;
    opacity: 0;
  }

  &.checkbox input:focus + label {
    box-shadow: 0 0 0 3px var(--focus-color);
    background-color: var(--focus-color);
  }

  &.checkbox input:checked + label {
    background-color: var(--link-color);
    background-image: url("../images/checked.svg");
    background-repeat: no-repeat;
    background-size: 22px;
    background-position: center;
  }

  & label.checkmark {
    display: block;
    width: 30px;
    height: 30px;
    cursor: pointer;
    background: white;
    position: absolute;
    border: 2px solid var(--text-color);
  }
`;

function FormFieldConsentBox({
  fieldName,
  fieldId,
  value,
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
        cols: "12",
      }}
      hideLabel
      render={() => (
        <ConsentBox className="form-row checkbox consent-box col-lg-10">
          <input
            type="checkbox"
            id={fieldId}
            defaultValue={value}
            required={required}
            autoFocus={autofocus}
          />
          {/* TODO: there should be only one label for an input */}
          {/* eslint-disable-next-line */}
          <label htmlFor={fieldId} className="checkmark" />
          <label
            htmlFor={fieldId}
            className="col-sm-10 col-form-label ml-3 pt-0"
          >
            {labelText}
          </label>
        </ConsentBox>
      )}
    />
  );
}

FormFieldConsentBox.propTypes = {
  fieldName: PropTypes.string.isRequired,
  fieldId: PropTypes.string.isRequired,
  labelText: PropTypes.oneOfType([PropTypes.string, PropTypes.element])
    .isRequired,
  value: PropTypes.string,
  errors: PropTypes.arrayOf(PropTypes.string).isRequired,
  required: PropTypes.bool,
  autofocus: PropTypes.bool,
};

FormFieldConsentBox.defaultProps = {
  value: "y", // the default of WTForms BooleanField
  required: false,
  autofocus: false,
};

export default FormFieldConsentBox;
