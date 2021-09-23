import React from "react";
import PropTypes from "prop-types";
import styled from "styled-components";
import FieldLabelScaffolding from "./FieldLabelScaffolding";

const Legend = styled.legend`
  &.field-label {
    margin-bottom: var(--spacing-01);
  }
`;

// TODO: Use for Radio, SteuerlotseDate fields
export default function FieldLabelForSeparatedFields(props) {
  return (
    <FieldLabelScaffolding
      {...props}
      render={(innerContent, className) => (
        <span>
          <Legend className={className}>{innerContent}</Legend>
        </span>
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
