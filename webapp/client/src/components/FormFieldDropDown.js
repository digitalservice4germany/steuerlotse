import PropTypes from "prop-types";
import styled from "styled-components";
import FormFieldScaffolding from "./FormFieldScaffolding";
import FieldLabel from "./FieldLabel";
import selectIcon from "../assets/icons/select_icon.svg";

const DropDown = styled.div`
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
  options,
  defaultOption,
  selectedValue,
  required,
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
          <FieldLabel {...{ label, fieldId, details }} />
          <select
            id={fieldId}
            className="custom-select steuerlotse-select"
            name={fieldId}
            defaultValue={selectedValue}
            required={required}
            autoFocus={Boolean(errors.length)}
            onBlur={onChangeHandler}
            onChange={onChangeHandler}
          >
            {defaultOption && (
              <option value="" key={fieldId + defaultOption}>
                {defaultOption}
              </option>
            )}
            {options.map((option) => (
              <option value={option.value} key={fieldId + option.value}>
                {option.displayName}
              </option>
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
  options: PropTypes.arrayOf(PropTypes.object).isRequired,
  defaultOption: PropTypes.string,
  selectedValue: PropTypes.string,
  label: FieldLabel.propTypes.label,
  details: FieldLabel.propTypes.details,
  errors: PropTypes.arrayOf(PropTypes.string).isRequired,
  required: PropTypes.bool,
  autofocus: PropTypes.bool,
  onChangeHandler: PropTypes.func,
};

FormFieldDropDown.defaultProps = {
  defaultOption: undefined,
  selectedValue: undefined,
  label: FieldLabel.defaultProps.label,
  required: false,
  autofocus: false,
  details: FieldLabel.defaultProps.details,
  onChangeHandler: undefined,
};

export default FormFieldDropDown;
