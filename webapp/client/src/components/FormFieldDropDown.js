import PropTypes from "prop-types";
import styled from "styled-components";
import { useTranslation } from "react-i18next";
import FormFieldScaffolding from "./FormFieldScaffolding";
import FieldLabel from "./FieldLabel";
import selectIcon from "../assets/icons/select_icon.svg";

const DropDown = styled.select`
  .steuerlotse-select {
    border: 2px solid var(--border-color);
    border-radius: 0;
    background-image: url(${selectIcon});
    background-repeat: no-repeat;
    background-size: 0.75rem;
    min-height: 55px;
  }

  .steuerlotse-select:focus {
    border: 2px solid var(--focus-border-color);
    box-shadow: 0 0 0 2px var(--focus-color);
  }
`;

function FormFieldDropDown({
  fieldName,
  fieldId,
  options,
  selectedValue,
  required,
  label,
  details,
  errors,
  onChangeHandler,
}) {
  const { t } = useTranslation();
  return (
    <FormFieldScaffolding
      {...{
        fieldName,
        errors,
        cols: "6",
      }}
      labelComponent=<FieldLabel {...{ label, fieldId, details }} />
      render={() => (
        <DropDown
          id={fieldId}
          className="custom-select steuerlotse-select"
          name={fieldName}
          defaultValue={selectedValue}
          required={required}
          autoFocus={Boolean(errors.length)}
          onChange={onChangeHandler}
        >
          {
            <option value="" key={`${fieldId}defaultOption`}>
              {t("dropDown.defaultOption")}
            </option>
          }
          {options.map((option) => (
            <option value={option.value} key={fieldId + option.value}>
              {option.displayName}
            </option>
          ))}
        </DropDown>
      )}
    />
  );
}

FormFieldDropDown.propTypes = {
  fieldName: PropTypes.string.isRequired,
  fieldId: PropTypes.string.isRequired,
  options: PropTypes.arrayOf(PropTypes.object).isRequired,
  selectedValue: PropTypes.string,
  label: FieldLabel.propTypes.label,
  details: FieldLabel.propTypes.details,
  errors: PropTypes.arrayOf(PropTypes.string).isRequired,
  required: PropTypes.bool,
  autofocus: PropTypes.bool,
  onChangeHandler: PropTypes.func,
};

FormFieldDropDown.defaultProps = {
  selectedValue: undefined,
  label: FieldLabel.defaultProps.label,
  required: false,
  autofocus: false,
  details: FieldLabel.defaultProps.details,
  onChangeHandler: undefined,
};

export default FormFieldDropDown;
