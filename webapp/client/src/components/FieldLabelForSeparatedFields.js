import React from "react";
import PropTypes from "prop-types";
import FieldLabelScaffolding from "./FieldLabelScaffolding";

// TODO: Use for Radio, SteuerlotseDate fields
export default function FieldLabelForSeparatedFields(props) {
  return (
    <FieldLabelScaffolding
      {...props}
      render={(innerContent, className) => (
        <span>
          <legend className={className}>{innerContent}</legend>
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
