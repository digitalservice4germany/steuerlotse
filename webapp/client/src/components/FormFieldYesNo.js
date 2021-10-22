import { useState } from "react";
import PropTypes from "prop-types";
import styled from "styled-components";
import FormFieldScaffolding from "./FormFieldScaffolding";
import FieldLabelForSeparatedFields from "./FieldLabelForSeparatedFields";

const YesNo = styled.div`
  & .switch-yes,
  .switch-no {
    padding: 1rem 1.45rem;
    color: var(--text-color) !important;
    background: var(--bg-white) !important;
    font-size: var(--text-s);
    box-shadow: none;
    border-radius: 0;
    border: 1px solid var(--border-color) !important;
  }

  & .switch-yes:focus,
  .switch-no:focus {
    color: var(--focus-text-color) !important;
    background: var(--focus-color) !important;

    box-shadow: none;
    border: 1px solid var(--text-color) !important;
    border-bottom: 4px solid var(--text-color) !important;
  }

  & .switch-yes.active,
  .switch-no.active {
    color: var(--inverse-text-color) !important;
    background: var(--link-color) !important;
    border-radius: 0;
    border: 1px solid var(--link-color) !important;
  }

  & .switch-yes.active.focus,
  .switch-no.active.focus {
    box-shadow: 0 0 0 3px var(--focus-color) !important;
  }

  & .switch-yes.active:hover,
  .switch-no.active:hover {
    background: var(--link-hover-color) !important;
    border: 1px solid var(--link-hover-color) !important;
  }
`;

function FormFieldYesNo({
  fieldName,
  fieldId,
  value,
  required,
  autofocus,
  label,
  details,
  errors,
}) {
  const [selectedValue, setSelectedValue] = useState(value);
  const yesFieldId = `${fieldId}-yes`;
  const noFieldId = `${fieldId}-no`;

  const toggleYesNoButton = (event) => {
    setSelectedValue(event.target.value);
  };

  return (
    <FormFieldScaffolding
      {...{
        fieldName,
        errors,
        cols: "12",
      }}
      hideLabel
      render={() => (
        <YesNo>
          <FieldLabelForSeparatedFields {...{ label, fieldId, details }} />
          <fieldset
            className="btn-group btn-group-toggle"
            id="steuernummer_exists"
            name="steuernummer_exists"
            data-toggle="buttons"
          >
            <label
              htmlFor={yesFieldId}
              className={`btn btn-secondary switch-yes ${
                selectedValue === "yes" ? "active" : ""
              }`}
            >
              <input
                type="radio"
                id={yesFieldId}
                name={fieldId}
                required={required}
                value="yes"
                active={selectedValue === "yes"}
                onClick={toggleYesNoButton}
              />
              Ja
            </label>
            <label
              htmlFor={noFieldId}
              className={`btn btn-secondary switch-yes ${
                selectedValue === "no" ? "active" : ""
              }`}
            >
              <input
                type="radio"
                id={noFieldId}
                name={fieldId}
                required={required}
                autoFocus={autofocus || Boolean(errors.length)}
                value="no"
                active={selectedValue === "no"}
                onClick={toggleYesNoButton}
              />
              Nein
            </label>
          </fieldset>
        </YesNo>
      )}
    />
  );
}

FormFieldYesNo.propTypes = {
  fieldName: PropTypes.string.isRequired,
  fieldId: PropTypes.string.isRequired,
  value: PropTypes.string,
  label: PropTypes.oneOfType([PropTypes.string, PropTypes.element]).isRequired,
  details: FieldLabelForSeparatedFields.propTypes.details,
  errors: PropTypes.arrayOf(PropTypes.string).isRequired,
  required: PropTypes.bool,
  autofocus: PropTypes.bool,
};

FormFieldYesNo.defaultProps = {
  value: undefined,
  required: false,
  autofocus: false,
  details: FieldLabelForSeparatedFields.defaultProps.details,
};

export default FormFieldYesNo;
