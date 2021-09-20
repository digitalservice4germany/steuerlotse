import React from "react";
import PropTypes from "prop-types";
import FieldLabelScaffolding from "./FieldLabelScaffolding";

export default function FieldLabel(props) {
  return (
    <FieldLabelScaffolding
      {...props}
      render={(innerContent, className) => (
        <label htmlFor={props.fieldId} className={className}>
          {innerContent}
        </label>
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
