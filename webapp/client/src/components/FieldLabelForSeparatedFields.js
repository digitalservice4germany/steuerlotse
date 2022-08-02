import React from "react";
import PropTypes from "prop-types";
import styled from "styled-components";
import FieldLabelScaffolding from "./FieldLabelScaffolding";
import { labelPropType } from "../lib/propTypes";

const Legend = styled.legend`
  margin-bottom: 0;

  & > span {
    display: block;
  }

  & > span.field-label {
    -webkit-margin-top-collapse: separate; // Added because Safari won't display the margin inside of a legend
    -webkit-margin-bottom-collapse: separate; // Added because Safari won't display the margin inside of a legend
    margin-bottom: var(--spacing-01);
  }

  & > span.field-label-example {
    margin-bottom: var(--spacing-01);
  }
`;

// TODO: Use for Radio
export default function FieldLabelForSeparatedFields(props) {
  return (
    <FieldLabelScaffolding
      {...props}
      render={(innerContent, className) => (
        <Legend>
          {" "}
          <span className={className}>{innerContent} </span>
        </Legend>
      )}
    />
  );
}

FieldLabelForSeparatedFields.propTypes = {
  fieldId: PropTypes.string.isRequired,
  label: labelPropType,
  details: FieldLabelScaffolding.propTypes.details,
  disable: PropTypes.bool,
};

FieldLabelForSeparatedFields.defaultProps = {
  ...FieldLabelScaffolding.defaultProps,
  disable: false,
};
