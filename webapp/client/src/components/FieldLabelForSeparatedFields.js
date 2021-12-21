import React from "react";
import PropTypes from "prop-types";
import styled from "styled-components";
import FieldLabelScaffolding from "./FieldLabelScaffolding";

const Legend = styled.legend`
  &.field-label {
    margin-bottom: var(--spacing-01);
  }

  &.field-label-example {
    margin-bottom: var(--spacing-01);
  }
`;

// TODO: Use for Radio
export default function FieldLabelForSeparatedFields(props) {
  return (
    <FieldLabelScaffolding
      {...props}
      render={(innerContent, className) => (
        <Legend className={className}>{innerContent}</Legend>
      )}
    />
  );
}

FieldLabelForSeparatedFields.propTypes = {
  fieldId: PropTypes.string.isRequired,
  label: FieldLabelScaffolding.propTypes.label,
  details: FieldLabelScaffolding.propTypes.details,
};

FieldLabelForSeparatedFields.defaultProps = {
  ...FieldLabelScaffolding.defaultProps,
};
