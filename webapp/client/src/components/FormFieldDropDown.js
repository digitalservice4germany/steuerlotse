import PropTypes from "prop-types";
import styled from "styled-components";
import FormFieldScaffolding from "./FormFieldScaffolding";
import FieldLabelForSeparatedFields from "./FieldLabelForSeparatedFields";
import selectIcon from "../assets/icons/select_icon.svg";

const DropDown = styled.div`
  & label {
    display: block;
    width: 30px;
    height: 30px;
    cursor: pointer;
    background: white;
    position: absolute;
  }

  & steuerlotse-select {
    border: 2px solid var(--border-color);
    border-radius: 0;
    background-color: #fff;
    background-image: url(${selectIcon});
    background-repeat: no-repeat;
    background-size: 0.75rem;
    background-position: center;
    min-height: 55px;
  }

  & form-control {
    border: 2px solid var(--border-color);
    border-radius: 0;
    min-height: 55px;
  }

  & form-control:hover {
    border: 2px solid var(--hover-border-color);
  }

  & form-control:focus {
    border: 2px solid var(--border-color);
    box-shadow: 0 0 0 2px var(--focus-color);
  }

  & form-control:active {
    border: 2px solid var(--border-color);
    box-shadow: 0 0 0 2px var(--active-outline-color);
  }

  & form-control.field-error-found {
    border: 2px solid var(--error-color);
  }
`;

function FormFieldDropDown({
  fieldName,
  fieldId,
  values,
  defaultValue,
  required,
  autofocus,
  label,
  details,
  errors,
}) {
  const options = defaultValue ? [<option>{defaultValue}</option>] : [];
  values.forEach((value) => {
    options.push(<option value={value[0]}>{value[1]}</option>);
  });
  return (
    <FormFieldScaffolding
      {...{
        fieldName,
        errors,
        cols: "12",
      }}
      hideLabel
      render={() => (
        <DropDown>
          <FieldLabelForSeparatedFields {...{ label, fieldId, details }} />
          <select
            id={fieldId}
            className="form-control custom-select steuerlotse-select"
            input_req_err_msg="Bundesland auswählen"
            name={fieldId}
            required={required}
            autoFocus={autofocus || Boolean(errors.length)}
          >
            {options}
          </select>
        </DropDown>
      )}
    />
  );
}

FormFieldDropDown.propTypes = {
  fieldName: PropTypes.string.isRequired,
  fieldId: PropTypes.string.isRequired,
  values: PropTypes.arrayOf(PropTypes.arrayOf(PropTypes.string)).isRequired,
  defaultValue: PropTypes.string,
  label: PropTypes.oneOfType([PropTypes.string, PropTypes.element]).isRequired,
  details: FieldLabelForSeparatedFields.propTypes.details,
  errors: PropTypes.arrayOf(PropTypes.string).isRequired,
  required: PropTypes.bool,
  autofocus: PropTypes.bool,
};

FormFieldDropDown.defaultProps = {
  defaultValue: undefined,
  required: false,
  autofocus: false,
  details: FieldLabelForSeparatedFields.defaultProps.details,
};

export default FormFieldDropDown;
