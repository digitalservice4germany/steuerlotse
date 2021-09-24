import React from "react";
import PropTypes from "prop-types";
import styled from "styled-components";
import FieldLabelScaffolding from "./FieldLabelScaffolding";

const Label = styled.label`
  &.field-label {
    margin-bottom: var(--spacing-01);
  }
`;

export default function FieldLabel(props) {
  return (
    <FieldLabelScaffolding
      {...props}
      render={(innerContent, className) => (
        <Label htmlFor={props.fieldId} className={className}>
          {innerContent}
        </Label>
      )}
    />
  );
}

FieldLabel.propTypes = {
  fieldId: PropTypes.string.isRequired,
  label: FieldLabelScaffolding.propTypes.label,
  details: FieldLabelScaffolding.propTypes.details,
};

FieldLabel.defaultProps = {
  ...FieldLabelScaffolding.defaultProps,
};
