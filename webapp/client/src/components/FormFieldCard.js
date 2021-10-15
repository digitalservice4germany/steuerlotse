import PropTypes from "prop-types";
import styled from "styled-components";
import FormFieldScaffolding from "./FormFieldScaffolding";
import checkedIcon from "../assets/icons/checked.svg";

const Card = styled.label`
  background-color: var(--bg-white);

  padding: var(--spacing-04);
  margin-bottom: var(--spacing-03);
  margin-right: 0;

  border-radius: 4px;
  border: 1px;
  border-style: solid;
  border-color: var(--bg-highlight-color);

  justify-content: space-between;
  align-items: flex-start;

  &.checkbox {
    margin-top: var(--spacing-02);
    flex-wrap: inherit;
  }

  &.checkbox input {
    width: 1px;
    height: 1px;
    opacity: 0;
    position: absolute;
    overflow: hidden;
  }

  &.checkbox input:focus + .checkmark {
    box-shadow: 0 0 0 3px var(--focus-color);
    background-color: var(--focus-color);
  }

  &.checkbox input:checked + .checkmark {
    background-color: var(--link-color);
    background-image: url(${checkedIcon});
    background-repeat: no-repeat;
    background-size: 22px;
    background-position: center;
  }

  & .checkmark {
    display: block;
    position: absolute;
    right: var(--spacing-04); // the card's padding
    width: 30px;
    height: 30px;
    min-width: 30px;
    min-height: 30px;
    margin-left: var(--spacing-06);
    cursor: pointer;
    background: white;
    border: 2px solid var(--text-color);
  }
  --checkmark-width: calc(30px + var(--spacing-06));

  @media (max-width: 510px) {
    & .checkmark {
      margin-left: var(--spacing-02);
  }
`;

const LabelTitle = styled.span`
  display: block;
  font-weight: var(--font-bold);
  font-size: var(--text-xl);
`;

const LabelText = styled.span`
  display: block;
  margin-top: var(--spacing-02);
`;

const CardIcon = styled.img`
  display: block;
  margin-right: var(--spacing-06);
  margin-bottom: var(--spacing-01);
`;

const IconTextWrapper = styled.div`
  display: flex;
  flex-direction: row;
  flex-wrap: inherit;
  align-items: flex-start;

  margin-right: var(--checkmark-width);

  @media (max-width: 510px) {
    flex-wrap: wrap;
    margin-right: 0;
  }
`;

function FormFieldCard({
  fieldName,
  fieldId,
  checked,
  required,
  autofocus,
  labelTitle,
  labelText,
  icon,
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
        <Card htmlFor={fieldId} className="form-row checkbox">
          <IconTextWrapper>
            {icon && <CardIcon src={icon} alt="Icon" />}
            <div>
              <LabelTitle>{labelTitle}</LabelTitle>
              <LabelText>{labelText}</LabelText>
            </div>
          </IconTextWrapper>
          <input
            type="checkbox"
            name={fieldName}
            id={fieldId}
            defaultChecked={checked}
            required={required}
            autoFocus={autofocus}
          />
          <span htmlFor={fieldId} className="checkmark" />
        </Card>
      )}
    />
  );
}

FormFieldCard.propTypes = {
  fieldName: PropTypes.string.isRequired,
  fieldId: PropTypes.string.isRequired,
  labelText: PropTypes.oneOfType([PropTypes.string, PropTypes.element])
    .isRequired,
  labelTitle: PropTypes.oneOfType([PropTypes.string, PropTypes.element])
    .isRequired,
  icon: PropTypes.string,
  checked: PropTypes.bool,
  errors: PropTypes.arrayOf(PropTypes.string).isRequired,
  required: PropTypes.bool,
  autofocus: PropTypes.bool,
};

FormFieldCard.defaultProps = {
  icon: null,
  checked: false,
  required: false,
  autofocus: false,
};

export default FormFieldCard;
