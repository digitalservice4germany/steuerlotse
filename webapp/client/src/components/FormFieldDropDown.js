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

  & .steuerlotse-select {
    border: 2px solid var(--border-color);
    border-radius: 0;
    background-image: url(${selectIcon});
    background-repeat: no-repeat;
    background-size: 0.75rem;
    min-height: 55px;
  }

  & .steuerlotse-select:focus {
    border: 2px solid var(--focus-border-color);
    box-shadow: 0 0 0 2px var(--focus-color);
  }
`;

function FormFieldDropDown({
  fieldName,
  fieldId,
  values,
  defaultValue,
  preselectedValue,
  required,
  autofocus,
  label,
  details,
  errors,
  onChangeHandler,
}) {
  return (
    <FormFieldScaffolding
      {...{
        fieldName,
        errors,
        cols: "6",
      }}
      hideLabel
      render={() => (
        <DropDown>
          <FieldLabelForSeparatedFields {...{ label, fieldId, details }} />
          <select
            id={fieldId}
            className="custom-select steuerlotse-select"
            input_req_err_msg="Bundesland auswählen"
            name={fieldId}
            value={preselectedValue}
            required={required}
            autoFocus={autofocus || Boolean(errors.length)}
            onBlur={onChangeHandler}
            onChange={onChangeHandler}
          >
            {defaultValue && <option value="">{defaultValue}</option>}
            {values.map((value) => (
              <option value={value[0]}>{value[1]}</option>
            ))}
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
  preselectedValue: PropTypes.string,
  label: PropTypes.oneOfType([PropTypes.string, PropTypes.element]).isRequired,
  details: FieldLabelForSeparatedFields.propTypes.details,
  errors: PropTypes.arrayOf(PropTypes.string).isRequired,
  required: PropTypes.bool,
  autofocus: PropTypes.bool,
  onChangeHandler: PropTypes.func,
};

FormFieldDropDown.defaultProps = {
  defaultValue: undefined,
  preselectedValue: undefined,
  required: false,
  autofocus: false,
  details: FieldLabelForSeparatedFields.defaultProps.details,
  onChangeHandler: () => {},
};

export default FormFieldDropDown;
